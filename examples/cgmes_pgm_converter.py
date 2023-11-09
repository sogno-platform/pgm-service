import logging
import numpy as np
from enum import Enum

from power_grid_model import initialize_array


class System():
    def __init__(self):
        self.nodes = []
        self.voltages = []
        # self.branches = []

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
        list_ACLineSegment = [elem for elem in res.values() if elem.__class__.__name__ == "ACLineSegment"]
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
            # line = initialize_array("input", "line", len(self.lines))
            #
            # # Map each Line mRID to the assigned numerical Line ID
            # line["id"] = mapd(self.lines.keys(), self.asset_lookup)
            #
            # # Map the terminal mRID on the from/to side of each line to a Node mRID,
            # # and the Node mRID to the assigned numerical Node ID
            # line["from_node"] = mapd(
            #     mapd(
            #         self.lines.values(),
            #         self.terminals_to_node_lookup,
            #         lambda l: l.terminal_from,
            #         "Line-from Terminal",
            #         "Topology",
            #     ),
            #     self.asset_lookup,
            # )
            # line["to_node"] = mapd(
            #     mapd(
            #         self.lines.values(),
            #         self.terminals_to_node_lookup,
            #         lambda l: l.terminal_to,
            #         "Line-to Terminal",
            #         "Topology",
            #     ),
            #     self.asset_lookup,
            # )
            # # Map the terminal mRID on the from/to side of each line to a terminal status
            # line["from_status"] = mapd(
            #     self.lines.values(),
            #     self.terminal_status,
            #     lambda l: l.terminal_from,
            #     "Line-from Status",
            #     "SteadyStateHypothesis",
            # )
            # line["to_status"] = mapd(
            #     self.lines.values(),
            #     self.terminal_status,
            #     lambda l: l.terminal_to,
            #     "Line-to Status",
            #     "SteadyStateHypothesis",
            # )
            #
            # # Extract the Line parameters
            # # TODO r0, x0, c0 and tan0 are not defined yet, since they are only needed for asymmetrical calculations
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
