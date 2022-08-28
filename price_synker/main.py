import asyncio
from pyppeteer import launch
from pyppeteer.network_manager import Response
from pyppeteer.page import Page
from typing import List, Dict, Any
from url_utils import UrlConfig
from kink import di
import json
from time import sleep
import argparse
from detail_worker import DetailWorker
from store_utils import StoreProcedure 
import pandas as pd
from multiprocessing import Queue, Process
from mongo_manager import MongoManager


DEFAULT_WORKERS = 10


class RegionCode:
    taipei: int = 1
    xinpei: int = 3


async def get_cookies_to_header_format(page: Page) -> str:
    cookies = await page.cookies()
    cookie_key = 'name'
    cookie_value = 'value'
    cookie_list = '; '.join([f'{item.get(cookie_key)}={item.get(cookie_value)}' for item in cookies])
    return cookie_list


async def fetch_original_page_and_neccessary_info(page: Page, region_id: int) -> Dict[str, str]:
    main_page = UrlConfig.generate_original_method(region_id)
    await page.goto(main_page, {'waitUntil' : 'domcontentloaded'})
    await page.waitForSelector(".TotalRecord", timeout=1e5)

    csrf_selector_path = 'head > meta:nth-child(13)'
    selector = await page.querySelector(csrf_selector_path)
    name = await (await selector.getProperty('name')).jsonValue()
    if name != 'csrf-token':
        raise Exception('csrf-token not existed.')
    csrf_token = await (await selector.getProperty('content')).jsonValue()

    match_results_selector_path = '#rent-list-app > div > div.list-container-content > div > section.vue-public-list-page > div > span.TotalRecord > span'
    match_results_selector = await page.querySelector(match_results_selector_path)
    result_size = await (await match_results_selector.getProperty('textContent')).jsonValue()
    result_size = str.strip(result_size) 

    cookies = await get_cookies_to_header_format(page)

    neccessary_info = {
        'headers': {
            'X-CSRF-TOKEN': csrf_token,
            'Cookie': cookies,
        },
        'result_size': int(result_size),
    }

    return neccessary_info


class BriefInfoParser():

    def __init__(self) -> None:
        self.task_list = []

    async def intercept_brief_info_response(self, response: Response):
        # In this example, we care only about responses returning JSONs
        if "application/json" in response.headers.get("content-type", ""):
            try:
                # await response.json() returns the response as Python object
                # print("Content: ", await response.json())
                json_resp = await response.json()
                if json_resp['status'] == 1:
                    brief_datas: List[Dict[str, Any]] = json_resp['data']['data']
                    self.task_list.extend(brief_datas)

            except json.decoder.JSONDecodeError:
                # NOTE: Use await response.text() if you want to get raw response text
                print("Failed to decode JSON from", await response.text())

    async def fetch_brief_info_from_datalist(self, page: Page, neccessary_info: Dict[str, Any], datalist: List[str]) -> None:
        request_headers: Dict[str, str] = neccessary_info['headers']
        await page.setExtraHTTPHeaders(request_headers)

        page.on('response', lambda response: asyncio.ensure_future(self.intercept_brief_info_response(response)))

        for task_url in datalist:
            print('Parsing url: ', task_url)
            await page.goto(task_url)
            await page.waitFor(1000)
    
    def get_task_list(self) -> List[Dict[str, Any]]:
        return self.task_list


async def prepare_di(args: argparse.Namespace, task_queue: Queue) -> None:
    di['args'] = args
    di['detail_task_queue'] = task_queue
    di[StoreProcedure] = StoreProcedure()
    di[MongoManager] = MongoManager()


def monitor(queue: Queue) -> None:
    while queue.qsize() != 0:
        print(f'Current queue size: {queue.qsize()}')
        sleep(5)


def prepare_task_queue(brief_tasks: List[Dict[str, Any]], region_id: int) -> Queue:
    task_queue = Queue()
    for task in brief_tasks:
        task['region'] = region_id
        task_queue.put_nowait(task)
    return task_queue


async def house_scraper(args: argparse.Namespace) -> None:
    region_id = getattr(RegionCode, args.region_name)    

    browser = await launch()
    page = await browser.newPage()
    neccessary_info = await fetch_original_page_and_neccessary_info(page, region_id)
    datalist_url = UrlConfig.generate_dynamic_url(neccessary_info.get('result_size'))
    print(neccessary_info)
    print('-----------Start Parsing-------------')

    brief_parser = BriefInfoParser()
    await brief_parser.fetch_brief_info_from_datalist(page, neccessary_info, datalist_url)
    await browser.close()

    task_queue = await prepare_task_queue(brief_parser.get_task_list(), region_id)
    prepare_di(args, task_queue)

    print('Start processing detail task.')

    workers = [DetailWorker.spawn_worker() for _ in range(DEFAULT_WORKERS)]
    for worker in workers:
        worker.start()

    monitor_process = Process(target=monitor, args=(di['detail_task_queue'],))
    monitor_process.start()

    for worker in workers:
        worker.join()
    monitor_process.join()

    print('Finish processing task.')
    if args.save_csv:
        print('Store results into csv.')
        store_proc: StoreProcedure = di[StoreProcedure]
        results = store_proc.get_collected_results()
        result_df = pd.DataFrame(results)
        result_df.to_csv(f'./{args.region_name}.csv')


def main() -> None:
    parser = argparse.ArgumentParser()
    region_choices = [k for k, _ in RegionCode.__annotations__.items()]
    parser.add_argument('--region_name',
                        help='Region to scrape.',
                        choices=region_choices,
                        required=True)
    parser.add_argument('--save_csv',
                        help='Save detailed results to csv.',
                        action='store_true')
    parser.add_argument('--save_mongo',
                        help='Save detailed results to mongodb. (make sure setting was provided)',
                        action='store_true')
    args = parser.parse_args()
    print(args)
    asyncio.get_event_loop().run_until_complete(house_scraper(args))


def test_main():
    test_original_url = UrlConfig.generate_original_method(RegionCode.taipei)
    assert test_original_url == 'https://rent.591.com.tw/?kind=0&region=1'

    test_original_url = UrlConfig.generate_original_method(RegionCode.xinpei)
    assert test_original_url == 'https://rent.591.com.tw/?kind=0&region=3'

    assert UrlConfig.generate_dynamic_url(total_row=0) == []
    assert UrlConfig.generate_dynamic_url(total_row=1) == [
        'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&firstRow=0&totalRows=1',
    ]
    assert UrlConfig.generate_dynamic_url(total_row=60) == [
        'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&firstRow=0&totalRows=60',
        'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&firstRow=30&totalRows=60',
    ]
    assert UrlConfig.generate_dynamic_url(total_row=95) == [
        'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&firstRow=0&totalRows=95',
        'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&firstRow=30&totalRows=95',
        'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&firstRow=60&totalRows=95',
        'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&firstRow=90&totalRows=95',
    ]

    di[StoreProcedure] = StoreProcedure()
    store_proc: StoreProcedure = di[StoreProcedure]
    store_proc.insert_result(1)
    store_proc.insert_result(2)
    assert store_proc.get_collected_results() == [1, 2]


if __name__ == '__main__':
    # test_main()
    main()
