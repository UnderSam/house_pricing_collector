from fastapi import APIRouter, Request, HTTPException, status
from typing import List
from fastapi_pagination import Page, paginate

from ..models.house_record import HouseRecord
from .region_record import router as RegionRouter
from .contact_record import router as ContactRouter

router = APIRouter(
    prefix='/records',
    tags=['records'],
    responses={404: {'description': 'API Error Encountered'}}
)
router.include_router(RegionRouter)
router.include_router(ContactRouter)

@router.get("/", response_description="List all house records", response_model=Page[HouseRecord])
async def list_records(request: Request):
    record = list(request.app.collection.find())
    return paginate(record)


@router.get("/{id}", response_description="Get a single house record by post_id", response_model=HouseRecord)
async def find_records(id: int, request: Request):
    record = request.app.collection.find_one({"post_id": id})
    if record is not None:
        return record 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"record with post ID {id} not found")


@router.get("/phone_number/{phone_number}", response_description="Get a single house record by contact phone_number", response_model=Page[HouseRecord])
async def find_records(phone_number: str, request: Request):
    records = list(request.app.collection.find({"phone_number": { '$regex': phone_number}}))
    return paginate(records)
