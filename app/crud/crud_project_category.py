from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.models.db_project_category import DBProjectCategory as DBProjectCatModel
from app.schemas.project_category import ProjectCategoryCreate, ProjectCategoryUpdate

class CRUDProjectCategory(CRUDBase[ProjectCategoryCreate, ProjectCategoryUpdate,DBProjectCatModel]):
    def get_porject_categories(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(DBProjectCatModel).offset(skip).limit(limit).all()

    def get_project_category_by_id(self, db: Session, project_cat_id: int):
        return db.query(DBProjectCatModel).filter(DBProjectCatModel.id == project_cat_id).first()

    def get_project_category_by_name(self, db: Session, project_cat_name: str):
        return db.query(DBProjectCatModel).filter(DBProjectCatModel.name == project_cat_name).first()

    def create_project(self, db: Session, obj_in: ProjectCategoryCreate):
        db_project_cat = DBProjectCatModel(name=obj_in.name,slug=obj_in.slug,description=obj_in.description,parent_id=obj_in.parent_id)
        db.add(db_project_cat)
        db.commit()
        db.refresh(db_project_cat)
        return db_project_cat

    def update_project(self, db: Session, obj_in: ProjectCategoryUpdate, db_project_cat : DBProjectCatModel):
        db_project_cat.name = obj_in.name
        db_project_cat.slug = obj_in.slug
        db_project_cat.description = obj_in.description
        db_project_cat.parent_id = obj_in.parent_id
        db.commit()
        db.refresh(db_project_cat)
        return db_project_cat

    def delete_project(self, db: Session, project_cat_id: int):
        db_project_cat = db.query(DBProjectCatModel).filter(DBProjectCatModel.id == project_cat_id).first()
        if db_project_cat:
            db.delete(db_project_cat)
            db.commit()
            db.refresh(db_project_cat)
        return db_project_cat

project_cat = CRUDProjectCategory(DBProjectCatModel)

