import logging
from pathlib import Path
import cimpy
import os
import requests
import glob
import pandas

from pgm_service.power_grid.cgmes_pgm_converter import System
from power_grid_model import PowerGridModel

logging.basicConfig(filename='run_powerflow.log', level=logging.INFO, filemode='w')

def download_grid_data(name, url):
    with open(name, 'wb') as out_file:
        content = requests.get(url, stream=True).content
        out_file.write(content)

url = 'https://raw.githubusercontent.com/dpsim-simulator/cim-grid-data/master/BasicGrids/NEPLAN/Slack_Load_Line_Sample/'
filename = 'Rootnet_FULL_NE_19J18h'
this_file_folder =  Path(__file__).parents[0]

absolute_path_EQ = os.path.join(this_file_folder, filename + '_EQ.xml')
absolute_path_TP = os.path.join(this_file_folder, filename + '_TP.xml')
absolute_path_SV = os.path.join(this_file_folder, filename + '_SV.xml')

#download_grid_data(absolute_path_EQ, url + filename + '_EQ.xml')
#download_grid_data(absolute_path_TP, url + filename + '_TP.xml')
#download_grid_data(absolute_path_SV, url + filename + '_SV.xml')

xml_files = [os.path.join(absolute_path_EQ),
             os.path.join(absolute_path_TP),
             os.path.join(absolute_path_SV)]

print('CGMES files to be loaded:')
print(xml_files)

## Read cim files and create new network.System object
res = cimpy.cim_import(xml_files, "cgmes_v2_4_15")

system = System()
system.load_cim_data(res)
pgm_input = system.create_pgm_input()
print('PGM input:')
print(pgm_input)

pgm = PowerGridModel(input_data=pgm_input)
results = pgm.calculate_power_flow()

print('PGM results:')
print(results["node"])

print(pandas.DataFrame(results["node"]))

system.pgm_to_SV(results, res)
