from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel

class DbCategory(BaseModel):
    __tablename__ = 'db_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)


