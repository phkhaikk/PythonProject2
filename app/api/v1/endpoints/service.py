import json
from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.crud.crud_service import service as crud_service
from app.schemas.service import ServiceDB, ServiceCreate, ServiceUpdate
from app.api import deps

from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=list[ServiceDB])
def get_services(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100, ) -> Any:
    db_services = crud_service.get_services(db=db, skip=skip, limit=limit)
    if not db_services:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No services found")
    return db_services


@router.get("/{service_id}", response_model=ServiceDB)
def get_service_by_id(service_id: int, db: Session = Depends(deps.get_db)):
    db_service = crud_service.get_service_by_id(db=db, service_id=service_id)
    if not db_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return db_service


@router.post("/", response_model=ServiceDB)
def create_service(service_in: ServiceCreate, db: Session = Depends(deps.get_db)):
    db_service = crud_service.get_service_by_title(db=db, service_title=service_in.title)
    if db_service:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service already exists")
    return crud_service.create_service(db=db, service_obj_in=service_in)


@router.put("/{service_id}", response_model=ServiceDB)
def update_service(service_id: int, service_in: ServiceUpdate, db: Session = Depends(deps.get_db)):
    db_service = crud_service.get_service_by_id(db=db, service_id=service_id)
    if not db_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return crud_service.update_service_by_id(db=db, service_obj_in=service_in, db_service=db_service)


@router.delete("/{service_id}", response_model=ServiceDB)
def delete_service(service_id: int, db: Session = Depends(deps.get_db)):
    db_service = crud_service.get_service_by_id(db=db, service_id=service_id)
    if not db_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    crud_service.delete_service_by_id(db=db, service_id=service_id)
    return db_service
