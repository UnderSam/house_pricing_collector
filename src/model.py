from dataclasses import dataclass
from datetime import datetime


@dataclass
class HouseRecord():
    title: str = ''
    type: str = '' 
    post_id: int = 0
    kind_name: str = ''
    contact: str = ''
    role_name: str = '' 
    phone_number: str = ''
    area: str = '0'
    region: int = 0
    section_name: str = ''
    street_name: str = ''
    prefered_sex: str = ''
    location: str = ''
    price: str = '0'
    price_unit: str = ''
    update_time: datetime = None

