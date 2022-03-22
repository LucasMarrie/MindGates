import pygame
import os
from game.logicGate import logicGates
from .displayGrid import GameGrid, SelectorGrid, gridType
from .components import Button
from .colors import *

pygame.init()

class GameWindow():

    def __init__(self) -> None:
        self.components = {}

    def display(self):
        pass

    def keyEvent(self, x, y, eventName):
        for component in self.components.values():
            if hasattr(component, eventName):
                getattr(component, eventName)(x, y)

    def stopRunning(self):
        self.running = False

    def run(self):
        self.running = True
        LEFT = 1
        RIGHT = 3
        while self.running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                x, y = pygame.mouse.get_pos()                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == LEFT:
                        self.keyEvent(x,y, "onLeftClick")
                    elif event.button == RIGHT:
                        self.keyEvent(x,y, "onRightClick")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.keyEvent(x,y, "onRKey")

            pygame.display.update()

        pygame.quit()


class EditWindow(GameWindow):

    def __init__(self, gridName) -> None:
        super().__init__()
        self.gridName = gridName
        self.display()
        self.run()

    def display(self):
        self.surface = pygame.display.set_mode((1000,700))
        self.surface.fill(BACKGROUND_COLOR)
        self.components["gameGrid"] = GameGrid(self.surface, 200, 50, 500, 500, self.gridName, gridType.edit)
        self.components["selectorGrid"] = SelectorGrid(self.surface, 50, 50, 143, 500, 2, 7, logicGates, self.components["gameGrid"].changeSelection)
        self.components["saveButton"] = Button(self.surface, 50, 600, 100, 100, "save", 20, self.components["gameGrid"].save)
        self.components["exitButton"] = Button(self.surface, 150, 600, 100, 100, "exit", 20, self.stopRunning)

