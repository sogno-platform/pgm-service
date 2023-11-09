import logging
import numpy as np
from enum import Enum

from power_grid_model import initialize_array


FREQUENCY = 50.0
DEFAULT_SOURCE_SHORT_CIRCUIT_POWER = 1e20

class System():
    def __init__(self):
        self.nodes = []
        self.voltages = []
        self.lines = {}
        self.sources = {}

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
        list_ACLineSegment = [elem for elem in res['topology'].values() if elem.__class__.__name__ == "ACLineSegment"]
        list_Terminals = [elem for elem in res['topology'].values() if elem.__class__.__name__ == "Terminal"]
        # list_Terminals_ES = [elem for elem in list_Terminals if
        #                      elem.ConductingEquipment.__class__.__name__ == "EnergySource"]
        # list_Terminals_EC = [elem for elem in list_Terminals if
        #                      elem.ConductingEquipment.__class__.__name__ == "EnergyConsumer"]
        list_Source = [elem for elem in res['topology'].values() if elem.__class__.__name__ == "ExternalNetworkInjection"]

        # create nodes
        for TPNode in list_TPNode:
            self.nodes.append(TPNode.mRID)
            self.voltages.append(dict_VoltageLevel[TPNode])

        # create branches type ACLineSegment
        for ACLineSegment in list_ACLineSegment:
            uuid_ACLineSegment = ACLineSegment.mRID
            connected_nodes = self._get_nodes(list_Terminals, uuid_ACLineSegment)
            node_ids = list(connected_nodes.keys())
            status = list(connected_nodes.values())
            self.lines[ACLineSegment.mRID] = {"from_node": self.nodes.index(node_ids[0]),
                                              "to_node": self.nodes.index(node_ids[1]),
                                              "from_status": status[0],
                                              "to_status": status[0],
                                              "r1": ACLineSegment.r,
                                              "x1": ACLineSegment.x,
                                              "c1": ACLineSegment.bch / (2 * np.pi * FREQUENCY),
                                              "tan1": ACLineSegment.gch / ACLineSegment.bch}
            # TODO: check if there is a multiplier for r1/x1, c1, tan1, i_n

        for source in list_Source:
            connected_node = self._get_node(list_Terminals, source.mRID)
            node_id = next(iter(connected_node))
            status = connected_node[node_id]
            self.sources[source.mRID] = {"node": self.nodes.index(node_id),
                                         "status": status,
                                         "u_ref": 1.0,
                                         "sk": DEFAULT_SOURCE_SHORT_CIRCUIT_POWER}

    def create_pgm_input(self):
        id_counter = 0
        node = initialize_array("input", "node", len(self.nodes))
        node["id"] = range(len(self.nodes))
        node["u_rated"] = self.voltages
        id_counter += len(self.nodes)

        line = initialize_array("input", "line", len(self.lines))
        line["id"] = range(id_counter, id_counter + len(self.lines))
        line["from_node"] = [line_param["from_node"] for line_param in self.lines.values()]
        line["to_node"] = [line_param["to_node"] for line_param in self.lines.values()]
        line["from_status"] = [line_param["from_status"] for line_param in self.lines.values()]
        line["to_status"] = [line_param["to_status"] for line_param in self.lines.values()]
        line["r1"] = [line_param["r1"] for line_param in self.lines.values()]
        line["x1"] = [line_param["x1"] for line_param in self.lines.values()]
        line["c1"] = [line_param["c1"] for line_param in self.lines.values()]
        line["tan1"] = [line_param["tan1"] for line_param in self.lines.values()]
        id_counter += len(self.lines)

        source = initialize_array("input", "source", len(self.sources))
        source["id"] = range(id_counter, id_counter + len(self.sources))
        source["node"] = [source_param["node"] for source_param in self.sources.values()]
        source["status"] = [source_param["status"] for source_param in self.sources.values()]
        source["u_ref"] = [source_param["u_ref"] for source_param in self.sources.values()]
        source["sk"] = [source_param["sk"] for source_param in self.sources.values()]

        return {"node": node,
                "line": line,
                "source": source}

    def _get_nodes(self, list_Terminals, elem_uuid):
        start_node_uuid = None
        end_node_uuid = None
        start_node_connected = None
        end_node_connected = None

        for terminal in list_Terminals:
            if terminal.ConductingEquipment.mRID != elem_uuid:
                continue
            sequence_number = terminal.sequenceNumber
            if sequence_number == 1:
                start_node_uuid = terminal.TopologicalNode.mRID
                start_node_connected = terminal.connected
            elif sequence_number == 2:
                end_node_uuid = terminal.TopologicalNode.mRID
                end_node_connected = terminal.connected


        return {start_node_uuid: start_node_connected, end_node_uuid: end_node_connected}

    def _get_node(self, list_Terminals, elem_uuid):
        node_uuid = None
        node_connected = None

        for terminal in list_Terminals:
            if terminal.ConductingEquipment.mRID != elem_uuid:
                continue
            node_uuid = terminal.TopologicalNode.mRID
            node_connected = terminal.connected

        return {node_uuid: node_connected}
