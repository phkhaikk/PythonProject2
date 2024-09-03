from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel


class DBService(BaseModel):
    __tablename__ = 'db_service'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
