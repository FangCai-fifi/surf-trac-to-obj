import sys
import numpy as np
from utils import read_obj_color
from vispy import app, scene, io
from vispy.visuals.filters import ShadingFilter
# from vispy.util.transforms import scale
from vispy.visuals.transforms import STTransform

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


## ---- Set headlight ---- ##
def attach_headlight(view):
    light_dir = (0, 1, 0, 0)
    shading_filter.light_dir = light_dir[:3]
    initial_light_dir = view.camera.transform.imap(light_dir)

    @view.camera.transform.changed.connect
    def on_transform_change(event):
        transform = view.camera.transform
        shading_filter.light_dir = transform.map(initial_light_dir)[:3]


## ---- Load subject obj ---- ##
verts_surf, faces_surf, normals_surf, texcoords_surf = io.read_mesh(f"assets/{subname}/pial.obj")
verts_lh_v1, faces_lh_v1, normals_lh_v1, texcoords_lh_v1 = io.read_mesh(f"assets/{subname}/lh.V1_exvivo.obj")
verts_lh_mt, faces_lh_mt, normals_lh_mt, texcoords_lh_mt = io.read_mesh(f"assets/{subname}/lh.MT_exvivo.obj")
verts_rh_v1, faces_rh_v1, normals_rh_v1, texcoords_rh_v1 = io.read_mesh(f"assets/{subname}/rh.V1_exvivo.obj")
verts_rh_mt, faces_rh_mt, normals_rh_mt, texcoords_rh_mt = io.read_mesh(f"assets/{subname}/rh.MT_exvivo.obj")
verts_lh_lip, faces_lh_lip, normals_lh_lip, texcoords_lh_lip = io.read_mesh(f"assets/{subname}/lh.S_intrapariet_and_P_trans.obj")
verts_rh_lip, faces_rh_lip, normals_rh_lip, texcoords_rh_lip = io.read_mesh(f"assets/{subname}/rh.S_intrapariet_and_P_trans.obj")
verts_lh_lgn, faces_lh_lgn, normals_lh_lgn, texcoords_lh_lgn = io.read_mesh(f"assets/{subname}/lh.lgn1.obj")
verts_rh_lgn, faces_rh_lgn, normals_rh_lgn, texcoords_rh_lgn = io.read_mesh(f"assets/{subname}/rh.lgn1.obj")
verts_nuclei, faces_nuclei, normals_nuclei, texcoords_nuclei = io.read_mesh(f"assets/{subname}/thalamicNuclei.obj")


## ---- Assign obj to each camera scene ---- ##

# obj transformation
scale_factor = 0.65
scale_arr = np.array([scale_factor, scale_factor, scale_factor])
translate_arr = np.array([0, 0, -70])

# shading setup
shading_filter = ShadingFilter(shading='smooth',
                               ambient_coefficient=(1, 1, 1, 1),
                               diffuse_coefficient=(1, 1, 1, 1),
                               specular_coefficient=(1, 1, 1, 1),
                               shininess=250,
                               light_dir=(0, 0, -1),
                               ambient_light=(1, 1, 1, 0.25),
                               diffuse_light=(1, 1, 1, 0.7),
                               specular_light=(1, 1, 1, 0.25),
                               enabled=True)

shading_filter_v1_rh = ShadingFilter(shading='smooth', light_dir=(1, 1, 0))
shading_filter_v1_lh = ShadingFilter(shading='smooth', light_dir=(-1, 1, 0))
shading_filter_mt_rh = ShadingFilter(shading='smooth', light_dir=(-1, 1, 0))
shading_filter_mt_lh = ShadingFilter(shading='smooth', light_dir=(1, 1, 0))

# put obj in viewboxes
for par in vb:

    image_lh_v1 = scene.visuals.Mesh(vertices=verts_lh_v1, faces=faces_lh_v1, color=(0.6314, 0.8588, 0.7922, 1), parent=par.scene)
    image_lh_v1.transform = STTransform(scale=scale_arr, translate=translate_arr)
    image_lh_v1.attach(shading_filter_v1_lh)
    image_rh_v1 = scene.visuals.Mesh(vertices=verts_rh_v1, faces=faces_rh_v1, color=(0.6314, 0.8588, 0.7922, 1), parent=par.scene)
    image_rh_v1.transform = STTransform(scale=scale_arr, translate=translate_arr)
    image_rh_v1.attach(shading_filter_v1_rh)

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
    
    # image_lh_lgn = scene.visuals.Mesh(vertices=verts_lh_lgn, faces=faces_lh_lgn, color=(1, 0.5529, 0.1020, 1), parent=par.scene)
    # image_lh_lgn.transform = STTransform(scale=scale_arr, translate=translate_arr)
    # image_rh_lgn = scene.visuals.Mesh(vertices=verts_rh_lgn, faces=faces_rh_lgn, color=(1, 0.5529, 0.1020, 1), parent=par.scene)
    # image_rh_lgn.transform = STTransform(scale=scale_arr, translate=translate_arr)
    
    image_nuclei = scene.visuals.Mesh(vertices=verts_nuclei, faces=faces_nuclei, color=(1, 0.5529, 0.1020, 1), parent=par.scene)
    image_nuclei.transform = STTransform(scale=scale_arr, translate=translate_arr)

    image_surf = scene.visuals.Mesh(vertices=verts_surf, faces=faces_surf, color=(1, 1, 1, 1.0), parent=par.scene)
    image_surf.transform = STTransform(scale=scale_arr, translate=translate_arr)
    image_surf.attach(shading_filter)
    # attach_headlight(view=par)

    


## ---- Set initial params for each camera ---- ##
vb1.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=180, roll=0, up='-z') # anterior
vb2.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=0, roll=0, up='+y') # left
vb3.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=180, roll=0, up='+y') # right
vb4.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=0, roll=0) # posterior


## ---- Set update params for each camera ---- ##
delta = 0 # general rotation angle

def update(ev):
    global delta

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


## ---- Set up timer ---- ##
timer = app.Timer()
timer.connect(update)
timer.start(.01) # slow this down a bit to better see what happens

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()
