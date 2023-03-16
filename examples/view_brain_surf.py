from vispy import scene, io

# create a scene
canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()


# read an obj and create a mesh in the view
verts, faces, normals, nothing = io.read_mesh('assets/pial.obj')
mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth')
view.add(mesh)


# camera type and params
view.camera = scene.TurntableCamera()
view.camera.depth_value = 10

if __name__ == '__main__':
    canvas.app.run()