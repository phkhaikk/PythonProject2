from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel

class DbEvent(BaseModel):
    __tablename__ = 'db_event'

    id = Column(Integer, primary_key=True)
    event_name = Column(String,nullable=False)
    slug = Column(String, unique=True, nullable=False)
    start_time = Column(Integer)
    end_time = Column(Integer)
    content = Column(String)
    category_event = Column(Integer)

