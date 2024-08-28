from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.crud.crud_project_category import project_cat as crud_project_cat
from app.schemas.project_category import ProjectCategoryDB, ProjectCategoryCreate, ProjectCategoryUpdate
from app.api import deps

from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[ProjectCategoryDB])
def get_project_categories(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    db_project_cat = crud_project_cat.get_porject_categories(db=db, skip=skip, limit=limit)
    if not db_project_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Project Category To List")
    return db_project_cat


@router.get("/{project_id}", response_model=ProjectCategoryDB)
def get_project_cat_by_id(project_id: int, db: Session = Depends(deps.get_db)):
    db_project_cat = crud_project_cat.get_project_category_by_id(db=db, project_cat_id=project_id)
    if not db_project_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project Category not found")
    return db_project_cat


@router.post("/", response_model=ProjectCategoryDB)
def create_project_category(project_cat_in: ProjectCategoryCreate, db: Session = Depends(deps.get_db)):
    db_project_cat = crud_project_cat.get_project_category_by_name(db=db, project_cat_name=project_cat_in.name)
    if db_project_cat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project Category already exists")
    return crud_project_cat.create_project(db=db, obj_in=project_cat_in)


@router.put("/{project_id}", response_model=ProjectCategoryDB)
def update_project_cat(project_cat_id: int, project_cat_in: ProjectCategoryUpdate, db: Session = Depends(deps.get_db)):
    db_project_cat = crud_project_cat.get_project_category_by_id(db=db, project_cat_id=project_cat_id)
    if not db_project_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project Category not found")

    return crud_project_cat.update_project(db=db, obj_in=project_cat_in, db_project_cat=db_project_cat)


@router.delete("/{project_id}", response_model=ProjectCategoryDB)
def delete_project_category(project_cat_id: int, db: Session = Depends(deps.get_db)):
    db_project_cat = crud_project_cat.get_project_category_by_id(db=db, project_cat_id=project_cat_id)
    if not db_project_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project Category not found")
    crud_project_cat.delete_project(db=db, project_cat_id=project_cat_id)
    return db_project_cat
