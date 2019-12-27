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

from segmentation.cut import prepare_polydata, cut
from segmentation.field import compute_field, add_field, add_field_gui, save_stl, add_brush
from segmentation.viewer import show_field, show_field_gui, get_cusps, get_cusps_gui, select_spline
from registration.mesh_registration import set_source_polydata, set_target_polydata, perform_ICP_PointTransform, set_ICP_transform_filter, display_transformed_polydata

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
        
        #self.setMouseTracking(False)
        
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
        
#        widget1 = RadioWidget(self)
#        widget2 = CheckWidget(self)
#        widget3 = ComboWidget(self)
#
#        tab = QTabWidget()
#        tab.addTab(widget1, "radio")
#        tab.addTab(widget2, "check")
#        tab.addTab(widget3, "combo")
#        
#        table = QTableWidget(2, 3)
#        self.table = table
#
#        header = ["A", "B", "C"]
#        data = [["apple", "1", "100"], ["banana", "2", "200"]]
#
#        table.setHorizontalHeaderLabels(header)
#
#        for i in range(len(data)):
#            for j in range(len(data[i])):
#                table.setItem(i, j, QTableWidgetItem(data[i][j]))

        checkButton = QPushButton("Check")
        checkButton.clicked.connect(self.buttonClicked)
        
        self.processButton = QPushButton("Process")
        self.pickedPointsButton = QPushButton("Stop picking")


        
        #///////////////////////////
        
#        tree_widget = QTreeWidget()
#        self.tree_widget = tree_widget
#
#        tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
#        tree_widget.customContextMenuRequested.connect(self.contextMenu)
#
#        branch1 = QTreeWidgetItem()
#        branch1.setData(0, Qt.CheckStateRole, Qt.Checked)
#        branch1.setText(0, "branch1")
#
#        branch2 = QTreeWidgetItem()
#        branch2.setData(0, Qt.CheckStateRole, Qt.Checked)
#        branch2.setText(0,"branch2")
#
#        def addItem(branch, name, num, num2):
#            item = QTreeWidgetItem(branch)
#            item.setData(0, Qt.CheckStateRole, Qt.Checked)
#            item.setText(0, name)
#            item.setText(1, str(num))
#            item.setText(2, str(num2))
#
#        addItem(branch1, "apple", 1, 100)
#        addItem(branch1, "banana", 2, 200)
#        addItem(branch2, "lemon", 3, 300)
#        addItem(branch2, "orange", 4, 400)
#
#        tree_widget.addTopLevelItem(branch1)
#        tree_widget.addTopLevelItem(branch2)
#
#        tree_widget.setColumnCount(3)
#        tree_widget.setHeaderLabels(["A", "B", "C"])
#
#        tree_widget.itemClicked.connect(self.selectItem)
#        tree_widget.itemChanged.connect(self.changeItem)
#
#        branch1.setExpanded(True)
#        branch2.setExpanded(True)        
        
        # renderer
        self.ren = vtk.vtkRenderer()
        #self.ren.AddActor(actor)
        self.ren.SetBackground(0.1, 0.2, 0.4)

        ## interactor
        self.frame = QFrame()
        self.inter = QVTKRenderWindowInteractor(self.frame)
        self.inter.SetInteractorStyle(MouseInteractorStyle())
        
        #self.inter.AddObserver('KeyPressEvent', keypress_callback, 1.0)
        self.inter.AddObserver("KeyPressEvent", self.key_pressed_callback)
        
        self.ren_win = self.inter.GetRenderWindow()
        self.ren_win.AddRenderer(self.ren)

        self.ren.ResetCamera()
        self.ren.GetActiveCamera().Zoom(1.5)

        self.ren_win.Render()
        self.inter.Initialize()
        self.inter.Start()
        
        
        #//////////////////////////
        
        self.frame = QFrame()
 
        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
 
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        #self.ren.AddActor(actor)
        self.ren.ResetCamera()
 
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
 
        self.show()
        #self.iren.Initialize()
        
        #////////////////////////////
        
        print("Loading STL files")
        #filename = './STL/6000_2017-02-03_13-14_Mandibular_export.stl'
        filename = '/Users/ocros/Downloads/copie-CROS de STL non segmentés/STL non segmentés/9056_2015-05-20_13-36_Mandibular_export.stl'
    
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)
    
        print("STL file is now loaded")

        dummy, polydata = prepare_polydata(reader)
        full_jaw_polydata = polydata
        
        cutted_polydata, gencives = cut(polydata, shift=5)
        
        #clicked_0,clicked_1 = get_cusps(self, cutted_polydata)
        clicked_0, clicked_1 = get_cusps_gui(self.ren, self.iren, cutted_polydata)   # in viewer.py
        
        print(clicked_0)
        #self.pickedPointsButton.clicked.connect(self.changePickedPointFlag)
        
        print(len(clicked_0))
        print("Here now")

        cusps_0 = add_brush(cutted_polydata, clicked_0, radius=0.5)
        cusps_1 = add_brush(cutted_polydata, clicked_1, radius=0.5)

        #self.processButton.clicked.connect(self.performSegmentation(self.cusps_0, self.cusps_1,self.gencives, self.cutted_polydata))
        self.processButton.clicked.connect(lambda: self.performSegmentation(cusps_0, cusps_1, gencives, cutted_polydata))
        
