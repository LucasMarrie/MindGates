import tkinter as tk
from PIL import Image, ImageTk
from game.gameWindow import EvaluateOutput


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

def createGoBackButton(root, master):
    createButton("go_back.png", root=root, command= lambda: master.goToPage(MainPage), x=28.5, y=28.5)

class MindGatesApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.goToPage(MainPage)

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
        createTitle("main_title.png", root = self, x = 28.5, y = 71.5)
        createButton("choose_gamemode.png", root = self, command = lambda: self.master.goToPage(ChooseGameModePage), x=28.5, y=150)
        createButton("create_custom.png", root = self, command = lambda: self.master.goToPage(CreateCustomPage), x=28.5, y=200)
        createButton("how_to_play.png", root = self, command = lambda: self.master.goToPage(HowToPlayPage), x=28.5, y=250)
        createButton("credits.png", root = self, command = lambda: self.master.goToPage(CreditsPage), x=28.5, y=300)
        createButton("exit.png", root = self, command = self.master.destroy, x=28.5, y=350)



class ChooseGameModePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()

    def hover1(self,e):
        self.n1 = createTitle("hover_1.png", root = self, x = 500.5, y = 380.5)
    def notHover1(self,e):
        self.n1.destroy()

    def hover2(self,e):
        self.n1 = createTitle("hover_2.png", root = self, x = 500.5, y = 380.5)
    def notHover2(self,e):
        self.n1.destroy()
    
    def hover3(self,e):
        self.n1 = createTitle("hover_3.png", root = self, x = 530.5, y = 378.5)
    def notHover3(self,e):
        self.n1.destroy()

    def hover4(self,e):
        self.n1 = createTitle("hover_4.png", root = self, x = 530.5, y = 380.5)
    def notHover4(self,e):
        self.n1.destroy()
    
    def createAll(self):
        createTitle("choose_gamemode_title.png", root = self, x = 28.5, y = 71.5)
        createTitle("evaluation_title.png", root = self, x = 95.5, y = 150.5)
        createTitle("generate_title.png", root = self, x = 415.5, y = 150.5)

        b1 = createButton("evaluate_output.png", root = self, command=lambda: EvaluateOutput(), x = 28.5 , y = 180.5)
        b1.bind("<Enter>", self.hover1)
        b1.bind("<Leave>", self.notHover1)

        b2 = createButton("evaluate_truth_table.png", root = self, command=None, x = 190, y = 180.5)
        b2.bind("<Enter>", self.hover2)
        b2.bind("<Leave>", self.notHover2)

        b3 = createButton("generate_truth_table.png", root = self, command=None, x = 385, y = 180.5)
        b3.bind("<Enter>", self.hover3)
        b3.bind("<Leave>", self.notHover3)

        b4 = createButton("generate_proposition.png", root = self, command=None, x = 545, y = 180.5)
        b4.bind("<Enter>", self.hover4)
        b4.bind("<Leave>", self.notHover4)

        createGoBackButton(self, self.master)

class CreateCustomPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()
    
    def hover1(self,e):
        self.n1 = createTitle("hover_1.png", root = self, x = 500.5, y = 380.5)
    def notHover1(self,e):
        self.n1.destroy()

    def hover2(self,e):
        self.n1 = createTitle("hover_2.png", root = self, x = 500.5, y = 380.5)
    def notHover2(self,e):
        self.n1.destroy()
    
    def hover3(self,e):
        self.n1 = createTitle("hover_3.png", root = self, x = 530.5, y = 378.5)
    def notHover3(self,e):
        self.n1.destroy()

    def hover4(self,e):
        self.n1 = createTitle("hover_4.png", root = self, x = 530.5, y = 380.5)
    def notHover4(self,e):
        self.n1.destroy()
    def createAll(self):
        createTitle("create_custom_title.png", root = self, x = 28.5, y = 71.5)
        createTitle("evaluation_title.png", root = self, x = 95.5, y = 150.5)
        createTitle("generate_title.png", root = self, x = 415.5, y = 150.5)

        b1 = createButton("evaluate_output.png", root = self, command=None, x = 28.5 , y = 180.5)
        b1.bind("<Enter>", self.hover1)
        b1.bind("<Leave>", self.notHover1)

        b2 = createButton("evaluate_truth_table.png", root = self, command=None, x = 190, y = 180.5)
        b2.bind("<Enter>", self.hover2)
        b2.bind("<Leave>", self.notHover2)

        b3 = createButton("generate_truth_table.png", root = self, command=None, x = 385, y = 180.5)
        b3.bind("<Enter>", self.hover3)
        b3.bind("<Leave>", self.notHover3)

        b4 = createButton("generate_proposition.png", root = self, command=None, x = 545, y = 180.5)
        b4.bind("<Enter>", self.hover4)
        b4.bind("<Leave>", self.notHover4)

        createGoBackButton(self, self.master)

class HowToPlayPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()
    
    def createAll(self):
        createTitle("how_to_play_title.png", root = self, x = 28.5, y = 71.5)
        createGoBackButton(self, self.master)

class CreditsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()
    
    def createAll(self):
        createTitle("credits_title.png", root = self, x = 28.5, y = 71.5)
        createGoBackButton(self, self.master)


def run():
    app = MindGatesApp()
    app.mainloop()

if __name__ == "__main__":
    run()