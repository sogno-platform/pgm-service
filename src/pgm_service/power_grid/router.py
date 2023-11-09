from fastapi import APIRouter
from pydantic import BaseModel

from pgm_service.power_grid.aux_models import JobComplete
from pgm_service.power_grid.models import Grid


router = APIRouter(prefix="/power_grid", tags=["Grid"])


@router.get("/")
async def get_all_grid_model() -> list[str]:
    """Returns list of existing grid_model IDs"""  # XXX should this return url/uris?
    raise NotImplementedError()  # TODO this should look up ids from DB and return them


@router.post("/")
async def new_grid_model(
    resource: Grid,
) -> JobComplete:  # TODO should be wrapped in jonb
    # raise NotImplementedError()  # TODO This should create a new job entry in DB
    resource = Grid(**resource.model_dump())
    job = JobComplete(id="test",input=resource)
    return job


@router.get("/{id}")
async def get_grid_model(id: str) -> JobComplete:
    raise NotImplementedError()  # TODO fetch Job with ID from the DB



@router.delete("/{id}")
async def delete_grid_model(id: str) -> JobComplete:
    raise NotImplementedError()  # TODO this should fetch the hob if possible then delete and return it