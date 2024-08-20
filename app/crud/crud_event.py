from http.client import HTTPException

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.models.db_event import DbEvent as DbEventModel
from app.schemas.event import EventCreate, EventUpdate


class CRUDEvent(CRUDBase[DbEventModel, EventCreate, EventUpdate]):
    def read_all_event(self, db: Session, skip: int = 0, limit: int = 0):
        return db.query(DbEventModel).offset(skip).limit(limit).all()

    def get_event_by_id(self, db: Session, event_id: int):
        return db.query(DbEventModel).filter(DbEventModel.id == event_id).first()

    def get_event_by_name(self, db: Session, event_name: str):
        return db.query(DbEventModel).filter(DbEventModel.name == event_name).first()

    def create_event(self, db: Session, obj_in: EventCreate):
        db_event = DbEventModel(event_name=obj_in.event_name, slug=obj_in.slug, start_time=obj_in.start_time,
                                end_time=obj_in.end_time, category_event=obj_in.category_event)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    def update_event(self, db: Session, db_event: DbEventModel, obj_in: EventUpdate):
        db_event.event_name = obj_in.event_name
        db_event.slug = obj_in.slug
        db_event.start_time = obj_in.start_time
        db_event.end_time = obj_in.end_time
        db_event.category_event = obj_in.event_category
        db.commit()
        db.refresh(db_event)
        return db_event

    def delete_event(self, db: Session, event_id: int, db_event: DbEventModel):
        db_event = db.query(DbEventModel).filter(DbEventModel.id == event_id).first()
        if db_event:
            db.delete(db_event)
            db.commit()
            db.refresh(db_event)
        return db_event


event = CRUDEvent(DbEventModel)
