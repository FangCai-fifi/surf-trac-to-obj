from vispy import scene, io

TRKLIST = ['lh.atr', 'lh.cab', 'lh.ccg', 'lh.cst', 'lh.ilf', 'lh.slfp', 'lh.slft', 'lh.unc',
           'rh.atr', 'rh.cab', 'rh.ccg', 'rh.cst', 'rh.ilf', 'rh.slfp', 'rh.slft', 'rh.unc',
           'fmajor', 'fminor']

# create a scene
canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()


# read an obj and create a mesh in the view
for item in TRKLIST:
    verts, faces, normals, nothing = io.read_mesh(f"assets/{item}.obj")
    mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth')
    view.add(mesh)


# camera type and params
view.camera = scene.TurntableCamera()
view.camera.depth_value = 10

if __name__ == '__main__':
    canvas.app.run()