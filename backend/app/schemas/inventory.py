from pydantic import BaseModel, Field
from uuid import UUID
from typing import Dict
import decimal

class TransactionCreate(BaseModel):
    product_id: UUID
    location_id: UUID | None = None
    qty_change: decimal.Decimal
    transaction_type: str = Field(..., pattern="^(receive|issue|transfer|adjust)$")
    reference_id: UUID | None = None

class StockResponse(BaseModel):
    sku: str
    name: str
    total: float
    locations: Dict[str, float]