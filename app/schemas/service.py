from pydantic import BaseModel

class ServiceBase(BaseModel):
    title: str
    content: str

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class ServiceInDBBase(ServiceBase):
    id: str
    class Config:
        orm_mode = True

class ServiceDB(ServiceInDBBase):
    pass