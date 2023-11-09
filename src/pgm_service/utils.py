import os
import pickle
import tempfile
from typing import Any
from pgm_service.pgm_powerflow.models import InputData
import requests


def store_py_obj(
    data: any,
    url: str = os.getenv("FILESERVICE_URL", "127.0.0.1"),
    port: int = int(os.getenv("FILESERVICE_PORT", 8080)),
) -> requests.Response:
    ret = post_to_fileservice(pickle.dumps(data), url, port)
    print(ret.json())
    return ret


def update_py_obj(
    data: Any,
    id: str,
    url: str = os.getenv("FILESERVICE_URL", "127.0.0.1"),
    port: int = int(os.getenv("FILESERVICE_PORT", 8080)),
):
    return requests.put(f"http://{url}:{port}/files/{id}", data=pickle.dumps(data))


def get_py_obj(
    id: str, url: str = os.getenv("FILESERVICE_URL", "127.0.0.1"), port: int = int(os.getenv("FILESERVICE_PORT", 8080))
) -> Any:
    return pickle.loads(get_from_fileservice(id, url, port).content)


def post_to_fileservice(
    data, url: str = os.getenv("FILESERVICE_URL", "127.0.0.1"), port: int = int(os.getenv("FILESERVICE_PORT", 8080))
) -> requests.Response:
    return requests.post(f"http://{url}:{port}/files", data=data)


def get_from_fileservice(
    id: str, url: str = os.getenv("FILESERVICE_URL", "127.0.0.1"), port: int = int(os.getenv("FILESERVICE_PORT", 8080))
):  # TODO ->CIMFILE
    return requests.get(f"http://{url}:{port}/data/{id}")


def download_grid_data(input_data: InputData, tmp_dir):
    eq = get_from_fileservice(input_data.eq).content
    sv = get_from_fileservice(input_data.sv).content
    tp = get_from_fileservice(input_data.tp).content

    eq_path = os.path.join(tmp_dir, f"{input_data.eq}_EQ.xml")
    sv_path = os.path.join(tmp_dir, f"{input_data.eq}_SV.xml")
    tp_path = os.path.join(tmp_dir, f"{input_data.eq}_TP.xml")
    with open(eq_path, "bw") as outfile:
        outfile.write(eq)
    with open(sv_path, "bw") as outfile:
        outfile.write(sv)
    with open(tp_path, "bw") as outfile:
        outfile.write(tp)
    return [eq_path, sv_path, tp_path]


if __name__ == "__main__":
    testob = {"id": 3, "testdata": "test"}
    post_response = store_py_obj(testob).json()
    print(f"{post_response = }")
    get_resp = get_py_obj(id=post_response["data"]["fileID"])
    print(get_resp)
