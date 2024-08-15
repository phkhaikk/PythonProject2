from pydantic import BaseModel

class ProductCategoryBase(BaseModel):
    parent_id: int
    name: str
    slug: str
    description: str

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategoryUpdate(ProductCategoryBase):
    pass

class ProductCategoryInDB(ProductCategoryBase):
    id: int
    class Config:
        orm_mode = True

class ProductCategoryDB(ProductCategoryInDB):
    pass