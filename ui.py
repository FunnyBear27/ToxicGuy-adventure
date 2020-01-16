import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('beginning screen.ui', self)
        self.initUI()

    def initUI(self):
        self.play_button.clicked.connect(self.begin)
        self.history_button.clicked.connect(self.story)

    def begin(self):
        self.close()

    def story(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartScreen()
    ex.show()
    sys.exit(app.exec())
