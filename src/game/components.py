from typing import Callable, Tuple
import pygame
from settings import FONT_PATH
from .colors import TEXT_COLOR
from .colors import BACKGROUND_COLOR

class Component():

    def __init__(self, surface: pygame.Surface, x : int, y : int, width : int, height : int) -> None:
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def inBound(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height



class Button(Component):

    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, text : str, fontSize : int, leftClickEvent : Callable) -> None:
        super().__init__(surface, x, y, width, height)
        self.leftClickEvent = leftClickEvent
        self.text = text
        self.fontSize = fontSize
        self.draw()
    
    def createTextBox(self):
        font = pygame.font.Font(FONT_PATH, self.fontSize)
        text = font.render(self.text, True, TEXT_COLOR, BACKGROUND_COLOR)
        textRect = text.get_rect()
        textRect.center = (self.x + self.width//2, self.y + self.height//2)
        self.surface.blit(text, textRect)


    def onLeftClick(self, x, y):
        if not self.inBound(x, y):
            return
        self.leftClickEvent()

    def draw(self):
        self.createTextBox()
        
class ToggleBox(Component):

    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, imageSrc_false : str, imageSrc_true : str) -> None:
        super().__init__(surface, x, y, width, height)
        self.imageSrc_false = imageSrc_false
        self.imageSrc_true = imageSrc_true
        self.value = False

    def onLeftClick(self, x, y):
        if not self.inBound(x, y):
            return
        self.leftClickEvent()
    
    def draw(self):
        imageSrc = self.imageSrc_true if self.value else self.imageSrc_false
        image = pygame.image.load(imageSrc)
        image = pygame.transform.scale(image, (self.width, self.height)) 
        self.surface.blit(image, (self.x, self.y))