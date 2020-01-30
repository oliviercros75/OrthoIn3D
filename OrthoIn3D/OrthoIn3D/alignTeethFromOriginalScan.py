from segmentation.cut import prepare_polydata, cut
from segmentation.field import compute_field, compute_field_gui, add_field, add_field_gui, save_stl, add_brush
from segmentation.viewer import show_field, show_field_gui, get_cusps, get_cusps_gui, select_spline, select_spline_gui
from registration.mesh_registration import set_source_polydata, set_target_polydata, perform_ICP_PointTransform, set_ICP_transform_filter, display_transformed_polydata

import vtk

#originalJaw_fname = QFileDialog.getOpenFileName(self.centralwidget, 'Choose STL file', os.sep.join((os.path.expanduser('~'), 'Documents')),'STL file (*.stl)')

originalJaw_reader = vtk.vtkSTLReader()
originalJaw_fname = '/Users/ocros/Downloads/Copie de patient_01 Initial inférieur.stl'
originalJaw_reader.SetFileName(str(originalJaw_fname))

#finalJaw_fname = QFileDialog.getOpenFileName(self.centralwidget, 'Choose STL file', os.sep.join((os.path.expanduser('~'), 'Documents')),'STL file (*.stl)')

finalJaw_reader = vtk.vtkSTLReader()
finalJaw_fname = '/Users/ocros/Downloads/Copie de patient_01 stade final #7 inférieur.stl'
finalJaw_reader.SetFileName(str(finalJaw_fname))

# Create the graphics structure. The renderer renders into the render
# window. The render window interactor captures mouse events and will
# perform appropriate camera or actor manipulation depending on the
# nature of the events.
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# The mapper is responsible for pushing the geometry into the graphics
# library. It may also do color mapping, if scalars or other
# attributes are defined.
originalJaw_Mapper = vtk.vtkPolyDataMapper()
originalJaw_Mapper.SetInputConnection(originalJaw_reader.GetOutputPort())

finalJaw_Mapper = vtk.vtkPolyDataMapper()
finalJaw_Mapper.SetInputConnection(finalJaw_reader.GetOutputPort())

# The actor is a grouping mechanism: besides the geometry (mapper), it
# also has a property, transformation matrix, and/or texture map.
# Here we set its color and rotate it -22.5 degrees.
originalJaw_Actor = vtk.vtkActor()
originalJaw_Actor.SetMapper(originalJaw_Mapper)
originalJaw_Actor.GetProperty().SetColor(1.0,0.0,0.0);
originalJaw_Actor.GetProperty().SetOpacity(0.6);
#originalJaw_Actor.GetProperty().SetColor(tomato)
#originalJaw_Actor.RotateX(30.0)
#originalJaw_Actor.RotateY(-45.0)

finalJaw_Actor = vtk.vtkActor()
finalJaw_Actor.SetMapper(finalJaw_Mapper)
finalJaw_Actor.GetProperty().SetColor(0.0,1.0,0.0);
finalJaw_Actor.GetProperty().SetOpacity(1.0);
#originalJaw_Actor.GetProperty().SetColor(tomato)

# Add the actors to the renderer, set the background and size
ren.AddActor(finalJaw_Actor)
ren.AddActor(originalJaw_Actor)


ren.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(200, 200)

# This allows the interactor to initalize itself. It has to be
# called before an event loop.
iren.Initialize()

# We'll zoom in a little by accessing the camera and invoking a "Zoom"
# method on it.
ren.ResetCamera()
ren.GetActiveCamera().Zoom(1.5)
renWin.Render()

# Start the event loop.
iren.Start()
