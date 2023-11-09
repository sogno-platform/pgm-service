from datetime import datetime
from typing import Dict
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks

from pgm_service.pgm_powerflow.aux_models import JobComplete, Status
from pgm_service.pgm_powerflow.models import PGM_Powerflow
from pgm_service.power_grid.power_grid_model import calculate_powerflow
from pgm_service.utils import get_py_obj, store_py_obj, update_py_obj


router = APIRouter(prefix="/pgm_powerflow", tags=["Powerflow"])

JOBS: Dict[str, JobComplete] = {}


@router.get("/")
async def get_all_powerflow_calculation() -> list[str]:
    """Returns list of existing powerflow_calculation IDs"""
    return list(JOBS.keys())


async def _calculate(job: JobComplete):
    job.status = Status.RUNNING
    update_py_obj(job, job.id)

    try:
        grid = job.input.model
        pf_kwargs = job.input.calculation_args.model_dump()

        await calculate_powerflow(grid=grid, pf_kwargs=pf_kwargs)

        job.finished = datetime.now()
        job.status = Status.SUCCESS
    except Exception as e:
        job.status = Status.FAILED
        job.details = repr(e)

    update_py_obj(job, job.id)


@router.post("/")
async def new_powerflow_calculation(
    resource: PGM_Powerflow,
    background_tasks: BackgroundTasks,
) -> JobComplete:  # TODO should be wrapped in jonb
    job = JobComplete(id="tmp", input=resource)
    fileID = store_py_obj(job).json()["fileID"]
    job.id = fileID
    update_py_obj(job, id=job.id)
    # _id = str(uuid4())
    # JOBS[_id] = JobComplete(id=_id, input=resource)
    # job = JOBS[_id]

    background_tasks.add_task(_calculate, job=job)

    return job


@router.get("/{id}")
async def get_powerflow_calculation(id: str) -> JobComplete:
    return get_py_obj(id)


# @router.put("/{id}")
# async def update_powerflow_calculation(resource: TYPE_UPDATE) -> JobComplete:
#     raise NotImplementedError()  # TODO update the job in the db, this might be impossible in our structure since worker might have a differnt verison of this
#     # Maybe check status is pending, success or failed to restart


@router.delete("/{id}")
async def delete_powerflow_calculation(id: str) -> JobComplete:
    return JOBS.pop(id)
