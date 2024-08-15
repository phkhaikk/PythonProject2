from pydantic import BaseModel

class Post(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    body: str
    tags: str
    category: int
    author: int
    favorited: bool
    favorites_count: int

class PostCreate(Post):
    pass

class PostUpdate(Post):
    pass

class PostDelete(Post):
    pass

class PostInDB(Post):
    id: int

    class Config:
        orm_mode = True

class PostDb(PostInDB):
    pass