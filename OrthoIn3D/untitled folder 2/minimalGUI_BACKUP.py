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
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
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
        self.another_menu = self.file_menu.addMenu("Parent Menu")
        self.submenu = QAction("Submenu1")
        self.another_menu.addAction(self.submenu)
        self.another_menu.addAction(QAction("Submenu 2"))
        self.another_menu.addAction(QAction("Submenu 3"))
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
        
        self.computeButton = QPushButton("Compute Harmonic Field")
        self.gridlayout.addWidget(self.computeButton, 96,48,1,1)
        self.computeButton.clicked.connect(compute_harmonic_field)
        self.computeButton.show()
        
        self.showFieldButton = QPushButton("Show Results")
        self.gridlayout.addWidget(self.showFieldButton, 96,48,1,1)
        self.showFieldButton.clicked.connect(show_harmonic_field)
        self.showFieldButton.hide()
        
        self.editTeethContourButton = QPushButton("Edit Teeth Contour")
        self.gridlayout.addWidget(self.editTeethContourButton, 96,48,1,1)
        self.editTeethContourButton.clicked.connect(edit_teeth_contours)
        self.editTeethContourButton.hide()
        
        self.saveFieldButton = QPushButton("Save segmentation")
        self.gridlayout.addWidget(self.saveFieldButton, 96,48,1,1)
        self.saveFieldButton.clicked.connect(save_segmented_items)
        self.saveFieldButton.hide()
        
        self.quitFieldButton = QPushButton("Quit")
        self.gridlayout.addWidget(self.quitFieldButton, 96,48,1,1)
        self.quitFieldButton.clicked.connect(quitApplication)
        self.quitFieldButton.hide()        
        
        MainWindow.setCentralWidget(self.centralwidget)
        
    def do_something(self):
        print("Clicked")
        
    def openStlFile(self):
        
        fname = QFileDialog.getOpenFileName(self.centralwidget, 'Choose STL file', os.sep.join((os.path.expanduser('~'), 'Documents')),
                                                 'STL file (*.stl)')
        self.filename = fname[0]
        
        
        
    def show_status(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()
        print(state)
        

#class Ui_MainWindowTwo(object):
#    def setupUi(self, MainWindow):
#        MainWindow.setObjectName("MainWindow")
#        MainWindow.resize(800, 600)
#        
#        self.centralWidget = QWidget(MainWindow)
#        self.gridlayout = QGridLayout(self.centralWidget)
#        
#
#        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
#        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 100, 100)
#        
#        self.computeButton = QPushButton("Compute Harmonic Field")
#        self.gridlayout.addWidget(self.computeButton, 96,48,1,1)
#        self.computeButton.clicked.connect(compute_harmonic_field)
#        self.computeButton.show()
#        
#        self.showFieldButton = QPushButton("Show Results")
#        self.gridlayout.addWidget(self.showFieldButton, 96,48,1,1)
#        self.showFieldButton.clicked.connect(show_harmonic_field)
#        self.showFieldButton.hide()
#        
#        self.editTeethContourButton = QPushButton("Edit Teeth Contour")
#        self.gridlayout.addWidget(self.editTeethContourButton, 96,48,1,1)
#        self.editTeethContourButton.clicked.connect(edit_teeth_contours)
#        self.editTeethContourButton.hide()
#        
#        self.saveFieldButton = QPushButton("Save segmentation")
#        self.gridlayout.addWidget(self.saveFieldButton, 96,48,1,1)
#        self.saveFieldButton.clicked.connect(save_segmented_items)
#        self.saveFieldButton.hide()
#        
#        self.quitFieldButton = QPushButton("Quit")
#        self.gridlayout.addWidget(self.quitFieldButton, 96,48,1,1)
#        self.quitFieldButton.clicked.connect(quitApplication)
#        self.quitFieldButton.hide()
#        
##       self.buttonRight = QPushButton("Right")
##       self.gridlayout.addWidget(self.buttonRight, 96,52,1,1)
##       self.buttonUp= QPushButton("Up")
##       self.gridlayout.addWidget(self.buttonUp, 94,50,1,1)
##       self.buttonDown = QPushButton("Down")
##       self.gridlayout.addWidget(self.buttonDown, 98,50,1,1)
##       self.buttonFire = QPushButton("Fire Torpedo")
##       self.gridlayout.addWidget(self.buttonFire, 95,50,3,1)
#        
##        MainWindow.setCentralWidget(self.centralWidget)
#    
##        self.layout= QHBoxLayout()
##        self.menubar= QMenuBar()
##        self.file=self.menubar.addMenu("File")
##        self.file.addAction("New File")
##        self.save=QAction("Save")
##        self.save.setShortcut("Ctrl+S")
##        
##        self.edit=self.file.addMenu("Edit")
##        self.edit.addAction("copy")
##        self.edit.addAction("paste")
##        self.quit=QAction("Quit")
##        
##        self.setLayout(self.layout)
#
#        
#    
#    def processtrigger(self,qaction):
#        print(qaction.text()+" is triggered!")


class SimpleView(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        print("Filename is: " + self.ui.filename)
                
        #self.ren = vtk.vtkRenderer()
        #self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        #self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        
        #self.ui.vtkWidget = QVTKRenderWindowInteractor(self.ui.frame)
        #self.ui.vl = QVBoxLayout() #I think the mistake might be here..
        #self.ui.vl.addWidget(self.ui.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        
        #make_sphere(self)
        
        if(self.ui.filename != ""):
            #self.ui.filename = './STL/6000_2017-02-03_13-14_Mandibular_export.stl'
            #self.ui.filename = '/Users/ocros/Documents/STL non segmentés/9056_2015-05-20_13-36_Mandibular_export.stl'
        
            prepare_jaw(self, self.ui.filename)
        else:
            self.ui.filename = '/Users/ocros/Documents/OrthoIn3D/OrthoIn3D/OrthoIn3D/data/data_input/6000_2017-02-03_13-14_Mandibular_export.stl'
            prepare_jaw(self, self.ui.filename)
        print("Filename is: " + self.ui.filename)
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

# initial sphere creation with user selected values
#def make_sphere(self):
#    global renderer
#    # ---------------------------------------------------------------
#    # The following code is identical to render_demo.py...
#    # ---------------------------------------------------------------
#    # create a sphere
#    sphere.SetRadius(1.0)
#    sphere.SetCenter(0.0, 0.0, 0.0)
#    sphere.SetThetaResolution(args.resolution[0])
#    sphere.SetPhiResolution(args.resolution[1])
#    # extract the edges
#    edge_extractor = vtk.vtkExtractEdges()
#    edge_extractor.SetInputConnection(sphere.GetOutputPort())
#    # map sphere and edges separately
#    sphere_mapper = vtk.vtkPolyDataMapper()
#    sphere_mapper.SetInputConnection(sphere.GetOutputPort())
#    edge_mapper = vtk.vtkPolyDataMapper()
#    edge_mapper.SetInputConnection(edge_extractor.GetOutputPort())
#    # define different rendering styles for sphere and edges
#    sphere_actor.SetMapper(sphere_mapper)
#    sphere_actor.GetProperty().SetColor(args.color)
#    edge_actor = vtk.vtkActor()
#    edge_actor.SetMapper(edge_mapper)
#    edge_actor.GetProperty().SetColor(0.5, 0.5, 0)
#    edge_actor.GetProperty().SetLineWidth(3)
#    # add resulting primitives to renderer
#    self.ren.AddActor(sphere_actor)
#    self.ren.AddActor(edge_actor)
    

def prepare_jaw(self, fname):
    print("Loading STL files")
    
    
    reader = vtk.vtkSTLReader()
    reader.SetFileName(fname)
    
    print("STL file is now loaded")

    self.dummy, self.polydata = prepare_polydata(reader)
    self.full_jaw_polydata = self.polydata
    #global reduced_polydata
    #global gingiva 
    self.shift=5
    self.reduced_polydata, self.gingiva = cut(self.polydata, self.shift)

    #clicked_0,clicked_1 = get_cusps(self, cutted_polydata)
    #global clicked_0
    #global clicked_1
    self.clicked_0, self.clicked_1 = get_cusps_gui(self.ren, self.iren, self.reduced_polydata)

#def prepare_jaw_gui(ren, inter):
#    print("Loading STL files")
#    #filename = './STL/6000_2017-02-03_13-14_Mandibular_export.stl'
#    filename = '/Users/ocros/Downloads/copie-CROS de STL non segmentés/STL non segmentés/9056_2015-05-20_13-36_Mandibular_export.stl'
#    
#    reader = vtk.vtkSTLReader()
#    reader.SetFileName(filename)
#    
#    print("STL file is now loaded")
#
#    dummy, polydata = prepare_polydata(reader)
#    full_jaw_polydata = polydata
#    global reduced_polydata
#    global gingiva 
#    reduced_polydata, gingiva = cut(polydata, shift=5)
#
#    #clicked_0,clicked_1 = get_cusps(self, cutted_polydata)
#    global clicked_0
#    global clicked_1
#    clicked_0, clicked_1 = get_cusps_gui(ren, inter, reduced_polydata)    
    
def compute_harmonic_field(self):

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
    
    window.ui.computeButton.hide()
    window.ui.showFieldButton.show()
    
    
def show_harmonic_field(self):
    print("Visualize the harmonic field")
    
    window.add_iso=False
    
    show_field_gui(window.ren, window.field_polydata, window.add_iso)
    
    window.ui.showFieldButton.hide()
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