from PyQt5.QtWidgets import *
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys

class Ui_MainWindow(object):
   def setupUi(self, MainWindow):
       MainWindow.setObjectName("MainWindow")
       MainWindow.resize(603, 553)
       self.centralWidget = QWidget(MainWindow)
       self.gridlayout = QGridLayout(self.centralWidget)
       self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
       self.gridlayout.addWidget(self.vtkWidget, 0, 0, 100, 100)
       self.buttonLeft = QPushButton("Left")
       self.gridlayout.addWidget(self.buttonLeft, 96,48,1,1)
       self.buttonRight = QPushButton("Right")
       self.gridlayout.addWidget(self.buttonRight, 96,52,1,1)
       self.buttonUp= QPushButton("Up")
       self.gridlayout.addWidget(self.buttonUp, 94,50,1,1)
       self.buttonDown = QPushButton("Down")
       self.gridlayout.addWidget(self.buttonDown, 98,50,1,1)
       self.buttonFire = QPushButton("Fire Torpedo")
       self.gridlayout.addWidget(self.buttonFire, 95,50,3,1)
       MainWindow.setCentralWidget(self.centralWidget)


class SimpleView(QMainWindow):

   def __init__(self, parent = None):
       QMainWindow.__init__(self, parent)
       self.ui = Ui_MainWindow()
       self.ui.setupUi(self)
       self.ren = vtk.vtkRenderer()
       self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
       self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

       # Create source
       source = vtk.vtkSphereSource()
       source.SetCenter(0, 0, 0)
       source.SetRadius(5.0)

       # Create a mapper
       mapper = vtk.vtkPolyDataMapper()
       mapper.SetInputConnection(source.GetOutputPort())

       # Create an actor
       actor = vtk.vtkActor()
       actor.SetMapper(mapper)

       self.ren.AddActor(actor)

if __name__ == "__main__":

   app = QApplication(sys.argv)
   window = SimpleView()
   window.show()
   window.iren.Initialize() # Need this line to actually show the render inside Qt
   sys.exit(app.exec_())