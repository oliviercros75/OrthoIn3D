# -*- coding: utf-8 -*-
'''
Created on 2 déc. 2018

@author: Théo Moutakanni
'''
import numpy as np

from scipy import sparse
from scipy.sparse import linalg

import vtk
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.util import numpy_support as nps

def add_brush(polydata, clicked, radius = 1.2):
    """
    Return the points within the spheres of radius=radius and of center the clicked's points
    """
    np_mesh = dsa.WrapDataObject(polydata.GetOutput())
    verts = np_mesh.GetPoints()
    
    cusps = []
    
    for point in clicked:
        px,py,pz = verts[point]
        vx = verts[:,0]
        vy = verts[:,1]
        vz = verts[:,2]
         #Radius of the brush
        
        #Take all the points in a sphere around the picker point
        points = np.where(((vx-px)**2<radius) & ((vy-py)**2<radius )& ((vz-pz)**2<radius))[0]
        points = list(set(points)-set(cusps))
        cusps.extend(points)
        
    return cusps

def add_field(polydata,field,name=None):
    """
    Add a numpy field to a VTK polydata.
    Return the polydata with the field.
    """
    vtk_field = nps.numpy_to_vtk(field)
    if name:
        vtk_field.SetName(name)
    polydata.GetOutput().GetPointData().SetScalars(vtk_field)
    return polydata

def add_field_gui(self, polydata, field, name=None):
    """
    Add a numpy field to a VTK polydata.
    Return the polydata with the field.
    """
    vtk_field = nps.numpy_to_vtk(field)
    if name:
        vtk_field.SetName(name)
    polydata.GetOutput().GetPointData().SetScalars(vtk_field)
    return polydata

def mean_vertex(verts,tris,coef=0):
    """Compute the mean value on the vector verts on the 1-Ring neighbors according to faces polys
    
    N the number of points, M the number of faces
    verts: (N x 3) a numpy array of vertices' positions    ex: [ (x0,y0,z0), (x1,y1,z1) ...]
    tris: (M x 3) a numpy array of the faces of the triangular mesh (by vertex id) ex: [ (0,1,4), (2,4,5), ...]
    coef: The coefficient of the central vertex of the 1-Ring
    
    return an array of size (N x ?)
    """
    mean = np.zeros(verts.shape)
    nb = np.zeros(len(verts))
    for i1, i2, i3 in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        vi1 = tris[:,i1]
        vi2 = tris[:,i2]
        vi3 = tris[:,i3]
        mean[vi1] += verts[vi2]+verts[vi3]
        nb[vi1]+=2
    mean[range(len(mean))] += coef*verts[range(len(mean))]
    nb[range(len(mean))] += coef
    return (mean.T/nb).T

def veclen(vectors):
    return np.sqrt(np.sum(vectors**2, axis=-1))

def compute_laplacian(verts, tris, concav, fS=0.001, fL=1.):
    """
    Compute the Laplacian of the mesh
    
    N the number of points, M the number of faces
    verts: (N x 3) a numpy array of vertices' positions    ex: [ (x0,y0,z0), (x1,y1,z1) ...]
    tris: (M x 3) a numpy array of the faces of the triangular mesh (by vertex id) ex: [ (0,1,4), (2,4,5), ...]
    concav: (N x 3) a boolean numpy array True -> concav False -> convex
    fS: a float that correspond to the weight of the matrix on a concav area
    fL: "" "" convex area
    
    return a sparse matric of size (N x N)
    """
    n = len(verts)
    W_ij = np.empty(0)
    I = np.empty(0, np.int32)
    J = np.empty(0, np.int32)
    for i1, i2, i3 in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        vi1 = tris[:,i1]
        vi2 = tris[:,i2]
        vi3 = tris[:,i3]
        u = verts[vi2] - verts[vi1]
        v = verts[vi3] - verts[vi1]
        
        concav_ij = (concav[vi2] | concav[vi3]).astype(np.int32)
        gamma_ij = fS*concav_ij + fL*(1-concav_ij)
        
        cotan = gamma_ij*(u * v).sum(axis=1) / veclen(np.cross(u, v))
        W_ij = np.append(W_ij, 0.5 * cotan)
        I = np.append(I, vi2)
        J = np.append(J, vi3)
        W_ij = np.append(W_ij, 0.5 * cotan)
        I = np.append(I, vi3)
        J = np.append(J, vi2)
    L = sparse.csr_matrix((W_ij, (I, J)), shape=(n, n))
    L = L - sparse.spdiags(L * np.ones(n), 0, n, n)
    L = L.tocsr()
    return L

