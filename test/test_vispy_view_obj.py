from vispy import scene, io

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()


# read an obj and create a mesh in the view
verts, faces, normals, nothing = io.read_mesh('assets/pial.obj')
mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth')
view.add(mesh)

# read an obj and create a mesh in the view
verts, faces, normals, nothing = io.read_mesh('assets/lh.ilf.obj')
mesh1 = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth')
view.add(mesh1)


view.camera = scene.TurntableCamera()
view.camera.depth_value = 10

if __name__ == '__main__':
    canvas.app.run()