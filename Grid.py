
import pickle
import shelve
import math
import os

from LogicGate import LogicGate, direction, logicGates

class Cell():

    def __init__(self) -> None:
        self.empty = True
        self.value = False

    def setGate(self, logicGate: LogicGate, rotation: direction):
        self.value = False
        self.logicGate = logicGate
        self.rotation = rotation
        if logicGate is None:
            self.empty = True
        else:
            self.empty = False

    #For toggling the cell value of switch nodes (nodes with not inputs)
    def toggleSwitch(self, value : bool) -> None:
        self.value = value


class Grid():

    def __init__(self, sizeX, sizeY) -> None:
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.grid = [[Cell() for _ in range(sizeY)] for _ in range(sizeX)]


    def setCell(self, coordinate: tuple[int, int], logicGate: LogicGate, rotation: direction = direction(0)) -> None:
        x, y = coordinate
        self.grid[x][y].setGate(logicGate, rotation)

    def getCell(self, coordinate: tuple[int, int]) -> Cell:
        x, y = coordinate
        return self.grid[x][y]

    def evaluateCell(self, coordinate: tuple[int, int], outputIndex : int = 0, outputDirection : direction = direction.right):

        if not self.inBound(coordinate) or self.getCell(coordinate).empty:
            return False
        cell = self.getCell(coordinate)
        x, y = coordinate
        logicGate = cell.logicGate
        inputs = []

        #When a logic gate has no inputs, it's a switch, thus we evaluate based off the value given to the cell
        if len(logicGate.inOut.inputs) == 0:
            return cell.value

        #getting the desired input based off the output index, only applies to cells that have an output count greater than 1
        input = logicGate.inOut.getInputs(outputDirection)[outputIndex]
        rotation = cell.rotation.rotate(input.value)
        newX = round(x + math.cos(math.pi/2 * rotation.value))
        newY = round(y - math.sin(math.pi/2 * rotation.value))
        newCoord = (newX, newY) 

        if self.inBound(newCoord) and not self.getCell(newCoord).empty:
            outputCell = self.getCell(newCoord)
            outputRotation = rotation.rotate(2 - outputCell.rotation.value)
            if outputCell.logicGate.inOut.matchingOut(outputRotation, logicGate.inOut.inCount):
                # fetches multiple inputs if needed
                for i in range(logicGate.inOut.inCount):
                    inputs.append(self.evaluateCell(newCoord, i, outputRotation))
            else:
                for i in range(logicGate.inOut.inCount):
                    inputs.append(False)
        else:
            for i in range(logicGate.inOut.inCount):
                inputs.append(False)

        return cell.logicGate.evaluate(*inputs)


    def inBound(self, coordinate: tuple[int, int]) -> bool:
        x, y = coordinate
        if x < 0 or y < 0 or x >= self.sizeX or y >= self.sizeY:
            return False
        return True

    def printOut(self):
        for y in range(self.sizeY):
            line = ""
            for x in range(self.sizeX):
                cell = self.getCell((x,y))
                if cell.empty:
                    line += " "
                else:
                    line += cell.logicGate.name[0]
            print(line)


    saveFile = "data/gridData.json"

    def save(self, saveName):
        try:
            with shelve.open(self.saveFile) as data:
                data[saveName] = self

        except Exception as ex:
            print("Error During Grid data save:", ex)

    @classmethod
    def loadSave(cls, saveName):
        try:
            with shelve.open(cls.saveFile) as data:
                if saveName in data:
                    return data[saveName]
                else:
                    return None

        except Exception as ex:
            print("Error During Grid data load:", ex)

 
    @classmethod
    def deleteSave(cls, saveName):
        try:
            with shelve.open(cls.saveFile) as data:
                if saveName in data:
                    data.pop(saveName)

        except Exception as ex:
            print("Error During Grid data deletion:", ex)


if __name__ == "__main__":
    grid = Grid(10, 10)

    grid.setCell((0,0), logicGates["Switch"])
    grid.setCell((0,1), logicGates["Line"], direction.down)
    grid.setCell((0,2), logicGates["Merger"])
    grid.setCell((1,2), logicGates["AND"])
    grid.setCell((0,3), logicGates["Switch"])

    grid.getCell((0,0)).toggleSwitch(True)
    grid.getCell((0,3)).toggleSwitch(True)
    

    grid.printOut()

