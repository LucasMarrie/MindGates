
import json
import math
import os

import random
from .logicGate import LogicGate, direction, gateType, logicGates

from settings import GRIDDATA_FILE, GRID_SIZE

class Cell():

    def __init__(self) -> None:
        self.empty = True
        self.value = False
        self.logicGate = None
        self.rotation = direction(0)

    def setGate(self, logicGate: LogicGate, rotation: direction):
        self.value = False
        self.logicGate = logicGate
        self.rotation = rotation
        if logicGate is None:
            self.empty = True
        else:
            self.empty = False

    #For toggling the cell value of switch nodes (nodes with not inputs)
    def toggleSwitch(self) -> None:
        self.value = not self.value


class Grid():

    def __init__(self, sizeX, sizeY) -> None:
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.grid = [[Cell() for _ in range(sizeY)] for _ in range(sizeX)]

    def __iter__(self) -> Cell:
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                yield x, y

    def setCell(self, coordinate: tuple[int, int], logicGate: LogicGate, rotation: direction = direction(0)) -> None:
        x, y = coordinate
        self.grid[x][y].setGate(logicGate, rotation)

    def getCell(self, coordinate: tuple[int, int]) -> Cell:
        x, y = coordinate
        return self.grid[x][y]

    def toggleCell(self, coordinate: tuple[int, int]) -> None:
        x, y = coordinate
        self.grid[x][y].toggleSwitch()

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

    
    def scrambleInputs(self):
        for coord in self:
            cell = self.getCell(coord)
            if (not cell.empty) and (cell.logicGate.type == gateType.start):
                if random.choice([True, False]):
                    cell.toggleSwitch()

    def save(self, saveName):

        classData = {}
        classData["cells"] = []

        classData["sizeX"] = self.sizeX
        classData["sizeY"] = self.sizeY
        

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                cell = self.grid[x][y]
                if not cell.empty:
                    cellData = {}
                    cellData["x"] = x
                    cellData["y"] = y
                    cellData["logicGate"] = cell.logicGate.name
                    cellData["rotation"] = cell.rotation.value
                    classData["cells"].append(cellData)

        try:
            if os.path.exists(GRIDDATA_FILE):
                with open(GRIDDATA_FILE, "r") as file:
                    data = json.load(file)
            else:
                data = {}
            
            data[saveName] = classData

            with open(GRIDDATA_FILE, "w") as file:
                json.dump(data, file)
        except Exception as ex:
            print("Error occured while saving to file:", ex)
        
    def updateSave(self, oldName, newName):
        self.deleteSave(oldName)
        self.save(newName)


    @classmethod
    def loadSave(cls, saveName) -> 'Grid':
        try:
            with open(GRIDDATA_FILE, "r") as file:
                data = json.load(file)
            
            if saveName not in data:
                return Grid(GRID_SIZE, GRID_SIZE)

            saveData = data[saveName]
            grid = Grid(saveData["sizeX"], saveData["sizeY"])
            for cell in saveData["cells"]:
                grid.setCell((cell["x"], cell["y"]), logicGates[cell["logicGate"]], direction(cell["rotation"]))

            return grid

        except Exception as ex:
            print("Error occured while loading save from file:", ex)

        return Grid(GRID_SIZE, GRID_SIZE)

    @classmethod
    def getSaves(cls) -> list[str]:
        try:
            with open(GRIDDATA_FILE, "r") as file:
                data = json.load(file)
            
            return list(data.keys())

        except Exception as ex:
            print("Error occured while loading save from file:", ex)

        return []
        
    @classmethod
    def deleteSave(cls, saveName):
        try:
            with open(GRIDDATA_FILE, "r") as file:
                data = json.load(file)
            if saveName in data:
                data.pop(saveName)
                with open(GRIDDATA_FILE, "w") as file:
                    json.dump(data, file)

        except Exception as ex:
            print("Error occured while deleting a save from file:", ex)

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

