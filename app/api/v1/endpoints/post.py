from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.crud.crud_post import post as crud_post
from app.schemas.post import PostDb, PostCreate, PostUpdate
from app.api import deps

from app.core.config import settings
from app.core.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=list[PostDb])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    posts = crud_post.get_post(db=db, skip=skip, limit=limit)
    return posts


@router.get("/{id}", response_model=PostDb)
def read_post_by_id(id: int, db: Session = Depends(deps.get_db)):
    posts = crud_post.get_post_by_id(db=db, post_id=id)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return posts


@router.post("/", response_model=PostDb)
def create_post(post: PostCreate, db: Session = Depends(deps.get_db)):
    db_post = crud_post.get_post_by_name(db=db, post_name=post.title)
    if db_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post already exists")
    return crud_post.create_post(db=db, obj_in=post)


@router.put("/{id}", response_model=PostDb)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(deps.get_db)):
    db_post = crud_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return crud_post.update_post(db=db, db_post=db_post, obj_in=post_update)


@router.delete("/{id}", response_model=PostDb)
def delete_post(post_id: int, db: Session = Depends(deps.get_db)):
    db_post = crud_post.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    crud_post.delete_post(db=db, post_id=post_id)
    return db_post
