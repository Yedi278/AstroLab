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
        
        self.__size__:QSize = (1800, 1200)

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

        self.splitter.setSizes([self.__size__[0], self.__size__[1]])
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)

        self.setCentralWidget(self.splitter)

        self.graphicsView.resizeEvent = lambda event: self.OnRescale(event)
        self.drawScene()
        
        self.graphicsView.show()


    def drawSector(self, center, r, R, w, divisions, labels=None, color: QColor=Qt.red):

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
            angle = 2 * pi * i / divisions

            xmin = (r) * cos(angle)
            ymin = (r) * sin(angle)
            xmax = (R) * cos(angle)
            ymax = (R) * sin(angle)

            line = QGraphicsLineItem(center[0]+xmin, center[1]+ymin, center[0]+xmax, center[1]+ymax)
            line.setPen(QPen(Qt.black, w, Qt.SolidLine))
            self.scene.addItem(line)

    def drawScene(self, R=100, r=50, w=2, divisions=12):

        center = (self.__graph_size__.width()/2, self.__graph_size__.height()/2)

        color = QColor(255, 0, 0)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.__graph_size__.width(), self.__graph_size__.height())
        self.scene.setBackgroundBrush(QBrush(Qt.white))
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)

        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QPainter.Antialiasing)

        self.drawSector(center, r, R, w, divisions, color=color)

    def OnRescale(self, event=None):
        
        self.__graph_size__ = self.graphicsView.size()
        
        R = min(self.__graph_size__.width(), self.__graph_size__.height())
        R = R * 0.4
        r = R * 0.5
        w = 2

        divisions = 12

        self.drawScene(R=R, r=r, w=w, divisions=divisions)



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