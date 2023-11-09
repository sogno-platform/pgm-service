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



        #
        #
        # self._setNodeType(list_Terminals)
        #
        # # create branches type ACLineSegment
        # for ACLineSegment in list_ACLineSegment:
        #     uuid_ACLineSegment = ACLineSegment.mRID
        #     nodes = self._get_nodes(list_Terminals, uuid_ACLineSegment)
        #     start_node = nodes[0]
        #     end_node = nodes[1]
        #
        #     base_voltage = ACLineSegment.BaseVoltage.nominalVoltage
        #     self.branches.append(Branch(uuid=uuid_ACLineSegment, r=ACLineSegment.r, x=ACLineSegment.x,
        #                                 start_node=start_node, end_node=end_node,
        #                                 base_voltage=base_voltage, base_apparent_power=base_apparent_power))
        #
        # # create branches type powerTransformer
        # for power_transformer in list_PowerTransformer:
        #     uuid_power_transformer = power_transformer.mRID
        #     nodes = self._get_nodes(list_Terminals, uuid_power_transformer)
        #     start_node = nodes[0]
        #     end_node = nodes[1]
        #
        #     # base voltage = high voltage side (=primaryConnection)
        #     primary_connection = self._get_primary_connection(list_PowerTransformerEnds, uuid_power_transformer)
        #     base_voltage = primary_connection.BaseVoltage.nominalVoltage
        #     self.branches.append(Branch(uuid=uuid_power_transformer, r=primary_connection.r, x=primary_connection.x,
        #                                 start_node=start_node, end_node=end_node, base_voltage=base_voltage,
        #                                 base_apparent_power=base_apparent_power))
        #
        # # create breakers
        # for obj_Breaker in list_Breakers:
        #     is_open = obj_Breaker.normalOpen
        #     nodes = self._get_nodes(list_Terminals, obj_Breaker.mRID)
        #     self.breakers.append(Breaker(from_node=nodes[0], to_node=nodes[1], is_open=is_open))
        #
        #     # if the breaker is open == closed --> close broker
        #     if is_open is False:
        #         self.breakers[-1].close_breaker()
        #     else:
        #         self.breakers[-1].ideal_connected_with = ''
        #
        # # calculate admitance matrix
        # self.Ymatrix_calc()


    def create_pgm_input(self):
        node = initialize_array("input", "node", len(self.nodes))
        node["id"] = range(len(self.nodes))
        node["u_rated"] = self.voltages
        print("debug")

        return {"node": node}