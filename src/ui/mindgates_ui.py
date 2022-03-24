from game.gameWindow import EditWindow, EvaluateOutput
from game.grid import Grid
import tkinter as tk
from PIL import Image, ImageTk
import os
from game import scores
from game.popup import Popup
from settings import MAX_SCORES

basedir = os.path.dirname(__file__)
os.path.join(basedir, "go_back.png")

def createTitle(filename, root=None , x=None, y=None):
    title = Image.open(filename)
    title = ImageTk.PhotoImage(title)
    title_label = tk.Label(root, image = title, bg = '#00162D')
    title_label.image = title
    title_label.place(x = x, y = y)
    return title_label

def createButton(filename, root, command, x=None, y=None):
    logo = Image.open(filename)
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Button(root, image = logo, bg = '#00162D', fg = '#00162D', activebackground = '#00162D', command=command, borderwidth=0)
    logo_label.image = logo
    logo_label.place(x=x, y=y)
    return logo_label
    # no need for return

def createTextButton(root, saveText, command, x=None, y=None):
    button = tk.Button(root, text=saveText, bg = '#00162D', font=("Endless Boss Battle", 22), fg = '#D4FAFF', activebackground = '#D4FAFF', command=command, borderwidth=0)
    button.place(x=x,y=y)
    return button

def createTextLabel(root,saveText, x=None, y=None):
    text_label = tk.Button(root, text=saveText, bg = '#00162D', font=("Endless Boss Battle", 25), fg = '#D4FAFF', activebackground = '#D4FAFF', borderwidth=0)
    text_label.place(x=x, y=y)
    return text_label


def createGoBackButton(root, master):
    createButton(os.path.join(basedir, "go_back.png"), root=root, command= lambda: master.goToPage(MainPage), x=28.5, y=28.5)

class MindGatesApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.goToPage(MainPage)
        self.title("MindGates")
        self.eval('tk::PlaceWindow . center')


    def goToPage(self, namePage):
        nextFrame = namePage(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = nextFrame
        self.frame.pack()
        

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()
    
    def createAll(self):
        createTitle(os.path.join(basedir, "main_title.png"), root = self, x = 28.5, y = 71.5)
        createButton(os.path.join(basedir, "play.png"), root = self, command = lambda: openGame(self.master), x=32.5, y=165)
        createButton(os.path.join(basedir, "create_custom.png"), root = self, command = lambda: self.master.goToPage(CreateCustomPage), x=28.5, y=200)
        createButton(os.path.join(basedir, "leaderboard.png"), root = self, command = lambda: self.master.goToPage(LeaderboardPage), x=32.5, y=245)
        createButton(os.path.join(basedir, "how_to_play.png"), root = self, command = lambda: self.master.goToPage(HowToPlayPage), x=28.5, y=280)
        createButton(os.path.join(basedir, "credits.png"), root = self, command = lambda: self.master.goToPage(CreditsPage), x=28.5, y=320)
        createButton(os.path.join(basedir, "exit.png"), root = self, command = self.master.destroy, x=29.5, y=360)

class CreateCustomPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()
    
    def createAll(self):
        createTitle(os.path.join(basedir, "create_custom_title.png"), root = self, x = 28.5, y = 71.5)
        createTextButton(self, "Create New Level", lambda: openNewEdit(self.master) ,x=200, y=130)
        saves = Grid.getSaves()
        for i, save in enumerate(saves):
            createTextButton(self,save, lambda: openEdit(self.master, save), 120 + 200 * (i//5), 200  + 50 * (i % 5))

        createGoBackButton(self, self.master)

class HowToPlayPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()
    
    def createAll(self):
        createTitle(os.path.join(basedir, "how_to_play_title.png"), root = self, x = 28.5, y = 71.5)
        createTitle(os.path.join(basedir, "how_to_play_explained.png"), root = self, x = 32.5, y = 165.5)
        createGoBackButton(self, self.master)


class LeaderboardPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()
    
    def createAll(self):
        createTitle(os.path.join(basedir, "leaderboard_title.png"), root = self, x = 28.5, y = 71.5)
        highScores = scores.getSortedScores()
        for i, score in enumerate(highScores):
            if i >= MAX_SCORES:
                break
            createTextLabel(self, f'score: {score["score"]}, time: {round(score["time"],2)}', 180 , 125 + 50 * i)
            

        createGoBackButton(self, self.master)


class CreditsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()
    
    def createAll(self):
        createTitle(os.path.join(basedir, "credits_title.png"), root = self, x = 28.5, y = 71.5)
        createTitle(os.path.join(basedir, "credits_names.png"), root = self, x = 32.5, y = 165)

        createGoBackButton(self, self.master)

def run():
    app = MindGatesApp()
    app.mainloop()

def openGame(app):
    app.destroy()
    if len(Grid.getSaves()) == 0:
        Popup("No Existing Levels", "You must create at least 1 custom \n level before playing")
    else:
        EvaluateOutput()
    run()


def openEdit(app, saveName):
    app.destroy()
    EditWindow(saveName)
    run()

def openNewEdit(app):
    saveName = "save0"
    saves = set(Grid.getSaves())
    counter = 1
    while saveName in saves:
        saveName = "save" + str(counter)
        counter += 1
    openEdit(app, saveName)


if __name__ == "__main__":
    run()