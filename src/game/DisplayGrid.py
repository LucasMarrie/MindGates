import pygame
from Grid import Grid
from Colors import *

class DisplayGrid():

    def __init__(self, surface, x, y, width, height, gridName) -> None:
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.grid = Grid.loadSave(gridName)
        self.cellSizeX = self.width/ self.grid.sizeX
        self.cellSizeY = self.width/ self.grid.sizeY

    def toCoord(self, gridX, gridY):
        x = self.x + (gridX / self.grid.sizeX) * self.width
        y = self.y + (gridY / self.grid.sizeY) * self.height
        return x, y

    def toGrid(self, x, y):
        gridX = (x - self.x) // (self.width / self.grid.sizeX)
        gridY = (y - self.y) // (self.height / self.grid.sizeY)
        return gridX, gridY

    def onClick(self, x, y):
        if not self.inBound(x,y):
            return
        gridX, gridY = self.toGrid(x, y)
        print(gridX, gridY)

    def inBound(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height

    #drawing functions
    def redraw(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, rect)
        self.drawGridLines()
        self.drawLogicGates()

    def drawGridLines(self):
        for i in range(self.grid.sizeX + 1):
            fromPos = self.toCoord(i, 0)
            toPos = self.toCoord(i, self.grid.sizeY)
            pygame.draw.line(self.surface, BLACK, fromPos, toPos)

        for i in range(self.grid.sizeY + 1):
            fromPos = self.toCoord(0, i)
            toPos = self.toCoord(self.grid.sizeX, i)
            pygame.draw.line(self.surface, BLACK, fromPos, toPos)

    def drawLogicGates(self):
        for x, y in self.grid:
            if not self.grid.getCell((x,y)).empty:
                self.updateCell(x, y)


    def updateCell(self, x, y):
        coordX, coordY = self.toCoord(x,y)
        rect = pygame.Rect(coordX + 1, coordY + 1, self.cellSizeX-1, self.cellSizeY-1)
        if self.grid.getCell((x,y)).empty:
            pygame.draw.rect(self.surface, BACKGROUND_COLOR, rect)
        else:
            pygame.draw.rect(self.surface, BLACK, rect)
    