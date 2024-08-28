from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel

class DBProject(BaseModel):
    __tablename__ = 'db_project'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)
    content = Column(String)
    project_category = Column(Integer)
