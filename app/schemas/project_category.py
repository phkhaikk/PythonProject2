from pydantic import BaseModel


class ProjectCategoryBase(BaseModel):
    name: str
    slug: str
    description: str
    parent_id: int


class ProjectCategoryCreate(ProjectCategoryBase):
    pass


class ProjectCategoryUpdate(ProjectCategoryBase):
    pass


class ProjectCategoryInDBBase(ProjectCategoryBase):
    id: int

    class Config:
        orm_mode = True


class ProjectCategoryDB(ProjectCategoryInDBBase):
    pass
