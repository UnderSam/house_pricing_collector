from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from ..models.house_record import HouseRecord

router = APIRouter(
    prefix='/records',
    tags=['records'],
    responses={404: {'description': 'API Error Encountered'}}
)


@router.get("/", response_description="List all house records", response_model=List[HouseRecord])
def list_records(request: Request):
    records = list(request.app.collection.find(limit=100))
    return records


@router.get("/{id}", response_description="Get a single house record by post_id", response_model=HouseRecord)
def find_records(id: int, request: Request):
    record = request.app.collection.find_one({"post_id": id})
    if record is not None:
        return record 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"record with post ID {id} not found")
