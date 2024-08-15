from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.db_product import DbProduct as DbProductModel
from app.schemas.product import ProductCreate,ProductUpdate

class CRUDProduct(CRUDBase[DbProductModel,ProductCreate,ProductUpdate]):
    def get_products(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(DbProductModel).offset(skip).limit(limit).all()

    def get_product_by_id(self, db: Session, product_id: int):
        return db.query(DbProductModel).filter(DbProductModel.id == product_id).first()

    def get_product_by_name(self, db: Session, name: str):
        return db.query(DbProductModel).filter(DbProductModel.name == name).first()

    def create_product(self, db: Session, obj_in: ProductCreate):
        db_product = DbProductModel(
            name=obj_in.name,
            slug=obj_in.slug,
            price=obj_in.price,
            price_sale=obj_in.price_sale,
            content=obj_in.content,
            short_description=obj_in.short_description,
            product_cat=obj_in.product_cat
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def update_product(self, db: Session, db_product: DbProductModel, obj_in: ProductUpdate):
        db_product.name = obj_in.name
        db_product.slug = obj_in.slug
        db_product.price = obj_in.price
        db_product.price_sale = obj_in.price_sale
        db_product.content = obj_in.content
        db_product.short_description = obj_in.short_description
        db_product.product_cat = obj_in.product_cat
        db.commit()
        db.refresh(db_product)
        return db_product

    def delete_product(self, db: Session, product_id: int):
        db_product = db.query(DbProductModel).filter(DbProductModel.id == product_id).first()
        if db_product:
            db.delete(db_product)
            db.commit()
        return db_product


product = CRUDProduct(DbProductModel)