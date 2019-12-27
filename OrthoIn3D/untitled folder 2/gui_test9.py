import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QAction, qApp


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(qApp.quit)

        doAction = QAction("&Do", self)
        doAction.triggered.connect(self.do)

        menubar = self.menuBar()

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(doAction)

        subMenu = fileMenu.addMenu("&Sub")
        subMenu.addAction(doAction)

        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        self.setWindowTitle("menu")
        self.show()

    def do(self):
        print("Do")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())