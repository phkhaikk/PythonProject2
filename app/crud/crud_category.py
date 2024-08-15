from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.db_category import DbCategory as DbCategoryModel
from app.schemas.category import CategoryCreate, CategoryUpdate

class CRUDCategory(CRUDBase[CategoryCreate, CategoryUpdate, DbCategoryModel]):
    def get_all_categoies(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(DbCategoryModel).offset(skip).limit(limit).all()

    def get_category_by_id(self, db: Session, category_id: int):
        return db.query(DbCategoryModel).filter(DbCategoryModel.id == category_id).first()

    def get_category_by_name(self, db: Session, name : str):
        return db.query(DbCategoryModel).filter(DbCategoryModel.name == name).first()

    def create_category(self, db: Session, obj_in: CategoryCreate):
        db_category = DbCategoryModel(slug=obj_in.slug, name=obj_in.name, description=obj_in.description)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    def update_category(self, db: Session, db_category : DbCategoryModel , obj_update_in: CategoryUpdate):
        db_category.name = obj_update_in.name
        db_category.slug = obj_update_in.slug
        db_category.description = obj_update_in.description
        db.commit()
        db.refresh(db_category)
        return db_category

    def delete_category(self, db: Session, category_id : int):
        db_category = db.query(DbCategoryModel).filter(DbCategoryModel.id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
        return db_category


category = CRUDCategory(DbCategoryModel)