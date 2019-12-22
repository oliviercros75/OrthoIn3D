# -*- coding: utf-8 -*-
'''
Created on 2 déc. 2018

@author: Théo Moutakanni
'''

import vtk

def get_cusps(polydata):
    """
    Allow to pick the cusps of each tooth
    Return two lists, each is a list of points where the field must be 0 or 1
    """
    clicked_0 = []
    clicked_1 = []

    picker = vtk.vtkCellPicker()
    
    oscillation = [False]

    def annotatePick(object, event):
        if picker.GetCellId() >= 0:
            point = picker.GetPointId()
            
            if oscillation[0]:
                clicked = clicked_0
            else:
                clicked = clicked_1
            oscillation[0] = not oscillation[0]

            clicked.append(point)
    
    picker.AddObserver("EndPickEvent", annotatePick) 
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(polydata.GetOutputPort())
    mapper.ScalarVisibilityOff()
  
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1.0,1.0,1.0)
    
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.SetPicker(picker)
    
    ren.AddActor(actor)
    iren.Initialize()
    renWin.Render()
    iren.Start()
    
    return clicked_0,clicked_1

def show_field(polydata, add_iso=False):
    """
    Show the field
    """
    colors = vtk.vtkNamedColors()
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToDiverging()
    p1 = [0.0] + list(colors.GetColor3d("MidnightBlue"))
    p2 = [1.0] + list(colors.GetColor3d("DarkOrange"))
    ctf.AddRGBPoint(*p1)
    ctf.AddRGBPoint(*p2)
    cc = list()
    for i in range(256):
        cc.append(ctf.GetColor(float(i) / 255.0))
    
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfColors(256)
    for i, item in enumerate(cc):
        lut.SetTableValue(i, item[0], item[1], item[2], 1.0)
    lut.SetRange(-1,1)
    
    scalarBar = vtk.vtkScalarBarActor()
    scalarBar.SetLookupTable(lut)
    scalarBar.SetTitle("Harmonic Field")
    scalarBar.SetNumberOfLabels(4)
    
    isolines = vtk.vtkContourFilter()

    isolines.SetInputConnection(polydata.GetOutputPort())
    isolines.GenerateValues(10,-1,1)
    isolines.Update()
    
    mapper_field = vtk.vtkPolyDataMapper()
    mapper_field.SetInputConnection(polydata.GetOutputPort())
    mapper_field.SetLookupTable(lut)
    mapper_field.SetUseLookupTableScalarRange(1)
    
    mapper_iso = vtk.vtkPolyDataMapper()
    mapper_iso.SetInputConnection(isolines.GetOutputPort())
    mapper_iso.SetScalarModeToUseCellData()
    mapper_iso.SetScalarRange(-1,1)
    
    actor_field = vtk.vtkActor()
    actor_field.SetMapper(mapper_field)
    
    actor_iso = vtk.vtkActor()
    actor_iso.SetMapper(mapper_iso)
    actor_iso.GetProperty().SetColor(1.0,0.0,0.0)
    
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    ren.AddActor(actor_field)
    if add_iso:
        ren.AddActor(actor_iso)
    ren.AddActor(scalarBar)
    
    iren.Initialize()
    renWin.Render()
    iren.Start()
    
def select_spline(polydata):
    """
    Selecte the splines after the field is computed.
    Return a list of splines as polydatas
    """
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(polydata.GetOutputPort())
    mapper.ScalarVisibilityOff()
     
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToFlat()
    
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    
    renderer.AddActor(actor)
    renderer.SetBackground(.3, .4, .5)
    
    isolines = vtk.vtkContourFilter()
    isolines.SetInputConnection(polydata.GetOutputPort())
    isolines.SetValue(0,0.7)
    isolines.SetValue(1,-0.7)
    isolines.Update()
    
    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(isolines.GetOutputPort())
    stripper.Update()

    def order_points(stripper, keep_ratio=1):
        sample_rate = int(1/keep_ratio)
        lines = stripper.GetOutput().GetLines()
        points = stripper.GetOutput().GetPoints()
        NumberOfLines = stripper.GetOutput().GetNumberOfLines()
        pts = vtk.vtkIdList()
        lines.InitTraversal()
        list_poly = []
        
        for i in range(NumberOfLines):
            lines.GetNextCell(pts)
            
            nb_pts = pts.GetNumberOfIds()
            points_ord = vtk.vtkPoints()
            line_ord = vtk.vtkCellArray()
            line_ord.InsertNextCell(pts)
            
            for j in range(nb_pts):
                if j%sample_rate==0:
                    points_ord.InsertPoint(j//sample_rate, points.GetPoint(pts.GetId(j)))
            
            poly_ordered = vtk.vtkPolyData()
            poly_ordered.SetPoints(points_ord)
            poly_ordered.SetLines(line_ord)
            list_poly.append(poly_ordered)
        return list_poly[::-1]

    polys_ordered = order_points(stripper, keep_ratio=0.2)
    polys_ordered = [poly for poly in polys_ordered if poly.GetNumberOfPoints() > 10]
    representations = []
    contours = []
    
    contourWidget = vtk.vtkContourWidget()
    contours.append(contourWidget)
    contourWidget.SetInteractor(interactor)
    #rep = vtk.vtkOrientedGlyphContourRepresentation(contourWidget.GetRepresentation())
    rep = contourWidget.GetRepresentation()
    representations.append(rep)
    rep.GetLinesProperty().SetColor(1, 0.2, 0);
    rep.GetLinesProperty().SetLineWidth(3.0);
    
    pointPlacer = vtk.vtkPolygonalSurfacePointPlacer()
    pointPlacer.AddProp(actor)
    pointPlacer.SnapToClosestPointOn()
    pointPlacer.GetPolys().AddItem( polydata.GetOutput() )
    rep.SetPointPlacer(pointPlacer)
    
    #interpolator = vtk.vtkPolygonalSurfaceContourLineInterpolator()
    #interpolator.GetPolys().AddItem(polydata.GetOutput())
    interpolator = vtk.vtkBezierContourLineInterpolator()
    rep.SetLineInterpolator(interpolator)

    contourWidget.EnabledOn()
    
    splines = []
    
    i = [0]
    def keyPressEvent(obj, event):
        
        key = obj.GetKeySym()
        if key == 'Return' and i[0]<len(polys_ordered):
            if i[0]!=0:
                spline = vtk.vtkPolyData()
                spline.DeepCopy(rep.GetContourRepresentationAsPolyData())
                splines.append(spline)
            contourWidget.Initialize(polys_ordered[i[0]], 1)#, pts)
            contourWidget.Modified()
            obj.GetRenderWindow().Render()
            i[0]+=1
        elif key == 'Return':
            splines.append(rep.GetContourRepresentationAsPolyData())
            renderWindow.Finalize()
            interactor.TerminateApp()
    
    interactor.AddObserver("KeyPressEvent", keyPressEvent)
    
    renderer.ResetCamera()
    renderWindow.Render()
    interactor.Initialize()
    interactor.Start()

    return splines