from turtle import right
import pygame

from game.logicGate import logicGates
from .displayGrid import GameGrid, SelectorGrid, gridType
from .colors import *

class GameWindow():

    def __init__(self) -> None:
        self.surface = pygame.display.set_mode((700,700))
        self.surface.fill(BACKGROUND_COLOR)
        self.gameGrid = GameGrid(self.surface, 100, 100, 500, 500, "Amogus Grid", gridType.edit)
        self.gameGrid.redraw()
        self.gameGrid.changeSelection(logicGates["AND"])
        self.run()

    def onLeftClick(self, x, y):
        self.gameGrid.onLeftClick(x, y)

    def onRightClick(self, x, y):
        self.gameGrid.onRightClick(x, y)

    def onRKey(self, x , y):
        self.gameGrid.onRKey(x,y)

    def run(self):
        pygame.init()
        LEFT = 1
        RIGHT = 3
        run = True
        while run:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                x, y = pygame.mouse.get_pos()                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == LEFT:
                        self.onLeftClick(x,y)
                    elif event.button == RIGHT:
                        self.onRightClick(x,y)
                elif event.type == pygame.KEYDOWN:
                    print("key down")
                    if event.key == pygame.K_r:
                        print("r press")
                        self.onRKey(x,y)

            pygame.display.update()

        pygame.quit()