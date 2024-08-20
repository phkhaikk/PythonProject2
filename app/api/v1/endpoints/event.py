from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.crud.crud_event import event as crud_event
from app.models import db_event
from app.schemas.event import EventDb, EventCreate, EventUpdate
from app.api import deps

from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[EventDb])
def get_events(skip: int = 0, limit: int = 0, db: Session = Depends(deps.get_db)):
    db_events = crud_event.read_all_event(db=db, skip=skip, limit=limit)
    if not db_events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No events found")
    return db_events


@router.post("/{event_id}", response_model=EventDb)
def get_event_by_id(event_id: int, db: Session = Depends(deps.get_db)):
    db_event = crud_event.get_event_by_id(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return db_event


@router.post("/", response_model=EventDb)
def create_event(event_in=EventCreate, db: Session = Depends(deps.get_db)):
    db_event = crud_event.get_event_by_name(db=db, event_name=event_in.event_name)
    if db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event already exists")
    return crud_event.create_event(db=db, obj_in=event_in)


@router.put("/{event_id}", response_model=EventDb)
def update_event(event_db=EventDb, event_in=EventUpdate, db: Session = Depends(deps.get_db)):
    db_event = crud_event.get_event_by_id(db=db, event_id=event_in.id)
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return crud_event.update_event(db=db, db_event=db_event, obj_in=event_in)


@router.delete("/{event_id}", response_model=EventDb)
def delete_event(event_id: int, db: Session = Depends(deps.get_db)):
    db_event = crud_event.get_event_by_id(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    crud_event.delete_event(db=db, event_id=event_id)
    return db_event
