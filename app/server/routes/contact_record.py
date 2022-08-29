from fastapi import APIRouter, Request
from typing import List
from fastapi_pagination import Page, paginate

from ..models.house_record import HouseRecord

router = APIRouter(
    prefix='/role_name',
    tags=['role_name'],
    responses={404: {'description': 'API Error Encountered'}}
)


@router.get("/{role_name}", response_description="Get a single house record by region_id and sex_prefered", response_model=Page[HouseRecord])
async def find_records(request: Request, role_name: str):
    """Return Records of specified role_name.

    - **role_name**: 代理人, 屋主 ...
    """
    records = list(request.app.collection.find({"role_name": role_name}))
    return paginate(records)
