from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel

class DbProduct(BaseModel):
    __tablename__ = 'db_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,nullable=False)
    slug = Column(String,nullable=False,unique=True)
    price = Column(Integer,nullable=False)
    price_sale = Column(Integer,nullable=True)
    content = Column(String,nullable=True)
    short_description = Column(String,nullable=True)
    product_cat = Column(Integer,nullable=True)



