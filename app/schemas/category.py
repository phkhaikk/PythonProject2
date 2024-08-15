from pydantic import BaseModel

class CategoryBase(BaseModel):
    slug: str
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class CategoryDB(CategoryInDBBase):
    pass


