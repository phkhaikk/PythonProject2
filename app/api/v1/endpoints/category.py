from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.crud.crud_category import category as crud_category
from app.schemas.category import CategoryDB, CategoryCreate, CategoryUpdate
from app.api import deps

from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=list[CategoryDB])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    categories = crud_category.get_all_categoies(db=db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=CategoryDB)
def read_category_by_id(category_id: int, db: Session = Depends(deps.get_db)):
    db_category = crud_category.get_category_by_id(db=db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category


# @router.get("/{category_name}", response_model=CategoryDB)
# def read_category_by_name(category_name: str, db: Session = Depends(deps.get_db)):
#     db_category = crud_category.get_category_by_name(db=db, category_name=category_name)
#
#     if not db_category:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
#     return db_category


@router.post("/", response_model=CategoryDB)
def create_category(category: CategoryCreate, db: Session = Depends(deps.get_db)):
    db_category = crud_category.get_category_by_name(db=db, name=category.name)
    if db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category already exists")
    return crud_category.create_category(db=db, obj_in=category)

@router.put("/{category_id}", response_model=CategoryDB)
def update_category(category_id : int, category: CategoryUpdate,db:Session = Depends(deps.get_db)):
    db_category = crud_category.get_category_by_id(db=db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return crud_category.update_category(db=db, db_category=db_category, obj_update_in=category)

@router.delete("/{category_id}", response_model=CategoryDB)
def delete_category(category_id: int, db: Session = Depends(deps.get_db)):
    db_category = crud_category.get_category_by_id(db=db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    crud_category.delete_category(db=db, category_id=category_id)
    return db_category