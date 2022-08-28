import asyncio
from typing import Dict, Any
from pyppeteer import launch
from pyppeteer.page import Page
from multiprocessing import Process, Queue
from url_utils import UrlConfig
from kink import inject
from store_utils import StoreProcedure


@inject
class DetailWorker():
    def __init__(self, detail_task_queue: Queue, store_proc: StoreProcedure):
        self.task_queue = detail_task_queue
        self.store_proc = store_proc 

    async def run(self):
        browser = await launch() 
        page = await browser.newPage()

        try:
            while self.task_queue.qsize() != 0:
                brief_info: Dict[str, Any] = self.task_queue.get()

                try:
                    detailed_info = await self.fetch_detail_page(page, int(brief_info['post_id']))
                except Exception:
                    self.store_proc.insert_failed(brief_info)

                for k, v in detailed_info.items():
                    brief_info[k] = v

                self.store_proc.insert_result(brief_info)
                await page.waitFor(1000)
        except Exception:
            raise
        finally:
            await browser.close()

    async def fetch_detail_page(self, page: Page, post_id: int) -> Dict[str, str]:
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

        phone_number = ''
        phone_number_selector_path = '#rightConFixed > section > div.js-dialing.kfDialingNum.tel-phone-btn > div > div.reference > span.tel-txt'
        phone_number_selector = await page.querySelector(phone_number_selector_path)
        if phone_number_selector is not None:
            phone_number = await (await phone_number_selector.getProperty('textContent')).jsonValue()
            phone_number = str.strip(phone_number)

        preferred_sex_text = ''
        preferred_sex_selector_path = '#service > div.service-rule > div > span'
        preferred_sex_selector = await page.querySelector(preferred_sex_selector_path)
        if preferred_sex_selector is not None:
            preferred_sex_text = await (await preferred_sex_selector.getProperty('textContent')).jsonValue()
        prefered_sex = prefered_sex_filter(preferred_sex_text)

        detailed_info = {
            'phone_number': phone_number,
            'prefered_sex': prefered_sex
        }

        return detailed_info

    def process(self):
        asyncio.run(self.run())
        
    @classmethod
    def spawn_worker(cls):
        return Process(target=cls().process)

def main():
    p = Process(target=DetailWorker().process)
    p.start()
    p.join()

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(main())
    main()
