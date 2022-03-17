from ctypes import resize
import tkinter as tk
from PIL import Image, ImageTk
from click import command

root = tk.Tk()

canvas = tk.Canvas(root, width = 720, height = 512, bg = '#00162D')
canvas.grid(columnspan = 3,rowspan = 6)

title = Image.open('title.png')
title = ImageTk.PhotoImage(title)
title_label = tk.Label(image = title, bg = '#00162D')
title_label.image = title
title_label.place(x = 28.5, y = 71.5 )

def createButtons(filename, command, x, y):
    logo = Image.open(filename)
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Button(image = logo, bg = '#00162D', fg = '#00162D', activebackground = '#00162D', command=command, borderwidth=0)
    logo_label.image = logo
    logo_label.place(x=x, y=y)

createButtons("choose_gamemode.png", None, 28.5, 150)
createButtons("create_custom.png",None, 28.5, 200)
createButtons("how_to_play.png", None, 28.5, 250)
createButtons("credits.png", None, 28.5, 300)
createButtons("exit.png", None, 28.5, 350)



#gamemode = Image.open('choose_gamemode.png')
#logo_gamemode = ImageTk.PhotoImage(logo_gamemode)
#text=""
#btn1 = tk.Button(root, image=, bg = "#00162D", command=None)
#btn1.place(x=40,y=205)

root.mainloop()