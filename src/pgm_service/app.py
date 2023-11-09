from fastapi import FastAPI
from power_grid_model import initialize_array

app = FastAPI()


@app.get("/initialize/{dataset_type}/{component}/{size}")
def initialize(dataset_type: str, component: str, size: int):
    arr = initialize_array(dataset_type, component, size)
    return repr(arr)


@app.get("/")
def initialize_default():
    arr = initialize_array("input", "node", 1)
    return repr(arr)
