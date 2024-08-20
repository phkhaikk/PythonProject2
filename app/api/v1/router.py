from fastapi import APIRouter

from app.api.v1.endpoints import (status, authen, users, category, post, product, product_category, event_category)

api_router = APIRouter()
api_router.include_router(status.router, tags=["StarterAPI"])
api_router.include_router(authen.router, tags=["Authen"])
api_router.include_router(users.router, prefix="/user", tags=["Users"])

api_router.include_router(post.router, prefix="/post", tags=["Post"])

api_router.include_router(category.router, prefix="/category", tags=["Category"])

api_router.include_router(product.router, prefix="/product", tags=["Product"])

api_router.include_router(product_category.router, prefix="/product_cat", tags=["ProductCat"])


api_router.include_router(event_category.router, prefix="/event_cat", tags=["EventCategory"])

