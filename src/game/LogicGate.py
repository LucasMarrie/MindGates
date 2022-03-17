from enum import Enum
from sysconfig import get_path_names
from typing import Callable

class direction(Enum):
    right = 0
    up = 1
    left = 2
    down = 3

    @classmethod
    def _missing_(cls, value):
        return direction.right

    @classmethod
    def rotation(cls, dir, rotation: int):
        value = (dir.value +  rotation) % len(direction)
        if value < 0:
            value += len(direction)
        return direction(value)

    def rotate(self, rotation: int):
        return direction.rotation(self, rotation)
        

class gateType(Enum):
    logic = 0
    connector = 1
    start = 2
    end = 3


class InOut():

    def __init__(self, inputs : list[direction], inCount : int, outputs : list[direction], outCount : int, bidirectional : bool = False) -> None:
        self.inputs = inputs
        #In and Out count are the amount of inputs/outputs received from the same direction
        self.inCount = inCount
        self.outputs = outputs
        self.outCount = outCount

        self.bidirectional = bidirectional
        if bidirectional:
            #omni can only be used if outputs and inputs are the same
            assert(inCount == outCount and len(inputs) == 1 and len(outputs) == 1)

    def matchingOut(self, requiredOutput, inputCount):
        if self.outCount != inputCount:
            return False
        if self.bidirectional:
            return requiredOutput in self.inputs or requiredOutput in self.outputs
        else:
            return requiredOutput in self.outputs

    def getInputs(self, output):
        if self.bidirectional and output in self.inputs:
            return self.outputs
        return self.inputs


class LogicGate():

    #to be assumed that the default logic gate rotation is right
    def __init__(self, name: str, type : gateType, inOut : InOut, operation : Callable[..., bool], image: str = "") -> None:
        self.name = name
        self.type = gateType
        self.image = image
        self.inOut = inOut
        self.operation = operation
        #makes sure inputs and outputs do not overlap
        

    def evaluate(self, *args):
        return self.operation(*args)



logicGates_list = [
    #Logic Gates
    LogicGate("AND", gateType.logic, InOut([direction.left], 2, [direction.right], 1), lambda x, y: x and y), #AND gate
    LogicGate("NAND", gateType.logic, InOut([direction.left], 2, [direction.right], 1), lambda x, y: not (x and y) ), #NAND gate
    LogicGate("OR", gateType.logic, InOut([direction.left], 2, [direction.right], 1), lambda x, y: x or y), #OR gate
    LogicGate("NOR", gateType.logic, InOut([direction.left], 2, [direction.right], 1), lambda x, y: not (x or y) ), #NOR gate
    LogicGate("XOR", gateType.logic, InOut([direction.left], 2, [direction.right], 1), lambda x, y: (x or y) and not (x and y)), #XOR gate
    LogicGate("XNOR", gateType.logic, InOut([direction.left], 2, [direction.right], 1), lambda x, y: not ((x or y) and not (x and y)) ), #XOR gate
    LogicGate("NOT", gateType.logic, InOut([direction.left], 1, [direction.right], 1), lambda x: not x), #NOT gate

    #Connecters
    LogicGate("Line", gateType.connector, InOut([direction.left], 1, [direction.right], 1, bidirectional=True), lambda x: x), #Linear Connector
    LogicGate("Bend", gateType.connector, InOut([direction.down], 1, [direction.right], 1, bidirectional=True), lambda x: x), #Bend Connector

    LogicGate("Splitter", gateType.connector, InOut([direction.left], 1, [direction.up, direction.down], 1,), lambda x: x), #Splits an output into 2 direction
    LogicGate("Merger", gateType.connector, InOut([direction.up, direction.down], 1, [direction.right], 2), lambda x: x), #Combines inputs from 2 directions into the same direction

    #Start and End
    LogicGate("Switch", gateType.start, InOut([], 0, [direction.right, direction.up, direction.left, direction.down], 1), lambda: True), #Start Node that's on

    LogicGate("End", gateType.end, InOut([direction.left], 1, [], 0), lambda x: x), #End Node
]

logicGates = {gate.name : gate for gate in logicGates_list}



