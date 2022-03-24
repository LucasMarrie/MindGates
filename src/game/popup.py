import tkinter as tk
import pyglet
from settings import FONT_PATH

pyglet.font.add_file(FONT_PATH)

class Popup(tk.Tk):
    def __init__(self, title, text):
        tk.Tk.__init__(self)
        self.frame = PopUpFrame(self, text)
        self.frame.pack()
        self.title(title)
        self.eval('tk::PlaceWindow . center')
        self.mainloop()
    
class PopUpFrame(tk.Frame):
    def __init__(self, master, text):
        tk.Frame.__init__(self, master, width = 300, height = 150, bg = '#00162D')
        text = tk.Label(self, text=f"\n   {text}   \n", bg="#00162D", fg="#D4FAFF", font=("Endless Boss Battle", 18))
        text.pack()
        button = tk.Button(self, text="OK", bg = '#00162D', font=("Endless Boss Battle", 18), fg = '#D4FAFF', activebackground = '#D4FAFF', command=self.master.destroy, borderwidth=0)
        button.pack()

class DialogBox(tk.Tk):
    def __init__(self, title, text, default, callBack):
        tk.Tk.__init__(self)
        self.frame = DialogFrame(self, text, default, callBack)
        self.frame.pack()
        self.title(title)
        self.eval('tk::PlaceWindow . center')
        self.mainloop()
    
class DialogFrame(tk.Frame):
    def __init__(self, master, text, default, callBack):
        self.callBack = callBack
        tk.Frame.__init__(self, master, width = 300, height = 150, bg = '#00162D')
       
        text = tk.Label(self, text=f"\n   {text}   \n", bg="#00162D", fg="#D4FAFF", font=("Endless Boss Battle", 18))
        text.pack()

        self.textBoxEntry= tk.Entry(self, width=15, font=("Endless Boss Battle", 18))
        self.textBoxEntry.insert(0, default)
        self.textBoxEntry.pack()
        # self.textBoxEntry.bind("<Return>", button)
        self.master.bind()

        button = tk.Button(self, text="OK", bg = '#00162D', font=("Endless Boss Battle", 18), fg = '#D4FAFF', activebackground = '#D4FAFF', command=lambda: self.submit(self.textBoxEntry.get()), borderwidth=0)
        button.pack()
        
    def submit(self, text):
        self.callBack(text)
        self.master.destroy()


