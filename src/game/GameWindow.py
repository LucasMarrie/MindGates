import random
import pygame
import time
from game.grid import Grid
from game.logicGate import gateType, logicGates
from .displayGrid import GameGrid, SelectorGrid, gridType
from .components import Button, Label
from .colors import *
from settings import EVALUATE_OUTPUT_ROUNDS
from .popup import Popup
from . import scores

class GameWindow():

    def __init__(self) -> None:
        pygame.init()
        self.components = {}

    def display(self):
        pass

    def keyEvent(self, x, y, eventName):
        try:
            for component in self.components.values():
                if hasattr(component, eventName):
                    getattr(component, eventName)(x, y)
        except Exception as ex:
            print("error: ", ex)

    def onEnterKey(self):
        pass

    def stopRunning(self):
        self.running = False

    def run(self):
        self.running = True
        LEFT = 1
        RIGHT = 3
        self.start()
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
                    elif event.key == pygame.K_RETURN:
                        self.onEnterKey()

            self.update()
            pygame.display.update()

        pygame.quit()
    
    def start(self):
        pass

    def update(self):
        pass


class EditWindow(GameWindow):

    def __init__(self, gridName) -> None:
        super().__init__()
        self.gridName = gridName
        self.grid = Grid.loadSave(gridName)
        self.display()
        self.run()

    def display(self):
        self.surface = pygame.display.set_mode((750,625))
        self.surface.fill(BACKGROUND_COLOR)
        self.components["gameGrid"] = GameGrid(self.surface, 200, 25, 500, 500, self.grid, self.gridName, gridType.edit)
        self.components["selectorGrid"] = SelectorGrid(self.surface, 50, 25, 143, 500, 2, 7, logicGates, self.components["gameGrid"].changeSelection)
        self.components["saveButton"] = Button(self.surface, 50, 538, 200, 75, "SAVE", 40, self.components["gameGrid"].save)
        self.components["deleteButton"] = Button(self.surface, 275, 538, 200, 75, "DELETE", 40, self.deleteSave)
        self.components["exitButton"] = Button(self.surface, 500, 538, 200, 75, "EXIT", 40, self.stopRunning)

    def onEnterKey(self):
        self.components["gameGrid"].save()

    def deleteSave(self):
        self.components["gameGrid"].delete()
        self.stopRunning()

class EvaluateOutput(GameWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.score = 0
        self.round = 1
        self.playing = True
        self.newExercise()
        self.run()

    def newExercise(self):
        saveNames = Grid.getSaves()
        self.grid = Grid.loadSave(random.choice(saveNames))
        self.grid.scrambleInputs()
        self.display()

    def determineCorrectness(self):
        for gridX, gridY in self.grid:
            cell = self.grid.getCell((gridX,gridY))
            if not cell.empty and cell.logicGate.type == gateType.end:
                return self.grid.evaluateCell((gridX, gridY)) == cell.value
        return True

    def submit(self):
        if not self.playing:
            return
        if self.determineCorrectness():
            self.score += 1
        if self.round == EVALUATE_OUTPUT_ROUNDS:
            self.time = time.time() - self.startTime
            self.playing = False
            scores.addScore(self.score, self.time)
            highScores = scores.getSortedScores()
            for i, score in enumerate(highScores):
                if score["score"] == self.score and score["time"] == self.time:
                    self.ranking = i + 1
                    break
            self.displayEndScreen()
        else:
            self.round += 1
            self.newExercise()

    def onEnterKey(self):
        self.submit()

    def display(self):
        self.surface = pygame.display.set_mode((600,675))
        self.surface.fill(BACKGROUND_COLOR)
        self.components["timeLabel"] = Label(self.surface, 50, 0, 250, 75, "TIME: ", 40, "left")
        self.components["roundLabel"] = Label(self.surface, 300, 0, 250, 75, f"ROUND: {self.round}", 40, "right")
        self.components["gameGrid"] = GameGrid(self.surface, 50, 75, 500, 500, self.grid, "", gridType.evaluateOutput)
        self.components["nextButton"] = Button(self.surface, 50, 587, 225, 75, "SUBMIT", 40, self.submit)
        self.components["exitButton"] = Button(self.surface, 325, 587, 225, 75, "EXIT", 40, self.stopRunning)

    def displayEndScreen(self):
        self.surface = pygame.display.set_mode((600,675))
        self.surface.fill(BACKGROUND_COLOR)
        self.components["titleLabel"] = Label(self.surface, 50, 50, 500, 75, "RESULTS ", 100, "left")
        self.components["scoreLabel"] = Label(self.surface, 50, 150, 500, 75, f"SCORE: {self.score}", 60, "left")
        self.components["accuracyLabel"] = Label(self.surface, 50, 250, 500, 75, f"ACCURACY: {self.score/self.round * 100}%", 60, "left")
        self.components["rankingLabel"] = Label(self.surface, 50, 350, 500, 75, f"RANKING: {self.ranking}", 60, "left")
        self.components["timeLabel"] = Label(self.surface, 50, 450, 500, 75, f"TIME: " + str(round(self.time, 2)), 60, "left")
        self.components["exitButton"] = Button(self.surface, 50, 550, 500, 75, "EXIT", 40, self.stopRunning)


    def start(self):
        self.startTime = time.time() 

    def update(self):
        if self.playing:
            elapsedtime = time.time() - self.startTime
            self.components["timeLabel"].updateText("TIME: " + str(round(elapsedtime, 2)))