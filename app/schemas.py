from pydantic import BaseModel, PositiveFloat, Field
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    amount: PositiveFloat = Field(..., description="The amount of the transaction need to be positive")
    category: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    is_income: bool = False

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BalanceResponse(BaseModel):
    total_income: float
    total_expense: float
    current_balance: float