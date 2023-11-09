# Example for the user input
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

# XXX StrEnum is available from enum in python 3.11
class StrEnum(str, Enum):
    pass

# Basic input data
class PGM_Powerflow(BaseModel):
    model: str
    symetric: bool = True
    error_toleerance: 
    

