from fastapi import APIRouter

from app.api.v1.endpoints import (status, authen, users, category,post)

api_router = APIRouter()
api_router.include_router(status.router, tags=["StarterAPI"])
api_router.include_router(authen.router, tags=["Authen"])
api_router.include_router(users.router, prefix="/user", tags=["Users"])

api_router.include_router(post.router, prefix="/post", tags=["Post"])

api_router.include_router(category.router, prefix="/category", tags=["Category"])