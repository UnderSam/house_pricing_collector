from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return v
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)


class HouseRecord(BaseModel):
    id: ObjectIdStr = Field(..., alias='_id')
    title: str = Field(...)
    type: Optional[int] = Field(...)
    post_id: int = Field(...)
    kind_name: Optional[str] = Field(...)
    room_str: Optional[str] = Field(...)
    floor_str: Optional[str] = Field(...)
    community: Optional[str] = Field(...)
    price: Optional[str] = Field(...)
    price_unit: Optional[str] = Field(...)
    photo_list: Optional[str] = Field(...)
    section_name: Optional[str] = Field(...)
    street_name: Optional[str] = Field(...)
    location: Optional[str] = Field(...)
    rent_tag: Optional[str] = Field(...)
    area: Optional[int] = Field(...)
    role_name: Optional[str] = Field(...)
    contact: Optional[str] = Field(...)
    refresh_time: Optional[str] = Field(...)
    yesterday_hit: Optional[int] = Field(...)
    is_vip: Optional[int] = Field(...)
    is_combine: Optional[int] = Field(...)
    hurry: Optional[int] = Field(...)
    is_socail: Optional[int] = Field(...)
    surrounding: Optional[str] = Field(...)
    discount_price_str: Optional[str] = Field(...)
    cases_id: Optional[int] = Field(...)
    is_video: Optional[int] = Field(...)
    preferred: Optional[int] = Field(...)
    phone_number: Optional[str] = Field(...)
    prefered_sex: str = Field(...)
    region: int = Field(...)
    update_datetime: datetime = Field(...)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                '_id': '630b32ec56393b713fa0d8b6',
                'title': '(年租)文化大學套房出租.需看房請來電',
                'type': 1,
                'post_id': 12865005,
                'kind_name': '分租套房',
                'room_str': 'null',
                'floor_str': '1F/1F',
                'community': 'null',
                'price': '8,333',
                'price_unit': '元/月',
                'photo_list': '[\'https://img2.591.com.tw/house/2022/08/07/165985253131308858.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253131369589.jpg!510x400.jpg\', \'https://img1.591.com.tw/house/2022/08/07/165985253131345672.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253131331232.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253131412524.jpg!510x400.jpg\', \'https://img1.591.com.tw/house/2022/08/07/165985253131450378.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253131444810.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253131461875.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253131554574.jpg!510x400.jpg\', \'https://img1.591.com.tw/house/2022/08/07/165985253131587639.jpg!510x400.jpg\', \'https://img1.591.com.tw/house/2022/08/07/165985253131585601.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253131533156.jpg!510x400.jpg\', \'https://img1.591.com.tw/house/2022/08/07/165985253131632000.jpg!510x400.jpg\', \'https://img1.591.com.tw/house/2022/08/07/165985253131698358.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253189586424.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253196239423.jpg!510x400.jpg\', \'https://img1.591.com.tw/house/2022/08/07/165985253203246217.jpg!510x400.jpg\', \'https://img2.591.com.tw/house/2022/08/07/165985253234300218.jpg!510x400.jpg\', \'https://img1.591.com.tw/house/2022/08/07/165985253238128648.jpg!510x400.jpg\']',
                'section_name': '士林區',
                'street_name': '格致路',
                'location': '士林區-格致路55巷36弄2號',
                'rent_tag': '[]',
                'area': 45,
                'role_name': '代理人',
                'contact': '楊小姐',
                'refresh_time': '30分鐘內',
                'yesterday_hit': 57,
                'is_vip': 1,
                'is_combine': 1,
                'hurry': 0,
                'is_socail': 0,
                'surrounding': '{\'type\': \'bus_station\', \'desc\': \'距山仔后派出所\', \'distance\': \'200公尺\'}',
                'discount_price_str': 'null',
                'cases_id': 0,
                'is_video': 0,
                'preferred': 0,
                'phone_number': '0970-116-359',
                'prefered_sex': 'both',
                'region': 1,
            }
        }
