from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.crud.crud_event_category import event_cat as crud_event_cat
from app.schemas.event_category import EventCategoryDB, EventCategoryCreate, EventCategoryUpdate
from app.api import deps

from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=list[EventCategoryDB])
def get_event_categories(skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)):
    event_cat = crud_event_cat.get_all_event_cat(db=db, skip=skip, limit=limit)
    return event_cat


@router.get("/{event_category_id}", response_model=EventCategoryDB)
def get_event_by_id(event_cat_id: int, db: Session = Depends(deps.get_db)):
    event_cat = crud_event_cat.get_event_cat_by_id(db=db, event_cat_id=event_cat_id)
    if not event_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event category not found")
    return event_cat


@router.post("/", response_model=EventCategoryDB)
def create_event_category(event_cat_in: EventCategoryCreate, db: Session = Depends(deps.get_db)):
    event_cat = crud_event_cat.get_event_cat_by_name(db=db, event_cat_name=event_cat_in.name)
    if event_cat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event category already exists")
    return crud_event_cat.create_event_cat(db=db, obj_in=event_cat_in)


@router.put("/{event_category_id}", response_model=EventCategoryDB)
def update_event_category(event_cat_id: int, event_cat_in: EventCategoryUpdate, db: Session = Depends(deps.get_db)):
    event_cat = crud_event_cat.get_event_cat_by_id(db=db, event_cat_id=event_cat_id)
    if not event_cat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event category not found")
    return crud_event_cat.update_event_cat(db=db, db_event_cat=event_cat, obj_in=event_cat_in)


@router.delete("/{event_category_id}", response_model=EventCategoryDB)
def delete_event_category(event_cat_id: int, db: Session = Depends(deps.get_db)):
    event_cat = crud_event_cat.get_event_cat_by_id(db=db, event_cat_id=event_cat_id)
    if not event_cat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event category not found")
    crud_event_cat.delete_event_cat(db=db, event_cat_id=event_cat_id)
    return event_cat
