# graphics.py

import moderngl

class Graphics:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.prog = None
        self.vbo = None
        self.ibo = None
        self.vao = None
        self.texture = None

    def load_program_from_files(self, vert_path: str, frag_path: str):
        with open(vert_path, "r", encoding="utf-8") as f:
            v_src = f.read()
        with open(frag_path, "r", encoding="utf-8") as f:
            f_src = f.read()
        self.prog = self.ctx.program(vertex_shader=v_src, fragment_shader=f_src)

    def create_fullscreen_quad(self):
        import struct
        vertices = [
            #   x,   y,   u,  v
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
             1.0,  1.0, 1.0, 1.0,
            -1.0,  1.0, 0.0, 1.0,
        ]
        indices = [0, 1, 2,  0, 2, 3]

        vbin = struct.pack(f"{len(vertices)}f", *vertices)
        ibin = struct.pack(f"{len(indices)}I", *indices)

        self.vbo = self.ctx.buffer(vbin)
        self.ibo = self.ctx.buffer(ibin)

        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vbo, "2f 2f", "in_pos", "in_uv"),
            ],
            self.ibo
        )

    def create_texture(self, width: int, height: int, data: bytes | None = None):
        # Formato RGB 8-bit
        self.texture = self.ctx.texture((width, height), components=3, data=data)
        self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

    def update_texture(self, width: int, height: int, data: bytes):
        if self.texture is None or self.texture.size != (width, height):
            self.create_texture(width, height, data)
        else:
            self.texture.write(data)

    def draw(self):
        # Si hay textura + uniform, la usamos; si no, simplemente dibujamos el quad.
        if self.texture is not None and "u_tex" in self.prog:
            self.texture.use(location=0)
            self.prog["u_tex"].value = 0
        self.vao.render()
