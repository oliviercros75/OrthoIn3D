#!/usr/bin/env python

# Our example needs the VTK Python package
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
from PyQt5.QtGui import QIcon

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
import os
from os import path
import argparse
import wx
import math

import json

from segmentation.cut import prepare_polydata, cut
from segmentation.field import compute_field, add_field, add_field_gui, save_stl, add_brush
from segmentation.viewer import show_field, show_field_gui, get_cusps, get_cusps_gui, select_spline, select_spline_gui
from registration.mesh_registration import set_source_polydata, set_target_polydata, perform_ICP_PointTransform, set_ICP_transform_filter, display_transformed_polydata

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        #self.setWindowTitle("Hello World")
        #MainWindow.setGeometry(100, 100, 400, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")  
        
        self.filename=""
        
        self.act = QAction("Open STL File")
        self.act.triggered.connect(self.openStlFile)
        print(self.filename)
        
        self.exit_act = QAction(QIcon('diagram-icon.png'), '&Exit')
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.setStatusTip('Exit application')
        self.exit_act.triggered.connect(qApp.quit)
        
        self.menu_bar = QMenuBar()
        
        self.file_menu = self.menu_bar.addMenu('&File')
        self.file_menu.addAction(self.act)
        self.file_menu.addAction(self.exit_act)
        
        self.settings_menu = self.menu_bar.addMenu('&Settings')
        self.settings_menu.addAction(self.act)
        self.settings_menu.addAction(self.exit_act)
        
        #self.another_menu = self.file_menu.addMenu("Parent Menu")
        #self.submenu = QAction("Submenu1")
        #self.another_menu.addAction(self.submenu)
        #self.another_menu.addAction(QAction("Submenu 2"))
        #self.another_menu.addAction(QAction("Submenu 3"))
        self.view_menu = self.menu_bar.addMenu('&View')
        self.show_status_action = QAction("Show status")
        self.show_status_action.setStatusTip("This will show status bar")
        self.show_status_action.setCheckable(True)
        self.show_status_action.setChecked(False)
        self.show_status_action.triggered.connect(self.show_status)
        self.view_menu.addAction(self.show_status_action)
        
        MainWindow.statusBar().showMessage('This is a status bar')
        
        self.frame = QFrame(self.centralwidget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.gridlayout = QGridLayout(self.centralwidget)
        
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralwidget)
        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 800, 600)
        
        self.width = MainWindow.frameGeometry().width()
        self.height = MainWindow.frameGeometry().height()
        self.buttpnPosX = math.floor(self.width/2)
        self.buttpnPosY = math.floor(self.height/2)
        self.xOffset = 370
        self.yOffset = 0
        
        self.computeButton = QPushButton("Compute Harmonic Field")
        self.gridlayout.addWidget(self.computeButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.computeButton.clicked.connect(compute_harmonic_field)
        self.computeButton.show()
        
        #self.showFieldButton = QPushButton("Show Results")
        #self.gridlayout.addWidget(self.showFieldButton, #self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        #self.showFieldButton.clicked.connect(show_harmonic_field)
        #self.showFieldButton.hide()
        
        self.editTeethContourButton = QPushButton("Edit Teeth Contour")
        self.gridlayout.addWidget(self.editTeethContourButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.editTeethContourButton.clicked.connect(edit_teeth_contours)
        self.editTeethContourButton.hide()
        
        self.saveFieldButton = QPushButton("Save segmentation")
        self.gridlayout.addWidget(self.saveFieldButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.saveFieldButton.clicked.connect(save_segmented_items)
        self.saveFieldButton.hide()
        
        self.quitFieldButton = QPushButton("Quit")
        self.gridlayout.addWidget(self.quitFieldButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.quitFieldButton.clicked.connect(quitApplication)
        self.quitFieldButton.hide()
        
        self.yOffset = -100
        self.settingsFieldButton = QPushButton("Settings")
        self.gridlayout.addWidget(self.settingsFieldButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.settingsFieldButton.clicked.connect(self.toggleSettingsWindow)
        self.yOffset = 0
        
        self.yOffset = 100
        self.backFieldButton = QPushButton("Back")
        self.gridlayout.addWidget(self.backFieldButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.backFieldButton.clicked.connect(goBack)
        self.yOffset = 0
        self.backFieldButton.hide()
        
        MainWindow.setCentralWidget(self.centralwidget)
    
    def toggleSettingsWindow(self):
        self.SW = SettingsWindow()
        self.SW.show()
        
    def do_something(self):
        print("Clicked")
        
    def openStlFile(self):
        
        fname = QFileDialog.getOpenFileName(self.centralwidget, 'Choose STL file', os.sep.join((os.path.expanduser('~'), 'Documents')),
                                                 'STL file (*.stl)')
        self.filename = fname[0]
        return self.filename
        
    def show_status(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()
        print(state)


class SettingsWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Settings")
        self.resize(300, 50)
        
        self.jaw_type = "mandi"
        
        self.thegrid = QGridLayout()
        
        self.title_label = QLabel("Check missing teeth:")
        self.thegrid.addWidget(self.title_label,0,0)
        if (self.jaw_type == "mandi"):
            self.thegrid.addWidget(self.setCuspsSphereMandi(), 1, 0)
        elif (self.jaw_type == "maxi"):
            self.thegrid.addWidget(self.setCuspsSphereMaxi(), 1, 0)
        else:
            self.thegrid.addWidget(self.setCuspsSphereMandi(), 1, 0)
            self.thegrid.addWidget(self.setCuspsSphereMaxi(), 2, 0)
        #self.thegrid.addWidget(self.createExampleGroup(), 0, 1)
        #self.thegrid.addWidget(self.createExampleGroup(), 1, 1)
        self.setLayout(self.thegrid)

        
        
    def setCuspsSphereMandi(self):
        
        self.groupBoxMandi = QGroupBox("Mandibular")

        self.thevboxMandi = QVBoxLayout()    
        self.makeMandiSideOne()
        #self.showMandiSideOneSphereDiam
        self.makeMandiSideTwo()
        #self.showMandiSideTwoSphereDiam
        
        self.thevboxMandi.addLayout(self.mandiSideOneBox)
        #self.thevboxMandi.addLayout(self.mandiSideOneSphereDiamBox)
        self.thevboxMandi.addLayout(self.mandiSideTwoBox)
        #self.thevboxMandi.addLayout(self.mandiSideTwoSphereDiamBox)
        self.thevboxMandi.addStretch(1)
        
        self.groupBoxMandi.setLayout(self.thevboxMandi)

        return self.groupBoxMandi
    
    def setCuspsSphereMaxi(self):
        self.groupBoxMaxi = QGroupBox("Maxillary")

        self.thevboxMaxi = QVBoxLayout()    
        self.makeMaxiSideOne()
        self.makeMaxiSideTwo()
        self.thevboxMaxi.addLayout(self.maxiSideOneBox)
        self.thevboxMaxi.addLayout(self.maxiSideTwoBox)
        self.thevboxMaxi.addStretch(1)
        
        self.groupBoxMaxi.setLayout(self.thevboxMaxi)
        return self.groupBoxMaxi
    
    def makeMandiSideOne(self):
        self.mandiSideOneBox = QHBoxLayout()
#        self.thevbox.addWidget(self.radio1)
#        self.thevbox.addWidget(self.slider)
        self.mandiSideOneBox.addStretch(1)

        self.tooth18cb = QCheckBox("18",self)
        self.tooth18cb.stateChanged.connect(self.clickBox)
        self.tooth18cb.move(20,20)
        self.tooth18cb.resize(60,40)
        
        self.tooth17cb = QCheckBox("17",self)
        self.tooth17cb.stateChanged.connect(self.clickBox)
        self.tooth17cb.move(20,40)
        self.tooth17cb.resize(60,40)
        
        self.tooth16cb = QCheckBox("16",self)
        self.tooth16cb.stateChanged.connect(self.clickBox)
        self.tooth16cb.move(20,60)
        self.tooth16cb.resize(60,40)
        
        self.tooth15cb = QCheckBox("15",self)
        self.tooth15cb.stateChanged.connect(self.clickBox)
        self.tooth15cb.move(20,80)
        self.tooth15cb.resize(60,40)
        
        self.tooth14cb = QCheckBox("14",self)
        self.tooth14cb.stateChanged.connect(self.clickBox)
        self.tooth14cb.move(20,80)
        self.tooth14cb.resize(60,40)
        
        self.tooth13cb = QCheckBox("13",self)
        self.tooth13cb.stateChanged.connect(self.clickBox)
        self.tooth13cb.move(20,100)
        self.tooth13cb.resize(60,40)
        
        self.tooth12cb = QCheckBox("12",self)
        self.tooth12cb.stateChanged.connect(self.clickBox)
        self.tooth12cb.move(20,120)
        self.tooth12cb.resize(60,40)
        
        self.tooth11cb = QCheckBox("11",self)
        self.tooth11cb.stateChanged.connect(self.clickBox)
        self.tooth11cb.move(20,140)
        self.tooth11cb.resize(60,40)
        
        self.tooth10cb = QCheckBox("10",self)
        self.tooth10cb.stateChanged.connect(self.clickBox)
        self.tooth10cb.move(20,160)
        self.tooth10cb.resize(60,40)
        
        self.mandiSideOneBox.addWidget(self.tooth18cb)
        self.mandiSideOneBox.addWidget(self.tooth17cb)
        self.mandiSideOneBox.addWidget(self.tooth16cb)
        self.mandiSideOneBox.addWidget(self.tooth15cb)
        self.mandiSideOneBox.addWidget(self.tooth14cb)
        self.mandiSideOneBox.addWidget(self.tooth13cb)
        self.mandiSideOneBox.addWidget(self.tooth12cb)
        self.mandiSideOneBox.addWidget(self.tooth11cb)
        self.mandiSideOneBox.addWidget(self.tooth10cb)
        
        return self.mandiSideOneBox
    
    

    def makeMandiSideTwo(self):
        self.mandiSideTwoBox = QHBoxLayout()
#        self.thevbox.addWidget(self.radio1)
#        self.thevbox.addWidget(self.slider)
        self.mandiSideTwoBox.addStretch(1)

        self.tooth28cb = QCheckBox("28",self)
        self.tooth28cb.stateChanged.connect(self.clickBox)
        self.tooth28cb.move(20,20)
        self.tooth28cb.resize(60,40)
        
        self.tooth27cb = QCheckBox("27",self)
        self.tooth27cb.stateChanged.connect(self.clickBox)
        self.tooth27cb.move(20,40)
        self.tooth27cb.resize(60,40)
        
        self.tooth26cb = QCheckBox("26",self)
        self.tooth26cb.stateChanged.connect(self.clickBox)
        self.tooth26cb.move(20,60)
        self.tooth26cb.resize(60,40)
        
        self.tooth25cb = QCheckBox("25",self)
        self.tooth25cb.stateChanged.connect(self.clickBox)
        self.tooth25cb.move(20,80)
        self.tooth25cb.resize(60,40)
        
        self.tooth24cb = QCheckBox("24",self)
        self.tooth24cb.stateChanged.connect(self.clickBox)
        self.tooth24cb.move(20,80)
        self.tooth24cb.resize(60,40)
        
        self.tooth23cb = QCheckBox("23",self)
        self.tooth23cb.stateChanged.connect(self.clickBox)
        self.tooth23cb.move(20,100)
        self.tooth23cb.resize(60,40)
        
        self.tooth22cb = QCheckBox("22",self)
        self.tooth22cb.stateChanged.connect(self.clickBox)
        self.tooth22cb.move(20,120)
        self.tooth22cb.resize(60,40)
        
        self.tooth21cb = QCheckBox("21",self)
        self.tooth21cb.stateChanged.connect(self.clickBox)
        self.tooth21cb.move(20,140)
        self.tooth21cb.resize(60,40)
        
        self.tooth20cb = QCheckBox("20",self)
        self.tooth20cb.stateChanged.connect(self.clickBox)
        self.tooth20cb.move(20,160)
        self.tooth20cb.resize(60,40)
        
        self.mandiSideTwoBox.addWidget(self.tooth28cb)
        self.mandiSideTwoBox.addWidget(self.tooth27cb)
        self.mandiSideTwoBox.addWidget(self.tooth26cb)
        self.mandiSideTwoBox.addWidget(self.tooth25cb)
        self.mandiSideTwoBox.addWidget(self.tooth24cb)
        self.mandiSideTwoBox.addWidget(self.tooth23cb)
        self.mandiSideTwoBox.addWidget(self.tooth22cb)
        self.mandiSideTwoBox.addWidget(self.tooth21cb)
        self.mandiSideTwoBox.addWidget(self.tooth20cb)
        
        return self.mandiSideTwoBox
        
    def makeMaxiSideOne(self):
        self.maxiSideOneBox = QHBoxLayout()
#        self.thevbox.addWidget(self.radio1)
#        self.thevbox.addWidget(self.slider)
        self.maxiSideOneBox.addStretch(1)

        self.tooth38cb = QCheckBox("38",self)
        self.tooth38cb.stateChanged.connect(self.clickBox)
        self.tooth38cb.move(20,20)
        self.tooth38cb.resize(60,40)
        
        self.tooth37cb = QCheckBox("37",self)
        self.tooth37cb.stateChanged.connect(self.clickBox)
        self.tooth37cb.move(20,40)
        self.tooth37cb.resize(60,40)
        
        self.tooth36cb = QCheckBox("36",self)
        self.tooth36cb.stateChanged.connect(self.clickBox)
        self.tooth36cb.move(20,60)
        self.tooth36cb.resize(60,40)
        
        self.tooth35cb = QCheckBox("35",self)
        self.tooth35cb.stateChanged.connect(self.clickBox)
        self.tooth35cb.move(20,80)
        self.tooth35cb.resize(60,40)
        
        self.tooth34cb = QCheckBox("34",self)
        self.tooth34cb.stateChanged.connect(self.clickBox)
        self.tooth34cb.move(20,80)
        self.tooth34cb.resize(60,40)
        
        self.tooth33cb = QCheckBox("33",self)
        self.tooth33cb.stateChanged.connect(self.clickBox)
        self.tooth33cb.move(20,100)
        self.tooth33cb.resize(60,40)
        
        self.tooth32cb = QCheckBox("32",self)
        self.tooth32cb.stateChanged.connect(self.clickBox)
        self.tooth32cb.move(20,120)
        self.tooth32cb.resize(60,40)
        
        self.tooth31cb = QCheckBox("31",self)
        self.tooth31cb.stateChanged.connect(self.clickBox)
        self.tooth31cb.move(20,140)
        self.tooth31cb.resize(60,40)
        
        self.tooth30cb = QCheckBox("30",self)
        self.tooth30cb.stateChanged.connect(self.clickBox)
        self.tooth30cb.move(20,160)
        self.tooth30cb.resize(60,40)
        
        self.maxiSideOneBox.addWidget(self.tooth38cb)
        self.maxiSideOneBox.addWidget(self.tooth37cb)
        self.maxiSideOneBox.addWidget(self.tooth36cb)
        self.maxiSideOneBox.addWidget(self.tooth35cb)
        self.maxiSideOneBox.addWidget(self.tooth34cb)
        self.maxiSideOneBox.addWidget(self.tooth33cb)
        self.maxiSideOneBox.addWidget(self.tooth32cb)
        self.maxiSideOneBox.addWidget(self.tooth31cb)
        self.maxiSideOneBox.addWidget(self.tooth30cb)
        
        return self.maxiSideOneBox

    def makeMaxiSideTwo(self):
        self.maxiSideTwoBox = QHBoxLayout()
#        self.thevbox.addWidget(self.radio1)
#        self.thevbox.addWidget(self.slider)
        self.maxiSideTwoBox.addStretch(1)

        self.tooth48cb = QCheckBox("48",self)
        self.tooth48cb.stateChanged.connect(self.clickBox)
        self.tooth48cb.move(20,20)
        self.tooth48cb.resize(60,40)
        
        self.tooth47cb = QCheckBox("47",self)
        self.tooth47cb.stateChanged.connect(self.clickBox)
        self.tooth47cb.move(20,40)
        self.tooth47cb.resize(60,40)
        
        self.tooth46cb = QCheckBox("46",self)
        self.tooth46cb.stateChanged.connect(self.clickBox)
        self.tooth46cb.move(20,60)
        self.tooth46cb.resize(60,40)
        
        self.tooth45cb = QCheckBox("45",self)
        self.tooth45cb.stateChanged.connect(self.clickBox)
        self.tooth45cb.move(20,80)
        self.tooth45cb.resize(60,40)
        
        self.tooth44cb = QCheckBox("44",self)
        self.tooth44cb.stateChanged.connect(self.clickBox)
        self.tooth44cb.move(20,80)
        self.tooth44cb.resize(60,40)
        
        self.tooth43cb = QCheckBox("43",self)
        self.tooth43cb.stateChanged.connect(self.clickBox)
        self.tooth43cb.move(20,100)
        self.tooth43cb.resize(60,40)
        
        self.tooth42cb = QCheckBox("42",self)
        self.tooth42cb.stateChanged.connect(self.clickBox)
        self.tooth42cb.move(20,120)
        self.tooth42cb.resize(60,40)
        
        self.tooth41cb = QCheckBox("41",self)
        self.tooth41cb.stateChanged.connect(self.clickBox)
        self.tooth41cb.move(20,140)
        self.tooth41cb.resize(60,40)
        
        self.tooth40cb = QCheckBox("40",self)
        self.tooth40cb.stateChanged.connect(self.clickBox)
        self.tooth40cb.move(20,160)
        self.tooth40cb.resize(60,40)
        
        self.maxiSideTwoBox.addWidget(self.tooth48cb)
        self.maxiSideTwoBox.addWidget(self.tooth47cb)
        self.maxiSideTwoBox.addWidget(self.tooth46cb)
        self.maxiSideTwoBox.addWidget(self.tooth45cb)
        self.maxiSideTwoBox.addWidget(self.tooth44cb)
        self.maxiSideTwoBox.addWidget(self.tooth43cb)
        self.maxiSideTwoBox.addWidget(self.tooth42cb)
        self.maxiSideTwoBox.addWidget(self.tooth41cb)
        self.maxiSideTwoBox.addWidget(self.tooth40cb)
        
        return self.maxiSideTwoBox
    
    
    def clickBox(self, state):

        if state == QtCore.Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')
        

class SimpleView(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        print("Filename is: " + self.ui.filename)
        
        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        
        
        self.ui.filename = '/Users/ocros/Documents/OrthoIn3D/OrthoIn3D/OrthoIn3D/data/data_input/6000_2017-02-03_13-14_Mandibular_export.stl'
        print("Filename is: " + self.ui.filename)
        
        data_dict = {'patientName': 'Doe',
                          'patientSurname': 'John',
                          'Sex' : 'None',
                          'age': 45,
                          'mandi': False,
                          'maxi': False,
                          'missingTeethMandi' : [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          'missingTeethMaxi' : [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                          'inclusionSphereDiamMandi' : [8,8,7,7,6,5,3,2,2,3,5,6,7,7,8,8],
                          'inclusionSphereDiamMaxi' : [8,8,7,7,6,5,3,2,2,3,5,6,7,7,8,8],
                     'pickedPoints': {}
                         }
        orthonIn3D_data = json.dumps(data_dict)
        with open('./patientA.json', 'w') as j_file:
            json.dump(orthonIn3D_data, j_file)
        # Pretty Printing JSON string back
        #print(json.dumps(orthonIn3D_data, indent = 4, sort_keys=True))
        
        prepare_jaw(self, self.ui.filename)
        pick_the_teeth_on_jaw(self, self.ui, data_dict)
        
        self.txt = vtk.vtkTextActor()
        self.txt.SetInput("1) Click with the mouse on the black screen,")
        self.txtprop=self.txt.GetTextProperty()
        self.txtprop.SetFontFamilyToArial()
        self.txtprop.SetFontSize(18)
        self.txtprop.SetColor(1,1,0)
        self.txt.SetDisplayPosition(20,500)
        
        self.txt2 = vtk.vtkTextActor()
        self.txt2.SetInput("2) Place the cursor over a tooth")
        self.txtprop2=self.txt2.GetTextProperty()
        self.txtprop2.SetFontFamilyToArial()
        self.txtprop2.SetFontSize(18)
        self.txtprop2.SetColor(1,1,0)
        self.txt2.SetDisplayPosition(20,480)
        
        self.txt3 = vtk.vtkTextActor()
        self.txt3.SetInput("3) Press 'p' on your keybooard ")
        self.txtprop3=self.txt3.GetTextProperty()
        self.txtprop3.SetFontFamilyToArial()
        self.txtprop3.SetFontSize(18)
        self.txtprop3.SetColor(1,1,0)
        self.txt3.SetDisplayPosition(20,460)
        
        self.txt4 = vtk.vtkTextActor()
        self.txt4.SetInput("4) Repeat the same for all teeth ")
        self.txtprop4=self.txt4.GetTextProperty()
        self.txtprop4.SetFontFamilyToArial()
        self.txtprop4.SetFontSize(18)
        self.txtprop4.SetColor(1,1,0)
        self.txt4.SetDisplayPosition(20,440)
        
        self.txt5 = vtk.vtkTextActor()
        self.txt5.SetInput("5) click on Compute Field ")
        self.txtprop5=self.txt5.GetTextProperty()
        self.txtprop5.SetFontFamilyToArial()
        self.txtprop5.SetFontSize(18)
        self.txtprop5.SetColor(1,1,0)
        self.txt5.SetDisplayPosition(20,420)
        
        self.ren.AddActor(self.txt)
        self.ren.AddActor(self.txt2)
        self.ren.AddActor(self.txt3)
        self.ren.AddActor(self.txt4)
        self.ren.AddActor(self.txt5)

        self.iren.AddObserver("KeyPressEvent", key_pressed_callback)
        #self.ren.AddActor(actor)

def pickedSphereBounds(self):
    allActors = window.ren.GetActors()
    allActors.InitTraversal()
    num_items = allActors.GetNumberOfItems()
    boundsPickedSpheres = {}
    for i in range(num_items):
        bounds = [0]*6
        currentActor = allActors.GetNextActor() 
        currentActor.GetBounds(bounds)
        print(bounds)
        boundsPickedSpheres.append({i : [bounds[0], bounds[1], bounds[2], bounds[3], bounds[4], bounds[5]]})
    return boundsPickedSpheres


def hidePickerRedBoundingBox(self):
    # reset actor colors
    actorCollection = window.ren.GetActors()
    actorCollection.InitTraversal()

    cactor = actorCollection.GetNextActor() # first actor
    while cactor != actorCollection.GetLastActor():
        #print("going through objects")
        currentActorColor = cactor.GetProperty().GetColor()
        if ((currentActorColor[0]==1) and
            (currentActorColor[1]==0) and
            (currentActorColor[2]==0)):
            cactor.GetProperty().SetOpacity(0.0)
        cactor = actorCollection.GetNextActor()
     # Last actor
    currentActorColor = cactor.GetProperty().GetColor()
    if ((currentActorColor[0]==1) and
        (currentActorColor[1]==0) and
        (currentActorColor[2]==0)):
        cactor.GetProperty().SetOpacity(0.0) 
        
def hidePickedSphere(self):
    
    #print("Hiding the green spheres")    
    # reset actor colors
    actorCollection = window.ren.GetActors()
    actorCollection.InitTraversal()

    cactor = actorCollection.GetNextActor() # first actor
    while cactor != actorCollection.GetLastActor():
        #print("going through objects")
        currentActorColor = cactor.GetProperty().GetColor()
        if ((currentActorColor[0]==0) and
            (currentActorColor[1]==1) and
            (currentActorColor[2]==0)):
            cactor.GetProperty().SetOpacity(0.0)
        cactor = actorCollection.GetNextActor()
    # Last actor
    currentActorColor = cactor.GetProperty().GetColor()
    if ((currentActorColor[0]==0) and
        (currentActorColor[1]==1) and
        (currentActorColor[2]==0)):
        cactor.GetProperty().SetOpacity(0.0)

def displayPickedSphere(self):
    #print("Displaying the green spheres")
    actorCollection = window.ren.GetActors()
    actorCollection.InitTraversal()

    cactor = actorCollection.GetNextActor() # first actor
    while cactor != actorCollection.GetLastActor():
        #print("going through objects")
        currentActorColor = cactor.GetProperty().GetColor()
        if ((currentActorColor[0]==0) and
            (currentActorColor[1]==1) and
            (currentActorColor[2]==0)):
            cactor.GetProperty().SetOpacity(1.0)
            #cactor.GetProperty().SetColor(1,1,0)
        cactor = actorCollection.GetNextActor()
    # Last actor
    currentActorColor = cactor.GetProperty().GetColor()
    if ((currentActorColor[0]==0) and
        (currentActorColor[1]==1) and
        (currentActorColor[2]==0)):
        cactor.GetProperty().SetOpacity(1.0)
        #cactor.GetProperty().SetColor(1,1,0)

def changePickedSphereColor(self, color_name):
    
    print("changing the colour of the spheres")
    if color_name is None:
        color_to_apply = (0.0, 1.0, 0.0)
    if (color_name == 'red'):
        color_to_apply = (1.0, 0.0, 0.0)
    elif (color_name == 'blue'):
        color_to_apply = (0.0, 1.0, 0.0)
    elif (color_name == 'yellow'):
        color_to_apply = (1.0, 1.0, 0.0)
    elif (color_name == 'cyan'):
        color_to_apply = (0.0, 1.0, 1.0)
    elif (color_name == 'magenta'):
        color_to_apply = (1.0, 0.0, 0.0)
    elif (color_name == 'orange'):
        color_to_apply = (1.0, 0.65, 0.0)    
    elif (color_name == 'white'):
        color_to_apply = (1.0, 1.0, 1.0)
    else:
        color_to_apply = (0.0, 1.0, 0.0)
        
    actorCollection = window.ren.GetActors()
    actorCollection.InitTraversal()

    cactor = actorCollection.GetNextActor() # first actor
    while cactor != actorCollection.GetLastActor():
        #print("going through objects")
        currentActorColor = cactor.GetProperty().GetColor()
        if ((currentActorColor[0]==0) and
            (currentActorColor[1]==1) and
            (currentActorColor[2]==0)):
            cactor.GetProperty().SetOpacity(1.0)
            cactor.GetProperty().SetColor(color_to_apply[0],color_to_apply[1],color_to_apply[2])
        cactor = actorCollection.GetNextActor()
    # Last actor
    currentActorColor = cactor.GetProperty().GetColor()
    if ((currentActorColor[0]==0) and
        (currentActorColor[1]==1) and
        (currentActorColor[2]==0)):
        cactor.GetProperty().SetOpacity(1.0)
        cactor.GetProperty().SetColor(color_to_apply[0],color_to_apply[1],color_to_apply[2])
        
def goBack(self):
        print("Should go back to former step")
def prepare_jaw(self, fname):
    print("Loading STL files")
     
    reader = vtk.vtkSTLReader()
    reader.SetFileName(fname)
    
    print("STL file is now loaded")

    self.dummy, self.polydata = prepare_polydata(reader)
    self.full_jaw_polydata = self.polydata
    self.shift=5
    self.reduced_polydata, self.gingiva = cut(self.polydata, self.shift)

def pick_the_teeth_on_jaw(self, ui, tdict):
    
    ui.backFieldButton.hide()
    
    self.clicked_0, self.clicked_1, update_data_dict = get_cusps_gui(self.ren, self.iren, self.reduced_polydata, tdict)
    
    orthonIn3D_updated_data = json.dumps(update_data_dict)
    with open('./patientA.json', 'w') as j_file:
            json.dump(orthonIn3D_updated_data, j_file)
    # Pretty Printing JSON string back
    #print(json.dumps(orthonIn3D_updated_data, indent = 4, sort_keys=True))

    #print(tdict["pickedPoints"]["2"]["Coords"][2])
    
def compute_harmonic_field(self):
    
    hidePickerRedBoundingBox(self)
    
    print("Computing the harmonic field")

    window.radius=0.5
    
    print("clicked_0: " + str(len(window.clicked_0)))
    print("clicked_1: " + str(len(window.clicked_1)))
    
    window.cusps_0 = add_brush(window.reduced_polydata, window.clicked_0, window.radius)
    window.cusps_1 = add_brush(window.reduced_polydata, window.clicked_1, window.radius)
    
    #global field
    window.old_field=[]
    window.field = compute_field(window.cusps_0, window.cusps_1, window.gingiva, window.reduced_polydata, window.old_field)
    
    print('{0:.3f} Mb'.format(window.field.nbytes/10**6))
    
    #global field_polydata
    window.field_polydata = add_field(window.reduced_polydata, window.field, name="Harmonic Field")
    
    #window.ui.computeButton.hide()
    #window.ui.showFieldButton.show()
    window.ui.backFieldButton.show()
    
    hidePickedSphere(self)
    #displayPickedSphere(self)
    #changePickedSphereColor(self, 'orange')
    
    show_harmonic_field(self)
    
def show_harmonic_field(self):
    print("Visualize the harmonic field")
    
    window.add_iso=False
    
    show_field_gui(window.ren, window.field_polydata, window.add_iso)
    
    #window.ui.showFieldButton.hide()
    window.ui.computeButton.hide()
    window.ui.editTeethContourButton.show()

def edit_teeth_contours(self):
    #splines_polydata = select_spline(self, field_polydata)
    window.splines_polydata = select_spline_gui(window.ren, window.iren, window.field_polydata)
    window.ui.editTeethContourButton.hide()
    window.ui.saveFieldButton.show()
    
def save_segmented_items(self):
    save_stl(window.field_polydata, window.splines_polydata,window.clicked_0,window.clicked_1)
    window.ui.saveFieldButton.hide()
    window.ui.quitFieldButton.show()
    
def save_frame():
    global frame_counter
    global window
    # ---------------------------------------------------------------
    # Save current contents of render window to PNG file
    # ---------------------------------------------------------------
    file_name = str(args.output) + str(frame_counter).zfill(5) + ".png"
    image = vtk.vtkWindowToImageFilter()
    image.SetInput(window)
    png_writer = vtk.vtkPNGWriter()
    png_writer.SetInputConnection(image.GetOutputPort())
    png_writer.SetFileName(file_name)
    window.Render()
    png_writer.Write()
    frame_counter += 1
    if args.verbose:
        print(file_name, " has been successfully exported")
    


def print_camera_settings():
    global renderer
    # ---------------------------------------------------------------
    # Print out the current settings of the camera
    # ---------------------------------------------------------------
    camera = renderer.GetActiveCamera()
    print("Camera settings:")
    print("  * position:        %s" % (camera.GetPosition(),))
    print("  * focal point:     %s" % (camera.GetFocalPoint(),))
    print("  * up vector:       %s" % (camera.GetViewUp(),))
    print("  * clipping range:  %s" % (camera.GetViewUp(),))
    


def update_theta(delta):
    print("theta = theta+", delta)
    res[0] = res[0]+delta
    sphere.SetThetaResolution(res[0])
    sphere.Update()



def update_phi(delta):
    print("phi = phi+", delta)
    res[1] = res[1]+delta
    sphere.SetPhiResolution(res[1])
    sphere.Update()
    


def change_color(colorid):
    global window
    print("changing color to ", colorid)
    if colorid==0:
        color=[0.5, 0.5, 0.5]
    elif colorid==1:
        color=[0, 0, 1]
    elif colorid==2:
        color=[0, 1, 1]
    elif colorid==3:
        color=[0, 1, 0]
        # this is a hack to prevent the renderer to switch to stereo mode
        # since the number 3 will trigger a stereo mode switch
        window.StereoRenderOn()
    elif colorid==4:
        color=[1, 1, 0]
    elif colorid==5:
        color=[1, 0.5, 0]
    elif colorid==6:
        color=[1, 0, 0]
    elif colorid==7:
        color=[1, 0, 1]
    else:
        color=[1,1,1]
    sphere_actor.GetProperty().SetColor(color)
    window.Render()
    

    

def key_pressed_callback(obj, event):
    
    # ---------------------------------------------------------------
    # Attach actions to specific keys
    # ---------------------------------------------------------------
    key = obj.GetKeySym()
    print("key=", key)
    if key == "s":
        save_frame()
    elif key == "c":
        #print_camera_settings()
        compute_harmonic_field(self)
    elif key == "v":
        show_harmonic_field(self)
    elif key == "q":
        if verbose:
            print("User requested exit.")
        sys.exit()
    #global window
    #window.ui.Render()
    
    #elif key == "plus":
    #    update_theta(1)
    #elif key == "minus":
    #    update_theta(-1)
    #elif key == "less":
    #    update_phi(-1)
    #elif key == "greater":
    #    update_phi(1)
    #elif not key[0].isalpha():
    #    change_color(int(key[0]))


def quitApplication():
    window.ui.quitFieldButton.clicked.connect(sys.exit(app.exec_()))

def main():
    global renderer
    global interactor
    global window
    
    # name of the executable
    #me = sys.argv[0]
    #nargs = len(sys.argv)
    
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(args.background)
    #make_sphere()
    renderer.ResetCamera()
    
    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(args.size[0], args.size[1])
    
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    
    prepare_jaw(renderer, interactor)
    
    # ---------------------------------------------------------------
    # Add a custom callback function to the interactor
    # ---------------------------------------------------------------
    interactor.AddObserver("KeyPressEvent", key_pressed_callback)
    
    interactor.Initialize()
    window.Render()
    interactor.Start()

if __name__=="__main__":
      #main()
      app = QApplication(sys.argv)
      window = SimpleView()
      window.setWindowTitle('OrthoIn3D')
      window.show()
      window.iren.Initialize() # Need this line to actually show the render inside Qt
      sys.exit(app.exec_())