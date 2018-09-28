import sys
from PyQt5 import Qt, uic, QtCore

from sokoban import Sokoban,CellType


class Window(Qt.QMainWindow):
    def __init__(self):  # , matrix):
        Qt.QMainWindow.__init__(self)
        uic.loadUi(Window.designer, self)
        self.grid = self.findChild(Qt.QGridLayout, 'gridLayout')

    def view(self, matrix,position):

        size = [len(matrix), len(matrix[0])]

        for i in range(size[0]):
            for j in range(size[1]):
                b = Qt.QLabel()
                b.setStyleSheet('font-size:50px;text-align: center;'+Window.__cell_color(matrix[i][j]))
                if i == position[0] and j == position[1]:
                    b.setAlignment(QtCore.Qt.AlignCenter)
                    b.setText(' O ')
                self.grid.addWidget(b, i, j)

    @staticmethod
    def __cell_color(cell_type):
        if cell_type == CellType.wall:
            return 'background-color:#A40'
        elif cell_type == CellType.box:
            return 'background-color:#0F0'
        elif cell_type == CellType.goal:
            return 'background-color:#F00'
        elif cell_type == CellType.done:
            return 'background-color:#FF0'
        elif cell_type == CellType.empty:
            return 'background-color:#FA0'

    designer = 'designer.ui'


if __name__ == '__main__':
    file_path = 'asd.txt'
    sokoban = Sokoban(file_path)

    app = Qt.QApplication(sys.argv)
    w = Window()
    w.show()
    for model in sokoban.__iter__():
        w.view(model.matrix,model.position)
        Qt.QTest.qWait(1000)
    sys.exit(app.exec_())
