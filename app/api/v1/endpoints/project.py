import json
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.crud.crud_project import project as crud_project
from app.schemas.project import ProjectDB, ProjectCreate, ProjectUpdate
from app.api import deps

from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.utils import send_new_account_email

from redis import Redis

router = APIRouter()

redis_client = Redis(host='localhost', port=6380, db=0)


@router.get("/", response_model=List[ProjectDB])
def get_projects(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):

    cache_key = f'projects:{skip}:{limit}'
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return cached_data

    db_project = crud_project.get_projects(db=db, skip=skip, limit=limit)
    project_dict = jsonable_encoder(db_project)

    redis_client.setex(cache_key, 10800, json.dumps(project_dict))

    return project_dict


@router.get("/{project_id}", response_model=ProjectDB)
def get_project_by_id(project_id: int, db: Session = Depends(deps.get_db)):

    cache_key = f'project_by_id:{project_id}'
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return cached_data

    db_project = crud_project.get_project_by_id(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    project_dict = jsonable_encoder(db_project)
    redis_client.setex(cache_key, 10800, json.dumps(project_dict))
    return project_dict


@router.post("/", response_model=ProjectDB)
def create_project(project: ProjectCreate, db: Session = Depends(deps.get_db)):
    db_project = crud_project.get_project_by_name(db=db, project_title=project.title)
    if db_project:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project already exists")
    return crud_project.create_project(db=db, obj_in=project)


@router.put("/{project_id}", response_model=ProjectDB)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(deps.get_db)):
    db_project = crud_project.get_project_by_id(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return crud_project.update_project(db=db, project_in=db_project, obj_in=project)


@router.delete("/{project_id}", response_model=ProjectDB)
def delete_project(project_id: int, db: Session = Depends(deps.get_db)):
    db_project = crud_project.get_project_by_id(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    crud_project.delete_project(db=db, project_id=project_id)
    return db_project
