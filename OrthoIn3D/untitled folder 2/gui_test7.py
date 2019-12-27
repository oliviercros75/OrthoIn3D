import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QSplitter
from PyQt5.QtWidgets import QRadioButton, QButtonGroup
from PyQt5.QtWidgets import QCheckBox, QLabel, QComboBox
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt


class RadioFrame(QFrame):
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


class CheckFrame(QFrame):
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


class ComboFrame(QFrame):
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

        hbox = QHBoxLayout(self)

        frame1 = RadioFrame(self)
        frame1.setFrameShape(QFrame.Panel)

        frame2 = CheckFrame(self)
        frame2.setFrameShape(QFrame.Panel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(frame1)
        splitter1.addWidget(frame2)
        splitter1.setHandleWidth(10)

        frame3 = ComboFrame(self)
        frame3.setFrameShape(QFrame.Panel)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(frame3)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.setWindowTitle("splitter")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())