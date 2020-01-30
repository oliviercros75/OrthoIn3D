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
from PyQt5.QtGui import QIcon, QPixmap

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
import base64 # for converting an image to a string and back to an image again for json purposes
import codecs
from functools import partial

import json

from segmentation.cut import prepare_polydata, cut
from segmentation.field import compute_field, compute_field_gui, add_field, add_field_gui, save_stl, save_stl_nospline, add_brush
from segmentation.viewer import show_field, show_field_gui, get_cusps, get_cusps_gui, select_spline, select_spline_gui
from registration.mesh_registration import set_source_polydata, set_target_polydata, perform_ICP_PointTransform, set_ICP_transform_filter, display_transformed_polydata

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
    
    def makeMaxiSideOne(self):
        self.maxiSideOneBox = QHBoxLayout()
#        self.thevbox.addWidget(self.radio1)
#        self.thevbox.addWidget(self.slider)
        self.maxiSideOneBox.addStretch(1)

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
        
        self.maxiSideOneBox.addWidget(self.tooth18cb)
        self.maxiSideOneBox.addWidget(self.tooth17cb)
        self.maxiSideOneBox.addWidget(self.tooth16cb)
        self.maxiSideOneBox.addWidget(self.tooth15cb)
        self.maxiSideOneBox.addWidget(self.tooth14cb)
        self.maxiSideOneBox.addWidget(self.tooth13cb)
        self.maxiSideOneBox.addWidget(self.tooth12cb)
        self.maxiSideOneBox.addWidget(self.tooth11cb)
        self.maxiSideOneBox.addWidget(self.tooth10cb)
        
        return self.maxiSideOneBox
    
    def makeMaxiSideTwo(self):
        self.maxiSideTwoBox = QHBoxLayout()
#        self.thevbox.addWidget(self.radio1)
#        self.thevbox.addWidget(self.slider)
        self.maxiSideTwoBox.addStretch(1)

        self.tooth28cb = QCheckBox("2à",self)
        self.tooth28cb.stateChanged.connect(self.clickBox)
        self.tooth28cb.move(20,20)
        self.tooth28cb.resize(60,40)
        
        self.tooth27cb = QCheckBox("21",self)
        self.tooth27cb.stateChanged.connect(self.clickBox)
        self.tooth27cb.move(20,40)
        self.tooth27cb.resize(60,40)
        
        self.tooth26cb = QCheckBox("22",self)
        self.tooth26cb.stateChanged.connect(self.clickBox)
        self.tooth26cb.move(20,60)
        self.tooth26cb.resize(60,40)
        
        self.tooth25cb = QCheckBox("23",self)
        self.tooth25cb.stateChanged.connect(self.clickBox)
        self.tooth25cb.move(20,80)
        self.tooth25cb.resize(60,40)
        
        self.tooth24cb = QCheckBox("24",self)
        self.tooth24cb.stateChanged.connect(self.clickBox)
        self.tooth24cb.move(20,80)
        self.tooth24cb.resize(60,40)
        
        self.tooth23cb = QCheckBox("25",self)
        self.tooth23cb.stateChanged.connect(self.clickBox)
        self.tooth23cb.move(20,100)
        self.tooth23cb.resize(60,40)
        
        self.tooth22cb = QCheckBox("26",self)
        self.tooth22cb.stateChanged.connect(self.clickBox)
        self.tooth22cb.move(20,120)
        self.tooth22cb.resize(60,40)
        
        self.tooth21cb = QCheckBox("27",self)
        self.tooth21cb.stateChanged.connect(self.clickBox)
        self.tooth21cb.move(20,140)
        self.tooth21cb.resize(60,40)
        
        self.tooth20cb = QCheckBox("28",self)
        self.tooth20cb.stateChanged.connect(self.clickBox)
        self.tooth20cb.move(20,160)
        self.tooth20cb.resize(60,40)
        
        self.maxiSideTwoBox.addWidget(self.tooth28cb)
        self.maxiSideTwoBox.addWidget(self.tooth27cb)
        self.maxiSideTwoBox.addWidget(self.tooth26cb)
        self.maxiSideTwoBox.addWidget(self.tooth25cb)
        self.maxiSideTwoBox.addWidget(self.tooth24cb)
        self.maxiSideTwoBox.addWidget(self.tooth23cb)
        self.maxiSideTwoBox.addWidget(self.tooth22cb)
        self.maxiSideTwoBox.addWidget(self.tooth21cb)
        self.maxiSideTwoBox.addWidget(self.tooth20cb)
        
        return self.maxiSideTwoBox
        
    def makeMandiSideOne(self):
        self.mandiSideOneBox = QHBoxLayout()
