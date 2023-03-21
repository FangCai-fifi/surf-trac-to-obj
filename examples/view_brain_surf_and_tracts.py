from vispy import scene, io
from utils import read_obj_color
from vispy.visuals.filters import Alpha


TRKLIST = ['lh.atr', 'lh.cab', 'lh.ccg', 'lh.cst', 'lh.ilf', 'lh.slfp', 'lh.slft', 'lh.unc',
           'rh.atr', 'rh.cab', 'rh.ccg', 'rh.cst', 'rh.ilf', 'rh.slfp', 'rh.slft', 'rh.unc',
           'fmajor', 'fminor']

# create a scene
canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', show=True)
view = canvas.central_widget.add_view()


# read an obj and create a mesh in the view
for item in TRKLIST:
    # print(item)
    verts, faces, normals, nothing = io.read_mesh(f"assets/{item}.obj")
    verts_color = read_obj_color(objfile=f"assets/{item}.obj")
    trac_mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth', vertex_colors=verts_color)
    trac_mesh.attach(Alpha(0.7))
    view.add(trac_mesh)

verts, faces, normals, nothing = io.read_mesh('assets/pial.obj')
surf_mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth', color=(1,1,1))
surf_mesh.attach(Alpha(0.2))
view.add(surf_mesh)

# camera type and params
view.camera = scene.TurntableCamera()
view.camera.depth_value = 10

if __name__ == '__main__':
    canvas.app.run()