from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.crud.crud_product_category import product_cat as crud_product_cat
from app.schemas.product_category import ProductCategoryDB, ProductCategoryCreate, ProductCategoryUpdate
from app.api import deps

from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=list[ProductCategoryDB])
def read_product_categories(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    product_cat = crud_product_cat.get_all_product_cat(db=db, skip=skip, limit=limit)
    return product_cat


@router.get("/{product_cat_id}", response_model=ProductCategoryDB)
def read_product_cat_by_id(product_cat_id: int, db: Session = Depends(deps.get_db)):
    db_product_cat = crud_product_cat.get_product_cat_by_id(db=db, product_cat_id=product_cat_id)
    if not db_product_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Category not found")
    return db_product_cat


@router.post("/", response_model=ProductCategoryDB)
def create_product_cat(product_cat: ProductCategoryCreate, db: Session = Depends(deps.get_db)):
    db_product_cat = crud_product_cat.get_product_cat_by_name(name=product_cat.name, db=db)
    if db_product_cat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product Category already exists")
    return crud_product_cat.create_product_cat(db=db, obj_in=product_cat)


@router.put("/{product_cat_id}", response_model=ProductCategoryDB)
def update_product_cat(product_cat_id: int, product_cat: ProductCategoryUpdate, db: Session = Depends(deps.get_db)):
    db_product_cat = crud_product_cat.get_product_cat_by_id(db=db, product_cat_id=product_cat_id)
    if not db_product_cat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product Category not found")
    return crud_product_cat.update_product_cat(db=db, db_product_cat=db_product_cat, obj_in=product_cat)


@router.delete("/{product_cat_id}", response_model=ProductCategoryDB)
def delete_product_cat(product_cat_id: int, db: Session = Depends(deps.get_db)):
    db_product_cat = crud_product_cat.get_product_cat_by_id(db=db, product_cat_id=product_cat_id)
    if not db_product_cat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product Category not found")
    crud_product_cat.delete_product_cat(db=db, product_cat_id=product_cat_id)
    return db_product_cat
