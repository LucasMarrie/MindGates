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
    
    def drawOneLine(self,startPos,endPos):
        pygame.draw.line(self.surface, TEXT_COLOR, startPos, endPos)
    
    def drawFullOutline(self):
        self.drawOneLine((self.x,self.y), (self.x+self.width, self.y))
        self.drawOneLine((self.x,self.y), (self.x, self.y+self.height))
        self.drawOneLine((self.x,self.y+self.height), (self.x+self.width, self.y+self.height))
        self.drawOneLine((self.x + self.width, self.y), (self.x + self.width, self.y+self.height))

    def draw(self):
        self.createTextBox()
        self.drawFullOutline()


class Label(Component):

    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, text: str, fontSize : int, textAlign : str) -> None:
        super().__init__(surface, x, y, width, height)
        self.fontSize = fontSize
        self.textAlign = textAlign
        self.updateText(text)

    def updateText(self, text):
        self.text = text
        pygame.draw.rect(self.surface, BACKGROUND_COLOR, pygame.Rect(self.x, self.y, self.width, self.height))
        self.draw()


    def drawOneLine(self,startPos,endPos):
        pygame.draw.line(self.surface, TEXT_COLOR, startPos, endPos)
    
    def createTextBox(self):
        font = pygame.font.Font(FONT_PATH, self.fontSize)
        text = font.render( self.text , True, TEXT_COLOR, BACKGROUND_COLOR)
        textRect = text.get_rect()
        if self.textAlign == "center":
            textRect.center = (self.x + self.width//2, self.y + self.height//2)
        elif self.textAlign == "left":
            textRect.midleft = (self.x, self.y + self.height//2)
        elif self.textAlign == "right":
            textRect.midright = (self.x + self.width, self.y + self.height//2)
        self.surface.blit(text, textRect)

    def draw(self):
        self.createTextBox()


class ToggleBox(Component):

    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        super().__init__(surface, x, y, width, height)
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