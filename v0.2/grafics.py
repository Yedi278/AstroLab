import tkinter as tk
import numpy as np

def drawCircle(canvas:tk.Canvas, r:float, R:float, color='white'):

    x,y = canvas.winfo_width()//2, canvas.winfo_height()//2
    r = r/2
    R = R/2
    canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=None, width=2)
    canvas.create_oval(x-R, y-R, x+R, y+R, outline=color, fill=None, width=2)

    for i in range(12):
        _angle = 2*np.pi * i / 12
        x1 = x + r*np.cos(_angle)
        y1 = y + r*np.sin(_angle)
        x2 = x + R*np.cos(_angle)
        y2 = y + R*np.sin(_angle)
        canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

    canvas.create_line(x+r*np.cos(-np.pi), y+r*np.sin(-np.pi), x+R*np.cos(-np.pi), y+R*np.sin(-np.pi), fill='red', width=1)

