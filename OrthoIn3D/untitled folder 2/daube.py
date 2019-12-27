#!/usr/bin/python3
import sys

from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QPushButton, QHBoxLayout, QVBoxLayout, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        parameterOneButton = QtWidgets.QPushButton("Value")
        exitAct = QtWidgets.QAction('Exit', self)

        toolbar = self.addToolBar("Exit")

        toolbar.addWidget(parameterOneButton)
        toolbar.addAction(exitAct)

        menu = QtWidgets.QMenu()
        list_of_values=[1000, 5000, 10000, 15000]
        for ind in range(len(list_of_values)):
            menu.addAction(str(list_of_values[ind]))
        
        parameterOneButton.setMenu(menu)

        menu.triggered.connect(lambda action: print(action.text()))

    def selectAndChangeName(self):
        parameterOneButton.setText("Press Me")
if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(application.exec_())