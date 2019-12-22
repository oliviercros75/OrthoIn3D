# -*- coding: utf-8 -*-
'''
Created on Sun 15 Dec 2019

@author: Olivier Cros
'''

import vtk

def set_source_polydata(polydata):
    source = vtk.vtkPolyData()
    sourcePoints = vtk.vtkPoints()
    #sourceVertices = vtk.vtkCellArray()
    #id = sourcePoints.SetPoints(polydata.GetPoints())
    sourcePoints.SetPoints(polydata.GetPoints())
    
    #sourceVertices.InsertNextCell(1)
    #sourceVertices.InsertCellPoint(id)

    source.SetPoints(sourcePoints)
    source.SetVerts(sourceVertices)
    if vtk.VTK_MAJOR_VERSION <= 5:
        source.Update()
    return source

def set_target_polydata(polydata):
    
    target = vtk.vtkPolyData()
    targetPoints = vtk.vtkPoints()
    target.SetPoints(polydata.GetPoints())
    #target.SetVerts(targetVertices)
    if vtk.VTK_MAJOR_VERSION <= 5:
        target.Update()
    return targert

def perform_ICP_PointTransform(source_polydata, target_polydata, nb_iter=None):
    if nb_iter is None:
        nb_iter = 20
    icp = vtk.vtkIterativeClosestPointTransform()
    icp.SetSource(source_polydata)
    icp.SetTarget(target_polydata)
    icp.GetLandmarkTransform().SetModeToRigidBody()

    #icp.DebugOn()
    icp.SetMaximumNumberOfIterations(nb_iter)
    icp.StartByMatchingCentroidsOn()
    icp.Modified()
    icp.Update()  
    return icp

def set_ICP_transform_filter(icp_point_transform, source_polydata):
    icpTransformFilter = vtk.vtkTransformPolyDataFilter()
    if vtk.VTK_MAJOR_VERSION <= 5:
        icpTransformFilter.SetInput(source_polydat)
    else:
        icpTransformFilter.SetInputData(source_polydat)

    icpTransformFilter.SetTransform(icp_point_transform)
    icpTransformFilter.Update()
    return icp_transformFilter.GetOutput()

def display_transformed_polydata(polydata):
    pointCount = 3
    for index in range(pointCount):
        point = [0,0,0]
        transformedSource.GetPoint(index, point)
        print("transformed source point[%s]=%s" % (index,point))

