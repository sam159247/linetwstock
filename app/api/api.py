from fastapi import APIRouter

from app.api.endpoints import get_stock_price

api_router = APIRouter()
api_router.include_router(get_stock_price.router, tags=["get_stock_price"])
