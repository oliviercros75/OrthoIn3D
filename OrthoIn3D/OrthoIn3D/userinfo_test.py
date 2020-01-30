# import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QStatusBar
from PyQt5.QtWidgets import QHBoxLayout, QTabWidget, QTextEdit
from PyQt5.QtWidgets import QRadioButton, QButtonGroup
from PyQt5.QtWidgets import QCheckBox, QLabel, QComboBox
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QAction, qApp, QFileDialog, QMenu, QStyle
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QRect, QCoreApplication, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp

# conn = sqlite3.connect('Contacts')
# c = conn.cursor()

# def tableCreate():
#     c.execute('CREATE TABLE ContactInfo(Name TEXT, Age INT, MobilePhone TEXT, Address TEXT)')

# name = ""
# age = int()
# mobilenum = ""
# Adr = ""

# def dataEntry():
#     c.execute('INSERT INTO CustomerInfo (Name, Age, MobilePhone, Address) VALUES (?,?,?,?)',
#         (Name, Age, MobilePhone, Adr))
#     conn.commit()



# GUI Code ------------------------------------------------------------

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_ContactCreator(object):
    def setupCreateContactUi(self, ContactCreator):
        ContactCreator.setObjectName(_fromUtf8("ContactCreator"))
        ContactCreator.resize(484, 165)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("CClogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ContactCreator.setWindowIcon(icon)
        name = ""
        age = int()
        mobilenum = ""
        address = ""
        self.addcontactBut = QPushButton(ContactCreator)
        self.addcontactBut.setGeometry(QtCore.QRect(190, 100, 101, 23))
        self.addcontactBut.setObjectName(_fromUtf8("addcontact"))
        self.addcontactBut.clicked.connect(self.addContact)

        self.nameLe = QLineEdit(ContactCreator)
        self.nameLe.setGeometry(QtCore.QRect(10, 60, 171, 20))
        self.nameLe.setAutoFillBackground(False)
        self.nameLe.setObjectName(_fromUtf8("name"))

        self.ageLe = QLineEdit(ContactCreator)
        self.ageLe.setGeometry(QtCore.QRect(190, 60, 41, 20))
        self.ageLe.setObjectName(_fromUtf8("age"))
        self.ageLe.setText("")

        self.mobphoLe = QLineEdit(ContactCreator)
        self.mobphoLe.setGeometry(QtCore.QRect(240, 60, 113, 20))
        self.mobphoLe.setObjectName(_fromUtf8("mobilephone"))

        self.adrLe = QLineEdit(ContactCreator)
        self.adrLe.setGeometry(QtCore.QRect(360, 60, 113, 20))
        self.adrLe.setObjectName(_fromUtf8("address"))

        self.label = QLabel(ContactCreator)
        self.label.setGeometry(QtCore.QRect(90, 40, 31, 20))
        self.label.setObjectName(_fromUtf8("label"))

        self.label_2 = QLabel(ContactCreator)
        self.label_2.setGeometry(QtCore.QRect(200, 40, 21, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.label_3 = QLabel(ContactCreator)
        self.label_3.setGeometry(QtCore.QRect(260, 40, 81, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.label_4 = QLabel(ContactCreator)
        self.label_4.setGeometry(QtCore.QRect(370, 40, 101, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.retranslateUi(ContactCreator)
        QtCore.QMetaObject.connectSlotsByName(ContactCreator)

    def addContact(self):
        self.name = str(self.nameLe.text())
        self.age = str(self.ageLe.text()‡)
        print(self.name)

    def retranslateUi(self, ContactCreator):
        ContactCreator.setWindowTitle(_translate("ContactCreator", "ContactCreator", None))
        self.addcontactBut.setText(_translate("ContactCreator", "Add New Contact", None))
        self.label.setText(_translate("ContactCreator", "Name", None))
        self.label_2.setText(_translate("ContactCreator", "Age", None))
        self.label_3.setText(_translate("ContactCreator", "  Mobile Phone", None))
        self.label_4.setText(_translate("ContactCreator", "      Address", None))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ContactCreator = QWidget()
    ui = Ui_ContactCreator()
    ui.setupCreateContactUi(ContactCreator)
    ContactCreator.show()
    sys.exit(app.exec_())