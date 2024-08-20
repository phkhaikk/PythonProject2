from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel

class DBEventCategory(BaseModel):
    __tablename__ = 'db_event_category'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    slug = Column(String,nullable=False)
    description = Column(String)
    parent_id = Column(Integer)