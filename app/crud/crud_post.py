from http.client import HTTPException
from typing import List

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.models.db_post import DbPost as DbPostModel
from app.schemas.post import PostCreate, PostUpdate

class CRUDPost(CRUDBase[DbPostModel,PostCreate,PostUpdate]):

    def get_post(self, db: Session, skip: int = 0, limit:int = 10):
        return db.query(DbPostModel).offset(skip).limit(limit).all()

    def get_post_by_id(self, db: Session, post_id: int) -> DbPostModel:
        return db.query(DbPostModel).filter(DbPostModel.id == post_id).first()

    def get_post_by_name(self, db: Session, post_name: str) -> DbPostModel:
        return db.query(DbPostModel).filter(DbPostModel.title == post_name).first()

    def create_post(self, db: Session, obj_in: PostCreate):
        db_post = DbPostModel(
            title=obj_in.title,
            slug=obj_in.slug,
            body=obj_in.body,
            description=obj_in.description,
            tags=obj_in.tags,
            category=int(obj_in.category),
            author=obj_in.author,
            favorited=obj_in.favorited,
            favorites_count=obj_in.favorites_count
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    def update_post(self, db: Session, db_post : DbPostModel, obj_in : PostUpdate):
        db_post.title = obj_in.title
        db_post.slug = obj_in.slug
        db_post.description = obj_in.description
        db_post.body = obj_in.body
        db_post.tags = obj_in.tags
        db_post.category = obj_in.category
        db_post.author = obj_in.author
        db_post.favorite = obj_in.favorited
        db_post.favorites_count = obj_in.favorites_count
        db.commit()
        db.refresh(db_post)
        return db_post

    def delete_post(self, db: Session, post_id: int):
        db_post = db.query(DbPostModel).filter(DbPostModel.id == post_id).first()
        if db_post:
            db.delete(db_post)
            db.commit()
        return db_post

post = CRUDPost(DbPostModel)

