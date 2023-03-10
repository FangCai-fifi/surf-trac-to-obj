import sys
from vispy import app, scene, io

canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 800, 800
canvas.show()

# Create four ViewBoxes
vb1 = scene.widgets.ViewBox(border_color='white', parent=canvas.scene)
vb2 = scene.widgets.ViewBox(border_color='white', parent=canvas.scene)
vb3 = scene.widgets.ViewBox(border_color='white', parent=canvas.scene)
vb4 = scene.widgets.ViewBox(border_color='white', parent=canvas.scene)
scenes = vb1.scene, vb2.scene, vb3.scene, vb4.scene

# Put viewboxes in a grid
grid = canvas.central_widget.add_grid()
grid.padding = 6
grid.add_widget(vb1, 0, 1)
grid.add_widget(vb2, 1, 0)
grid.add_widget(vb3, 1, 2)
grid.add_widget(vb4, 2, 1)

# read an obj and create a mesh
verts, faces, normals, nothing = io.read_mesh('assets/pial.obj')
mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth')
for par in scenes:
    image = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth', parent=par)

# Assign cameras
vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0)
vb2.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=90, roll=270)
vb3.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=270, roll=90)
vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180, roll=180)

if __name__ == '__main__':
    if sys.flags.interactive != 1:
        app.run()