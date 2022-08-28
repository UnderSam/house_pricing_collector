from typing import List


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