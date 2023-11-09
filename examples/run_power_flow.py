import logging
from pathlib import Path
import cimpy
import os

import requests
import glob

from src.pgm_service.power_grid.cgmes_pgm_converter import System

logging.basicConfig(filename='run_powerflow.log', level=logging.INFO, filemode='w')

def download_grid_data(name, url):
    with open(name, 'wb') as out_file:
        content = requests.get(url, stream=True).content
        out_file.write(content)

url = 'https://raw.githubusercontent.com/dpsim-simulator/cim-grid-data/master/BasicGrids/NEPLAN/Slack_Load_Line_Sample/'
filename = 'Rootnet_FULL_NE_19J18h'

# download_grid_data(filename+'_EQ.xml', url + filename + '_EQ.xml')
# download_grid_data(filename+'_TP.xml', url + filename + '_TP.xml')
# download_grid_data(filename+'_SV.xml', url + filename + '_SV.xml')
#
files = glob.glob(filename+'_*.xml')

print('CGMES files downloaded:')
print(files)

this_file_folder =  Path(__file__).parents[0]
p = str(this_file_folder)
xml_path = Path(p)
xml_files = [os.path.join(xml_path, filename+'_EQ.xml'),
             os.path.join(xml_path, filename+'_TP.xml'),
             os.path.join(xml_path, filename+'_SV.xml')]

print(xml_files)

## Read cim files and create new network.System object
res = cimpy.cim_import(xml_files, "cgmes_v2_4_15")

system = System()
system.load_cim_data(res)
pgm_input = system.create_pgm_input()

print(pgm_input)