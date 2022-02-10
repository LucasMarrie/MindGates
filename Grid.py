
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

    def evaluateCell(self, coordinate: tuple[int, int]):
        if not self.inBound(coordinate) or self.getCell(coordinate).empty:
            return False
        cell = self.getCell(coordinate)
        x, y = coordinate
        logicGate = cell.logicGate
        inputs = []

        if len(logicGate.inputs) == 0:
            return cell.value

        for input in logicGate.inputs:
            rotation = cell.rotation.rotate(input.value)
            newX = round(x + math.cos(math.pi/2 * rotation.value))
            newY = round(y + math.sin(math.pi/2 * rotation.value))
            newCoord = (newX, newY) 

            if not self.inBound(newCoord):
                inputs.append(False)
            else:
                newCell = self.getCell(newCoord)
                if not newCell.empty and rotation.rotate(2 - newCell.rotation.value) in newCell.logicGate.outputs:
                    inputs.append(self.evaluateCell(newCoord))
                else:
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
    grid.printOut()