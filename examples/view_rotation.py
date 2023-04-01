import sys
from utils import read_obj_color
from vispy import app, scene, io
from vispy.visuals.filters import Alpha

canvas = scene.SceneCanvas(keys='interactive',
                           size=(1280, 1024),
                           show=True,
                           decorate=False)
# canvas = scene.SceneCanvas(keys='interactive',
#                            # size=(1280, 1024),
#                            show=True,
#                            fullscreen=True)                           
canvas.show()

# Create four ViewBoxes
vb1 = scene.widgets.ViewBox(border_color=(0,0,0,0), parent=canvas.scene) # set border color alpha to 0!
vb2 = scene.widgets.ViewBox(border_color=(0,0,0,0), parent=canvas.scene)
vb3 = scene.widgets.ViewBox(border_color=(0,0,0,0), parent=canvas.scene)
vb4 = scene.widgets.ViewBox(border_color=(0,0,0,0), parent=canvas.scene)
vb = (vb1, vb2, vb3, vb4)

# Put viewboxes in a grid
grid = canvas.central_widget.add_grid()

grid.add_widget(vb1, row=0, col=2, row_span=6, col_span=6) # testing
grid.add_widget(vb2, row=4, col=0, row_span=6, col_span=6)
grid.add_widget(vb3, row=4, col=4, row_span=6, col_span=6)
grid.add_widget(vb4, row=8, col=2, row_span=6, col_span=6)

# turntable cameras for each viewbox
for box in vb:
    box.camera = 'turntable'
    box.camera.aspect = 1.0

# read obj
verts_surf, faces_surf, normals_surf, nothing_surf = io.read_mesh('assets/pial.obj')
verts_trac, faces_trac, normals_trac, nothing_trac = io.read_mesh('assets/lh.ilf.obj')
verts_trac_color = read_obj_color(objfile='assets/lh.ilf.obj')

# assign obj to each camera scene
for par in vb:
    image_trac = scene.visuals.Mesh(vertices=verts_trac, faces=faces_trac, shading='smooth', vertex_colors=verts_trac_color, parent=par.scene)
    image_trac.attach(Alpha(0.8))
    image_surf = scene.visuals.Mesh(vertices=verts_surf, faces=faces_surf, shading='smooth', color=(1, 1, 1), parent=par.scene)
    image_surf.attach(Alpha(0.2))

# set initial params for each camera
vb1.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=180, roll=0, up='-z') # frontal
vb2.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=0, roll=0, up='+y') # left
vb3.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=180, roll=0, up='+y') # right
vb4.camera = scene.TurntableCamera(fov=0, elevation=0, azimuth=0, roll=0) # occipital

# setup update parameters
delta = 0 # general rotation angle
y = 0 # key param for camera 2 & 3!!!

def update(ev):
    global delta, y
    # Assign cameras
    delta += .5
    y = delta % 360
    if y >= 0 and y < 90:
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=y, azimuth=0, roll=0, up='+y') # left
        vb3.camera = scene.TurntableCamera(fov=0, elevation=-y, azimuth=180, roll=0, up='+y') # right
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    elif y == 90:
        # exchange camera 2 & 3
        grid.add_widget(vb1, row=0, col=2, row_span=6, col_span=6)
        grid.add_widget(vb3, row=4, col=0, row_span=6, col_span=6)
        grid.add_widget(vb2, row=4, col=4, row_span=6, col_span=6)
        grid.add_widget(vb4, row=8, col=2, row_span=6, col_span=6)
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=180 - y, azimuth=0, roll=0, up='-y') # right
        vb3.camera = scene.TurntableCamera(fov=0, elevation=y - 180, azimuth=180, roll=0, up='-y') # left
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    elif y > 90 and y <= 180:   
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=180 - y, azimuth=0, roll=0, up='-y') # right
        vb3.camera = scene.TurntableCamera(fov=0, elevation=y - 180, azimuth=180, roll=0, up='-y') # left
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    elif y > 180 and y < 270:
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=180 - y, azimuth=0, roll=0, up='-y') # right
        vb3.camera = scene.TurntableCamera(fov=0, elevation=y - 180, azimuth=180, roll=0, up='-y') # left
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    elif y == 270:
        # exchange camera 2 & 3 back
        grid.add_widget(vb1, row=0, col=2, row_span=6, col_span=6)
        grid.add_widget(vb2, row=4, col=0, row_span=6, col_span=6)
        grid.add_widget(vb3, row=4, col=4, row_span=6, col_span=6)
        grid.add_widget(vb4, row=8, col=2, row_span=6, col_span=6)
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=y - 360, azimuth=0, roll=0, up='+y') # left
        vb3.camera = scene.TurntableCamera(fov=0, elevation=360 - y, azimuth=180, roll=0, up='+y') # right
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    else: # (270, 360)
        vb1.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=180+delta, roll=0, up='-z') # frontal
        vb2.camera = scene.TurntableCamera(fov=0, elevation=y - 360, azimuth=0, roll=0, up='+y') # left
        vb3.camera = scene.TurntableCamera(fov=0, elevation=360 - y, azimuth=180, roll=0, up='+y') # right
        vb4.camera = scene.TurntableCamera(fov=0, elevation=0.0, azimuth=0-delta, roll=0) # occipital

    canvas.update()

# setup timer
timer = app.Timer()
timer.connect(update)
timer.start(.1) # slow this down a bit to better see what happens

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()