def scipy_splu(A,b):
    K = linalg.splu(A)
    return K.solve(b)

def compute_field_gui(self, cusps_0, cusps_1, gencives, polydata, old_field=[]):
    """
    Compute the Harmonic Field
    cusps_0: numpy array of points' index that have the 0 value, blue teeth
    cusps_1: numpy array of points' index that have the 1 value, orange teeth
    gencives: numpy array of points' index that have the 0.5 value, correspond to the gingiva
    polydata: the teeth polydata
    old_field: (N x 1) the old field if you have to recompute it after adding a point to cusps_0, cusps_1 or gencives
    """
    np_mesh = dsa.WrapDataObject(self.polydata.GetOutput())

    verts = np_mesh.GetPoints()
    polys = np_mesh.GetPolygons()
    polys = polys.reshape((-1,4))[:,1:]
    curvs = nps.vtk_to_numpy(self.polydata.GetOutput().GetPointData().GetArray("Mean_Curvature"))

    fL = 1. #convex weights
    fS = 0.001  #concav weights
    const = -0.2 # The constant to see if an area is concav or not, usuallt -0.2
    
    mean_vertex_coef=3
    
    curvs = mean_vertex(curvs, polys, mean_vertex_coef) #Gaussian mean to reduce isolated points
    concav = curvs < const

    L = compute_laplacian(verts,polys,concav,fS,fL)

    cusps = self.cusps_0 + self.cusps_1
    n=len(cusps)+len(self.gencives)
    m=len(verts)
    
    w=1000 #constraint on the selected points
    
    J=cusps + self.gencives
    C_ij = [w]*n
    C = sparse.csr_matrix((C_ij, (J, J)), shape=(m, m))
    M = (L+C).tocsc()
    
    b = np.zeros(m)
    #b[cusps_0] += [0*w]*len(cusps_1) #Inutile ;)
    b[self.cusps_1] += [1*w]*len(self.cusps_1)
    b[self.gencives] += [0.5*w]*len(self.gencives)
    
    if self.old_field == []:
        self.old_field = np.zeros(m)
    r = b - M * self.old_field

    field = self.old_field + scipy_splu(M, r)
    
    #Pour afficher un joli champ décommenter
    self.field = 1*((self.field>0.7).astype(np.int8) - (self.field<0.3).astype(np.int8))
    self.field = self.field.astype(np.int8)
    return self.field

def compute_field(cusps_0, cusps_1, gencives, polydata, old_field=[]):
    """
    Compute the Harmonic Field
    cusps_0: numpy array of points' index that have the 0 value, blue teeth
    cusps_1: numpy array of points' index that have the 1 value, orange teeth
    gencives: numpy array of points' index that have the 0.5 value, correspond to the gingiva
    polydata: the teeth polydata
    old_field: (N x 1) the old field if you have to recompute it after adding a point to cusps_0, cusps_1 or gencives
    """
    np_mesh = dsa.WrapDataObject(polydata.GetOutput())

    verts = np_mesh.GetPoints()
    polys = np_mesh.GetPolygons()
    polys = polys.reshape((-1,4))[:,1:]
    curvs = nps.vtk_to_numpy(polydata.GetOutput().GetPointData().GetArray("Mean_Curvature"))

    fL = 1. #convex weights
    fS = 0.001  #concav weights
    const = -0.2 # The constant to see if an area is concav or not, usuallt -0.2
    
    mean_vertex_coef=3
    curvs = mean_vertex(curvs, polys, mean_vertex_coef) #Gaussian mean to reduce isolated points
    concav = curvs < const

    L = compute_laplacian(verts,polys,concav,fS,fL)

    cusps = cusps_0 + cusps_1
    n=len(cusps)+len(gencives)
    m=len(verts)
    
    w=1000 #constraint on the selected points
    
    J=cusps + gencives
    C_ij = [w]*n
    C = sparse.csr_matrix((C_ij, (J, J)), shape=(m, m))
    M = (L+C).tocsc()
    
    b = np.zeros(m)
    #b[cusps_0] += [0*w]*len(cusps_1) #Inutile ;)
    b[cusps_1] += [1*w]*len(cusps_1)
    b[gencives] += [0.5*w]*len(gencives)
    
    if old_field == []:
        old_field = np.zeros(m)
    r = b - M * old_field

    field = old_field + scipy_splu(M, r)
    
    #Pour afficher un joli champ décommenter
    field = 1*((field>0.7).astype(np.int8) - (field<0.3).astype(np.int8))
    field = field.astype(np.int8)
    return field
    
