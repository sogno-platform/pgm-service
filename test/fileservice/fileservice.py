from fastapi import FastAPI, Response, Request, HTTPException
import os
import re
import logging
import uuid
from datetime import datetime

DATA_DIR = os.getenv("DATA_DIR", "/data")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080/").removesuffix('/')

REGEX_ID = re.compile(r'^[a-zA-Z0-9_\-]+$')

app = FastAPI()


def path_from_id(id: str):
    if not REGEX_ID.fullmatch(id):
        raise HTTPException(400, "invalid ID")
    return os.path.join(DATA_DIR, id)


def from_exception(e: Exception):
    logging.error('Exception %s', e)
    if not isinstance(e, HTTPException):
        e = HTTPException(500, str(e))
    raise e


def file_info(id):
    path = os.path.join(DATA_DIR, id)
    mtime = datetime.fromtimestamp(os.path.getmtime(path))
    return {
        "fileID": id,
        "lastModified": mtime.isoformat(),
        "url": f"{BASE_URL}/data/{id}"
    }


@app.get("/files/")
def list_files() -> dict:
    try:
        files = [
            file_info(file) for file in os.listdir(DATA_DIR)
        ]
        return {
            "data": files
        }
    except Exception as e:
        return from_exception(e)


@app.post("/files/")
async def new_file(request: Request) -> dict | Response:
    try:
        id = str(uuid.uuid4())
        with open(os.path.join(DATA_DIR, id), 'wb') as file:
            async for chunk in request.stream():
                file.write(chunk)
        return {
            "data": file_info(id)
        }
    except Exception as e:
        return from_exception(e)


@app.get("/files/{id}")
def get_file_info(id: str):
    try:
        path = path_from_id(id)
        if not os.path.isfile(path):
            return Response(status_code=404)
        return {
            "data": file_info(id)
        }
    except Exception as e:
        return from_exception(e)


@app.put("/files/{id}")
async def put_file(id: str, request: Request):
    return await put_file_data(id, request)


@app.delete("/files/{id}")
def delete_file(id: str):
    return delete_file_data(id)


@app.get("/data/{id}")
def get_file_data(id: str) -> Response:
    try:
        path = path_from_id(id)
        with open(path, 'rb') as file:
            return Response(file.read())
    except FileNotFoundError:
        return Response(status_code=404)
    except Exception as e:
        return from_exception(e)


@app.put("/data/{id}")
async def put_file_data(id: str, request: Request) -> Response:
    try:
        path = path_from_id(id)
        with open(path, 'wb') as file:
            async for chunk in request.stream():
                file.write(chunk)
        return {
            "data": file_info(id)
        }
    except Exception as e:
        return from_exception(e)


@app.delete("/data/{id}")
def delete_file_data(id: str) -> Response:
    try:
        path = path_from_id(id)
        os.remove(path)
        return Response(status_code=204)
    except Exception as e:
        return from_exception(e)
