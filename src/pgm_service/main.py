from power_grid_model import initialize_array

from fastapi import FastAPI

import uvicorn

app = FastAPI()


@app.get("/initialize/{dataset_type}/{component}/{size}")
def initialize(dataset_type: str, component: str, size: int):
    arr = initialize_array(dataset_type, component, size)
    return repr(arr)


@app.get("/")
def initialize_default():
    arr = initialize_array("input", "node", 1)
    return repr(arr)


def main():
    # uvicorn.run("main:app", port=5000, log_level="info")
    print("Hello world!")
