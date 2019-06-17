from vtk import *

# Draws a series of cubes in different RGB colors
# inspired by the exmaples here https://lorensen.github.io/VTKExamples/site/Python/

def make_cube(coords,colors):
    """
      makes vtk render with cubes
      :param: coords - a list of coordinates [(x1,y1,z1),(x2,y2,z2)]
      :param: colors - a list of RGB values [(r1,g1,b1),(r2,g2,b2)].
    """
    cubes=[]

    renderer = vtk.vtkRenderer()
    for coord, color in zip(coords,colors):

        cube = vtk.vtkCubeSource()
        cube.SetXLength(1.0)
        cube.SetYLength(1.0)
        cube.SetZLength(1.0)

        cube_mapper = vtk.vtkPolyDataMapper()
        cube_mapper.SetInputConnection(cube.GetOutputPort())

        cube_actor = vtk.vtkActor()
        cube_actor.SetMapper(cube_mapper)
        cube_actor.GetProperty().SetColor(color)
        cube_actor.SetPosition(coord[0], coord[1], coord[2])

        renderer.AddActor(cube_actor)
    
    renderer.SetBackground(1,1,1)

    return renderer


def WritePNG(renWin, fn, magnification=1):
    """
      Screenshot
      Write out a png corresponding to the render window.
      :param: renWin - the render window.
      :param: fn - the file name.
      :param: magnification - the magnification.
    """
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renWin)
    # windowToImageFilter.SetMagnification(magnification) causes an error
    # Record the alpha (transparency) channel
    # windowToImageFilter.SetInputBufferTypeToRGBA()
    windowToImageFilter.SetInputBufferTypeToRGB()
    # Read from the back buffer
    windowToImageFilter.ReadFrontBufferOff()
    windowToImageFilter.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(fn)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()

# add extra coordings or colors
renderer = make_cube(colors = [(1,0,1),(0,1,0)],
                     coords = [(0,0,0),(2,2,2)])

camera = vtkCamera()
camera.SetPosition(0, 0,20)
camera.SetFocalPoint(0, 0, 0)

renderer.SetActiveCamera(camera)

render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("colour cubes")
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
# # Initialize the interactor and start the# rendering loop
interactor.Initialize()
render_window.Render()

#this opens the viewing window
interactor.Start()

WritePNG(render_window, 'cube.png')