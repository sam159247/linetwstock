from fastapi import APIRouter

from app.api.endpoints import get_stock_price, line_callback

api_router = APIRouter()
api_router.include_router(get_stock_price.router, tags=["get_stock_price"])
api_router.include_router(line_callback.router, tags=["line_callback"])
