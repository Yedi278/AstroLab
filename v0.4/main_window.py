from math import cos, sin, pi

import json

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QTabWidget, QSplitter, QSlider, QSpinBox, QGraphicsEllipseItem
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QSize


class MainWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()

        self.setWindowTitle('AstroLab')
        
        self.loadSettings()


        self.__size__:QSize = (1800, 1600)
        self.setGeometry(0, 0, self.__size__[0], self.__size__[1])
        self.setMinimumSize(800, 600)

        # find menu bar
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu('Load')

        self.edit_menu = self.menubar.addMenu('Save')

        self.settings_menu = self.menubar.addMenu('Settings')

        self.help_menu = self.menubar.addMenu('Help')

        # add Graphics View Widget
        self.graphicsView:QGraphicsView = QGraphicsView(self)
        self.__graph_size__:QSize = self.graphicsView.size()

        # load tabs_widget.ui file
        self.tabs:QTabWidget = QTabWidget(self)
        uic.loadUi('tabs_widget.ui', self.tabs)

        # add a variable splitter
        self.splitter:QSplitter = QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(True)

        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.graphicsView)

        self.scene = QGraphicsScene(self)

        self.splitter.setSizes([self.__size__[0]//2, self.__size__[0]//2])

        self.setCentralWidget(self.splitter)

        self.graphicsView.resizeEvent = lambda event: self.OnRescale(event)

        self.drawScene()

        self.graphicsView.show()
        
        # reset button 
        self.reset_button = self.tabs.findChild(QtWidgets.QPushButton, "reset_button")

        self.reset_button.clicked.connect(self.resetPhases)

        # save button
        self.save_button = self.tabs.findChild(QtWidgets.QPushButton, "save_button")

        self.save_button.clicked.connect(lambda: self.saveScreenshot(self.graphicsView, self.screenshotPath))

        self.slider_phase1:QSlider = self.tabs.findChild(QSlider, "slider_phase1")
        self.slider_phase2:QSlider = self.tabs.findChild(QSlider, "slider_phase2")
        self.slider_phase3:QSlider = self.tabs.findChild(QSlider, "slider_phase3")
        self.slider_phase4:QSlider = self.tabs.findChild(QSlider, "slider_phase4")

        self.sbox_phase1:QSpinBox = self.tabs.findChild(QSpinBox, "sbox_phase1")
        self.sbox_phase2:QSpinBox = self.tabs.findChild(QSpinBox, "sbox_phase2")
        self.sbox_phase3:QSpinBox = self.tabs.findChild(QSpinBox, "sbox_phase3")
        self.sbox_phase4:QSpinBox = self.tabs.findChild(QSpinBox, "sbox_phase4")

        # connect spinboxes changed signal to update phases
        self.sbox_phase1.valueChanged.connect(self.updatePhases_fromSpinBox)
        self.sbox_phase2.valueChanged.connect(self.updatePhases_fromSpinBox)
        self.sbox_phase3.valueChanged.connect(self.updatePhases_fromSpinBox)
        self.sbox_phase4.valueChanged.connect(self.updatePhases_fromSpinBox)

        # connect sliders to update phases
        self.slider_phase1.valueChanged.connect(self.updatePhases_fromSlider)
        self.slider_phase2.valueChanged.connect(self.updatePhases_fromSlider)
        self.slider_phase3.valueChanged.connect(self.updatePhases_fromSlider)
        self.slider_phase4.valueChanged.connect(self.updatePhases_fromSlider)

    def loadSettings(self):

        self.setDefaults()
        
        try:
            with open('settings.json', 'r') as f:
                settings:dict = json.load(f)

                print(f"settings found: {settings.keys()}")
                                
                if "label_sector1" in settings.keys():
                    self.label_sector1 = settings["label_sector1"]

                if "label_sector2" in settings.keys():
                    self.label_sector2 = settings["label_sector2"] * 12

                if "label_sector3" in settings.keys():
                    self.label_sector3 = settings["label_sector3"]

                if "label_sector4" in settings.keys():
                    self.label_sector4 = settings["label_sector4"]

                if "phases" in settings.keys():
                    self.phases:list[int] = settings["phases"]

                if "screenshot Path" in settings.keys():
                    self.screenshotPath:str = settings["screenshot Path"]


        except FileNotFoundError:
            print('Settings not found!, using defaults!')
            return
        
        except json.JSONDecodeError:
            print('Error Decoding the Json!, Check the settings!')
            return

        except Exception as e:
            print("Error loading Settings: ", e)
            return
    
    def setDefaults(self):

        self.label_sector1 = None
        self.label_sector2 = None
        self.label_sector3 = None
        self.label_sector4 = None

        self.phases = [0 for i in range(4)]

        self.screenshotPath = 'tmp/screenshot'

    def updatePhases_fromSlider(self):
        # update the phases from the sliders
        self.phases[0] = self.slider_phase1.value()
        self.phases[1] = self.slider_phase2.value()
        self.phases[2] = self.slider_phase3.value()
        self.phases[3] = self.slider_phase4.value()

        # update the spinboxes
        self.sbox_phase1.setValue(self.phases[0])
        self.sbox_phase2.setValue(self.phases[1])
        self.sbox_phase3.setValue(self.phases[2])
        self.sbox_phase4.setValue(self.phases[3])
        
        # update the scene
        self.OnRescale()

    def updatePhases_fromSpinBox(self):

        self.phases[0] = self.sbox_phase1.value()
        self.phases[1] = self.sbox_phase2.value()
        self.phases[2] = self.sbox_phase3.value()
        self.phases[3] = self.sbox_phase4.value()

        # update the sliders
        self.slider_phase1.setValue(self.phases[0])
        self.slider_phase2.setValue(self.phases[1])
        self.slider_phase3.setValue(self.phases[2])
        self.slider_phase4.setValue(self.phases[3])

        #update the scene
        self.OnRescale()

    def resetPhases(self):

        for i in self.phases:
            i = 0
        
        self.sbox_phase1.setValue(0)
        self.sbox_phase2.setValue(0)
        self.sbox_phase3.setValue(0)
        self.sbox_phase4.setValue(0)

        self.slider_phase1.setValue(0)
        self.slider_phase2.setValue(0)
        self.slider_phase3.setValue(0)
        self.slider_phase4.setValue(0)

        self.OnRescale()

    def drawSector(self, center, r, R, w, divisions, labels=None, color:QColor=Qt.red, phase=0):

        phase = -(phase + 180)

        if labels is not None:
            if len(labels) != divisions:
                raise ValueError("Number of labels must be equal to the number of divisions, {} != {}".format(len(labels), divisions))

        # draw the outer circle
        outer_circ = QGraphicsEllipseItem(center[0]-R, center[1]-R, 2*R, 2*R)
        outer_circ.setPen(QPen(color, w, Qt.SolidLine))

        # draw the inner circle
        inner_circ = QGraphicsEllipseItem(center[0]-r, center[1]-r, 2*r, 2*r)
        inner_circ.setPen(QPen(color, w, Qt.SolidLine))

        # add the circles to the scene
        self.scene.addItem(inner_circ)
        self.scene.addItem(outer_circ)

        pen = QPen(color, w, Qt.SolidLine)
        font = QtGui.QFont("Arial", 10, QtGui.QFont.Bold)

        # draw sector divisions
        for i in range(divisions):
            angle = 2 * pi * i / divisions + (pi * phase / 180)

            xmin = (r) * cos(angle)
            ymin = (r) * sin(angle)
            xmax = (R) * cos(angle)
            ymax = (R) * sin(angle)

            line = QGraphicsLineItem(center[0]+xmin, center[1]+ymin, center[0]+xmax, center[1]+ymax)
            line.setPen(pen)
            self.scene.addItem(line)
            
            if labels is None:
                continue
            else:
                text_item = QGraphicsTextItem(labels[-i])
                text_item.setPos(center[0] + xmin, center[1] + ymin)
                text_item.setDefaultTextColor(color)
                # add border to the text item

                text_item.setFont(font)
                text_item.setRotation(i * 360 / divisions + phase - 90)

                self.scene.addItem(text_item)

        # draw first line
        x_0 = (r) * cos(phase * pi / 180)
        y_0 = (r) * sin(phase * pi / 180)
        x_1 = (R) * cos(phase * pi / 180)
        y_1 = (R) * sin(phase * pi / 180)
        line = QGraphicsLineItem(center[0] + x_0, center[1] + y_0, center[0]+x_1, center[1]+y_1)
        line.setPen(QPen(Qt.red, 2*w, Qt.SolidLine))
        self.scene.addItem(line)

    def drawScene(self, R=100, w=2):

        center = (self.__graph_size__.width()/2, self.__graph_size__.height()/2)

        self.scene.clear()
        self.scene.setSceneRect(0, 0, self.__graph_size__.width(), self.__graph_size__.height())
        self.scene.setBackgroundBrush(QBrush(Qt.white))
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)

        self.graphicsView.setScene(self.scene)

        self.drawSector(center, r=R*0.9, R=R,     w=w, divisions=12, color=Qt.black, phase=self.phases[0], labels=self.label_sector1)
        self.drawSector(center, r=R*0.7, R=R*0.8, w=w, divisions=9*12, color=Qt.black, phase=self.phases[1], labels=self.label_sector2)
        self.drawSector(center, r=R*0.5, R=R*0.6, w=w, divisions=27, color=Qt.black, phase=self.phases[2], labels=self.label_sector3)
        self.drawSector(center, r=R*0.3, R=R*0.4, w=w, divisions=12, color=Qt.black, phase=self.phases[3], labels=self.label_sector4)

        self.scene.update()

    def drawTabs(self):
        self.tabs.clear()
        
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)

        # add one tab
        tab1 = QtWidgets.QWidget()
        tab1.setLayout(QtWidgets.QVBoxLayout())
        tab1.setContentsMargins(0, 0, 0, 0)
        tab1.setMinimumSize(200, 200)        

    def OnRescale(self, event=None):
        
        self.__graph_size__ = self.graphicsView.size()
        
        R = 0.4 * min(self.__graph_size__.width(), self.__graph_size__.height())
        w = 4

        self.drawScene(R=R, w=w)

    def saveScreenshot(self, widget, path:str):

        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow( widget.winId() )
        screenshot.save(path, 'jpg')


if __name__ == '__main__':
    import sys, os

    os.chdir(os.path.dirname(__file__))

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()