#        self.thevbox.addWidget(self.radio1)
#        self.thevbox.addWidget(self.slider)
        self.mandiSideOneBox.addStretch(1)

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
        
        self.mandiSideOneBox.addWidget(self.tooth38cb)
        self.mandiSideOneBox.addWidget(self.tooth37cb)
        self.mandiSideOneBox.addWidget(self.tooth36cb)
        self.mandiSideOneBox.addWidget(self.tooth35cb)
        self.mandiSideOneBox.addWidget(self.tooth34cb)
        self.mandiSideOneBox.addWidget(self.tooth33cb)
        self.mandiSideOneBox.addWidget(self.tooth32cb)
        self.mandiSideOneBox.addWidget(self.tooth31cb)
        self.mandiSideOneBox.addWidget(self.tooth30cb)
        
        return self.mandiSideOneBox

    def makeMandiSideTwo(self):
        self.mandiSideTwoBox = QHBoxLayout()
#        self.thevbox.addWidget(self.radio1)
#        self.thevbox.addWidget(self.slider)
        self.mandiSideTwoBox.addStretch(1)

        self.tooth48cb = QCheckBox("40",self)
        self.tooth48cb.stateChanged.connect(self.clickBox)
        self.tooth48cb.move(20,20)
        self.tooth48cb.resize(60,40)
        
        self.tooth47cb = QCheckBox("41",self)
        self.tooth47cb.stateChanged.connect(self.clickBox)
        self.tooth47cb.move(20,40)
        self.tooth47cb.resize(60,40)
        
        self.tooth46cb = QCheckBox("42",self)
        self.tooth46cb.stateChanged.connect(self.clickBox)
        self.tooth46cb.move(20,60)
        self.tooth46cb.resize(60,40)
        
        self.tooth45cb = QCheckBox("43",self)
        self.tooth45cb.stateChanged.connect(self.clickBox)
        self.tooth45cb.move(20,80)
        self.tooth45cb.resize(60,40)
        
        self.tooth44cb = QCheckBox("44",self)
        self.tooth44cb.stateChanged.connect(self.clickBox)
        self.tooth44cb.move(20,80)
        self.tooth44cb.resize(60,40)
        
        self.tooth43cb = QCheckBox("45",self)
        self.tooth43cb.stateChanged.connect(self.clickBox)
        self.tooth43cb.move(20,100)
        self.tooth43cb.resize(60,40)
        
        self.tooth42cb = QCheckBox("46",self)
        self.tooth42cb.stateChanged.connect(self.clickBox)
        self.tooth42cb.move(20,120)
        self.tooth42cb.resize(60,40)
        
        self.tooth41cb = QCheckBox("47",self)
        self.tooth41cb.stateChanged.connect(self.clickBox)
        self.tooth41cb.move(20,140)
        self.tooth41cb.resize(60,40)
        
        self.tooth40cb = QCheckBox("48",self)
        self.tooth40cb.stateChanged.connect(self.clickBox)
        self.tooth40cb.move(20,160)
        self.tooth40cb.resize(60,40)
        
        self.mandiSideTwoBox.addWidget(self.tooth48cb)
        self.mandiSideTwoBox.addWidget(self.tooth47cb)
        self.mandiSideTwoBox.addWidget(self.tooth46cb)
        self.mandiSideTwoBox.addWidget(self.tooth45cb)
        self.mandiSideTwoBox.addWidget(self.tooth44cb)
        self.mandiSideTwoBox.addWidget(self.tooth43cb)
        self.mandiSideTwoBox.addWidget(self.tooth42cb)
        self.mandiSideTwoBox.addWidget(self.tooth41cb)
        self.mandiSideTwoBox.addWidget(self.tooth40cb)
        
        return self.mandiSideTwoBox
    
    
    def clickBox(self, state):

        if state == QtCore.Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')
        
