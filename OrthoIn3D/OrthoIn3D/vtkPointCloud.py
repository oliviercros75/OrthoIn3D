

"""
Holds the vtk point cloud and window interactor class

VtkPointCloud:
    - creates a point cloud to visualize x, y, z
SetVtkWindow:
    - makes the interaction for the window
"""

import sys
import vtk
import numpy as np

class VtkPointCloud():
    """
    Makes the point cloud
    """
    def __init__(self, filename, scale_factor, abq_feature, point_size):
        """
        Initialize the point cloud

        Args:
            filename (string): csv file
            scale_factor (float):how much to scale the data
            abq_feature (int): which feature/column to explore in the file
            point_size: size of points in the cloud
        """

        # initialize file specific variables
        self.filename = filename
        self.scale_factor = scale_factor
        self.abq_feature = abq_feature
        self.point_size = point_size

        # setup the look up tabe
        self.lut = vtk.vtkLookupTable()
        self.build_lut()

        # create the poly data and clear
        self.vtkPolyData = vtk.vtkPolyData()
        self.clear_points()

        # initialize the mapping of the data
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputData(self.vtkPolyData)
        self.mapper.SetColorModeToDefault()
        self.mapper.SetScalarVisibility(1)
        self.mapper.SetLookupTable(self.lut)

        # create the actor
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(self.mapper)
        self.vtkActor.GetProperty().SetPointSize(self.point_size)

    def add_point(self, point):
        """
        Adds a point to the point cloud

        Args:
            point (float): array holding x,y,z
        """

        pointId = self.vtkPoints.InsertNextPoint(point[0], point[1], point[2])
        self.vtkDepth.InsertNextValue(point[2])
        self.vtkCells.InsertNextCell(1)
        self.vtkCells.InsertCellPoint(pointId)

        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def set_range(self):
        """
        Sets the scalar range in z
        """

        self.mapper.SetScalarRange(self.min_data, self.max_data)

    def clear_points(self):
        """
        Clears the points
        """

        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('PointDepth')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('PointDepth')

    def load_data(self):
        """
        Load a csv dataset which consists of exported ABAQUS data

        Args:
            point_cloud (VtkPointCloud): point cloud object
        """

        data = np.genfromtxt(self.filename, dtype=float, usecols=[1, 2, self.abq_feature], delimiter=' ')

        # scale the data so it can be displayed properly
        data[:, 2] = data[:, 2] / self.scale_factor

        # identify extremums to set the scalar range
        self.min_data = np.min(data[:, 2])
        self.max_data = np.max(data[:, 2])

        # place the scalar range
        self.set_range()

        # add the points
        for point_counter in range(data.shape[0]):
            point = data[point_counter]
            self.add_point(point)

    def build_lut(self):
        """
        Creates the lookup table

        Returns:
            - lut (vtkLookupTable): lookup table with red=max, blue=min
        """

        self.lut.SetHueRange(0.667, 0)
        self.lut.Build()

class SetVtkWindow():
    """
    Sets the window interactions
    """

    def __init__(self, point_cloud):
        # set renderer
        renderer = vtk.vtkRenderer()
        renderer.AddActor(point_cloud.vtkActor)
        renderer.SetBackground(.1, .2, .4)
        renderer.ResetCamera()

        # set the window
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)

        # set interactor
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        # create scalar bar
        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetOrientationToHorizontal()
        scalar_bar.SetLookupTable(point_cloud.lut)
        scalar_bar_widget = vtk.vtkScalarBarWidget()
        scalar_bar_widget.SetInteractor(renderWindowInteractor)
        scalar_bar_widget.SetScalarBarActor(scalar_bar)
        scalar_bar_widget.On()

        # start interactor
        renderWindow.Render()
        renderWindow.SetWindowName("CrackVis:" + point_cloud.filename)
        renderWindowInteractor.Start()

    def draw_color_range(self, mesh_lookup_table):
        """
        Draw the scalar range so that red is max, blue is min
        """

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = input("Enter file name: ")

    # display the x, y, z
    point_cloud = VtkPointCloud(filename, 10**8, 7, 10)
    point_cloud.load_data()
    vtk_window = SetVtkWindow(point_cloud)

