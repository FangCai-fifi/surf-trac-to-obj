import sys
from vispy import app, scene, io
from utils import read_obj_color
from vispy.visuals.filters import Alpha

canvas = scene.SceneCanvas(keys='interactive', bgcolor='white')
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

# read an surf obj and create a mesh
verts_surf, faces_surf, normals_surf, nothing_surf = io.read_mesh('assets/pial.obj')
verts_trac, faces_trac, normals_trac, nothing_trac = io.read_mesh('assets/lh.ilf.obj')
verts_trac_color = read_obj_color(objfile='assets/lh.ilf.obj')

for par in scenes:
    # image_surf = scene.visuals.Mesh(vertices=verts_surf, faces=faces_surf, shading='smooth', color=(1, 1, 1, 0.2), parent=par)
    # image_surf.attach(Alpha(1.0))
    image_trac = scene.visuals.Mesh(vertices=verts_trac, faces=faces_trac, shading='smooth', vertex_colors=verts_trac_color, parent=par)
    image_trac.attach(Alpha(0.8))
    image_surf = scene.visuals.Mesh(vertices=verts_surf, faces=faces_surf, shading='smooth', color=(1, 1, 1, 0.3), parent=par)
    # image_surf.attach(Alpha(0.2))
    
# Assign cameras
vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0)
vb2.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=90, roll=270)
vb3.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=270, roll=90)
vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180, roll=180)

if __name__ == '__main__':
    if sys.flags.interactive != 1:
        app.run()