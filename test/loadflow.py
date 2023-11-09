import requests
import os
import time
import argparse
from dataclasses import dataclass
import logging

FILESERVICE_URL = os.getenv('FILESERVICE_URL', 'http://localhost:8080').removeprefix('/')
PGM_URL = os.getenv('PGM_URL', 'http://localhost:80').removeprefix('/')

DEFAULT_REPO = 'https://raw.githubusercontent.com/dpsim-simulator/cim-grid-data/master/BasicGrids/NEPLAN/Slack_Load_Line_Sample/'
DEFAULT_NET = 'Rootnet_FULL_NE_19J18h'


@dataclass
class FileInfo:
    fileID: str
    lastModified: str
    url: str


def transfer_to_fileservice(url):
    resp = requests.get(url)
    resp.raise_for_status()
    file_data = resp.content
    resp = requests.post(f'{FILESERVICE_URL}/files/', data=file_data)
    return FileInfo(**resp.json()["data"])


def load_data(baseurl):
    id_EQ = transfer_to_fileservice(baseurl + '_EQ.xml')
    id_TP = transfer_to_fileservice(baseurl + '_TP.xml')
    id_SV = transfer_to_fileservice(baseurl + '_SV.xml')
    return (id_EQ, id_TP, id_SV)


def start_powerflow(input_data):
    (EQ, TP, SV) = input_data
    powerflow_args = {
        "model": {
            "input_data": {
                "eq": EQ,  # Equipment
                "tp": TP,  # Topology
                "sv": SV,  # State variables
            },
            "system_frequency": 50.0,  # Hz
        },
        "symmetric": True,
        "error_tolerance": 1e-8,
        "max_iterations": 20,
        "calculation_method": "newton_raphson",
        # "output_component_types": [],
    }
    resp = requests.post(f"{PGM_URL}/api/pgm_powerflow", json=powerflow_args)
    resp.raise_for_status()
    data = resp.json()
    logging.info("Job status: %s", repr(data))
    return data["id"]


def wait_for_completion(job_id):
    last_status = None
    while True:
        time.sleep(1)
        resp = requests.get(f"{PGM_URL}/api/pgm_powerflow/{job_id}")
        resp.raise_for_status()
        data = resp.json()
        if data["status"] is not last_status:
            logging.info('Job %s has status %s', job_id, data["status"])
            last_status = data["status"]
        if data["status"] not in ("created", "running"):
            break
    return last_status == 'success'


def process_results(job_id, output):
    resp = requests.get(f'{FILESERVICE_URL}/data/{job_id}')
    resp.raise_for_status()
    if output == '-':
        print(resp.content.decode('utf-8'))
    else:
        with open(output, 'rb') as file:
            file.write(resp.content)


def main(args):
    input_data = load_data(args.network_url)
    job_id = start_powerflow(input_data)
    if not wait_for_completion(job_id):
        logging.error('Job failed.')
        exit(1)
    process_results(job_id, args.output)


if __name__ == '__main__':
    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
    argp = argparse.ArgumentParser()
    argp.add_argument('network_url', nargs='?', default=DEFAULT_REPO+DEFAULT_NET)
    argp.add_argument('--output', '-o', default='-')
    main(argp.parse_args())
