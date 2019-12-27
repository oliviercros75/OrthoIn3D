from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, configparser

config = configparser.ConfigParser()
config.read("Settings.ini")

# Config get setting and change setting
#print(config.get("Main", "language"))
#config.set("Main", "language", "danish")
#with open("Settings.ini", "w") as cfg_file:
    #config.write(cfg_file)

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Window Settings
        self.x, self.y, self.w, self.h = 0, 0, 300, 200
        self.setGeometry(self.x, self.y, self.w, self.h)

        self.window = MainWindow(self)
        self.setCentralWidget(self.window)
        self.setWindowTitle("Window title") # Window Title
        self.show()

class GeneralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GeneralWidget, self).__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        # Buttons
        button_start = QtWidgets.QPushButton("start") #self.lang["btn_start"])
        button_stop = QtWidgets.QPushButton("stop") #self.lang["btn_stop"])

        # Button Extra
        button_start.setToolTip("This is a tooltip for the button!")    # Message to show when mouse hover
        button_start.clicked.connect(self.on_click)

        button_stop.clicked.connect(self.on_click)

        lay.addWidget(button_start)
        lay.addWidget(button_stop)
        lay.addStretch()

    @QtCore.pyqtSlot()
    def on_click(self):
        button = self.sender().text()
        if button == self.lang["btn_start"]:
            print("Dank")
        elif button == self.lang["btn_stop"]:
            print("Not dank")


class OptionsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OptionsWidget, self).__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        hlay = QtWidgets.QHBoxLayout()
        lay.addLayout(hlay)
        lay.addStretch()

        label_language = QtWidgets.QLabel("Language")
        combo_language = QtWidgets.QComboBox(self)
        combo_language.addItem("item1") #self.lang["language_danish"])
        combo_language.addItem("item2") #self.lang["language_english"])
        hlay.addWidget(label_language)
        hlay.addWidget(combo_language)



class MainWindow(QtWidgets.QWidget):        
    def __init__(self, parent):   
        super(MainWindow, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        # Run this after settings
        # self.lang = getLang(config.get("Main", "language"))
        # Initialize tabs
        tab_holder = QtWidgets.QTabWidget()   # Create tab holder
        tab_1 = GeneralWidget()           # Tab one
        tab_2 = OptionsWidget()           # Tab two
        # Add tabs
        tab_holder.addTab(tab_1, "General") #self.lang["tab_1_title"]) # Add "tab1" to the tabs holder "tabs"
        tab_holder.addTab(tab_2, "Options") #self.lang["tab_2_title"]) # Add "tab2" to the tabs holder "tabs" 

        layout.addWidget(tab_holder)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())