class PatientWindow(QWidget):
    def __init__(self):
        #super().__init__()
        QWidget.__init__(self)
        self.setWindowTitle("Patient Information")
        self.resize(200, 100)
        
        self.grid = QGridLayout()
        
        name = ""
        age = int()
        mobilenum = ""
        address = ""
        
        self.addcontactBut = QPushButton("New Patient")
        self.addcontactBut.setGeometry(QtCore.QRect(190, 100, 101, 23))
        self.addcontactBut.setObjectName("addcontact")
        self.addcontactBut.clicked.connect(self.addContact)

        self.nameLe = QLineEdit("Name")
        self.nameLe.setGeometry(QtCore.QRect(10, 60, 171, 20))
        self.nameLe.setAutoFillBackground(False)
        self.nameLe.setObjectName("name")

        self.ageLe = QLineEdit("Age")
        self.ageLe.setGeometry(QtCore.QRect(190, 60, 41, 20))
        self.ageLe.setObjectName("age")
        self.ageLe.setText("")

        self.mobphoLe = QLineEdit("Mobile Phone Nb:")
        self.mobphoLe.setGeometry(QtCore.QRect(240, 60, 113, 20))
        self.mobphoLe.setObjectName("mobilephone")

        self.adrLe = QLineEdit("Physical Address:")
        self.adrLe.setGeometry(QtCore.QRect(360, 60, 113, 20))
        self.adrLe.setObjectName("address")

        self.label = QLabel("")
        self.label.setGeometry(QtCore.QRect(90, 40, 31, 20))
        self.label.setObjectName("label")

        self.label_2 = QLabel("")
        self.label_2.setGeometry(QtCore.QRect(200, 40, 21, 20))
        self.label_2.setObjectName("label_2")

        self.label_3 = QLabel("")
        self.label_3.setGeometry(QtCore.QRect(260, 40, 81, 20))
        self.label_3.setObjectName("label_3")

        self.label_4 = QLabel("")
        self.label_4.setGeometry(QtCore.QRect(370, 40, 101, 20))
        self.label_4.setObjectName("label_4")
        
        self.layout = QFormLayout()
        self.layout.addRow('Name:', QLineEdit())
        self.layout.addRow('Age:', QLineEdit())
        self.layout.addRow('Job:', QLineEdit())
        self.layout.addRow('Hobbies:', QLineEdit())

        
        #self.central = QWidget(self)
        #self.im = QPixmap("./me.jpg")
        #self.label = QLabel()
        #self.label.setPixmap(self.im)

        #self.grid = QGridLayout()
        #self.grid.addWidget(self.label,1,1)
        #self.setLayout(self.grid)

        ##self.setGeometry(50,50,320,200)
        
        #self.vlayout = QVBoxLayout()        # Window layout
        #self.displays = QHBoxLayout()
        #self.disp = ImageWidget(self)    
        #self.displays.addWidget(self.disp)
        #self.vlayout.addLayout(self.displays)
        #self.label = QLabel(self)
        #self.vlayout.addWidget(self.label)
        
        #self.central.setLayout(self.vlayout)
        #self.show()
        ##self.setCentralWidget(self.central)
        
        self.setLayout(self.layout)
        
    def addContact(self):
        self.name = str(self.nameLe.text())
        self.age = str(self.ageLe.text())
        print(self.name)
        
