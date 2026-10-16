from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class VendorQuote(BaseModel):
    vendor: str | None = Field(description="Vendor name stated in the document")
    sku: str | None = Field(description="Campus Customs SKU stated in the document")
    unit_price: float | None = Field(description="Quoted unit price in dollars")
    lead_time_days: int | None = Field(description="Quoted lead time in days")
    minimum_order: int | None = Field(description="Quoted minimum order in units")
    decision: Literal["recommend", "do_not_recommend"]
    reason: str = Field(description="One sentence explaining the decision")
