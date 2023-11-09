from fastapi import APIRouter
from pydantic import BaseModel
from power_grid.aux_models import JobComplete
from power_grid.models import Grid

router = APIRouter(prefix="/power_grid", tags=["Grid"])


@router.get("/")
async def get_all_payment_calculation() -> list[str]:
    """Returns list of existing payment_calculation IDs"""  # XXX should this return url/uris?
    raise NotImplementedError()  # TODO this should look up ids from DB and return them


@router.post("/")
async def new_payment_calculation(
    resource: Grid,
) -> JobComplete:  # TODO should be wrapped in jonb
    # raise NotImplementedError()  # TODO This should create a new job entry in DB
    resource = Grid(**resource.model_dump())
    job = JobComplete(id="test",input=resource)
    return job


@router.get("/{id}")
async def get_payment_calculation(id: str) -> JobComplete:
    raise NotImplementedError()  # TODO fetch Job with ID from the DB



@router.delete("/{id}")
async def delete_payment_calculation(id: str) -> JobComplete:
    raise NotImplementedError()  # TODO this should fetch the hob if possible then delete and return it