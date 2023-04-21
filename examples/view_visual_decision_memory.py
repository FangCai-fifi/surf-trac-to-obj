import sys
import gc
import numpy as np
from vispy import app, scene, io
from vispy.visuals.filters import ShadingFilter
from vispy.visuals.transforms import STTransform

gc.enable()

## ---- Define a subject id ---- ##
subname = 'example'


## ---- Create a canvas ---- ##
canvas = scene.SceneCanvas(keys='interactive',
                           size=(1280, 1024),
                           show=True,
                           decorate=False)                          
canvas.show()


## ---- Create four ViewBoxes ---- ##
vb1 = scene.widgets.ViewBox(camera='turntable', parent=canvas.scene) # border_color=(1,1,1,0)
vb2 = scene.widgets.ViewBox(camera='turntable', parent=canvas.scene)
vb3 = scene.widgets.ViewBox(camera='turntable', parent=canvas.scene)
vb4 = scene.widgets.ViewBox(camera='turntable', parent=canvas.scene)
vb = (vb1, vb2, vb3, vb4)


## ---- Put viewboxes in a grid ---- ##
grid = canvas.central_widget.add_grid()
grid.add_widget(vb1, row=0, col=0, row_span=1, col_span=1)
grid.add_widget(vb2, row=0, col=0, row_span=1, col_span=1)
grid.add_widget(vb3, row=0, col=0, row_span=1, col_span=1)
grid.add_widget(vb4, row=0, col=0, row_span=1, col_span=1)


## ---- Load subject obj ---- ##
verts_surf, faces_surf, normals_surf, texcoords_surf = io.read_mesh(f"assets/{subname}/pial.obj")
verts_v1, faces_v1, normals_v1, texcoords_v1 = io.read_mesh(f"assets/{subname}/V1.obj")
verts_lh_mt, faces_lh_mt, normals_lh_mt, texcoords_lh_mt = io.read_mesh(f"assets/{subname}/lh.MT_exvivo.obj")
verts_rh_mt, faces_rh_mt, normals_rh_mt, texcoords_rh_mt = io.read_mesh(f"assets/{subname}/rh.MT_exvivo.obj")
verts_lh_lip, faces_lh_lip, normals_lh_lip, texcoords_lh_lip = io.read_mesh(f"assets/{subname}/lh.S_intrapariet_and_P_trans.obj")
verts_rh_lip, faces_rh_lip, normals_rh_lip, texcoords_rh_lip = io.read_mesh(f"assets/{subname}/rh.S_intrapariet_and_P_trans.obj")
verts_nuclei, faces_nuclei, normals_nuclei, texcoords_nuclei = io.read_mesh(f"assets/{subname}/thalamicNuclei.obj")


## ---- Assign obj to each camera scene ---- ##

## obj transformation
scale_factor = 0.80
scale_arr = np.array([scale_factor, scale_factor, scale_factor])
translate_arr = np.array([0, 0, -88])

## shading setup
shading_filter_surfs = ShadingFilter(shading='smooth', shininess=250, light_dir=(0, 0, -1))
shading_filter_v1 = ShadingFilter(shading='smooth', light_dir=(0, 1, 0))
shading_filter_mt_rh = ShadingFilter(shading='smooth', light_dir=(-1, 1, 0))
shading_filter_mt_lh = ShadingFilter(shading='smooth', light_dir=(1, 1, 0))

## put obj in viewboxes
for par in vb:
    image_v1 = scene.visuals.Mesh(vertices=verts_v1, faces=faces_v1, color=(0.6314, 0.8588, 0.7922, 1), parent=par.scene)
    image_v1.transform = STTransform(scale=scale_arr, translate=translate_arr)
    image_v1.attach(shading_filter_v1)

    image_lh_mt = scene.visuals.Mesh(vertices=verts_lh_mt, faces=faces_lh_mt, color=(0.9569, 0.8275, 0.7608, 1), parent=par.scene)
    image_lh_mt.transform = STTransform(scale=scale_arr, translate=translate_arr)
    image_lh_mt.attach(shading_filter_mt_lh)
    image_rh_mt = scene.visuals.Mesh(vertices=verts_rh_mt, faces=faces_rh_mt, color=(0.9569, 0.8275, 0.7608, 1), parent=par.scene)
    image_rh_mt.transform = STTransform(scale=scale_arr, translate=translate_arr)
    image_rh_mt.attach(shading_filter_mt_rh)

    image_lh_lip = scene.visuals.Mesh(vertices=verts_lh_lip, faces=faces_lh_lip, color=(0.0667, 0.2196, 0.5725, 1), parent=par.scene)
    image_lh_lip.transform = STTransform(scale=scale_arr, translate=translate_arr)
    image_rh_lip = scene.visuals.Mesh(vertices=verts_rh_lip, faces=faces_rh_lip, color=(0.0667, 0.2196, 0.5725, 1), parent=par.scene)
    image_rh_lip.transform = STTransform(scale=scale_arr, translate=translate_arr)
    
    image_nuclei = scene.visuals.Mesh(vertices=verts_nuclei, faces=faces_nuclei, color=(1, 0.5529, 0.1020, 1), parent=par.scene)
    image_nuclei.transform = STTransform(scale=scale_arr, translate=translate_arr)

    image_surf = scene.visuals.Mesh(vertices=verts_surf, faces=faces_surf, color=(1, 1, 1, 1.0), parent=par.scene)
    image_surf.transform = STTransform(scale=scale_arr, translate=translate_arr)
    image_surf.attach(shading_filter_surfs)


## ---- Release memory ---- ##
del verts_surf, verts_lh_lip, verts_lh_mt, verts_nuclei, verts_rh_lip, verts_rh_mt, verts_v1
del faces_surf, faces_lh_lip, faces_lh_mt, faces_nuclei, faces_rh_lip, faces_rh_mt, faces_v1
del normals_surf, normals_lh_lip, normals_lh_mt, normals_nuclei, normals_rh_lip, normals_rh_mt, normals_v1
del texcoords_surf, texcoords_lh_lip, texcoords_lh_mt, texcoords_nuclei, texcoords_rh_lip, texcoords_rh_mt, texcoords_v1
del image_surf, image_lh_lip, image_lh_mt, image_nuclei, image_rh_lip, image_rh_mt, image_v1
gc.collect()


## ---- Set initial params for each camera ---- ##
vb1.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=180, roll=0, up='-z') # anterior
vb2.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=0, roll=0, up='+y') # left
vb3.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=180, roll=0, up='+y') # right
vb4.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=0, roll=0) # posterior


## ---- Update params for each camera ---- ##
delta = 0 # general rotation angle

def update(ev):
    global delta

    delta += .5
    if delta >= 270:
        delta -= 360

    if delta >= -90 and delta < 90:
        vb2.camera.elevation = delta
        vb2.camera.up = '+y'
        vb3.camera.elevation = - delta
        vb3.camera.up = '+y'

    elif delta >= 90 and delta < 270:   
        vb2.camera.elevation = 180 - delta
        vb2.camera.up = '-y'
        vb3.camera.elevation = delta - 180
        vb3.camera.up = '-y'
    
    vb1.camera.azimuth = 180 + delta
    vb4.camera.azimuth = - delta

    canvas.update()


## ---- Set up timer ---- ##
timer = app.Timer()
timer.connect(update)
timer.start(0) # slow this down a bit to better see what happens


## ---- Keyboard event ---- ##
@canvas.events.key_press.connect
def on_key_press(event):
    if event.key == 'p':
        timer.disconnect(update)
    elif event.key == 's':
        timer.connect(update)


if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()