# Image widget

class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.image = None
 
    def setImage(self, image):
        self.image = image
        self.setMinimumSize(image.size())
        self.update()
 
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()
        

class PatientInfo:
    def __init__(self, id, firstname, lastname, age, address, country, phone, nssn, treated_jaw, tstr="12", practician_lastname=None, practician_firstname=None, practician_location=None, practician_phone_number=None, practician_email=None, comments=None):
        self.id = id
        self.firstName = firstname
        self.lastName = lastname
        self.age = age
        self.home_address = address
        self.country = country
        self.phone = phone
        self.nssn = nssn # social security number
        self.treatedJaw = treated_jaw
        self.picture_str = tstr
        self.practicianLastName = practician_lastname
        self.practicianFirstName = practician_firstname
        self.practicianLocation = practician_location
        self.practicianPhoneNumber = practician_phone_number
        self.practicianEmail = practician_email
        self.comments = comments
        self.jisonStruct = {}
    
    def setPatientID(self, pid):
        self.id = pid
        
    def getPatientID(self):
        return self.id
    
    def setfFirstName(self, pfirstname):
        self.firstName = pfirstname
        
    def getFirstName(self):
        return self.firstName
    
    def setLastName(self, plastname):
        self.firstName = plastname
        
    def getLastName(self):
        return self.lastName
    
    def setAge(self, page):
        self.age = page
        
    def getAge(self):
        return self.age
    
    def setHomeAddress(self, phome_address):
        self.home_address = phome_address
        
    def getHomeAddress(self):
        return self.home_address
    
    def setCountry(self, pcountry):
        self.country = pcountry
        
    def getCountry(self):
        return self.country
    
    def setPhoneNumber(self, pphone_number):
        self.phone = pphone_number
        
    def getPhoneNumber(self):
        return self.phone
    
    def setNSSN(self, pnssn):
        self.nssn = nssn
        
    def getNSSN(self):
        return self.nssn

    def setPatientPictureStr(self, pict_str):
        self.picture_str = pict_str
    def getPatientPictureStr(self):
        return self.picture_str
    def setTreatedJaw(self, jaw):
        self.treatedJaw = pTreatedJaw
        
    def getTreatedJaw(self):
        return self.treatedJaw
    
    def setPracticianLastName(self, practicLastName):
        self.practicianLastName = practicLastName
        
    def getPracticianLastName(self):
        return self.practicianLastName
    
    def setPracticianFirstName(self, practicFirstName):
        self.practicianFirstName = practicFirstName
        
    def getPracticianFirstName(self):
        return self.practicianFirstName
    
    def setPracticianLocation(self, practicLocation):
        self.practicianLocation = ppractician_location
        
    def getPracticianLocation(self):
        return self.practicianLocation
    
    def setPracticianPhoneNumber(self, pphone_number):
        self.practicianPhoneNumber = pphone_number
        
    def getPracticianPhoneNumber(self):
        return self.practicianPhoneNumber
    
    def setPracticianEmail(self, ppractician_email):
        self.practicianEmail = ppractician_email
        
    def getPracticianEmail(self):
        return self.practicianEmail
    
    def buildJsonDataStruct(self):
        self.jisonStruct = {
            "ID" : self.id,
            "FirstName" : self.firstName,
            "LastName" : self.lastName,
            "Age" : self.age,
            "Address" : self.home_address,
            "Country" : self.country,
            "PhoneNumber" : self.phone,
            "SocialSecurityNumber" : self.nssn,
            "TreatedJaw" : self.treatedJaw,
            "Comments" : "",
        }
        return self.jisonStruct
    
    def anonymizePatientInfoJsonDS(self):
        self.jisonStruct["firstName"] = "John"
        self.jisonStruct["lastName"] = "Doe"
        self.jisonStruct["Age"] = "XX"
        self.jisonStruct["Address"] = " "
        self.jisonStruct["Country"] = " "
        self.jisonStruct["Phone"] = " "
        self.jisonStruct["SocialSecurityNumber"]= "XXXXXXXXXXXXXXX"
        self.jisonStruct[" "]
        return self.jisonStruct
    
    def anonymizePractionerInfoJsonDS(self):
        self.jisonStruct["practicianFirstName"]=""
        self.jisonStruct["practicianLastName"]=""
        self.jisonStruct["practicianLocation"]=""
        self.jisonStruct["practicianPhoneNumber"]=""
        self.jisonStruct["practicianEmail"]=""
        return self.jisonStruct
    

    
    
    
