from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.db_user_profile import DbUserProfile
from app.models.db_category import DbCategory

class DbPost(BaseModel):
    __tablename__ = 'db_posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String, index=True, unique=True, nullable=False)
    title = Column(String)
    description = Column(String)
    body = Column(String)
    tags = Column(String)
    category = Column(Integer)
    author = Column(Integer)
    favorited = Column(Boolean, default=False)
    favorites_count = Column(Integer, default=0)


