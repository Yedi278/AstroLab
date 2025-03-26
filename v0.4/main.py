from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class AstroLab(QApplication):
    
    def __init__(self, argv):
        super(AstroLab, self).__init__(argv)

        self.main_window_shape = (800, 600)
        self.main_window_position = (100, 100)

    

if __name__ == '__main__':
    app = AstroLab(sys.argv)
    sys.exit(app.exec_())
