import sys
import argparse
import numpy as np
from utils import read_obj_color
from vispy import app, scene, io
from vispy.io import imread, load_data_file, read_mesh
from vispy.visuals.filters import TextureFilter
from vispy.visuals.filters import Alpha

parser = argparse.ArgumentParser()
parser.add_argument('--shading', default='smooth',
                    choices=['none', 'flat', 'smooth'],
                    help="shading mode")
args, _ = parser.parse_known_args()

mesh_path = load_data_file('pial_vt.obj', directory='assets')
texture_path = load_data_file('spot/spot.png')
vertices, faces, normals, texcoords = read_mesh(mesh_path)
texture = np.flipud(imread(texture_path))

canvas = scene.SceneCanvas(keys='interactive',
                           size=(1280, 1024),
                           show=True,
                           decorate=False)
                          
canvas.show()
view = canvas.central_widget.add_view()

# read obj
verts_surf, faces_surf, normals_surf, nothing_surf = io.read_mesh('assets/pial.obj')
verts_trac, faces_trac, normals_trac, nothing_trac = io.read_mesh('assets/lh.ilf.obj')
verts_trac_color = read_obj_color(objfile='assets/lh.ilf.obj')


image_trac = scene.visuals.Mesh(vertices=verts_trac, faces=faces_trac, shading='smooth', vertex_colors=verts_trac_color)
image_trac.attach(Alpha(0.8))
image_surf = scene.visuals.Mesh(vertices=verts_surf, faces=faces_surf, shading='smooth', color=(1, 1, 1))
image_surf.attach(Alpha(0.5))
view.add(image_trac)
view.add(image_surf)

texture_filter = TextureFilter(texture, texcoords)
image_surf.attach(texture_filter)

# set initial params for each camera
view.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=0, roll=0) # anterior

# setup update parameters
delta = 0 # general rotation angle

# def update(ev):
#     global delta

#     # Assign cameras
#     delta += .5
#     view.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=delta, roll=0) # frontal

#     canvas.update()

# # setup timer
# timer = app.Timer()
# timer.connect(update)
# timer.start(.1) # slow this down a bit to better see what happens

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()