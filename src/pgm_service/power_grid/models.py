# Example for the user input
from enum import Enum
from pydantic import BaseModel


# XXX StrEnum is available from enum in python 3.11
class StrEnum(str, Enum):
    pass


# Basic input data
class Grid(BaseModel):
    input_data: str
    system_frequency: float = 50.0

class InputData(BaseModel):
    sv: str
    eq: str
    tp: str
