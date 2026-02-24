from ui.mainwindow import * # import ui .py file, adjust ui.foo for filename

# main Qt core imports
from PySide6.QtCore import QCoreApplication, Qt, QIODevice, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QComboBox
from PySide6.QtGui import QIcon, QAction, QCloseEvent

import ctypes # Windows exclusive, allows for unique icon assignment
myappid = 'int.maldi' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# utils
from pathlib import Path
from time import *
import sys
from utils import FluigentController

class MainWindow(QMainWindow, Ui_MainWindow): # pass ui class
    def __init__(self):
        super(MainWindow, self).__init__() # inherit ui class assignments
        self.setupUi(self)

        icon = QIcon('assets/icon/icon.ico')
        self.setWindowIcon(icon)
        QApplication.setWindowIcon(icon)
        self.setWindowTitle("MALDI Control Suite")

        self.controller = FluigentController()

    def closeEvent(self, event: QCloseEvent) -> None: # gracefully exit
        try:
            # close instruments
            self.controller.close()
            pass
        except Exception as e:
            print(f'Error closing program: {e}')
        print('\nExited')

if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()

if __name__ == '__main__':
    window = MainWindow()
    app.setStyle('Windows')
    window.show()
    print(f'Running...\n')
    app.exec()