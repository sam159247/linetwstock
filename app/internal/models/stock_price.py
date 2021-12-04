from datetime import date

from pydantic import BaseModel


class Datum(BaseModel):
    date: date
    stock_id: int
    Trading_Volume: int
    Trading_money: int
    open: int
    max: int
    min: int
    close: int
    spread: int
    Trading_turnover: int


class Message(BaseModel):
    msg: str
    status: str
    data: list[Datum]
