import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QStatusBar
from PyQt5.QtWidgets import QHBoxLayout, QTabWidget
from PyQt5.QtWidgets import QRadioButton, QButtonGroup
from PyQt5.QtWidgets import QCheckBox, QLabel, QComboBox
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QAction, qApp, QFileDialog, QMenu, QStyle
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt


import vtk
from vtk.util.colors import tomato
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

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
        
        

class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)

    def leftButtonPressEvent(self, obj, event):
        self.OnLeftButtonDown()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setMouseTracking(True)
        
        toolbar = self.addToolBar("")

        aButtonIcon = QAction(
                #QIcon("adelie.png"),
                QApplication.style().standardIcon(QStyle.SP_DirOpenIcon),
                "button",
                self)
        aButtonIcon.triggered.connect(self.open)
        #aButtonIcon.setCheckable(True)

        aButtonIcon.triggered.connect(self.buttonIconPress)
        toolbar.addAction(aButtonIcon)
        
        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(qApp.quit)

        openAction = QAction("&Open", self)
        openAction.triggered.connect(self.open)
        
        saveAction = QAction("&Save", self)
        saveAction.triggered.connect(self.save)
        
        doAction = QAction("&Do", self)
        doAction.triggered.connect(self.do)

        menubar = self.menuBar()

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)

        subMenu = fileMenu.addMenu("&Sub")
        subMenu.addAction(doAction)

        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        
        statusBar = QStatusBar(self)
        statusBar.showMessage("status bar")
        self.setStatusBar(statusBar)
        self.setWindowTitle("status bar")
        
        widget1 = RadioWidget(self)
        widget2 = CheckWidget(self)
        widget3 = ComboWidget(self)

        tab = QTabWidget()
        tab.addTab(widget1, "radio")
        tab.addTab(widget2, "check")
        tab.addTab(widget3, "combo")
        
        table = QTableWidget(2, 3)
        self.table = table

        header = ["A", "B", "C"]
        data = [["apple", "1", "100"], ["banana", "2", "200"]]

        table.setHorizontalHeaderLabels(header)

        for i in range(len(data)):
            for j in range(len(data[i])):
                table.setItem(i, j, QTableWidgetItem(data[i][j]))

        checkButton = QPushButton("Check")
        checkButton.clicked.connect(self.buttonClicked)

        
        #///////////////////////////
        
        tree_widget = QTreeWidget()
        self.tree_widget = tree_widget

        tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        tree_widget.customContextMenuRequested.connect(self.contextMenu)

        branch1 = QTreeWidgetItem()
        branch1.setData(0, Qt.CheckStateRole, Qt.Checked)
        branch1.setText(0, "branch1")

        branch2 = QTreeWidgetItem()
        branch2.setData(0, Qt.CheckStateRole, Qt.Checked)
        branch2.setText(0,"branch2")

        def addItem(branch, name, num, num2):
            item = QTreeWidgetItem(branch)
            item.setData(0, Qt.CheckStateRole, Qt.Checked)
            item.setText(0, name)
            item.setText(1, str(num))
            item.setText(2, str(num2))

        addItem(branch1, "apple", 1, 100)
        addItem(branch1, "banana", 2, 200)
        addItem(branch2, "lemon", 3, 300)
        addItem(branch2, "orange", 4, 400)

        tree_widget.addTopLevelItem(branch1)
        tree_widget.addTopLevelItem(branch2)

        tree_widget.setColumnCount(3)
        tree_widget.setHeaderLabels(["A", "B", "C"])

        tree_widget.itemClicked.connect(self.selectItem)
        tree_widget.itemChanged.connect(self.changeItem)

        branch1.setExpanded(True)
        branch2.setExpanded(True)        
        
        
        #////////////////////////////
        
        
        
        
        #////////////////////////////
        
        
        #layout = QHBoxLayout(self)
        #layout.addWidget(tab)
        #self.setLayout(layout)

        # source
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetResolution(20)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cylinder.GetOutputPort())

        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(tomato)
        actor.RotateX(30.)
        actor.RotateY(-45.)

        # renderer
        ren = vtk.vtkRenderer()
        ren.AddActor(actor)
        ren.SetBackground(0.1, 0.2, 0.4)

        # interactor
        frame = QFrame()
        inter = QVTKRenderWindowInteractor(frame)
        inter.SetInteractorStyle(MouseInteractorStyle())

        ren_win = inter.GetRenderWindow()
        ren_win.AddRenderer(ren)

        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(1.5)

        ren_win.Render()
        inter.Initialize()

        layout = QVBoxLayout()
        layout.addWidget(inter)
        layout.addWidget(tab)
        layout.addWidget(table)
        layout.addWidget(checkButton)
        layout.addWidget(tree_widget)
        #layout.addWidget(treeButton)
        
        frame.setLayout(layout)
        self.setCentralWidget(frame)

        self.setWindowTitle("qtvtk with Tabs")
        self.resize(320, 240)
        self.centerOnScreen()
        self.show()

    def selectItem(self):
        if self.tree_widget.selectedItems() == []:
            return
        item = self.tree_widget.selectedItems()[0]
        print(item.text(0))

    def changeItem(self, item, column):
        if item.childCount() > 0:
            self.checkBranch(item, item.checkState(0))

        for i in range(self.tree_widget.topLevelItemCount()):
            branch = self.tree_widget.topLevelItem(i)
            print(branch.text(0))
            for j in range(branch.childCount()):
                item = branch.child(j)
                if item.checkState(0):
                    print("  ", end="")
                    for k in range(item.columnCount()):
                        print(item.text(k), end=" ")
                    print()

    def checkBranch(self, branch, check=2):
        for i in range(branch.childCount()):
            item = branch.child(i)
            item.setCheckState(0, check)

    def checkAll(self, check=2):
        for i in range(self.tree_widget.topLevelItemCount()):
            branch = self.tree_widget.topLevelItem(i)
            branch.setCheckState(0, check)
            self.checkBranch(branch, check)

    def contextMenu(self, point):
        menu = QMenu(self)
        check_all = menu.addAction("Check all")
        uncheck_all = menu.addAction("Uncheck all")

        action = menu.exec_(self.mapToGlobal(point))

        if action == check_all:
            self.checkAll()
        elif action == uncheck_all:
            self.checkAll(0)        
        
    def buttonClicked(self):
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                print(self.table.item(i, j).text(), end=" ")
            print()
    def buttonClicked2(self):
        for i in range(self.tree_widget.topLevelItemCount()):
            branch = self.tree_widget.topLevelItem(i)
            print(branch.text(0))
            for j in range(branch.childCount()):
                item = branch.child(j)
                print("  ", end="")
                for k in range(item.columnCount()):
                    print(item.text(k), end=" ")
                print()

        print("find: lemon")
        items = self.tree_widget.findItems("lemon", Qt.MatchRecursive)
        item = items[0]
        print("  ", end="")
        for k in range(item.columnCount()):
            print(item.text(k), end=" ")
        print()
        
    def buttonIconPress(self, active):
        if active:
            print("Active: TRUE")
        else:
            print("Active: FALSE")
        
    def mouseButtonKind(self, buttons):
        if buttons & Qt.LeftButton:
            print("LEFT")
        if buttons & Qt.MidButton:
            print("MIDDLE")
        if buttons & Qt.RightButton:
            print("RIGHT")

    def mousePressEvent(self, e):
        print("BUTTON PRESS")
        self.mouseButtonKind(e.buttons())

    def mouseReleaseEvent(self, e):
        print("BUTTON RELEASE")
        self.mouseButtonKind(e.buttons())

    def wheelEvent(self, e):
        print("wheel")
        print("(%d %d)" % (e.angleDelta().x(), e.angleDelta().y()))

    def mouseMoveEvent(self, e):
        print("(%d %d)" % (e.x(), e.y()))
        
        
    def centerOnScreen(self):
        res = QDesktopWidget().screenGeometry()
        self.move((res.width()/2) - (self.frameSize().width()/2),
                  (res.height()/2) - (self.frameSize().height()/2))

    def do(self):
        print("Do")
        
    def open(self):
        filename = QFileDialog.getOpenFileName(self, "Open File",
                None, "Python Files (*.py)")
        print(filename)

    def save(self):
        #filename = QFileDialog.getSaveFileName(self, "Save File",
        #        None, "Python files (*.py)")
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Save File")
        dialog.setNameFilters(["Python Files (*.py)", "All Files (*)"])
        filename = dialog.exec_()
        print(filename)
        
    def keyPressEvent(self, e):
        def isPrintable(key):
            printable = [
                Qt.Key_Space,
                Qt.Key_Exclam,
                Qt.Key_QuoteDbl,
                Qt.Key_NumberSign,
                Qt.Key_Dollar,
                Qt.Key_Percent,
                Qt.Key_Ampersand,
                Qt.Key_Apostrophe,
                Qt.Key_ParenLeft,
                Qt.Key_ParenRight,
                Qt.Key_Asterisk,
                Qt.Key_Plus,
                Qt.Key_Comma,
                Qt.Key_Minus,
                Qt.Key_Period,
                Qt.Key_Slash,
                Qt.Key_0,
                Qt.Key_1,
                Qt.Key_2,
                Qt.Key_3,
                Qt.Key_4,
                Qt.Key_5,
                Qt.Key_6,
                Qt.Key_7,
                Qt.Key_8,
                Qt.Key_9,
                Qt.Key_Colon,
                Qt.Key_Semicolon,
                Qt.Key_Less,
                Qt.Key_Equal,
                Qt.Key_Greater,
                Qt.Key_Question,
                Qt.Key_At,
                Qt.Key_A,
                Qt.Key_B,
                Qt.Key_C,
                Qt.Key_D,
                Qt.Key_E,
                Qt.Key_F,
                Qt.Key_G,
                Qt.Key_H,
                Qt.Key_I,
                Qt.Key_J,
                Qt.Key_K,
                Qt.Key_L,
                Qt.Key_M,
                Qt.Key_N,
                Qt.Key_O,
                Qt.Key_P,
                Qt.Key_Q,
                Qt.Key_R,
                Qt.Key_S,
                Qt.Key_T,
                Qt.Key_U,
                Qt.Key_V,
                Qt.Key_W,
                Qt.Key_X,
                Qt.Key_Y,
                Qt.Key_Z,
                Qt.Key_BracketLeft,
                Qt.Key_Backslash,
                Qt.Key_BracketRight,
                Qt.Key_AsciiCircum,
                Qt.Key_Underscore,
                Qt.Key_QuoteLeft,
                Qt.Key_BraceLeft,
                Qt.Key_Bar,
                Qt.Key_BraceRight,
                Qt.Key_AsciiTilde,
            ]

            if key in printable:
                return True
            else:
                return False

        control = False

        if e.modifiers() & Qt.ControlModifier:
            print("Control")
            control = True

        if e.modifiers() & Qt.ShiftModifier:
            print("Shift")

        if e.modifiers() & Qt.AltModifier:
            print("Alt")

        if e.key() == Qt.Key_Delete:
            print("Delete")

        elif e.key() == Qt.Key_Backspace:
            print("Backspace")

        elif e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            print("Enter")

        elif e.key() == Qt.Key_Escape:
            print("Escape")

        elif e.key() == Qt.Key_Right:
            print("Right")

        elif e.key() == Qt.Key_Left:
            print("Left")

        elif e.key() == Qt.Key_Up:
            print("Up")

        elif e.key() == Qt.Key_Down:
            print("Down")

        if not control and isPrintable(e.key()):
            print(e.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())
