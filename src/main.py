import asyncio
from pyppeteer import launch

class RegionCode:
    taipei: int = 1
    xinpei: int = 3

class UrlConfig:
    origin_url: str = 'https://rent.591.com.tw/?kind=0&region={region_code}'
    datalist_url: str = 'https://rent.591.com.tw/home/search/rsList'
    
    @classmethod
    def generate_original_method(cls, region_code: int) -> str:
        return cls.origin_url.format(region_code=region_code)

async def main():
    browser = await launch()
    page = await browser.newPage()
    main_page = UrlConfig.generate_original_method(RegionCode.taipei)
    await page.goto(main_page, {'waitUntil' : 'domcontentloaded'})
    await page.waitForSelector(".TotalRecord", timeout=1e5)
    
    csrf_selector_path = 'head > meta:nth-child(13)'
    selector = await page.querySelector(csrf_selector_path)
    name = await (await selector.getProperty('name')).jsonValue()
    value = await (await selector.getProperty('content')).jsonValue()
    
    match_results_selector_path = '#rent-list-app > div > div.list-container-content > div > section.vue-public-list-page > div > span.TotalRecord > span'
    match_results_selector = await page.querySelector(match_results_selector_path)
    result_size = await (await match_results_selector.getProperty('textContent')).jsonValue()

    print(name, value, result_size)
    # await page.screenshot({'path': 'example.png'})
    await browser.close()

def test_main():
    test_original_url = UrlConfig.generate_original_method(RegionCode.taipei)
    assert test_original_url == 'https://rent.591.com.tw/?kind=0&region=1'

if __name__ == '__main__':
    # test_main()
    asyncio.get_event_loop().run_until_complete(main())