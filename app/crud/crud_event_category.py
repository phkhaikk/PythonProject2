from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.models.db_event_category import DBEventCategory as DBEventCatModel
from app.schemas.event_category import EventCategoryCreate, EventCategoryUpdate


class CRUDEventCategory(CRUDBase[DBEventCatModel, EventCategoryCreate, EventCategoryUpdate]):

    def get_all_event_cat(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(DBEventCatModel).offset(skip).limit(limit).all()

    def get_event_cat_by_id(self, db: Session, event_cat_id: int):
        return db.query(DBEventCatModel).filter(DBEventCatModel.id == event_cat_id).first()

    def get_event_cat_by_name(self, db: Session, event_cat_name: str):
        return db.query(DBEventCatModel).filter(DBEventCatModel.name == event_cat_name).first()

    def create_event_cat(self, db: Session, obj_in=EventCategoryCreate):
        db_event_cat = DBEventCatModel(name=obj_in.name, slug=obj_in.slug, description=obj_in.description,
                                       parent_id=obj_in.parent_id)
        db.add(db_event_cat)
        db.commit()
        db.refresh(db_event_cat)
        return db_event_cat

    def update_event_cat(self, db: Session, db_event_cat=DBEventCatModel, obj_in=EventCategoryUpdate):
        db_event_cat.name = obj_in.name
        db_event_cat.slug = obj_in.slug
        db_event_cat.description = obj_in.description
        db_event_cat.parent_id = obj_in.parent_id
        db.commit()
        db.refresh(db_event_cat)
        return db_event_cat

    def delete_event_cat(self, db: Session, event_cat_id: int):
        db_event_cat = db.query(DBEventCatModel).filter(DBEventCatModel.id == event_cat_id).first()
        if db_event_cat:
            db.delete(db_event_cat)
            db.commit()
        return db_event_cat


event_cat = CRUDEventCategory(DBEventCatModel)
