import numpy as np
import tkinter as tk
import tkinter.messagebox  as msbx
from angles import angleStrToFloat
from PIL import ImageGrab
from changeAngles import anglesManager

class AstrGraph:

    def __init__(self):
        self._phase1:float = 0.
        self._phase2:float = 0.
        self._shape = [600,550]
        self.bottomHeight = 10

        try:
            self.angles = self.__loadAngles() * np.pi/180
        except Exception as e:
            self.angles = np.array([0])
            print(f'Error loading angles: {e}')

    def _onResize(self, event):
        ''' This function is called when the window is resized.'''
        self._pos = event
        self._shape = [self._canvas.winfo_width(), self._canvas.winfo_height()-self.bottomHeight]
        self.refresh()

    def __loadAngles(self) -> list:
        ''' This function loads the angles from a file.'''

        try:
            with open('tmp/angles.txt', 'r', encoding='UTF-8') as f:
                lines = f.readlines()
                angles = []
                for i in lines:

                    if i.strip() == '':
                        continue
                    if i.strip()[0] == '#':
                        continue
                    angles.append(angleStrToFloat(i.strip()))
                
                return np.array(angles)

        except Exception as e:

            msbx.showerror('Error', f'Error loading angles: {e}')
            return []

    def __drawSector(self, phase:float=0, n:int=0, color:str='white', r:int=100, R:int=200):
        
        x,y = self._shape[0]//2, self._shape[1]//2
        r = r/2
        R = R/2
        self._canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=None, width=2)
        self._canvas.create_oval(x-R, y-R, x+R, y+R, outline=color, fill=None, width=2)

        for i in range(n):
            _angle = 2*np.pi * i / n + phase
            x1 = x + r*np.cos(_angle)
            y1 = y + r*np.sin(_angle)
            x2 = x + R*np.cos(_angle)
            y2 = y + R*np.sin(_angle)
            self._canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

        self._canvas.create_line(x+r*np.cos(-np.pi + phase), y+r*np.sin(-np.pi + phase), x+R*np.cos(-np.pi + phase), y+R*np.sin(-np.pi + phase), fill='red', width=1)

    def _drawOuter(self, phase:float):
        ''' This function draws the outer circle.'''
        phase = -phase
        l = np.min(self._shape)
        R = l*0.9
        self.__drawSector(phase=phase, n=12, r=0.9*R, R=R, color='white')
        self.__drawSector(phase=phase, n=12*9, r=R*0.8, R=R*0.9, color='white')
        self.__drawSector(phase=phase, n=27, r=R*0.7, R=R*0.9, color='white')
        self.__drawSector(phase=phase, n=12, r=R*0.6, R=R*0.7, color='white')

    def _drawInner(self, phase:float):
        ''' This function draws the inner circle.'''
        phase = -phase
        color = 'green'
        x, y = self._shape[0]//2, self._shape[1]//2

        r = 0.15*np.min(self._shape)
        R = 0.2*np.min(self._shape)

        self._canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=None, width=2)
        self._canvas.create_oval(x-R, y-R, x+R, y+R, outline=color, fill=None, width=2)

        for i in self.angles:

            _angle = i + phase
            x1 = x + r*np.cos(_angle)
            y1 = y + r*np.sin(_angle)
            x2 = x + R*np.cos(_angle)
            y2 = y + R*np.sin(_angle)

            self._canvas.create_line(x1, y1, x2, y2, fill=color, width=1)
        self._canvas.create_line(x+r*np.cos(-np.pi + phase), y+r*np.sin(-np.pi + phase), x+R*np.cos(-np.pi + phase), y+R*np.sin(-np.pi + phase), fill='red', width=1)

    def refresh(self):
        ''' This function refreshes the canvas.'''
        self._canvas.config(width=self._shape[0], height=self._shape[1])
        self._canvas.delete('all')
        self._canvas.create_text(40,15, text=f'Phase 1: {round(self._phase1*180/np.pi,0)}', fill='white', justify=tk.LEFT)
        self._canvas.create_text(40,25, text=f'Phase 2: {round(self._phase2*180/np.pi,0)}', fill='white', justify=tk.LEFT)
        self._drawOuter(phase=self._phase1)
        self._drawInner(phase=self._phase2)
        self._canvas.create_line(self._shape[0]//2, self._shape[1]//2, self._shape[0]//2 - self._shape[0]//2*0.9, self._shape[1]//2, fill='grey', width=.5)
        self.packAll()

    def changePhase(self):
        ''' This function changes the phase of the graphs.'''

        self._phase1 = angleStrToFloat(self.phase1Text.get()) * np.pi/180
        self._phase2 = angleStrToFloat(self.phase2Text.get()) * np.pi/180
        self.refresh()

    def printImage(self):
        ''' This function prints thecanvas to an image file.'''

        x = self._canvas.winfo_rootx() * 2
        y = self._canvas.winfo_rooty()  * 2
        x1 = x + self._canvas.winfo_width() * 2
        y1 = y + self._canvas.winfo_height()    * 2
        ImageGrab.grab().crop((x, y, x1, y1)).save("astro_graph.png")

    def packAll(self):
        self.mainFrame.pack(side=tk.TOP,        expand=True, fill='both')
        self.topFrame.pack(side=tk.TOP,         expand=True, fill='both')
        self.bottomFrame.pack(side=tk.BOTTOM,   expand=True, fill='both')
        self._canvas.pack(side=tk.TOP,          expand=True, fill='both')
        self.leftFrame.pack(side=tk.LEFT,       expand=True, fill='both', padx=5, pady=5, ipadx=5, ipady=5)
        self.rightFrame.pack(side=tk.RIGHT,     expand=True, fill='both', padx=5, pady=5, ipadx=0, ipady=0)
        
        self.phase1Entry.pack(side=tk.LEFT,     expand=False, padx=5, pady=5)
        self.phase2Entry.pack(side=tk.LEFT,     expand=False)

        self.butt.pack(side=tk.TOP, expand=False, pady=20)
        self.saveButt.pack(side=tk.TOP, expand=False, pady=20)
        self.anglesButt.pack(side=tk.TOP, expand=False, pady=20)

    def run(self):
        # Create the GUI
        self._window = tk.Tk()
        self._window.title('AstroLab')

        self._window.geometry(f'{self._shape[0]}x{self._shape[1]+self.bottomHeight}')
        self._window.resizable(True, True)
        self._window.bind("<Configure>", func=self._onResize)
        # self._window.call('tk', 'scaling', 2) # for high DPI screens
        
        self.mainFrame = tk.Frame(self._window, relief=tk.RAISED)
        self.topFrame = tk.Frame(self.mainFrame, width=self._shape[0], height=self._shape[1])
        self.bottomFrame = tk.Frame(self.mainFrame, width=self._shape[0])
        self._canvas = tk.Canvas(self.topFrame, bg='black')
        
        self.phase1Text = tk.StringVar(value='0°0\'0"') # text for the entry
        self.phase2Text = tk.StringVar(value='0°0\'0"')

        self.leftFrame = tk.Frame(self.bottomFrame)

        self.rightFrame = tk.Frame(self.bottomFrame)

        leftup = tk.Frame(self.leftFrame)
        leftup.pack(side=tk.TOP, expand=True, fill='both', padx=5, pady=5, ipadx=5, ipady=5)
        leftdown = tk.Frame(self.leftFrame)
        leftdown.pack(side=tk.BOTTOM, expand=True, fill='both', padx=5, pady=5, ipadx=5, ipady=5)

        tk.Label(leftup, text='Phase 1:').pack(side=tk.LEFT, expand=False, padx=5, pady=5)
        tk.Label(leftdown, text='Phase 2:').pack(side=tk.LEFT, expand=False, padx=5, pady=5)
        
        self.phase1Entry = tk.Entry(leftup, width=5, font=('Arial', 12),
                                    textvariable=self.phase1Text)
        self.phase1Entry

        self.phase2Entry = tk.Entry(leftdown, width=10, font=('Arial', 12),
                                    textvariable=self.phase2Text)

        self.butt = tk.Button(self.rightFrame, text='Refresh', width=10, command=self.changePhase)
        self.saveButt = tk.Button(self.rightFrame, text='Save', width=10, command=self.printImage)
        self.anglesButt = tk.Button(self.rightFrame, text='Angles', width=10, command=lambda:anglesManager(self, self._window))

        self.refresh()
        self._window.mainloop()

if __name__ == '__main__':

    import os

    os.chdir(os.path.dirname(__file__))
    
    aG_test = AstrGraph()
    aG_test.run()