# The next two functions will convert an image to a string and back to an image
# in order to include the picture of the patient in the json file:

class JzonData:
    def __init__(self, numberOfSteps, mandi, maxi, missingTeethMandi, missingTeethMaxi, inclusionSphereDiamMandi, inclusionSphereDiamMaxi, pickedPoints):
        self.mandi = mandi
        self.maxi = maxi
        self.missingTeethMandi = missingTeethMandi
        self.missingTeethMaxi = missingTeethMaxi
        self.inclusionSphereDiamMandi = inclusionSphereDiamMandi
        self.inclusionSphereDiamMaxi = inclusionSphereDiamMaxi
        self.pickedPoints = pickedPoints
        self.main_dict = {}
        self.jisonStruct = {}
        self.numberOfSteps = numberOfSteps
    def setMandi(self, mandi):
        self.mandi = mandi
    def getMandi(self):
        return self.mandi
    def setMaxi(self, maxi):
        self.maxi = maxi
    def getMaxi(self):
        return self.maxi
    def setMissingTeethMandi(self, missingTeethMandi):
        self.missingTeethMandi = missingTeethMandi
    def getMissingTeethMandi(self):
        return self.missingTeethMandi
    def setMissingTeethMaxi(self, missingTeethMaxi):
        self.missingTeethMaxi = missingTeethMaxi
    def getMissingTeethMaxi(self):
        return self.missingTeethMaxi
    def setInclusionSphereDiamMandi(self, inclusionSphereDiamMandi):
        self.inclusionSphereDiamMandi = inclusionSphereDiamMandi
    def getInclusionSphereDiamMandi(self):
        return self.inclusionSphereDiamMandi
    def setInclusionSphereDiamMaxi(self, inclusionSphereDiamMaxi):
        self.inclusionSphereDiamMaxi = inclusionSphereDiamMaxi
    def getInclusionSphereDiamMaxi(self):
        return self.inclusionSphereDiamMaxi
    def setPickedPoints(self, pickedPoints):
        self.pickedPoints = pickedPoints
    def getPickedPoints(self):
        return self.pickedPoints
    def setNumberOfSteps(self, nb_steps):
        self.numberOfSteps = nb_steps
    def getNumberOfSteps(self):
        return self.numberOfSteps
    def setNewKeywordData(self, keyStr):
        self.newKeyData = keyStr
    def getKeywordData(self):
        return self.newKeyData
    def setNewDictData(self, dictData):
        self.newDictData = dictData
    def getNewDictData(self):
        return self.newDictData
    def appendKeyAndDictToMainStruct(self, newKeywordData, dictDataForNewKey):
        self.jisonStruct[newKeywordData]=dictDataForNewKey
        #return self.main_dict
    def clearPickedPoints(self):
        self.jisonStruct["pickedPoints"]={}
    def buildJsonDataStruct(self):
        self.jisonStruct = {
            "NumberOfSteps" : self.numberOfSteps,
            "Mandi" : self.mandi,
            "Maxi" : self.maxi,
            "MissingTeethMandi" : self.missingTeethMandi,
            "MissingTeethMaxi" : self.missingTeethMaxi,
            "InclusionSphereDiamMandi" : self.inclusionSphereDiamMandi,
            "InclusionSphereDiamMaxi" : self.inclusionSphereDiamMaxi,
            "pickedPoints" : self.pickedPoints,
        }
        return self.jisonStruct


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        #self.setWindowTitle("Hello World")
        #MainWindow.setGeometry(100, 100, 400, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget") 
                
        #self.filename=""
        #global filename
        self.act = QAction("Open STL File")
        self.act.triggered.connect(self.openStlFile)
        
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
        
        MainWindow.statusBar().showMessage('Status bar')
        
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
        
        self.xOffset = 0
        self.yOffset = 0
        
        # Definition of the Compute Harmonic button
        self.xOffset = +300
        self.yOffset = -25
        self.computeButton = QPushButton("Compute Harmonic Field")
        self.gridlayout.addWidget(self.computeButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.computeButton.clicked.connect(compute_harmonic_field)
        self.computeButton.show()
        self.xOffset = 0
        self.yOffset = 0
        
        # Definition of the Edit Teeth Contour button
        self.xOffset = +300
        self.yOffset = -25
        self.editTeethContourButton = QPushButton("Edit Teeth Contour")
        self.gridlayout.addWidget(self.editTeethContourButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.editTeethContourButton.clicked.connect(edit_teeth_contours)
        self.editTeethContourButton.clicked.connect(save_segmented_items)
        self.editTeethContourButton.hide()
        self.xOffset = 0
        self.yOffset = 0
        
        # Definition of the Save Segmentation button
        self.xOffset = +300
        self.yOffset = -25
        self.saveFieldButton = QPushButton("Save segmentation")
        self.gridlayout.addWidget(self.saveFieldButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.saveFieldButton.clicked.connect(save_segmented_items)
        self.saveFieldButton.hide()
        self.xOffset = 0
        self.yOffset = 0
        
        
        # Definition of the Quit button
        self.xOffset = +300
        self.yOffset = -25
        self.quitFieldButton = QPushButton("Quit")
        self.gridlayout.addWidget(self.quitFieldButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.quitFieldButton.clicked.connect(quitApplication)
        self.quitFieldButton.hide()
        self.xOffset = 0
        self.yOffset = 0
        
        # Definition of the Settings button
        self.yOffset = -280
        self.xOffset = +150
        self.settingsFieldButton = QPushButton("Settings")
        self.gridlayout.addWidget(self.settingsFieldButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.settingsFieldButton.clicked.connect(self.toggleSettingsWindow)
        self.yOffset = 0
        self.xOffset = 0
        
        # Definition of the PatientInfo button
        self.yOffset = -280
        self.xOffset = +160
        self.patientInfoButton = QPushButton("Patient Info")
        self.gridlayout.addWidget(self.patientInfoButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.patientInfoButton.clicked.connect(self.togglePatientInfoWindow)
        self.yOffset = 0
        self.xOffset = 0
        
        # Definition of the Back button
        self.yOffset = +280
        self.xOffset = +160
        self.backFieldButton = QPushButton("Back")
        self.gridlayout.addWidget(self.backFieldButton, self.buttpnPosX+self.xOffset,self.buttpnPosY+self.yOffset,1,1)
        self.backFieldButton.clicked.connect(goBack)
        self.backFieldButton.hide()
        self.yOffset = 0
        self.xOffset = 0
        
        MainWindow.setCentralWidget(self.centralwidget)
        
    def toggleSettingsWindow(self):
        self.SW = SettingsWindow()
        self.SW.show()
        
    def togglePatientInfoWindow(self):
        self.PW = PatientWindow()
        self.PW.show()
        
    def do_something(self):
        print("Clicked")
        
    def openStlFile(self):
        fname = QFileDialog.getOpenFileName(self.centralwidget, 'Choose STL file', os.sep.join((os.path.expanduser('~'), 'Documents')),
                                                 'STL file (*.stl)')
        #self.filname = str(fname[0])
        #SimpleView.updateFlag(True)
        #SimpleView.updateFname(self.filname)
        
        SimpleView.prepare_jaw(str(fname[0]))
        
        
    def show_status(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()
        print(state)

class SimpleView(QMainWindow):
    def __init__(self, flag=False, fname=None, reduced_polydata=None, gingiva=None, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.reduced_polydata = reduced_polydata
        self.gingiva = gingiva
        self.flag = flag
        self.fname = fname
        
        global currentPatient
        currentPatient = PatientInfo("ID0001", "Pierre", "Dupont", "34", " ", "France", " ", "1751075114168", "mandibular", None, None, None, None, None, None, "test person")
        currentPatient.buildJsonDataStruct()
       
        global data_dict
        data_dict = JzonData(4, True, False, [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], [8,8,7,7,6,5,3,2,2,3,5,6,7,7,8,8], [8,8,7,7,6,5,3,2,2,3,5,6,7,7,8,8], {})
        data_dict.buildJsonDataStruct()
        
        print("Loading STL files")
        print(fname)
        #fname = '/Users/ocros/Documents/OrthoIn3D/OrthoIn3D/OrthoIn3D/data/data_input/6000_2017-02-03_13-14_Mandibular_export.stl'
        fname = QFileDialog.getOpenFileName(self, 'Choose STL file', os.sep.join((os.path.expanduser('~'), 'Documents')),
                                                 'STL file (*.stl)')
        reader = vtk.vtkSTLReader()
        reader.SetFileName(str(fname[0]))
    
        print("STL file is now loaded")

        self.dummy, self.polydata = prepare_polydata(reader)
        self.full_jaw_polydata = self.polydata
        self.shift=10
        self.reduced_polydata, self.gingiva = cut(self.polydata, self.shift)
        
        self.pd_mapper = vtk.vtkPolyDataMapper()
        self.pd_mapper.SetInputConnection(self.reduced_polydata.GetOutputPort())
        self.pd_mapper.ScalarVisibilityOff()
  
        self.pd_actor = vtk.vtkActor()
        self.pd_actor.SetMapper(self.pd_mapper)
        self.pd_actor.GetProperty().SetColor(1.0,1.0,1.0)
        
        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        
        # Create a mapper
        self.mapper = vtk.vtkPolyDataMapper()
        ##if (self.reduced_polydata is not None):
            
        # Create an actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.ren.AddActor(self.pd_actor)
        
        data_dict=pick_the_teeth_on_jaw(self, data_dict)
        
        self.iren.AddObserver("KeyPressEvent", key_pressed_callback)
    
    
    def updateJaw(newpd):
        window.ren.RemoveActor(window.pd_actor);
        window.pd_mapper2 = vtk.vtkPolyDataMapper()
        window.pd_mapper2.SetInputConnection(newpd.GetOutputPort())
        window.pd_mapper2.ScalarVisibilityOff()
  
        window.pd_actor2 = vtk.vtkActor()
        window.pd_actor2.SetMapper(window.pd_mapper2)
        window.pd_actor2.GetProperty().SetColor(1.0,1.0,1.0)
        
        window.ren.AddActor(window.pd_actor2)
        window.show()
        window.iren.Initialize()
        
    def prepare_jaw(fname):
        print("Loading STL files")
    
        reader = vtk.vtkSTLReader()
        reader.SetFileName(fname)
    
        print("STL file is now loaded")

        dummy, polydata = prepare_polydata(reader)
        full_jaw_polydata = polydata
        SimpleView.shift=0
        #reduced_polydata, gingiva = cut(polydata, SimpleView.shift)
        reduced_polydata = polydata
        SimpleView.updateJaw(reduced_polydata)
        
        #return self.reduced_polydata, self.gingiva    

def convertImageToString(fname):
    with open(fname, mode='rb') as file:
        img = file.read()

    tststr = base64.b64encode(img)
    return tststr

def convertStringToImage(tstr, image_fname):
    fh = open("imageToSave.png", "wb")
    #fh.write(the_string.decode('base64'))
    fh.write(base64.b64decode(tstr))
    fh.close()




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
        print(boundsPickedSpheres)
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

def compareTwoFloats(self, target_val, ref_val, delta=0.000001):
    if  abs(target_val - ref_val) < delta:
        return True
    else:
        return False
    
    
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
        
#def pick_the_teeth_on_jaw(self, ui, tdict):
def pick_the_teeth_on_jaw(self, tdict):
    
    #ui.backFieldButton.hide()
    
    self.clicked_0, self.clicked_1, update_data_dict = get_cusps_gui(self.ren, self.iren, self.reduced_polydata, tdict)
    
    #orthonIn3D_updated_data = json.dumps(update_data_dict)
    #with open('./patientA.json', 'w') as j_file:
    #        json.dump(orthonIn3D_updated_data, j_file)
    ## Pretty Printing JSON string back
    #print(json.dumps(orthonIn3D_updated_data, indent = 4, #sort_keys=True))

    #print(update_data_dict)
    return update_data_dict
    
def compute_harmonic_field(self):
    
    hidePickerRedBoundingBox(self)
    
    #txt1.SetInput("")
    #txt2.SetInput("")
    #txt3.SetInput("")
    #txt4.SetInput("")
    #txt5.SetInput("")
    
    print("Computing the harmonic field")
    
    data_dict.appendKeyAndDictToMainStruct("field", {})
    data_dict.appendKeyAndDictToMainStruct("polydata_field", {})
    window.radius=0.05
    
    print("clicked_0: " + str(len(window.clicked_0)))
    print("clicked_1: " + str(len(window.clicked_1)))
    
    window.cusps_0 = add_brush(window.reduced_polydata, window.clicked_0, window.radius)
    window.cusps_1 = add_brush(window.reduced_polydata, window.clicked_1, window.radius)
    
    #global field
    window.old_field=[]
    window.field = compute_field_gui(window.cusps_0, window.cusps_1, window.gingiva, window.reduced_polydata, data_dict, window.old_field)
    
    print('{0:.3f} Mb'.format(window.field.nbytes/10**6))
    
    #global field_polydata
    data_dict.jisonStruct["field"]=window.field
    print("Length of window.field:" + str(len(window.field)))
    window.field_polydata = add_field_gui(window.reduced_polydata, window.field, name="Harmonic Field")
    for (key, value) in data_dict.jisonStruct.items() :
                print(key , " :: ", value )
    data_dict.jisonStruct["polydata_field"]=window.field_polydata
    
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
    #save_stl(window.field_polydata, window.splines_polydata,window.clicked_0,window.clicked_1)
    save_stl_nospline(window.field_polydata,window.splines_polydata, window.clicked_0,window.clicked_1)
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

    

#def mainB():
#    global renderer
#    global interactor
#    global window
#    
#    # name of the executable
#    #me = sys.argv[0]
#    #nargs = len(sys.argv)
#    
#    renderer = vtk.vtkRenderer()
#    renderer.SetBackground(args.background)
#    #make_sphere()
#    renderer.ResetCamera()
#    
#    window = vtk.vtkRenderWindow()
#    window.AddRenderer(renderer)
#    window.SetSize(args.size[0], args.size[1])
#    
#    interactor = vtk.vtkRenderWindowInteractor()
#    interactor.SetRenderWindow(window)
#    
#    #prepare_jaw(renderer, interactor)
#    
#    # ---------------------------------------------------------------
#    # Add a custom callback function to the interactor
#    # ---------------------------------------------------------------
#    interactor.AddObserver("KeyPressEvent", key_pressed_callback)
#    
#    interactor.Initialize()
#    window.Render()
#    interactor.Start()

if __name__=="__main__":
      #main()
      app = QApplication(sys.argv)
      window = SimpleView()
      window.setWindowTitle('OrthoIn3D')
      window.show()
      window.iren.Initialize() # Need this line to actually show the render inside Qt
      sys.exit(app.exec_())