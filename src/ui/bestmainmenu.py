import tkinter as tk
from PIL import Image, ImageTk


def createTitle(filename, root=None , x=None, y=None):
    title = Image.open(filename)
    title = ImageTk.PhotoImage(title)
    title_label = tk.Label(root, image = title, bg = '#00162D')
    title_label.image = title
    title_label.place(x = x, y = y)

def createButton(filename, root, command, x=None, y=None):
    logo = Image.open(filename)
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Button(root, image = logo, bg = '#00162D', fg = '#00162D', activebackground = '#00162D', command=command, borderwidth=0)
    logo_label.image = logo
    logo_label.place(x=x, y=y)
    # no need for return



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
        createButton("choose_gamemode.png", root = self, command =None, x=28.5, y=150)
        createButton("create_custom.png", root = self, command = None, x=28.5, y=200)
        createButton("how_to_play.png", root = self, command = None, x=28.5, y=250)
        createButton("credits.png", root = self, command = lambda: self.master.goToPage(CreditsPage), x=28.5, y=300)
        createButton("exit.png", root = self, command = lambda: self.master.destroy, x=28.5, y=350)

class CreditsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 720, height = 512, bg = '#00162D')
        self.createAll()
    
    def createAll(self):
        createTitle("credits_title.png", root = self, x = 28.5, y = 71.5)
        createButton("main_title.png", root=self, command= lambda: self.master.goToPage(MainPage), x=28.5, y=200.5)

# class PageTwo(tk.Frame):
#     def __init__(self, master):
#         tk.Frame.__init__(self, master)
#         tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)


if __name__ == "__main__":
    app = MindGatesApp()
    app.mainloop()