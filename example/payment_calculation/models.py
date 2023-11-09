# Example for the user input
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

# XXX StrEnum is available from enum in python 3.11
class StrEnum(str, Enum):
    pass

# Basic input data
class EmployeeIn(BaseModel):
    name: str
    job: str = Field(default="SWE")
    age: Optional[int] = None

# the feedback should also include the personal number
class EmployeeOut(EmployeeIn):
    personal_nr: str


class PaymentOption(StrEnum):
    PAYPAL = "paypal"
    CASH = "cash"
    BANK = "bank"

# this is the result of th payment calculation
class Payment(BaseModel):
    amount: float
    currency: str
    payment_option: PaymentOption = PaymentOption.BANK