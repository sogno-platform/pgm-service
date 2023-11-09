import logging
import numpy as np
from enum import Enum

from power_grid_model import initialize_array


class System():
    def __init__(self):
        self.nodes = []
        self.voltages = []
        self.lines = {}

    def load_cim_data(self, res):
        """
        fill the vectors node, branch and breakers
        """

        index = 0
        list_TPNode = [elem for elem in res['topology'].values() if elem.__class__.__name__ == "TopologicalNode"]
        dict_VoltageLevel = {elem.TopologicalNode[0]: elem.BaseVoltage.nominalVoltage * 1e3 for elem in res['topology'].values() if elem.__class__.__name__ == "VoltageLevel"}
        # list_SvVoltage = [elem for elem in res.values() if elem.__class__.__name__ == "SvVoltage"]
        # list_SvPowerFlow = [elem for elem in res.values() if elem.__class__.__name__ == "SvPowerFlow"]
        # list_EnergySources = [elem for elem in res.values() if elem.__class__.__name__ == "EnergySource"]
        # list_EnergyConsumer = [elem for elem in res.values() if elem.__class__.__name__ == "EnergyConsumer"]
        # list_ACLineSegment = [elem for elem in res.values() if elem.__class__.__name__ == "ACLineSegment"]
        # list_Terminals = [elem for elem in res.values() if elem.__class__.__name__ == "Terminal"]
        # list_Terminals_ES = [elem for elem in list_Terminals if
        #                      elem.ConductingEquipment.__class__.__name__ == "EnergySource"]
        # list_Terminals_EC = [elem for elem in list_Terminals if
        #                      elem.ConductingEquipment.__class__.__name__ == "EnergyConsumer"]

        # create nodes
        for TPNode in list_TPNode:
            self.nodes.append(TPNode.mRID)
            self.voltages.append(dict_VoltageLevel[TPNode])

        # # create branches type ACLineSegment
        # for ACLineSegment in list_ACLineSegment:
        #     self.lines[ACLineSegment]

        # line = initialize_array("input", "line", len(self.lines))
        # line["id"] =
        # line["from_node"] =
        # line["to_node"] =
        # line["from_status"] =
        # line["to_status"] =
        # line["r1"] = [single_line.r for single_line in self.lines.values()]
        # line["x1"] = [single_line.x for single_line in self.lines.values()]
        # line["c1"] = [single_line.bch / (2 * np.pi * FREQUENCY) for single_line in self.lines.values()]
        # line["tan1"] = [single_line.gch / single_line.bch for single_line in self.lines.values()]
        # line["i_n"] = [single_line.ratedCurrent for single_line in self.lines.values()]



    def create_pgm_input(self):
        node = initialize_array("input", "node", len(self.nodes))
        node["id"] = range(len(self.nodes))
        node["u_rated"] = self.voltages
        print("debug")

        return {"node": node}
