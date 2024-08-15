from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel

class DbProductCategory(BaseModel):
    __tablename__ = 'db_product_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    description = Column(String, nullable=True)