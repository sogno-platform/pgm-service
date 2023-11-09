# Example for the user input
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel

from power_grid_model import CalculationMethod

from pgm_service.power_grid.models import Grid


# XXX StrEnum is available from enum in python 3.11
class StrEnum(str, Enum):
    pass


class PGM_PowerflowCalculationArgs(BaseModel):
    symmetric: bool = True
    error_tolerance: float = 1e-8
    max_iterations: int = 20
    calculation_method: Union[CalculationMethod, str] = CalculationMethod.newton_raphson
    # update_data: Optional[str] = None
    # threading: int = -1
    output_component_types: Optional[List[str]] = None
    # continue_on_batch_error: bool = False


# Basic input data
class PGM_Powerflow(BaseModel):
    model: Grid
    calculation_args: PGM_PowerflowCalculationArgs
