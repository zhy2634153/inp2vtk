#!/usr/bin/env python3
#-*-coding:utf-8-*-

import vtk

filename = "data/Job-1-C3D20.vtk"
# filename = "test2.vtk"
# filename = "Hexahedron.vtk"

colors = vtk.vtkNamedColors()

reader = vtk.vtkDataSetReader()
reader.SetFileName(filename)

reader.Update()

mapper = vtk.vtkDataSetMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(colors.GetColor3d("Green"))

ren = vtk.vtkRenderer()
ren.AddActor(actor)
ren.SetBackground(colors.GetColor3d("White"))

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)

iren  = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

iren.Initialize()
iren.Start()
