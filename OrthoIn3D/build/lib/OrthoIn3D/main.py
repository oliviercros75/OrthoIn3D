# -*- coding: utf-8 -*-
'''
Created on 2 déc. 2018

@author: Théo Moutakanni
'''
from PyQt5.QtWidgets import *
import vtk
import os

from segmentation.cut import prepare_polydata, cut
from segmentation.field import compute_field, add_field, save_stl, add_brush
from segmentation.viewer import show_field, get_cusps, select_spline
from registration.mesh_registration import set_source_polydata, set_target_polydata, perform_ICP_PointTransform, set_ICP_transform_filter, display_transformed_polydata

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys

class Ui_MainWindow(object):
   def setupUi(self, MainWindow):
       MainWindow.setObjectName("MainWindow")
       MainWindow.resize(603, 553)
       self.centralWidget = QWidget(MainWindow)
       self.gridlayout = QGridLayout(self.centralWidget)
       self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
       self.gridlayout.addWidget(self.vtkWidget, 0, 0, 10, 10)
       self.buttonUp= QPushButton("Segment")
       self.gridlayout.addWidget(self.buttonUp, 0,0,1,1)
       MainWindow.setCentralWidget(self.centralWidget)


class SimpleView(QMainWindow):

   def __init__(self, parent = None):
       QMainWindow.__init__(self, parent)
       self.ui = Ui_MainWindow()
       self.ui.setupUi(self)
       self.ren = vtk.vtkRenderer()
       self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
       self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

def main(): 
    print("Loading STL files")
    #filename = './STL/6000_2017-02-03_13-14_Mandibular_export.stl'
    filename = '/Users/ocros/Downloads/copie-CROS de STL non segmentés/STL non segmentés/9056_2015-05-20_13-36_Mandibular_export.stl'
    
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    
    print("STL file is now loaded")

    polydata = prepare_polydata(reader)
    full_jaw_polydata = polydata
    cutted_polydata, gencives = cut(polydata, shift=5.5)

    #clicked_0,clicked_1 = get_cusps(self, cutted_polydata)
    clicked_0,clicked_1 = get_cusps(cutted_polydata)

    cusps_0 = add_brush(cutted_polydata, clicked_0, radius=0.5)
    cusps_1 = add_brush(cutted_polydata, clicked_1, radius=0.5)

    field = compute_field(cusps_0, cusps_1, gencives, cutted_polydata, old_field=[])
    
    print('{0:.3f} Mb'.format(field.nbytes/10**6))
    
    field_polydata = add_field(cutted_polydata,field,name="Harmonic Field")

    #show_field(self, field_polydata, add_iso=False)
    show_field(field_polydata, add_iso=False)
   
    #splines_polydata = select_spline(self, field_polydata)
    splines_polydata = select_spline(field_polydata)

    save_stl(field_polydata,splines_polydata,clicked_0,clicked_1)
#    
#    #path = "/var/www/html/"
#    path = "/Users/ocros/Desktop/segmentation/stl_seg"
    
#    for tooth_file in os.listdir(path):
#        if ((not tooth_file.startswith('.')) or (not tooth_file.startswith('g'))):
#            print("filename of source: " + tooth_file)
#            #source_stl_filename = './STL/6000_2017-02-03_13-14_Mandibular_export.stl'
#    
#            source_stl = vtk.vtkSTLReader()
#            source_stl.SetFileName(tooth_file)
#        
#            source_polydat = set_source_polydata(source_stl.GetOutputPort())
#            target_polydat = set_target_polydata(full_jaw_polydata)
#        
#            out_icp = vtk.vtkIterativeClosestPointTransform()
#            out_icp = perform_ICP_PointTransform(source_polydat, target_polydat, 20)
#        
#            icpTF = vtk.vtkTransformPolyDataFilter()
#            icpTF = set_ICP_transform_filter(out_icp, source_polydat)
#        
#            # ============ display transformed points ==============
#            pointCount = 3
#            for index in range(pointCount):
#                point = [0,0,0]
#                icpTF.GetPoint(index, point)
#                print("transformed source point[%s]=%s" % (index,point))
    
if __name__ == '__main__':
    main()
    
#if __name__ == "__main__":
#   app = QApplication(sys.argv)
#   window = SimpleView()
#   main(window) 
#   window.show()
#   window.iren.Initialize() # Need this line to actually show the render inside Qt
#   sys.exit(app.exec_())
