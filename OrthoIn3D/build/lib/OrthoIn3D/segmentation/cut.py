# -*- coding: utf-8 -*-
'''
Created on 29 oct. 2018

@author: Théo Moutakanni
'''

import vtk
import vtk.util.numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

import numpy as np
from scipy.linalg import svd

def prepare_polydata(polydata):
    """
    Add some arrays to compute on the polydata
    Return a polydata
    """
    min_curv = vtk.vtkCurvatures()
    min_curv.SetCurvatureTypeToMinimum()
    min_curv.SetInputConnection(polydata.GetOutputPort())
    min_curv.Update()
    
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(min_curv.GetOutputPort())
    normals.ComputeCellNormalsOff()
    normals.ComputePointNormalsOn()
    normals.SplittingOff()
    normals.Update()

    return min_curv, normals

def cartesian_product(a,b):
    A = a[:,np.array([[i]*3 for i in range(3)]).flatten()]
    B = b[:,list(range(3))*3]
    return (A*B).reshape(-1,3,3)

def get_plane(verts,curvs,threshold=-0.3):
    """
    Use a Principal Component Analysis (PCA) to obtain the plane that will cut the jaw
    
    N the number of points
    verts: (N x 3) a numpy array of vertices' positions    ex: [ (x0,y0,z0), (x1,y1,z1) ...]
    curvs: (N x 1) a numpy array of vertices' curvature    ex: [ 0.124, -1.58, ...]
    threshold: The curvature threshold to select the concav points under the teeth, usually -0.3 works
    
    Return a point of the plane and its normal
    """
    
    Fk = verts[curvs < threshold]
    barycentre = 1/len(Fk)*np.sum(Fk,axis=0)
    vec = verts-barycentre
    M = 1/len(Fk)*np.sum(cartesian_product(vec,vec),axis=0)
    
    U,s,Vh = svd(M)
    
    return barycentre,U[:,-1]

def cut(polydata, shift=-5.5): #5.5):
    """
    Cut the jaw just under the teeth to reduce the number of vertices.
    May rotate it.
    Take a polydata and the shifting value of the cutting plane (in milimeter).
    Return the clipped polydata
    """

    x,y,z,X,Y,Z = polydata.GetOutput().GetBounds()
    #Get the volume of the mesh before clipping
    volume_before = (Z-z)*(Y-y)*(X-x)

    
    rotate = vtk.vtkTransform()
    rotate.RotateX(90)

    transform = vtk.vtkTransformFilter()
    transform.SetTransform(rotate)
    transform.SetInputConnection(polydata.GetOutputPort())
    transform.Update()

    np_mesh = dsa.WrapDataObject(transform.GetOutput())
    verts = np_mesh.GetPoints()
    
    curvs = nps.vtk_to_numpy(transform.GetOutput().GetPointData().GetArray("Mean_Curvature"))

    origin,normal = get_plane(verts, curvs, threshold=-0.3)
    origin = origin-shift*normal
    
    plane = vtk.vtkPlane()
    plane.SetOrigin(*origin)
    plane.SetNormal(*normal)
    
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(transform.GetOutputPort())
    clipper.SetClipFunction(plane)
    clipper.GenerateClipScalarsOn()
    clipper.GenerateClippedOutputOn()
    clipper.SetValue(0.5)
    clipper.Update()
    
    x,y,z,X,Y,Z = clipper.GetOutput().GetBounds()
    #Get the volume of the clipped mesh
    volume_after = (Z-z)*(Y-y)*(X-x)
    
    #If the STL file is upside down the volume after the clipping is too big
    #If it cannot properly flip the polydata you can change the threshold
    if volume_after/volume_before >= 0.7:
        rotate.RotateX(180)
        transform.Update()
        
        np_mesh = dsa.WrapDataObject(transform.GetOutput())
        verts = np_mesh.GetPoints()
        curvs = nps.vtk_to_numpy(transform.GetOutput().GetPointData().GetArray("Mean_Curvature"))
        origin,normal = get_plane(verts, curvs, -0.3)
        origin = origin-shift*normal

        plane.SetOrigin(*origin)
        plane.SetNormal(*normal)
        clipper.Update()
    
    probe_clip = vtk.vtkProbeFilter()
    probe_clip.SetSourceConnection(transform.GetOutputPort())
    probe_clip.SetInputConnection(clipper.GetOutputPort())
    probe_clip.Update()

    cleaner = vtk.vtkCleanPolyData()
    cleaner.AddInputConnection(probe_clip.GetOutputPort())
    cleaner.Update()

    id_filter = vtk.vtkIdFilter()
    id_filter.SetInputConnection(cleaner.GetOutputPort())
    id_filter.PointIdsOn()
    id_filter.SetIdsArrayName("PointsID")
    id_filter.Update()
    
    np_clip = dsa.WrapDataObject(id_filter.GetOutput())
    points = np_clip.GetPoints()
    
    #Compute the distance between points and the plane and gets the one within the max distance
    dists = np.dot(points-origin,normal)
    max_dist_gingiva = 0.5
    gencives = list(np.where(dists < max_dist_gingiva)[0])
    
    return id_filter, gencives
    
    