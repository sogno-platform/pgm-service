from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from power_grid_model import initialize_array  # TODO(mgovers) remove

from pgm_service.pgm_powerflow.router import router as pf_router


app = FastAPI(title="API")

app.include_router(pf_router, prefix="/api")


@app.get("/initialize/{dataset_type}/{component}/{size}")
def initialize(dataset_type: str, component: str, size: int):
    arr = initialize_array(dataset_type, component, size)
    return repr(arr)


@app.get("/")
def redirect_to_docs():
    """Redirect users to the docs of the default API version (typically the latest)"""
    redirect_url = "/docs"
    return RedirectResponse(url=redirect_url)
