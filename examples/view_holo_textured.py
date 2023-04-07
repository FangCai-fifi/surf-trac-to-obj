import sys
import argparse
import numpy as np
from utils import read_obj_color
from vispy import app, scene
from vispy.io import imread, load_data_file, read_mesh
from vispy.visuals.filters import Alpha, TextureFilter
from vispy.visuals.transforms import STTransform


parser = argparse.ArgumentParser()
parser.add_argument('--shading', default='smooth',
                    choices=['none', 'flat', 'smooth'],
                    help="shading mode")
args, _ = parser.parse_known_args()

canvas = scene.SceneCanvas(keys='interactive',
                           size=(1280, 1024),
                           show=True,
                           decorate=False)                       
canvas.show()

# Create four ViewBoxes
vb1 = scene.widgets.ViewBox(border_color=(1,1,1,0), parent=canvas.scene) # set border color alpha to 0!
vb2 = scene.widgets.ViewBox(border_color=(1,1,1,0), parent=canvas.scene)
vb3 = scene.widgets.ViewBox(border_color=(1,1,1,0), parent=canvas.scene)
vb4 = scene.widgets.ViewBox(border_color=(1,1,1,0), parent=canvas.scene)
vb = (vb1, vb2, vb3, vb4)

# Put viewboxes in a grid
grid = canvas.central_widget.add_grid()

grid.add_widget(vb1, row=0, col=0, row_span=1, col_span=1)
grid.add_widget(vb2, row=0, col=0, row_span=1, col_span=1)
grid.add_widget(vb3, row=0, col=0, row_span=1, col_span=1)
grid.add_widget(vb4, row=0, col=0, row_span=1, col_span=1)

# turntable cameras for each viewbox
for box in vb:
    box.camera = 'turntable'
    box.camera.aspect = 1.0

# read obj
verts_surf, faces_surf, normals_surf, texcoords_surf = read_mesh('assets/pial_vt.obj')
verts_trac, faces_trac, normals_trac, texcoords_trac = read_mesh('assets/lh.ilf.obj')
verts_trac_color = read_obj_color(objfile='assets/lh.ilf.obj')

# load texture map
texture_path = load_data_file('spot.png', directory='assets')
texture = np.flipud(imread(texture_path))
texture_filter = TextureFilter(texture, texcoords_surf)

# transformation params for adjusting the object position in camera views
scale_factor = 0.65
scale_arr = np.array([scale_factor, scale_factor, scale_factor])
translate_arr = np.array([0, 0, -70])

# assign obj to each camera scene
for par in vb:
    image_trac = scene.visuals.Mesh(vertices=verts_trac, faces=faces_trac, shading='smooth', vertex_colors=verts_trac_color, parent=par.scene)
    image_trac.attach(Alpha(0.8))
    image_trac.transform = STTransform(scale=scale_arr, translate=translate_arr)

    image_surf = scene.visuals.Mesh(vertices=verts_surf, faces=faces_surf, shading='smooth', color=(1, 1, 1), parent=par.scene)
    image_surf.attach(Alpha(0.6))
    image_surf.transform = STTransform(scale=scale_arr, translate=translate_arr)
    image_surf.attach(texture_filter)

# set initial params for each camera
vb1.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=180, roll=0, up='-z') # anterior
vb2.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=0, roll=0, up='+y') # left
vb3.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=180, roll=0, up='+y') # right
vb4.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=0, roll=0) # posterior

# setup update parameters
delta = 0 # general rotation angle

def update(ev):
    global delta
    # Assign cameras
    delta += .5
    if delta > 360:
        delta -= 360

    if delta >= 0 and delta < 90:
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=delta, azimuth=0, roll=0, up='+y') # left
        vb3.camera = scene.TurntableCamera(fov=0, elevation=-delta, azimuth=180, roll=0, up='+y') # right
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    elif delta == 90:
        # exchange camera 2 & 3
        grid.add_widget(vb1, row=0, col=0, row_span=1, col_span=1)
        grid.add_widget(vb2, row=0, col=0, row_span=1, col_span=1)
        grid.add_widget(vb3, row=0, col=0, row_span=1, col_span=1)
        grid.add_widget(vb4, row=0, col=0, row_span=1, col_span=1)
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=180 - delta, azimuth=0, roll=0, up='-y') # right
        vb3.camera = scene.TurntableCamera(fov=0, elevation=delta - 180, azimuth=180, roll=0, up='-y') # left
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    elif delta > 90 and delta <= 180:   
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=180 - delta, azimuth=0, roll=0, up='-y') # right
        vb3.camera = scene.TurntableCamera(fov=0, elevation=delta - 180, azimuth=180, roll=0, up='-y') # left
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    elif delta > 180 and delta < 270:
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=180 - delta, azimuth=0, roll=0, up='-y') # right
        vb3.camera = scene.TurntableCamera(fov=0, elevation=delta - 180, azimuth=180, roll=0, up='-y') # left
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    elif delta == 270:
        # exchange camera 2 & 3 back
        grid.add_widget(vb1, row=0, col=0, row_span=1, col_span=1)
        grid.add_widget(vb2, row=0, col=0, row_span=1, col_span=1)
        grid.add_widget(vb3, row=0, col=0, row_span=1, col_span=1)
        grid.add_widget(vb4, row=0, col=0, row_span=1, col_span=1)
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=delta - 360, azimuth=0, roll=0, up='+y') # left
        vb3.camera = scene.TurntableCamera(fov=0, elevation=360 - delta, azimuth=180, roll=0, up='+y') # right
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    else: # (270, 360)
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=delta - 360, azimuth=0, roll=0, up='+y') # left
        vb3.camera = scene.TurntableCamera(fov=0, elevation=360 - delta, azimuth=180, roll=0, up='+y') # right
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    canvas.update()

# setup timer
timer = app.Timer()
timer.connect(update)
timer.start(.05) # slow this down a bit to better see what happens

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()