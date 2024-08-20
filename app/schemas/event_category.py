from pydantic import BaseModel

class EventCategoryBase(BaseModel):
    name: str
    slug: str
    description: str
    parent_id: int

class EventCategoryCreate(EventCategoryBase):
    pass

class EventCategoryUpdate(EventCategoryBase):
    pass

class EventCategoryRead(EventCategoryBase):
    pass

class EventCategoryInDBBase(EventCategoryBase):
    id: int
    class Config:
        orm_mode = True

class EventCategoryDB(EventCategoryInDBBase):
    pass