from fastapi import APIRouter

from power_grid_model import PowerGridModel

from pgm_service.pgm_powerflow.aux_models import JobComplete
from pgm_service.pgm_powerflow.models import PGM_Powerflow


router = APIRouter(prefix="/pgm_powerflow", tags=["Powerflow"])


@router.get("/")
async def get_all_payment_calculation() -> list[str]:
    """Returns list of existing payment_calculation IDs"""  # XXX should this return url/uris?
    raise NotImplementedError()  # TODO this should look up ids from DB and return them


@router.post("/")
async def new_payment_calculation(
    resource: PGM_Powerflow,
) -> JobComplete:  # TODO should be wrapped in jonb
    # raise NotImplementedError()  # TODO This should create a new job entry in DB
    resource.model.input_data = {}
    pf = PGM_Powerflow(**resource.model_dump())
    model = PowerGridModel(**resource.model.model_dump())
    calculation_result = model.calculate_power_flow(**resource.model_dump())
    print(calculation_result)
    job = JobComplete(id="test", input=resource)
    return job


@router.get("/{id}")
async def get_payment_calculation(id: str) -> JobComplete:
    raise NotImplementedError()  # TODO fetch Job with ID from the DB


# @router.put("/{id}")
# async def update_payment_calculation(resource: TYPE_UPDATE) -> JobComplete:
#     raise NotImplementedError()  # TODO update the job in the db, this might be impossible in our structure since worker might have a differnt verison of this
#     # Maybe check status is pending, success or failed to restart


@router.delete("/{id}")
async def delete_payment_calculation(id: str) -> JobComplete:
    raise NotImplementedError()  # TODO this should fetch the hob if possible then delete and return it
