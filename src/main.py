import asyncio
from unittest import result
from pyppeteer import launch
from pyppeteer.page import Page
from typing import List, Dict

class RegionCode:
    taipei: int = 1
    xinpei: int = 3


class UrlConfig:
    origin_url: str = 'https://rent.591.com.tw/?kind=0&region={region_code}'
    datalist_url: str = 'https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&firstRow={first_row}&totalRows={total_row}'
    detailed_info_url: str = 'https://rent.591.com.tw/home/{post_id}'

    @classmethod
    def generate_original_method(cls, region_code: int) -> str:
        return cls.origin_url.format(region_code=region_code)

    @classmethod
    def generate_dynamic_url(cls, total_row: int) -> List[str]:
        datalist_urls = []
        for step in range(0, total_row, 30):
            temp_datalist_url = cls.datalist_url.format(first_row=step, total_row=total_row)
            datalist_urls.append(temp_datalist_url)
        return datalist_urls

    @classmethod
    def generate_detailed_post_rul(cls, post_id: int) -> str:
        return cls.detailed_info_url.format(post_id=post_id)

async def get_cookies_to_header_format(page: Page) -> str:
    cookies = await page.cookies()
    cookie_key = 'name'
    cookie_value = 'value'
    cookie_list = '; '.join([f'{item.get(cookie_key)}={item.get(cookie_value)}' for item in cookies])
    return cookie_list


async def fetch_original_page_and_neccessary_info(page: Page) -> Dict[str, str]:
    main_page = UrlConfig.generate_original_method(RegionCode.taipei)
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


async def fetch_detail_page(page: Page, post_id: int) -> Dict[str, str]:
    def prefered_sex_filter(notice: str) -> str:
        prefered_sex = 'None'
        if '男女皆可' in notice:
            prefered_sex = '男女'
        elif '限女生' in notice:
            prefered_sex = '女'
        elif '限男生' in notice:
            prefered_sex = '男'
        return prefered_sex

    detailed_url = UrlConfig.generate_detailed_post_rul(post_id)
    await page.goto(detailed_url, {'waitUntil' : 'domcontentloaded'})
    await page.waitForSelector(".reference", timeout=1e5)

    phone_number_selector_path = '#rightConFixed > section > div.js-dialing.kfDialingNum.tel-phone-btn > div > div.reference > span.tel-txt'
    phone_number_selector = await page.querySelector(phone_number_selector_path)
    phone_number = await (await phone_number_selector.getProperty('textContent')).jsonValue()
    phone_number = str.strip(phone_number)
    
    preferred_sex_selector_path = '#service > div.service-rule > div > span'
    preferred_sex_selector = await page.querySelector(preferred_sex_selector_path)
    preferred_sex_text = await (await preferred_sex_selector.getProperty('textContent')).jsonValue()
    prefered_sex = prefered_sex_filter(preferred_sex_text)

    detailed_info = {
        'phone_number': phone_number,
        'prefered_sex': prefered_sex
    }

    return detailed_info


async def main():
    browser = await launch()
    page = await browser.newPage()
    neccessary_info = await fetch_original_page_and_neccessary_info(page)
    print(neccessary_info)

    datalist_url = UrlConfig.generate_dynamic_url(neccessary_info.get('result_size'))
    detailed_info = await fetch_detail_page(page, 13118587)
    print(detailed_info)
    await browser.close()


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


if __name__ == '__main__':
    # test_main()
    asyncio.get_event_loop().run_until_complete(main())
