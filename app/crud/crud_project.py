from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.models.db_project import DBProject as DBProjectModel
from app.schemas.project import ProjectBase, ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[DBProjectModel, ProjectCreate, ProjectUpdate]):

    def get_projects(self,db: Session, skip: int = 0, limit: int = 100):
        return db.query(DBProjectModel).offset(skip).limit(limit).all()

    def get_project_by_id(self, db: Session, project_id: int):
        return db.query(DBProjectModel).filter(DBProjectModel.id == project_id).first()

    def get_project_by_name(self, db: Session, project_title: str):
        return db.query(DBProjectModel).filter(DBProjectModel.title == project_title).first()


    def create_project(self, db: Session, obj_in: ProjectCreate):
        db_project = DBProjectModel(title = obj_in.title, slug = obj_in.slug, content = obj_in.content, project_category=obj_in.project_category)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    def update_project(self, db: Session, project_in: DBProjectModel, obj_in: ProjectUpdate):
        project_in.title = obj_in.title
        project_in.slug = obj_in.slug
        project_in.content = obj_in.content
        project_in.project_category = obj_in.project_category
        db.commit()
        db.refresh(project_in)
        return project_in

    def delete_project(self, db: Session, project_id: int):
        db_project = db.query(DBProjectModel).filter(DBProjectModel.id == project_id).first()
        if db_project:
            db.delete(db_project)
            db.commit()
        return db_project

project = CRUDProject(DBProjectModel)