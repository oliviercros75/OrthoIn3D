import vtk

sr = vtk.vtkSTLReader()
Filename = 'bunny-flatfoot.stl'
sr.SetFileName(Filename)
sr.Update()
BBox = sr.GetOutput().GetBounds()

# Cut the bunny straight at z=0.6 * z-height
SlicePos = 0.6*(BBox[4]+BBox[5])

# Define the cutting plane
plane=vtk.vtkPlane()
plane.SetOrigin(0,0,SlicePos)
plane.SetNormal(0,0,-1)

# Need a plane collection for clipping
planeCollection = vtk.vtkPlaneCollection()
planeCollection.AddItem(plane)

# The clipper generates a clipped polygonial model
clipper = vtk.vtkClipClosedSurface()
clipper.SetClippingPlanes(planeCollection)
clipper.SetInputConnection(sr.GetOutputPort())
clipper.SetGenerateFaces(1)
clipper.SetScalarModeToLabels()
clipper.Update()

# Threshold the polygonial model to extract only the end caps.
threshold = vtk.vtkThreshold()
threshold.SetInputConnection(clipper.GetOutputPort())
threshold.ThresholdByUpper(1)
threshold.SetInputArrayToProcess(0,0,0,vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS_THEN_CELLS,'Labels')
threshold.Update()

# Output the number of triangles. Outputs 607
print("Got", threshold.GetOutput().GetNumberOfCells(), "triangles")