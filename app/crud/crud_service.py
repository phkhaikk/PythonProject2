from http.client import HTTPException

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.models.db_service import DBService as DBServiceModel
from app.schemas.service import ServiceBase, ServiceCreate, ServiceUpdate


class CRUDService(CRUDBase[DBServiceModel, ServiceCreate, ServiceUpdate]):

    def get_services(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(DBServiceModel).offset(skip).limit(limit).all()

    def get_service_by_id(self, db: Session, service_id: int):
        return db.query(DBServiceModel).filter(DBServiceModel.id == service_id).first()

    def get_service_by_title(self, db: Session, service_title: str):
        return db.query(DBServiceModel).filter(DBServiceModel.title == service_title).first()

    def create_service(self, db: Session, service_obj_in: ServiceCreate):
        db_service = DBServiceModel(title=service_obj_in.title, content=service_obj_in.content)
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return db_service

    def update_service_by_id(self, db: Session, db_service: DBServiceModel, service_obj_in: ServiceUpdate):
        db_service.title = service_obj_in.title
        db_service.content = service_obj_in.content
        db.commit()
        db.refresh(db_service)
        return db_service

    def delete_service_by_id(self, db: Session, service_id: int):
        db_service = db.query(DBServiceModel).filter(DBServiceModel.id == service_id).first()
        if not db_service:
            raise HTTPException(status_code=404, detail='Service not found')
        db.delete(db_service)
        db.commit()

        return db_service


service = CRUDService(DBServiceModel)
