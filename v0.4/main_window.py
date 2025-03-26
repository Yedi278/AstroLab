from math import cos, sin, pi

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsPolygonItem
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem, QGraphicsItemGroup
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt

from pyopengl.OpenGL import GL as gl
from pyopengl.OpenGL import GLU as glu
from pyopengl.OpenGL import GLUT as glut

class MainWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()

        uic.loadUi('main_window.ui', self)
        self.setWindowTitle('AstroLab')
        
        self.__size__ = (1000, 1000)
        
    def setupUI(self):
        self.setFixedSize(*self.__size__)
        
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.__graph_size__ = self.graphicsView.size().width(), self.graphicsView.size().height()

        self.drawSector(graph=self.graphicsView, r=30, R=100, divisions=10)

        self.graphicsView.show()


    def drawSector(self, graph:QGraphicsView, r, R, divisions):

        center = (self.__graph_size__[0]//2, self.__graph_size__[1]//2)
        # draw a sector
        circle = QGraphicsEllipseItem(center[0], center[1], 2*R, 4*R)

        color = QColor(255, 0, 0)
        color.setAlpha(128)
        circle.setPen(QPen(color, r, Qt.SolidLine))

        self.scene.addItem(circle)
        
        # draw sector divisions
        
        for i in range(divisions):
            angle = 2 * pi * i / divisions
            x = R * cos(angle)
            y = R * sin(angle)
            line = QGraphicsLineItem(*center, x+center[0], y+center[1])
            line.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            self.scene.addItem(line)
        

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setupUI()
    window.show()
    app.exec_()
