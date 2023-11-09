from fastapi import FastAPI, Response, Request
import os
import re
import json
import logging
import uuid
from datetime import datetime

DATA_DIR = os.getenv("DATA_DIR", "/data")

app = FastAPI()

REGEX_ID = re.compile(r'^[a-zA-Z0-9_\-]+$')

def path_from_id(id: str):
    if not REGEX_ID.fullmatch(id):
        raise Exception("invalid ID")
    return os.path.join(DATA_DIR, id)

def from_exception(e: Exception):
    logging.error('Exception %s', e)
    data = json.dumps({ "message": str(e) })
    return Response(data.encode('utf-8'), 500, media_type="application/json")

@app.get("/files/")
def list_files():
    return os.listdir(DATA_DIR)

@app.post("/files/")
async def new_file(request: Request) -> dict|Response:
    try:
        id = str(uuid.uuid4())
        with open(os.path.join(DATA_DIR, id), 'wb') as file:
            async for chunk in request.stream():
                file.write(chunk)
        return { "id": id, "timestamp": datetime.now().isoformat() }
    except Exception as e:
        return from_exception(e)


@app.get("/files/{id}")
def get_file(id: str) -> Response:
    try:
        path = path_from_id(id)
        with open(path, 'rb') as file:
            return Response(file.read())
    except FileNotFoundError:
        return Response(status_code=404)
    except Exception as e:
        return from_exception(e)

@app.put("/files/{id}")
async def put_file(id: str, request: Request) -> Response:
    try:
        path = path_from_id(id)
        with open(path, 'wb') as file:
            async for chunk in request.stream():
                file.write(chunk)
        return Response(status_code=204)
    except Exception as e:
        return from_exception(e)

@app.delete("/files/{id}")
def delete_file(id: str) -> Response:
    try:
        path = path_from_id(id)
        os.remove(path)
        return Response(status_code=204)
    except Exception as e:
        return from_exception(e)
