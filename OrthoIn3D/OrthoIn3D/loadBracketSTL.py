#!/usr/bin/env python

import vtk

filename1 = '/Users/ocros/Documents/OrthoIn3D/OrthoIn3D/OrthoIn3D/data/other/ToothBrackety90.stl'
 
filename2 = '/Users/ocros/Documents/OrthoIn3D/OrthoIn3D/OrthoIn3D/data/data_input/6000_2017-02-03_13-14_Mandibular_export.stl'

reader1 = vtk.vtkSTLReader()
reader1.SetFileName(filename1)

reader2 = vtk.vtkSTLReader()
reader2.SetFileName(filename2)

# Set up the transform filter
translation = vtk.vtkTransform()
translation.Translate(1.0, 2.0, 3.0)

transformFilter = vtk.vtkTransformPolyDataFilter()
transformFilter.SetInputConnection(reader1.GetOutputPort())
transformFilter.SetTransform(translation)
transformFilter.Update()

# Clean the polydata so that the edges are shared !
cleanPolyData = vtk.vtkCleanPolyData()
cleanPolyData.SetInputConnection(transformFilter.GetOutputPort())

# Use a filter to smooth the data (will add triangles and smooth)
# Use two different filters to show the difference
#smooth_loop = vtk.vtkLoopSubdivisionFilter()
#smooth_loop.SetNumberOfSubdivisions(1)
#smooth_loop.SetInputConnection(transformFilter.GetOutputPort())
#smooth_butterfly = vtk.vtkButterflySubdivisionFilter()
#smooth_butterfly.SetNumberOfSubdivisions(3)
#smooth_butterfly.SetInputConnection(transformFilter.GetOutputPort())


transform = vtk.vtkTransform()
transform.Translate(1.0, 2.0, 3.0)
axes = vtk.vtkAxesActor()
#  The axes are positioned with a user transform
axes.SetUserTransform(transform)
axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(1,0,0)
axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0,1,0)
axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0,0,1)

mapper1 = vtk.vtkPolyDataMapper()
mapper2 = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper1.SetInput(reader2.GetOutput())
    mapper2.SetInput(cleanPolyData.GetOutput)
else:
    mapper1.SetInputConnection(reader2.GetOutputPort())
    mapper2.SetInputConnection(cleanPolyData.GetOutputPort())

actor1 = vtk.vtkActor()
actor1.SetMapper(mapper1)

actor2 = vtk.vtkActor()
actor2.SetMapper(mapper2)

# Create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# Create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Assign actor to the renderer
ren.AddActor(axes)
#ren.AddActor(actor1)
ren.AddActor(actor2)


# Enable user interface interactor
#ren.SetBackground(0.2, 0.3, 0.5) # Background color white
ren.SetBackground(.3, .6, .3)
iren.Initialize()
renWin.Render()
iren.Start()