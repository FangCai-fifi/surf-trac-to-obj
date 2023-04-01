import numpy as np

from vispy import app, gloo, io, scene
from vispy.gloo import Program, VertexBuffer, IndexBuffer
from vispy.util.transforms import ortho, perspective, translate, rotate
# from vispy.geometry import create_cube
from utils import read_obj_color

vertex = """
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

attribute vec3 position;
attribute vec4 color;

varying vec4 v_color;
void main()
{
    v_color = color;
    gl_Position = projection * view * model * vec4(position,1.0);
}
"""

fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""

def create_obj(objPath):
    """Generate vertices & indices for an .obj file
    Returns
    -------
    vertices : array
        Array of vertices suitable for use as a VertexBuffer.
    filled : array
        Indices to use to produce a filled cube.
    outline : array
        Indices to use to produce an outline of the cube.
    """
    vtype = [('position', np.float32, 3),
             ('color', np.float32, 4)]
    itype = np.uint32

    verts_surf, faces_surf, normals_surf, nothing_surf = io.read_mesh(objPath)
    # Vertices positions
    p = verts_surf

    # Vertice colors
    c = read_obj_color(objPath)
    if c.shape[1] != 4:
        c = np.resize(np.array([1,1,1,0.2]), (p.shape[0], 4))

    faces_p = np.reshape(faces_surf, (1,-1)).tolist()[0]
    faces_c = np.reshape(faces_surf, (1,-1)).tolist()[0]

    vertices = np.zeros(3*faces_surf.shape[0], vtype)
    vertices['position'] = p[faces_p]
    vertices['color'] = c[faces_c]

    a = np.arange(0, len(faces_p)-3, 3, dtype=itype)
    filled = np.column_stack((a, a+1, a+2))

    # outline = np.resize(np.array([0, 1, 1, 2, 2, 3, 3, 0], dtype=itype), 6 * (2 * 4))
    # outline += np.repeat(4 * np.arange(6, dtype=itype), 8)

    return vertices, filled #, outline


class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=(1024, 1024), title='Rotating brain', keys='interactive')
        
        # Build brain data
        V_trac, I_trac = create_obj(objPath='assets/lh.ilf.obj')
        vertices_trac = VertexBuffer(V_trac)
        self.indices_trac = IndexBuffer(I_trac)

        V_surf, I_surf = create_obj(objPath='assets/pial.obj')
        vertices_surf = VertexBuffer(V_surf)
        self.indices_surf = IndexBuffer(I_surf)

        # Build program
        self.program1 = Program(vertex, fragment)
        self.program2 = Program(vertex, fragment)
        self.program1.bind(vertices_trac)
        self.program2.bind(vertices_surf)

        # Build view, model, projection & normal
        view = translate((0, 0, -128))
        model = np.eye(4, dtype=np.float32)
        self.program1['model'] = model
        self.program1['view'] = view
        self.program2['model'] = model
        self.program2['view'] = view
        self.phi, self.theta = 0, 0
        gloo.set_state(clear_color=(0, 0, 0, 0.5), depth_test=False)

        self.activate_zoom()
        self.timer = app.Timer('auto', self.on_timer, start=True)

        self.show()

    def on_draw(self, event):
        gloo.clear(color=True, depth=True)
        self.program2.draw('triangles', self.indices_surf)
        self.program1.draw('triangles', self.indices_trac)
        

    def on_resize(self, event):
        self.activate_zoom()

    def activate_zoom(self):
        gloo.set_viewport(0, 0, *self.physical_size)
        projection = ortho(-200, 200, -200, 200, -200, 200)
        self.program1['projection'] = projection
        self.program2['projection'] = projection

    def on_timer(self, event):
        self.theta += 0
        self.phi += 0.5
        self.program1['model'] = np.dot(rotate(self.theta, (0, 0, 1)),
                                       rotate(self.phi, (0, 1, 0)))
        self.program2['model'] = np.dot(rotate(self.theta, (0, 0, 1)),
                                       rotate(self.phi, (0, 1, 0)))
        self.update()


if __name__ == '__main__':
    c = Canvas()
    app.run()