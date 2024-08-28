from pydantic import BaseModel

class ProjectBase(BaseModel):
    title: str
    slug: str
    content: str
    project_category: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectInDBBase(ProjectBase):
    id: int

    class Config:
        orm_mode = True


class ProjectDB(ProjectInDBBase):
    pass



