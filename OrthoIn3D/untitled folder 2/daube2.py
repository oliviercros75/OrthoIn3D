#!/usr/bin/python3
import sys

from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World")
        self.setGeometry(100, 100, 400, 300)
        act = QAction("Do something", self)
        act.triggered.connect(self.do_something)
        exit_act = QAction(QIcon('diagram-icon.png'), '&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(act)
        file_menu.addAction(exit_act)
        another_menu =file_menu.addMenu("Parent Menu")
        submenu = QAction("Submenu1", self)
        another_menu.addAction(submenu)
        another_menu.addAction(QAction("Submenu 2", self))
        another_menu.addAction(QAction("Submenu 3", self))
        view_menu = menu_bar.addMenu('&View')
        show_status_action = QAction("Show status", self)
        show_status_action.setStatusTip("This will show status bar")
        show_status_action.setCheckable(True)
        show_status_action.setChecked(False)
        show_status_action.triggered.connect(self.show_status)
        view_menu.addAction(show_status_action)
        self.statusBar().showMessage('This is a status bar')
    def do_something(self):
        print("Clicked")
    def show_status(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()
        print(state)
if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(application.exec_())