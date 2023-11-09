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


def create_model(grid: Grid):  # TODO make async
    # xml_files = download_data(url=grid.input_data)
    with tempfile.TemporaryDirectory() as tmpdir:
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
