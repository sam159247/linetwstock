from typing import Any

from fastapi import APIRouter, Depends

from app import models, schemas
from app.internal.finmind_api import FindMindAPI

router = APIRouter()


@router.get("/", response_model=schemas.RespStockPrice)
def get_stock_price(param: models.StockPrice = Depends()) -> Any:
    """Get basic stock information."""

    data = FindMindAPI.stock_price(param.stock_id, param.start_date, param.end_date)

    return {
        "msg": "OK",
        "status": "200",
        "data": data,
    }
