import sys
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class TabDialog(QDialog):                                     # +++       
    def __init__(self, sheetList):
        super().__init__()

        self.setWindowTitle("Tab Widget Application")
        self.setWindowIcon(QIcon("D:/_Qt/img/pyqt.jpg"))

        tabwidget = QTabWidget()
        for nameTab in sheetList:
            tabwidget.addTab(TabWindow(), nameTab)

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(tabwidget)
        self.setLayout(vboxLayout)


class TabWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tape Column Mapping')
        self.lbl = QLabel('For each worksheet you want to analyze, please associate each field with the appropriate worksheet column:',self)
        self.lbl.setFont(QFont("MS Shell Dlg 2", 8, QFont.Bold))

        self.initFormLayout()               # +++

        layout = QVBoxLayout(self)          # +++
        layout.addWidget(self.lbl)          # +++
        layout.addLayout(self.formLayout)   # +++
        layout.addStretch(1)              

    def initFormLayout(self):               # +++
        formList = [
            ["Address", ['A1', 'A2', 'A3', 'A4',]],
            ["City",    ['C1', 'C2', 'C3', 'C4', 'C5', 'C6',]],
            ["State",   ['S1', 'S2', 'S3', 'S4',]],
            ["Zip",     ['Z1', 'Z2', 'Z3',]],
            ["UPB",     ['U1', 'U2',]],
            ["Interest Rate", ['IR1', 'IR2', 'IR3', 'IR4',]],
            ["P&I",     ['PI1', 'PI2', 'PI3', 'PI4',]],
            ["Term",    ['T1', 'T2', 'T3', 'T4',]],
            ["Original Balance", ['OB1', 'OB2', 'OB3', 'OB4',]],
            ["Note Date",     ['ND1', 'ND2', 'ND3', 'ND4',]],
            ["Last Paid To",  ['LPT1', 'LPT2', 'LPT3', 'LPT4',]],
            ["Next Due Date", ['NDD1', 'NDD2', 'NDD3', 'NDD4',]],
            ["Maturity Date", ['MD1', 'MD2', 'MD3', 'MD4',]],
            ["Asset Type",    ['AT1', 'AT2', 'AT3', 'AT4',]],
            ["Note Status",   ['NS1', 'NS2', 'NS3', 'NS4',]],
        ]

        self.formLayout = QFormLayout()
        for item in formList:
            combo = QComboBox()
            combo.addItems(item[1])
            combo.activated[str].connect(self.comboActivate) # 2) How would I go about accessing the QComboBoxes 
            self.formLayout.addRow(QLabel(item[0]), combo)

    def comboActivate(self, text):                           # 2) How would I go about accessing the QComboBoxes 
        print("activated->`{}`".format(text))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NPN Tape Analyzer')
        self.setGeometry(100, 100, 640, 480)
        self.initUI()

    def initUI(self):
        self.lbl = QLabel('NPN Tape Analyzer', self)
        self.lbl.setGeometry(20, 10, 231, 31)
        self.lbl.setFont(QFont("MS Shell Dlg 2", 16, QFont.Bold))

        self.lbl1 = QLabel('(Open Tape Excel File)',self, alignment=Qt.AlignCenter)
        self.lbl1.setGeometry(250, 100, 140, 20)
        self.lbl1.setFont(QFont("MS Shell Dlg 2", 8))

        self.lbl2 = QLabel('Select Worksheets to analyze (ctrl + click for multiple selections):',self)
        self.lbl2.setGeometry(50, 190, 420, 20)
        self.lbl2.setFont(QFont("MS Shell Dlg 2", 9, QFont.Bold))

        btn = QPushButton('START ANALYSIS', self)
        btn.setGeometry(260, 60, 121, 41)
        btn.setFont(QFont("Arial", 8, QFont.Bold))
        btn.clicked.connect(self.openXLworksheetDialog)

        btn1 = QPushButton('NEXT >>', self)
        btn1.setGeometry(500, 280, 75, 23)
        btn1.setFont(QFont("Arial", 8))
        btn1.clicked.connect(self.collectSelectedSheets)

        btn2 = QPushButton('Exit Application',self)
        btn2.setGeometry(210, 380, 220, 40)
        btn2.setFont(QFont("Arial", 10, QFont.Bold))
        btn2.clicked.connect(self.close)

        self.fnametextBox = QLineEdit(self, alignment=Qt.AlignCenter)
        self.fnametextBox.setGeometry(35, 150, 571, 20)
        self.fnametextBox.setText("<No File>")
        self.fnametextBox.setStyleSheet("color: rgb(128, 128, 128);")
        self.fnametextBox.setReadOnly(True)

        self.sheetListWidg = QListWidget(self)
        self.sheetListWidg.setGeometry(200, 220, 241, 151)
        self.sheetListWidg.setStyleSheet("color: rgb(0, 0, 255);")
        self.sheetListWidg.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def openXLworksheetDialog(self):              
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        XLfilename, _ = QFileDialog.getOpenFileName(self,"Open MS Excel file","","Newer Excel files (*.xlsx);;Older Excel files (*.xls)",options=options)
        if XLfilename:
            self.fnametextBox.setText(XLfilename)
            self.WBdict = pd.read_excel(XLfilename, sheet_name=None)
            for key in self.WBdict:
                self.sheetListWidg.addItem(key)

    def collectSelectedSheets(self):
        tmpselSheets = self.sheetListWidg.selectedItems()
        self.selSheetList = []
        for i in range(len(tmpselSheets)):
            self.selSheetList.append(str(self.sheetListWidg.selectedItems()[i].text()))
        print(self.selSheetList)


        if self.selSheetList:                             # +++
            self.tabDialog = TabDialog(self.selSheetList) # +++    1) If this is a 2nd window,
            self.tabDialog.show()                         # +++    1) ...
        else:                                             # +++
            QMessageBox.information(self, 
                'Information', 
                'Select Worksheets to analyze' )

    def closeEvent(self, event):
            """Generate 'question' dialog on clicking 'X' button in title bar.
            Reimplement the closeEvent() event handler to include a 'Question'
            dialog with options on how to proceed - Close or Cancel buttons
            """
            reply = QMessageBox.question(
                self, "Message",
                "You are exiting the application. Are you sure you want to quit?",
                QMessageBox.Close | QMessageBox.Cancel,
                QMessageBox.Close)

            if reply == QMessageBox.Close:
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())