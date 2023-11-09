from fastapi import FastAPI

from power_grid.router import router as pg_router
from pgm_powerflow.router import router as pf_router


app = FastAPI(title=" API")

app.include_router(pg_router, prefix="/api")
app.include_router(pf_router, prefix="/api")
