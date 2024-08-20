from datetime import datetime

from pydantic import BaseModel

class EventBase(BaseModel):
    event_name: str
    slug: str
    start_time: int
    end_time: int
    content: str
    event_category: int

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventInDBBase(EventBase):
    id: int
    class Config:
        orm_mode = True

class EventDb(EventInDBBase):
    pass
