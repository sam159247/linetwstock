from typing import Optional

from pydantic import BaseModel


class StockPrice(BaseModel):
    stock_id: str
    start_date: str

    # FinMind default today
    end_date: Optional[str]
