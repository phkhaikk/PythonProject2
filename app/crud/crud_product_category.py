from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.db_product_category import DbProductCategory as DbProductCatModel
from app.schemas.product_category import ProductCategoryCreate,ProductCategoryUpdate

class CRUDProductCategory(CRUDBase[ProductCategoryCreate,ProductCategoryUpdate,DbProductCatModel]):
    def get_all_product_cat(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(DbProductCatModel).offset(skip).limit(limit).all()

    def get_product_cat_by_id(self, db: Session, product_cat_id: int):
        return db.query(DbProductCatModel).filter(DbProductCatModel.id == product_cat_id).first()

    def get_product_cat_by_name(self, db: Session, name: str):
        return db.query(DbProductCatModel).filter(DbProductCatModel.name == name).first()

    def create_product_cat(self, db: Session, obj_in: ProductCategoryCreate):
        db_product_cat = DbProductCatModel(parent_id=obj_in.parent_id,name=obj_in.name,slug=obj_in.slug ,description=obj_in.description)
        db.add(db_product_cat)
        db.commit()
        db.refresh(db_product_cat)
        return db_product_cat

    def update_product_cat(self, db: Session, db_product_cat : DbProductCatModel, obj_in: ProductCategoryUpdate):
        db_product_cat.parent_id = obj_in.parent_id
        db_product_cat.name = obj_in.name
        db_product_cat.slug = obj_in.slug
        db_product_cat.description = obj_in.description
        db.commit()
        db.refresh(db_product_cat)
        return db_product_cat

    def delete_product_cat(self, db:Session, product_cat_id:int):
        db_product_cat = db.query(DbProductCatModel).filter(DbProductCatModel.id == product_cat_id).first()
        if db_product_cat:
            db.delete(db_product_cat)
            db.commit()
        return db_product_cat


product_cat = CRUDProductCategory(DbProductCatModel)