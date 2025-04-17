from datetime import date
from typing import List
from pydantic import BaseModel, Field

class Mixin(BaseModel):
    created_at: date = Field(default_factory=date.today, description="Timestamp when the resource was created")
    updated_at: date = Field(default_factory=date.today, description="Timestamp when the resource was last updated")



class Campaign(Mixin):
    id: int = Field(..., description="Unique campaign identifier")
    name: str = Field(..., description="Name of the discount campaign")
    start_date: str = Field(..., description="Start date of the campaign (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date of the campaign (YYYY-MM-DD)")
    description: str = Field(..., description="Brief description of the campaign")
    discount_percentage: int = Field(..., description="Discount percentage to apply")
    campaign_amount: int = Field(..., description="Amount of discount for the campaign")
    max_transactions_per_day: int = Field(..., description="Maximum allowed transactions per customer per day")


class Customer(Mixin):
    id: int = Field(..., description="Unique customer ID")
    name: str = Field(..., description="Customer's full name")
    email: str = Field(..., description="Customer's email address")
    discount_available: bool = Field(..., description="Flag indicating if the customer is eligible for discounts")

class Order(Mixin):
    id: int = Field(..., description="Unique order ID")
    user_id: int = Field(..., description="ID of the customer who placed the order")
    campaign_id: int = Field(..., description="ID of the campaign applied to the order")
    total_cart_amount: float = Field(..., description="Total amount of the order")




