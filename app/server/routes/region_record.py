from fastapi import APIRouter, Request
from typing import List

from ..models.house_record import HouseRecord

router = APIRouter(
    prefix='/region',
    tags=['region'],
    responses={404: {'description': 'API Error Encountered'}}
)


@router.get("/{region}", response_description="Get a single house record by region_id and sex_prefered", response_model=List[HouseRecord])
async def find_records(request: Request, region: int):
    """Return Records of specified region.

    - **region**: 1 -> taipei, 3 -> xinpei
    """
    records = list(request.app.collection.find({"region": region}))
    return records


@router.get("/{region}/notice/{prefered_sex}", response_description="Get a single house record by region_id and sex_prefered", response_model=List[HouseRecord])
async def find_records(request: Request, region: int, prefered_sex: str):
    """Return Records of specified region and prefered_sex.

    - **region**: 1 -> taipei, 3 -> xinpei
    - **prefered_sex**: both, boy, girl
    """
    records = list(request.app.collection.find({"region": region, 'prefered_sex': prefered_sex}))
    return records


@router.get("/{region}/notice/{prefered_sex}", response_description="Get a single house record by region_id and sex_prefered", response_model=List[HouseRecord])
async def find_records(request: Request, region: int, prefered_sex: str):
    """Return Records of specified region and prefered_sex.

    - **region**: 1 -> taipei, 3 -> xinpei
    - **prefered_sex**: both, boy, girl
    """
    records = list(request.app.collection.find({"region": region, 'prefered_sex': prefered_sex}))
    return records


@router.get("/{region}/role_name/{role_name}/contact/{contact}", response_description="Get a single house record by region_id and sex_prefered", response_model=List[HouseRecord])
async def find_records(request: Request, region: int, role_name: str, contact: str):
    """Return Records of specified role_name and contact in target region.

    - **region**: 1 -> taipei, 3 -> xinpei  
    - **role_name**: 代理人, 屋主 ...
    - **contact**: 小姐, 先生, 吳小姐, 吳先生 ...
    """
    records = list(request.app.collection.find({'region': region, "role_name": role_name, 'contact': {'$regex': contact}}).limit(100))
    return records
