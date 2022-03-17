from turtle import onclick
import pygame
from DisplayGrid import DisplayGrid
from Colors import *

class GameWindow():

    def __init__(self) -> None:
        self.surface = pygame.display.set_mode((500,500))
        self.surface.fill(BACKGROUND_COLOR)
        self.displayGrid = DisplayGrid(self.surface, 100, 100, 300, 300, "Amogus Grid")
        self.displayGrid.redraw()
        self.run()

    def onClick(self, x, y):
        self.displayGrid.onClick(x, y)

    def run(self):
        pygame.init()
        run = True
        while run:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    self.onClick(x,y)
                    


            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    GameWindow()