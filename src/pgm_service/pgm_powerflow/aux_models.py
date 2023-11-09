from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from pgm_service.pgm_powerflow.models import PGM_Powerflow


base_config = ConfigDict(use_enum_values=True) # TODO Check if json_encoders = {datetime: lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%SZ")} is needed as it will be deprecated in the future


# XXX StrEnum is available from enum in python 3.11
class StrEnum(str, Enum):
    pass

class Status(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class JobBase(BaseModel):
    model_config = base_config
    id: str # TODO add default generator
    input: PGM_Powerflow


class JobComplete(JobBase):
    status: Status = Status.CREATED
    details: Optional[str] = None
    created: datetime = Field(default_factory=datetime.now)
    finished: Optional[datetime] = None
    result: PGM_Powerflow = None
