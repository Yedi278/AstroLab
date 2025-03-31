from math import cos, sin, pi

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsPolygonItem
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem, QGraphicsItemGroup
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt
from numpy import inner


class MainWindow(QMainWindow):

    def __init__(self, ui:str='main_window.ui'):
        super(QMainWindow, self).__init__()

        uic.loadUi(ui, self)
        self.setWindowTitle('AstroLab')
        
        self.__size__ = (1600, 1200)

        self.setGeometry(0, 0, *self.__size__)

        self.graphicsView.setGeometry(0, 0, self.size().height(), self.size().height())

        self.scene = QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setSceneRect(0, 0, self.graphicsView.size().width(), self.graphicsView.size().height())
        self.resizeEvent = lambda event: self.OnRescale(event)
        
        self.__graph_size__ = self.graphicsView.size().width(), self.graphicsView.size().height()

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
    
    def OnRescale(self, event=None):
        
        self.scene.clear()
        self.graphicsView.setSceneRect(0, 0, self.graphicsView.size().width(), self.graphicsView.size().height())
        self.__graph_size__ = self.graphicsView.size().width(), self.graphicsView.size().height()

        R = min(self.__graph_size__) / 3
        r = R - 100

        center = (self.__graph_size__[0] / 2, self.__graph_size__[1] / 2)

        color = QColor(0, 0, 0, 200)
        self.drawSector(center=center, r=r, w=3, R=R, divisions=10, color=Qt.red)

        self.scene.update()

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