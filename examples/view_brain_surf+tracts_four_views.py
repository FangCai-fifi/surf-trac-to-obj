import sys
from vispy import app, scene, io
from utils import read_obj_color
from vispy.visuals.filters import Alpha

canvas = scene.SceneCanvas(keys='interactive', bgcolor='black')
canvas.size = 2560, 1600
canvas.show()

# Create four ViewBoxes
vb1 = scene.widgets.ViewBox(border_color=(0,0,0,0), parent=canvas.scene) # set border color alpha(transparency) to 0!
vb2 = scene.widgets.ViewBox(border_color=(0,0,0,0), parent=canvas.scene)
vb3 = scene.widgets.ViewBox(border_color=(0,0,0,0), parent=canvas.scene)
vb4 = scene.widgets.ViewBox(border_color=(0,0,0,0), parent=canvas.scene)
scenes = vb1.scene, vb2.scene, vb3.scene, vb4.scene

# Put viewboxes in a grid
grid = canvas.central_widget.add_grid()

res = 15 # must be odd!!!
x = int((res-1)/2)
y = int((res+1)/2)
grid.add_widget(vb1, row=0, col=1, row_span=x, col_span=res-2)
grid.add_widget(vb2, row=1, col=0, row_span=res-2, col_span=x)
grid.add_widget(vb3, row=1, col=y, row_span=res-2, col_span=x)
grid.add_widget(vb4, row=y, col=1, row_span=x, col_span=res-2)

# read an surf obj and create a mesh
verts_surf, faces_surf, normals_surf, nothing_surf = io.read_mesh('assets/pial.obj')
verts_trac, faces_trac, normals_trac, nothing_trac = io.read_mesh('assets/lh.ilf.obj')
verts_trac_color = read_obj_color(objfile='assets/lh.ilf.obj')

for par in scenes:
    image_trac = scene.visuals.Mesh(vertices=verts_trac, faces=faces_trac, shading='smooth', vertex_colors=verts_trac_color, parent=par)
    image_trac.attach(Alpha(0.8))
    image_surf = scene.visuals.Mesh(vertices=verts_surf, faces=faces_surf, shading='smooth', color=(1, 1, 1), parent=par)
    image_surf.attach(Alpha(0.2))
    
# Assign cameras
vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180, roll=180) # frontal
vb2.camera = scene.TurntableCamera(fov=0, elevation=270.0, azimuth=0, roll=-90) # left
vb3.camera = scene.TurntableCamera(fov=0, elevation=90.0, azimuth=0, roll=90) # right
vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0, roll=0) # occipital

if __name__ == '__main__':
    if sys.flags.interactive != 1:
        app.run()