def save_stl_old(polydata,clicked_0,clicked_1):
    np_mesh = dsa.WrapDataObject(polydata.GetOutput())
    verts = np_mesh.GetPoints()
    
    isoline_threshold_1 = 0.7
    isoline_threshold_0 = -0.7
    
    cut_teeth_1 = vtk.vtkClipPolyData()
    cut_teeth_1.SetInputData(polydata.GetOutput())
    cut_teeth_1.SetValue(isoline_threshold_1)
    cut_teeth_1.Update()
    
    for i,p in enumerate(clicked_1):
        connectivity = vtk.vtkPolyDataConnectivityFilter()
        connectivity.SetExtractionModeToClosestPointRegion()
        connectivity.SetInputConnection(cut_teeth_1.GetOutputPort())
        connectivity.SetClosestPoint(*verts[p])
        connectivity.Update()
        
        writer = vtk.vtkSTLWriter()
        writer.SetFileName('./stl_seg/teeth_{}.stl'.format(2*i))
        writer.SetInputConnection(connectivity.GetOutputPort())
        writer.Write()
    
    cut_teeth_0 = vtk.vtkClipPolyData()
    cut_teeth_0.SetInputData(polydata.GetOutput())
    cut_teeth_0.SetValue(isoline_threshold_0)
    cut_teeth_0.InsideOutOn()
    cut_teeth_0.Update()
    
    for i,p in enumerate(clicked_0):
        connectivity = vtk.vtkPolyDataConnectivityFilter()
        connectivity.SetExtractionModeToClosestPointRegion()
        connectivity.SetInputConnection(cut_teeth_0.GetOutputPort())
        connectivity.SetClosestPoint(*verts[p])
        connectivity.Update()
        
        writer = vtk.vtkSTLWriter()
        writer.SetFileName('./stl_seg/teeth_{}.stl'.format(2*i+1))
        writer.SetInputConnection(connectivity.GetOutputPort())
        writer.Write()
    
    gengiva_0 =  vtk.vtkClipPolyData()
    gengiva_0.SetInputData(polydata.GetOutput())
    gengiva_0.SetValue(isoline_threshold_0)
    gengiva_0.Update()
    
    gengiva =  vtk.vtkClipPolyData()
    gengiva.SetInputData(gengiva_0.GetOutput())
    gengiva.SetValue(isoline_threshold_1)
    gengiva.InsideOutOn()
    gengiva.Update()
    
    writer = vtk.vtkSTLWriter()
    writer.SetFileName('./stl_seg/gengiva.stl')
    writer.SetInputConnection(gengiva.GetOutputPort())
    writer.Write()
        
def generate_gengiva(spline,gengiva):
    if spline:
        loop = vtk.vtkSelectPolyData()
        loop.SetInputData(gengiva)
        loop.SetLoop(spline.GetPoints())
        loop.GenerateSelectionScalarsOn()
        loop.SetSelectionModeToSmallestRegion()
        loop.Update()
        
        clip = vtk.vtkClipPolyData()
        clip.SetInputConnection(loop.GetOutputPort())
        clip.SetValue(0)
        clip.Update()
        return clip.GetOutput()
    else:
        return gengiva

def upsample_line(line_poly, mult=10):
    spline = vtk.vtkCardinalSpline()
    spline.SetLeftConstraint(2)
    spline.SetLeftValue(0.0)
    spline.SetRightConstraint(2)
    spline.SetRightValue(0.0)
    
    splineFilter = vtk.vtkSplineFilter()
    
    splineFilter.SetInputData(line_poly)
    
    splineFilter.SetNumberOfSubdivisions(line_poly.GetNumberOfPoints() * mult)
    splineFilter.SetSpline(spline)
    splineFilter.Update()
    return splineFilter.GetOutput()

def dist_poly2point(poly, point):
        cellLocator = vtk.vtkCellLocator()
        cellLocator.SetDataSet(poly)
        cellLocator.BuildLocator()
        
        cellId = vtk.reference(0)
        nearest_point = [0.0, 0.0, 0.0]
        subId = vtk.reference(0)
        dist = vtk.reference(0.0)
        cellLocator.FindClosestPoint(point, nearest_point, cellId, subId, dist)
        return float(dist)

