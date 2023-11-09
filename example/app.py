from fastapi import FastAPI

app = FastAPI(title=" API") 

from power_grid.router import router
app.include_router(router, prefix="/api")
