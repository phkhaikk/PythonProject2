from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel

class DBProjectCategory(BaseModel):
    __tablename__ = 'project_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    slug = Column(String)
    description = Column(String)
    parent_id = Column(Integer)
