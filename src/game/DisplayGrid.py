from enum import Enum
import math
import pygame
from .grid import Grid
from .logicGate import LogicGate, direction, gateType
from .colors import *

class gridType(Enum):
    edit = 0
    interactive = 1
    locked = 2

class DisplayGrid():

    def __init__(self, surface : pygame.Surface, x: int, y: int, width: int, height: int, gridSizeX: int, gridSizeY: int) -> None:
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gridSizeX = gridSizeX
        self.gridSizeY = gridSizeY
        self.cellSizeX = self.width / self.gridSizeX
        self.cellSizeY = self.height / self.gridSizeY

    #helper methods
    def toCoord(self, gridX, gridY):
        x = self.x + (gridX / self.gridSizeX) * self.width
        y = self.y + (gridY / self.gridSizeY) * self.height
        return x, y

    def toGrid(self, x, y):
        gridX = int( (x - self.x) / (self.width / self.gridSizeX) )
        gridY = int( (y - self.y) / (self.height / self.gridSizeY) )
        return gridX, gridY

    def inBound(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height

    def onLeftClick(self, x, y):
        if not self.inBound(x,y):
            return

    def onRightClick(self, x, y):
        if not self.inBound(x,y):
            return

    #drawing functions
    def redraw(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, rect)
        self.drawGridLines()

    def drawGridLines(self):
        for i in range(self.gridSizeX + 1):
            fromPos = self.toCoord(i, 0)
            toPos = self.toCoord(i, self.gridSizeY)
            pygame.draw.line(self.surface, GRIDLINE_COLOR, fromPos, toPos)

        for i in range(self.gridSizeY + 1):
            fromPos = self.toCoord(0, i)
            toPos = self.toCoord(self.gridSizeX, i)
            pygame.draw.line(self.surface, GRIDLINE_COLOR, fromPos, toPos)

    def drawImage(self, x, y, imageSrc, rotation : direction):
        image = pygame.image.load(imageSrc)
        image = pygame.transform.scale(image, (self.cellSizeX-1, self.cellSizeY-1)) 
        image = pygame.transform.rotate(image, rotation.value * 90)
        self.surface.blit(image, (x + 1, y + 1))


class GameGrid(DisplayGrid):

    def __init__(self, surface : pygame.Surface, x: int, y: int, width: int, height: int, gridName: str, type: gridType) -> None:
        self.grid = Grid.loadSave(gridName)
        super().__init__(surface, x, y, width, height, self.grid.sizeX, self.grid.sizeY)
        self.type = type

    #event handling methods
    def changeSelection(self, logicGate: LogicGate):
        self.selectedGate = logicGate

    def onLeftClick(self, x, y):
        if not self.inBound(x,y):
            return
        if self.type == gridType.edit:
            gridX, gridY = self.toGrid(x, y)
            self.grid.setCell((gridX, gridY), self.selectedGate)
            self.updateCell(gridX, gridY)
        elif self.type == gridType.interactive:
            gridX, gridY = self.toGrid(x, y)
            self.grid.toggleCell((gridX, gridY))
            self.updateCell(gridX, gridY)

    def onRightClick(self, x, y):
        if not self.inBound(x,y):
            return
        if self.type == gridType.edit:
            gridX, gridY = self.toGrid(x, y)
            self.grid.setCell((gridX, gridY), None)
            self.updateCell(gridX, gridY)

    def onRKey(self, x, y):
        if not self.inBound(x,y):
            return
        if self.type == gridType.edit:
            gridX, gridY = self.toGrid(x, y)
            self.grid.getCell((gridX, gridY)).rotation = self.grid.getCell((gridX, gridY)).rotation.rotate(1)
            self.updateCell(gridX, gridY)

    #drawing functions
    def redraw(self):
        super().redraw()
        self.drawLogicGates()

    def drawLogicGates(self):
        for x, y in self.grid:
            if not self.grid.getCell((x,y)).empty:
                self.updateCell(x, y)

    def updateCell(self, gridX, gridY):
        x, y = self.toCoord(gridX, gridY)
        rect = pygame.Rect(x + 1, y + 1, self.cellSizeX-1, self.cellSizeY-1)
        cell = self.grid.getCell((gridX, gridY))
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, rect)
        if not cell.empty:
            if cell.logicGate.type == gateType.start and cell.value:
                self.drawImage(x, y, cell.logicGate.images[1], cell.rotation)
            else:
                self.drawImage(x, y, cell.logicGate.images[0], cell.rotation)


class SelectorGrid(DisplayGrid):

    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, gridSizeX: int, gridSizeY: int, logicGates: list[LogicGate]) -> None:
        super().__init__(surface, x, y, width, height, gridSizeX, gridSizeY)

        count = 0
        self.grid = [[None] * gridSizeY for _ in gridSizeX]
        for gate in logicGates:
            gridX = count // gridSizeX
            gridY = count % gridSizeY
            self.grid[gridX][gridY] = gate
            self.drawImage(gridX, gridY, gate.images[0])
            count += 1

    def redraw(self):
        super().redraw()
        self.drawLogicGates()

    def drawLogicGates(self):
        pass