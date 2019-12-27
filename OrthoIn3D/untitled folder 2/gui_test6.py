import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QHBoxLayout, QTabWidget
from PyQt5.QtWidgets import QRadioButton, QButtonGroup
from PyQt5.QtWidgets import QCheckBox, QLabel, QComboBox
from PyQt5.QtWidgets import QPushButton, QVBoxLayout


class RadioWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        radio1 = QRadioButton("Radio1")
        radio2 = QRadioButton("Radio2")

        self.group = QButtonGroup()
        self.group.addButton(radio1, 1)
        self.group.addButton(radio2, 2)
        radio1.toggle()

        button = QPushButton("Check")
        button.clicked.connect(self.buttonClicked)

        layout = QVBoxLayout()
        layout.addWidget(radio1)
        layout.addWidget(radio2)
        layout.addWidget(button)

        self.setLayout(layout)

    def buttonClicked(self):
        print("Radio: %d" % self.group.checkedId())


class CheckWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.check1 = QCheckBox("Check1")
        self.check2 = QCheckBox("Check2")
        self.check1.setChecked(True)

        button = QPushButton("Check")
        button.clicked.connect(self.buttonClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.check1)
        layout.addWidget(self.check2)
        layout.addWidget(button)

        self.setLayout(layout)

    def buttonClicked(self):
        print("Check1: %d" % self.check1.isChecked())
        print("Check2: %d" % self.check2.isChecked())


class ComboWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        label = QLabel("Select")

        self.combo = QComboBox(self)
        self.combo.addItem("apple")
        self.combo.addItem("banana")
        self.combo.addItem("lemon")
        self.combo.addItem("orange")

        button = QPushButton("Check")
        button.clicked.connect(self.buttonClicked)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.combo)
        layout.addWidget(button)

        self.setLayout(layout)

    def buttonClicked(self):
        print("Combo: %d, %s"
                % (self.combo.currentIndex(), self.combo.currentText()))


class Main(QWidget):
    def __init__(self):
        super().__init__()

        widget1 = RadioWidget(self)
        widget2 = CheckWidget(self)
        widget3 = ComboWidget(self)

        tab = QTabWidget()
        tab.addTab(widget1, "radio")
        tab.addTab(widget2, "check")
        tab.addTab(widget3, "combo")

        layout = QHBoxLayout(self)
        layout.addWidget(tab)

        self.setLayout(layout)

        self.setWindowTitle("tab")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())