#        #splines_polydata = select_spline(self, field_polydata)
#        splines_polydata = select_spline(field_polydata)
#
#        save_stl(field_polydata,splines_polydata,clicked_0,clicked_1)
        
        
        #////////////////////////////
        
        
        #layout = QHBoxLayout(self)
        #layout.addWidget(tab)
        #self.setLayout(layout)

#        # source
#        cylinder = vtk.vtkCylinderSource()
#        cylinder.SetResolution(20)
#
#        # mapper
#        mapper = vtk.vtkPolyDataMapper()
#        mapper.SetInputConnection(cylinder.GetOutputPort())

#        # actor
#        actor = vtk.vtkActor()
#        actor.SetMapper(mapper)
#        actor.GetProperty().SetColor(tomato)
#        actor.RotateX(30.)
#        actor.RotateY(-45.)


        #layout = QVBoxLayout()
    
        #layout.addWidget(self.vtkWidget)
        
        #layout.addWidget(tab)
        #self.vl.addWidget(tab)
        #layout.addWidget(table)
        #self.vl.addWidget(table)
        #layout.addWidget(checkButton)
        self.vl.addWidget(checkButton)
        #layout.addWidget(self.processButton)
        self.vl.addWidget(self.processButton)
        #layout.addWidget(self.processButton)
        self.vl.addWidget(self.pickedPointsButton)        
        #layout.addWidget(tree_widget)
        #self.vl.addWidget(tree_widget)
        #layout.addWidget(treeButton)
        
        #self.frame.setLayout(layout)
        #self.setCentralWidget(self.frame)

        self.setWindowTitle("qtvtk with Tabs")
        self.resize(800, 600)
        self.centerOnScreen()
        self.show()
        
    def keypress_callback(obj,event):
        key = obj.GetKeySym()
        print(key, 'was pressed')
        
    def key_pressed_callback(obj, event):
        # ---------------------------------------------------------------
        # Attach actions to specific keys
        # ---------------------------------------------------------------
        key = obj.GetKeySym()
        print("key=", key)
        if key == "l":
            print("l was pressed")
    
    def performSegmentation(self, cusps_0, cusps_1, gencives, cutted_polydata):
        #old_field=[]
        field = compute_field(cusps_0, cusps_1, gencives, cutted_polydata, old_field=[]) # in file 'field.py'
        name = "Harmonic Field"
        field_polydata = add_field(cutted_polydata, field, name)   # in file 'field.py'
        add_iso=False
        show_field(field_polydata, add_iso) # in file 'viewer.py'
        
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
        
#    def mouseButtonKind(self, buttons):
#        if buttons & Qt.LeftButton:
#            print("LEFT")
#        if buttons & Qt.MidButton:
#            print("MIDDLE")
#        if buttons & Qt.RightButton:
#            print("RIGHT")
#
#    def mousePressEvent(self, e):
#        print("BUTTON PRESS")
#        self.mouseButtonKind(e.buttons())
#
#    def mouseReleaseEvent(self, e):
#        print("BUTTON RELEASE")
#        self.mouseButtonKind(e.buttons())
#
#    def wheelEvent(self, e):
#        print("wheel")
#        print("(%d %d)" % (e.angleDelta().x(), e.angleDelta().y()))
#
#    def mouseMoveEvent(self, e):
#        print("(%d %d)" % (e.x(), e.y()))
        
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())
