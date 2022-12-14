from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
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
    type: Optional[Union[int, str]] = Field(...)
    post_id: int = Field(...)
    kind_name: Optional[str] = Field(...)
    room_str: Optional[str] = Field(...)
    floor_str: Optional[str] = Field(...)
    community: Optional[str] = Field(...)
    price: Optional[str] = Field(...)
    price_unit: Optional[str] = Field(...)
    photo_list: Optional[List[str]] = Field(...)
    section_name: Optional[str] = Field(...)
    street_name: Optional[str] = Field(...)
    location: Optional[str] = Field(...)
    rent_tag: Optional[List[Dict[str, str]]] = Field(...)
    area: Optional[Union[int, str]] = Field(...)
    role_name: Optional[str] = Field(...)
    contact: Optional[str] = Field(...)
    refresh_time: Optional[str] = Field(...)
    yesterday_hit: Optional[Union[int, str]] = Field(...)
    is_vip: Optional[Union[int, str]] = Field(...)
    is_combine: Optional[Union[int, str]] = Field(...)
    hurry: Optional[Union[int, str]] = Field(...)
    is_socail: Optional[Union[int, str]] = Field(...)
    surrounding: Optional[Dict[str, str]] = Field(...)
    discount_price_str: Optional[str] = Field(...)
    cases_id: Optional[Union[int, str]] = Field(...)
    is_video: Optional[Union[int, str]] = Field(...)
    preferred: Optional[Union[int, str]] = Field(...)
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
                'title': '(??????)????????????????????????.??????????????????',
                'type': 1,
                'post_id': 12865005,
                'kind_name': '????????????',
                'room_str': 'null',
                'floor_str': '1F/1F',
                'community': 'null',
                'price': '8,333',
                'price_unit': '???/???',
                'photo_list': ['https://img2.591.com.tw/house/2022/08/07/165985253131308858.jpg!510x400.jpg', 'https://img2.591.com.tw/house/2022/08/07/165985253131369589.jpg!510x400.jpg', 'https://img1.591.com.tw/house/2022/08/07/165985253131345672.jpg!510x400.jpg', 'https://img2.591.com.tw/house/2022/08/07/165985253131331232.jpg!510x400.jpg', 'https://img2.591.com.tw/house/2022/08/07/165985253131412524.jpg!510x400.jpg', 'https://img1.591.com.tw/house/2022/08/07/165985253131450378.jpg!510x400.jpg', 'https://img2.591.com.tw/house/2022/08/07/165985253131444810.jpg!510x400.jpg', 'https://img2.591.com.tw/house/2022/08/07/165985253131461875.jpg!510x400.jpg', 'https://img2.591.com.tw/house/2022/08/07/165985253131554574.jpg!510x400.jpg', 'https://img1.591.com.tw/house/2022/08/07/165985253131587639.jpg!510x400.jpg', 'https://img1.591.com.tw/house/2022/08/07/165985253131585601.jpg!510x400.jpg', 'https://img2.591.com.tw/house/2022/08/07/165985253131533156.jpg!510x400.jpg', 'https://img1.591.com.tw/house/2022/08/07/165985253131632000.jpg!510x400.jpg'],
                'section_name': '?????????',
                'street_name': '?????????',
                'location': '?????????-?????????55???36???2???',
                'rent_tag': [],
                'area': 45,
                'role_name': '?????????',
                'contact': '?????????',
                'refresh_time': '30?????????',
                'yesterday_hit': 57,
                'is_vip': 1,
                'is_combine': 1,
                'hurry': 0,
                'is_socail': 0,
                'surrounding': {'type': 'bus_station', 'desc': '?????????????????????', 'distance': '200??????'},
                'discount_price_str': 'null',
                'cases_id': 0,
                'is_video': 0,
                'preferred': 0,
                'phone_number': '0970-116-359',
                'prefered_sex': 'both',
                'region': 1,
            }
        }
