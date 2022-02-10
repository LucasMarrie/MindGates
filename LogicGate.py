from enum import Enum
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

    def __init__(self, inputs, outputs) -> None:
        self.inputs = inputs
        self.outputs = outputs

    def inputCount(self) -> int:
        return len(self.inputs)
        
    def outputCount(self) -> int:
        return len(self.outputs)

class LogicGate():

    #to be assumed that the default logic gate rotation is right
    def __init__(self, name: str, inputs: set[direction, direction], outputs: set[direction, direction], operation : Callable[..., bool], image: str = "") -> None:
        self.name = name
        self.image = image
        self.outputs = outputs
        self.inputs = inputs
        self.operation = operation
        #makes sure inputs and outputs do not overlap
        for input in inputs:
            assert(input not in outputs)

    def evaluate(self, *args):
        return self.operation(*args)


logicGates = {
    #Logic Gates
    "AND" : LogicGate("AND", {direction.up, direction.down}, {direction.right}, lambda x, y: x and y), #AND gate
    "NAND" : LogicGate("NAND", {direction.up, direction.down}, {direction.right}, lambda x, y: not (x and y) ), #NAND gate
    "OR" : LogicGate("OR", {direction.up, direction.down}, {direction.right}, lambda x, y: x or y), #OR gate
    "NOR" : LogicGate("NOR", {direction.up, direction.down}, {direction.right}, lambda x, y: not (x or y) ), #NOR gate
    "XOR" : LogicGate("XOR", {direction.up, direction.down}, {direction.right}, lambda x, y: (x or y) and not (x and y)), #XOR gate
    "XNOR" : LogicGate("XNOR", {direction.up, direction.down}, {direction.right}, lambda x, y: not ((x or y) and not (x and y)) ), #XOR gate
    "NOT" : LogicGate("NOT", {direction.left}, {direction.right}, lambda x: not x), #NOT gate

    #Connecters
    "Line" : LogicGate("Line", {direction.left}, {direction.right}, lambda x: x), #Linear Connector
    "Bend" : LogicGate("Bend", {direction.down}, {direction.right}, lambda x: x), #Bend Connector

    #Start and End
    "Switch" : LogicGate("Switch", {}, {direction.right, direction.up, direction.left, direction.down}, lambda: True), #Start Node that's on
    #LogicGate("Switch", {}, {direction.right, direction.up, direction.left, direction.down}, lambda : False), #Start Node that's off

    "End" : LogicGate("End", {direction.left}, {}, lambda x: x), #End Node
}


    



