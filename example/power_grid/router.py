from fastapi import APIRouter
from pydantic import BaseModel
from payment_calculation.aux_models import JobComplete
from payment_calculation.models import EmployeeIn, EmployeeOut

router = APIRouter(prefix="/payment_calculation")


class TYPE_UPDATE(BaseModel):
    pass # TODO replace with a real example

@router.get("/")
async def get_all_payment_calculation() -> list[str]:
    """Returns list of existing payment_calculation IDs"""  # XXX should this return url/uris?
    raise NotImplementedError()  # TODO this should look up ids from DB and return them


@router.post("/")
async def new_payment_calculation(
    resource: EmployeeIn,
) -> JobComplete:  # TODO should be wrapped in jonb
    # raise NotImplementedError()  # TODO This should create a new job entry in DB
    emp = EmployeeOut(**resource.model_dump(), personal_nr="1")
    job = JobComplete(id="test",input=emp)
    return job


@router.get("/{id}")
async def get_payment_calculation(id: str) -> JobComplete:
    raise NotImplementedError()  # TODO fetch Job with ID from the DB


@router.put("/{id}")
async def update_payment_calculation(resource: TYPE_UPDATE) -> JobComplete:
    raise NotImplementedError()  # TODO update the job in the db, this might be impossible in our structure since worker might have a differnt verison of this
    # Maybe check status is pending, success or failed to restart


@router.delete("/{id}")
async def delete_payment_calculation(id: str) -> JobComplete:
    raise NotImplementedError()  # TODO this should fetch the hob if possible then delete and return it