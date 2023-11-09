from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime



from payment_calculation.models import EmployeeOut, Payment

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
    input: EmployeeOut # XXX is it a good idea to allow the server to add stuff to the input? I think it shows how the input was interpreted, so it good thisway


class JobComplete(JobBase):
    status: Status = Status.CREATED
    details: Optional[str] = None
    created: datetime = Field(default_factory=datetime.now)
    finished: Optional[datetime] = None
    result: Payment = None