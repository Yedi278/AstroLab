from math import cos, sin, pi

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QTabWidget, QSplitter
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsPolygonItem
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem, QGraphicsItemGroup
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize
from numpy import inner


class MainWindow(QMainWindow):

    def __init__(self, ui:str='main_window.ui'):
        super(QMainWindow, self).__init__()

        self.setWindowTitle('AstroLab')
        
        self.__size__:QSize = (1800, 1600)

        self.setGeometry(0, 0, self.__size__[0], self.__size__[1])

        self.setMinimumSize(800, 600)

        self.graphicsView:QGraphicsView = QGraphicsView(self)
        self.__graph_size__:QSize = self.graphicsView.size()

        self.tabs:QTabWidget = QTabWidget(self)

        self.splitter:QSplitter = QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(True)

        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.graphicsView)

        self.scene = QGraphicsScene(self)

        # self.splitter.setSizes([self.__size__[0], self.__size__[1]], 1)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)

        self.setCentralWidget(self.splitter)

        self.graphicsView.resizeEvent = lambda event: self.OnRescale(event)

        self.phases = [0, 180, 0, 0]
        self.drawScene()

        self.graphicsView.show()

        # load tabs_widget.ui file
        tabs_widget = uic.loadUi('tabs_widget.ui', self.tabs)
        self.tabs.setObjectName("tabs")
        
        # reset button 
        self.reset_button = self.tabs.findChild(QtWidgets.QPushButton, "reset_button")
        self.reset_button.setText("Reset")

        self.reset_button.clicked.connect(self.ResetPhases)

        self.slider_phase1 = self.tabs.findChild(QtWidgets.QSlider, "slider_phase1")
        self.slider_phase2 = self.tabs.findChild(QtWidgets.QSlider, "slider_phase2")
        self.slider_phase3 = self.tabs.findChild(QtWidgets.QSlider, "slider_phase3")
        self.slider_phase4 = self.tabs.findChild(QtWidgets.QSlider, "slider_phase4")

        self.label_phase1 = self.tabs.findChild(QtWidgets.QLabel, "label_phase1")
        self.label_phase2 = self.tabs.findChild(QtWidgets.QLabel, "label_phase2")
        self.label_phase3 = self.tabs.findChild(QtWidgets.QLabel, "label_phase3")
        self.label_phase4 = self.tabs.findChild(QtWidgets.QLabel, "label_phase4")
        
        # connect sliders to update phases
        self.slider_phase1.valueChanged.connect(self.updatePhases)
        self.slider_phase2.valueChanged.connect(self.updatePhases)
        self.slider_phase3.valueChanged.connect(self.updatePhases)
        self.slider_phase4.valueChanged.connect(self.updatePhases)

    def updatePhases(self):
        self.phases[0] = self.slider_phase1.value()
        self.phases[1] = self.slider_phase2.value()
        self.phases[2] = self.slider_phase3.value()
        self.phases[3] = self.slider_phase4.value()

        self.label_phase1.setText(f"Phase 1: {self.phases[0]}°")
        self.label_phase2.setText(f"Phase 2: {self.phases[1]}°")
        self.label_phase3.setText(f"Phase 3: {self.phases[2]}°")
        self.label_phase4.setText(f"Phase 4: {self.phases[3]}°")

        # update the scene
        self.drawScene()
        self.OnRescale()

    def ResetPhases(self):
        self.phases = [0, 0, 0, 0]
        self.drawScene()
        self.OnRescale()

    def drawSector(self, center, r, R, w, divisions, labels=None, color: QColor=Qt.red, phase=0):

        phase = -(phase + 180)
        # draw the outer circle
        outer_circ = QGraphicsEllipseItem(center[0]-R, center[1]-R, 2*R, 2*R)
        outer_circ.setPen(QPen(color, w, Qt.SolidLine))

        # draw the inner circle
        inner_circ = QGraphicsEllipseItem(center[0]-r, center[1]-r, 2*r, 2*r)
        inner_circ.setPen(QPen(color, w, Qt.SolidLine))

        # add the circles to the scene
        self.scene.addItem(inner_circ)
        self.scene.addItem(outer_circ)


        # draw sector divisions
        for i in range(divisions):
            angle = 2 * pi * i / divisions + (pi * phase / 180)

            xmin = (r) * cos(angle)
            ymin = (r) * sin(angle)
            xmax = (R) * cos(angle)
            ymax = (R) * sin(angle)

            line = QGraphicsLineItem(center[0]+xmin, center[1]+ymin, center[0]+xmax, center[1]+ymax)
            line.setPen(QPen(color, w, Qt.SolidLine))
            self.scene.addItem(line)

        # draw the labels
        if labels is not None:
            for i in range(len(labels)):
                angle = 2 * pi * i / divisions + (pi * phase / 180)
                x = (R + r) / 2 * cos(angle)
                y = (R + r) / 2 * sin(angle)

                text_item = QGraphicsTextItem(labels[i])
                text_item.setPos(center[0] + x, center[1] + y)
                text_item.setDefaultTextColor(color)
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

        color = QColor(0, 0, 0, 255)

        self.scene.clear()
        self.scene.setSceneRect(0, 0, self.__graph_size__.width(), self.__graph_size__.height())
        self.scene.setBackgroundBrush(QBrush(Qt.white))
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)

        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QPainter.Antialiasing)

        self.drawSector(center, r=R*0.9, R=R, w=w, divisions=12, color=color, phase=self.phases[0], labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])

        self.drawSector(center, r=R*0.7, R=R*0.8, w=w, divisions=9*12, color=color, phase=self.phases[1])
        self.drawSector(center, r=R*0.5, R=R*0.6, w=w, divisions=27, color=color, phase=self.phases[2])
        self.drawSector(center, r=R*0.3, R=R*0.4, w=w, divisions=12, color=color, phase=self.phases[3])

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




    def saveScreenshot(self, widget, path:str='shot'):
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow( widget.winId() )
        screenshot.save(path, 'jpg')


if __name__ == '__main__':
    import sys, os

    os.chdir(os.path.dirname(__file__))

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.saveScreenshot(widget=window.graphicsView, path='screenshot.jpg')
    app.exec_()