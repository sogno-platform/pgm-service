import glob
import os
from pathlib import Path
import tempfile
from typing import Dict, Any
from pgm_service.utils import download_grid_data
import requests
import cimpy
from power_grid_model import PowerGridModel

from pgm_service.power_grid.models import Grid
from pgm_service.power_grid.cgmes_pgm_converter import System as CGMESToPGMConverter


def download_data(url):
    def download_grid_data(name, url):
        with open(name, "wb") as out_file:
            content = requests.get(url, stream=True).content
            out_file.write(content)

    url = "https://raw.githubusercontent.com/dpsim-simulator/cim-grid-data/master/BasicGrids/NEPLAN/Slack_Load_Line_Sample/"
    filename = "Rootnet_FULL_NE_19J18h"

    download_grid_data(filename + "_EQ.xml", url + filename + "_EQ.xml")
    download_grid_data(filename + "_TP.xml", url + filename + "_TP.xml")
    download_grid_data(filename + "_SV.xml", url + filename + "_SV.xml")

    files = glob.glob(filename + "_*.xml")

    print("CGMES files downloaded:")
    print(files)

    this_file_folder = Path(__file__).parents[3]
    p = str(this_file_folder)
    xml_path = Path(p)
    xml_files = [
        os.path.join(xml_path, filename + "_EQ.xml"),
        os.path.join(xml_path, filename + "_TP.xml"),
        os.path.join(xml_path, filename + "_SV.xml"),
    ]

    print(xml_files)
    return xml_files


def create_model(grid: Grid):  # TODO make async
    # xml_files = download_data(url=grid.input_data)
    with tempfile.TemporaryDirectory(dir="./cim_files") as tmpdir:
        xml_files = download_grid_data(grid.input_data, tmp_dir=tmpdir)
        cgmes_data = cimpy.cim_import(xml_files, "cgmes_v2_4_15")
        converter = CGMESToPGMConverter()
        converter.load_cim_data(cgmes_data)
    pgm_data = converter.create_pgm_input()
    return PowerGridModel(input_data=pgm_data, system_frequency=grid.system_frequency)


def produce_output(grid: Grid, calculation_result: Any):
    print(calculation_result)


async def calculate_powerflow(grid: Grid, pf_kwargs: Dict[str, Any]):
    model = create_model(grid=grid)
    calculation_result = model.calculate_power_flow(**pf_kwargs)
    produce_output(grid, calculation_result)
