import logging
from pathlib import Path
import numpy
import cimpy
import os

from cgmes_pgm_converter import System


logging.basicConfig(filename='run_nv_powerflow.log', level=logging.INFO, filemode='w')

#python starts as module in subdirectory, 2 folders up to set the new path
this_file_folder =  Path(__file__).parents[0]
p = str(this_file_folder) + "/data"
xml_path = Path(p)


xml_files = [os.path.join(xml_path, "Rootnet_FULL_NE_19J18h_TP.xml"),
             os.path.join(xml_path, "Rootnet_FULL_NE_19J18h_EQ.xml"),
             os.path.join(xml_path, "Rootnet_FULL_NE_19J18h_SV.xml")]

# Read cim files and create new network.System object
res = cimpy.cim_import(xml_files, "cgmes_v2_4_15")

system = System()
system.load_cim_data(res)

print("debug")