from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    slug: str
    price: int
    price_sale: int
    content: str
    short_description: str
    product_cat: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductInDBBase(ProductBase):
    id: int
    class Config:
        orm_mode = True

class ProductDb(ProductInDBBase):
    pass