from vispy import scene, io
from utils import read_obj_color

# create a scene
canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', show=True)
view = canvas.central_widget.add_view()


# read an obj and create a mesh in the view
verts, faces, normals, nothing = io.read_mesh('assets/lh.ilf.obj')
verts_color = read_obj_color(objfile='assets/lh.ilf.obj')
mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth', vertex_colors=verts_color)
view.add(mesh)


# camera type and params
view.camera = scene.TurntableCamera()
view.camera.depth_value = 10

if __name__ == '__main__':
    canvas.app.run()