def save_stl(polydata,splines_polydata,clicked_0,clicked_1):
    """
    Cut teeth with the splines and save them as .stl
    """
    
    clean = vtk.vtkCleanPolyData()
    clean.AddInputConnection(polydata.GetOutputPort())
    clean.Update()
    
    triangulate = vtk.vtkTriangleFilter()
    triangulate.AddInputConnection(clean.GetOutputPort())
    triangulate.Update()
    
    np_mesh = dsa.WrapDataObject(polydata.GetOutput())
    verts = np_mesh.GetPoints()
    
    #splines_polydata = [upsample_line(spline_poly,mult=1) for spline_poly in splines_polydata]
    
    selected_polydata = []
    selected_spline = []
    #gengiva = vtk.vtkPolyData()
    #gengiva.DeepCopy(polydata.GetOutput())

    for spline in splines_polydata:
        if spline.GetNumberOfPoints() > 10:
            loop = vtk.vtkSelectPolyData()
            loop.SetInputData(triangulate.GetOutput())
            loop.SetLoop(spline.GetPoints())
            loop.GenerateSelectionScalarsOn()
            loop.SetSelectionModeToSmallestRegion()
            loop.Update()
            
            clip = vtk.vtkClipPolyData()
            clip.SetInputConnection(loop.GetOutputPort())
            clip.SetValue(0)
            clip.InsideOutOn()
            clip.Update()
                    
            selected_polydata.append(clip.GetOutput())
            selected_spline.append(spline)
        else:
            pass

    for i,poly in enumerate(selected_polydata):
        if poly.GetNumberOfPoints() == 0:
            print("error ",i)
            
            centerOfMassFilter = vtk.vtkCenterOfMass()
            centerOfMassFilter.SetInputData(selected_spline[i])
            centerOfMassFilter.SetUseScalarsAsWeights(False)
            centerOfMassFilter.Update()
            
            center = centerOfMassFilter.GetCenter()
            
            cut_teeth_0 = vtk.vtkClipPolyData()
            cut_teeth_0.SetInputData(polydata.GetOutput())
            cut_teeth_0.SetValue(-0.7)
            cut_teeth_0.InsideOutOn()
            cut_teeth_0.Update()
            
            cut_teeth_1 = vtk.vtkClipPolyData()
            cut_teeth_1.SetInputData(polydata.GetOutput())
            cut_teeth_1.SetValue(0.7)
            cut_teeth_1.Update()
            
            append = vtk.vtkAppendPolyData()
            append.AddInputConnection(cut_teeth_0.GetOutputPort())
            append.AddInputConnection(cut_teeth_1.GetOutputPort())
            
            connectivity = vtk.vtkPolyDataConnectivityFilter()
            connectivity.SetExtractionModeToClosestPointRegion()
            connectivity.SetInputConnection(append.GetOutputPort())
            connectivity.SetClosestPoint(*center)
            connectivity.Update()
            
            selected_polydata[i] = connectivity.GetOutput()
            selected_spline[i] = None
    
    #selected_spline = [selected_spline[i] for i in range(len(selected_polydata)) if selected_polydata[i].GetNumberOfPoints() != 0]
    #selected_polydata = [poly for poly in selected_polydata if poly.GetNumberOfPoints() != 0]

    for i,p in enumerate(clicked_1):
        point = verts[p]
        distance = [dist_poly2point(poly,point) for poly in selected_polydata]
        nearest = np.argmin(distance)

        writer = vtk.vtkSTLWriter()
        writer.SetFileName('./data/data_output/teeth_{}.stl'.format(2*i))
        writer.SetInputData(selected_polydata[nearest])
        writer.Write()
        
        selected_polydata.pop(nearest)
        #gengiva = generate_gengiva(selected_spline.pop(nearest),gengiva)
        
    for i,p in enumerate(clicked_0): 
        point = verts[p]
        distance = [dist_poly2point(poly,point) for poly in selected_polydata]
        nearest = np.argmin(distance)

        
        writer = vtk.vtkSTLWriter()
        writer.SetFileName('./data/data_output/teeth_{}.stl'.format(2*i+1))
        writer.SetInputData(selected_polydata[nearest])
        writer.Write()
        
        selected_polydata.pop(nearest)
        #gengiva = generate_gengiva(selected_spline.pop(nearest),gengiva)
    
    gengiva_0 =  vtk.vtkClipPolyData()
    gengiva_0.SetInputData(polydata.GetOutput())
    gengiva_0.SetValue(-0.7)
    gengiva_0.Update()
    
    gengiva =  vtk.vtkClipPolyData()
    gengiva.SetInputData(gengiva_0.GetOutput())
    gengiva.SetValue(0.7)
    gengiva.InsideOutOn()
    gengiva.Update()
    
    writer = vtk.vtkSTLWriter()
    writer.SetFileName('./data/data_output/gengiva.stl')
    writer.SetInputConnection(gengiva.GetOutputPort())
    writer.Write()
    
    
    