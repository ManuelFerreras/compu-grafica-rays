# scene.py

from typing import List
from camera import Camera
from cube import Cube
from graphics import Graphics
import glm
import struct
from pyglet.window import mouse  # para mouse.RIGHT

class Scene:
    def __init__(self, camera: Camera):
        self.camera: Camera = camera
        self.objects: List[Cube] = []
        self.ctx = None
        self.gfx: Graphics | None = None
        self.ROTATE = True

        # 💡 Dirección de luz (en mundo), inicial: arriba-izquierda
        self.light_dir = glm.normalize(glm.vec3(-0.5, 1.0, -0.7))

    def start(self):
        print("[Scene] start(): Luz direccional controlable con el mouse (botón derecho)")
        self.objects = [
            Cube(position=(0.0, 1.0, 0.0),   scale=(1.0, 1.0, 1.0), name="Cube_A"),
            Cube(position=(2.0, 1.0, 0.0),   scale=(1.0, 1.0, 1.0), name="Cube_B_rotY"),
            Cube(position=(-2.0, 1.0, 0.0),  scale=(1.2, 1.2, 0.8), name="Cube_C_scaled"),
        ]
        self.objects[1].rotation.y = 25.0

        self.gfx = Graphics(self.ctx)
        self.gfx.load_program_from_files("shaders/raytracing.vert", "shaders/raytracing.frag")
        self.gfx.create_fullscreen_quad()

    def _mat4_to_bytes(self, m: glm.mat4) -> bytes:
        # Column-major consistente
        return struct.pack(
            "16f",
            m[0][0], m[0][1], m[0][2], m[0][3],
            m[1][0], m[1][1], m[1][2], m[1][3],
            m[2][0], m[2][1], m[2][2], m[2][3],
            m[3][0], m[3][1], m[3][2], m[3][3],
        )

    def _colors_to_bytes_vec4(self, colors_rgba):
        flat = []
        for (r, g, b, a) in colors_rgba:
            flat.extend([float(r), float(g), float(b), float(a)])
        return struct.pack(f"{len(flat)}f", *flat)

    def update(self, dt: float):
        if self.ROTATE:
            self.objects[1].rotation.y = (self.objects[1].rotation.y + 30.0 * dt) % 360.0

    def render(self):
        if not self.gfx:
            return
        prog = self.gfx.prog

        # ----- Cámara -----
        prog["u_cam_pos"].value   = (self.camera.position.x, self.camera.position.y, self.camera.position.z)
        prog["u_fov_y"].value     = float(self.camera.fov_deg)
        prog["u_aspect"].value    = float(self.camera.aspect)
        prog["u_inv_view"].write(self._mat4_to_bytes(self.camera.inv_view))

        # ----- Cielo -----
        prog["u_sky_top"].value    = (self.camera.sky_top.x, self.camera.sky_top.y, self.camera.sky_top.z)
        prog["u_sky_bottom"].value = (self.camera.sky_bottom.x, self.camera.sky_bottom.y, self.camera.sky_bottom.z)

        # ----- Luz (controlable) -----
        L = glm.normalize(self.light_dir)
        prog["u_light_dir"].value = (L.x, L.y, L.z)

        # ----- Objetos -----
        MAX_OBJECTS = 16
        num = min(len(self.objects), MAX_OBJECTS)
        prog["u_num_objs"].value = int(num)

        # u_model: subir SIEMPRE 16 mat4 (identidad para los que faltan)
        mats = []
        for i in range(MAX_OBJECTS):
            if i < num:
                m = self.objects[i].get_model_matrix()
            else:
                m = glm.mat4(1.0)
            mats.append(self._mat4_to_bytes(m))
        prog["u_model"].write(b"".join(mats))

        # u_color: subir SIEMPRE 16 vec4 (rgba)
        palette = [
            (0.82, 0.20, 0.24, 1.0),  # A: rojo
            (0.20, 0.65, 0.90, 1.0),  # B: celeste
            (0.15, 0.80, 0.40, 1.0),  # C: verde
        ]
        colors16 = []
        for i in range(MAX_OBJECTS):
            if i < len(self.objects) and i < len(palette):
                colors16.append(palette[i])
            else:
                colors16.append((0.6, 0.6, 0.6, 1.0))  # gris por defecto
        prog["u_color"].write(self._colors_to_bytes_vec4(colors16))

        # Draw
        self.gfx.draw()

    def on_resize(self, width: int, height: int):
        if height == 0:
            height = 1
        self.camera.aspect = width / height
        self.camera.update_matrices()

    def on_mouse_click(self, u: float, v: float, button: int, modifiers: int):
        """
        Click izquierdo: picking (logs).
        Click derecho: reorienta la luz según la posición del click.
        """
        if button == mouse.RIGHT:
            # Mapear coords de ventana (u,v en [0,1]) a una dirección en hemisferio
            x = 2.0 * u - 1.0
            y = 2.0 * v - 1.0
            # z negativo “hacia la escena” para que ilumine desde la pantalla hacia adentro
            self.light_dir = glm.normalize(glm.vec3(x, 1.0, -y))
            print(f"[Light] Dir = ({self.light_dir.x:.2f}, {self.light_dir.y:.2f}, {self.light_dir.z:.2f})")
            return

        # Picking con botón izquierdo (como antes)
        ray = self.camera.raycast(u, v)
        closest_name = None
        closest_t = float('inf')
        for obj in self.objects:
            res = obj.check_hit(ray.origin, ray.direction)
            if res.hit and res.t_near < closest_t:
                closest_t = res.t_near
                closest_name = obj.name
        if closest_name is not None:
            print(f"[Hit] {closest_name} a distancia t={closest_t:.3f}")
        else:
            print("[Miss] No le pegaste a ningún objeto.")