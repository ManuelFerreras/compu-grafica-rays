# scene_normal.py
from typing import List
from camera import Camera
from cube import Cube
from graphics import Graphics
from texture import ImageData
import numpy as np
import glm
import struct

class SceneNormal:
    def __init__(self, camera: Camera):
        self.camera: Camera = camera
        self.objects: List[Cube] = []
        self.ctx = None
        self.gfx: Graphics | None = None
        # Tamaño base de la textura de cielo
        self._tex_w = 640
        self._tex_h = 360

    def start(self):
        print("[Scene] start(): MODO NORMAL (Raycasting)")
        # Objetos (para picking/logs)
        self.objects = [
            Cube(position=(0.0, 1.0, 0.0),   scale=(1.0, 1.0, 1.0), name="Cube_A"),
            Cube(position=(2.0, 1.0, 0.0),   scale=(1.0, 1.0, 1.0), name="Cube_B_rotY"),
            Cube(position=(-2.0, 1.0, 0.0),  scale=(1.2, 1.2, 0.8), name="Cube_C_scaled"),
        ]
        self.objects[1].rotation.y = 25.0

        # Quad + shader de sprite para mostrar un fondo
        self.gfx = Graphics(self.ctx)
        self.gfx.load_program_from_files("shaders/sprite.vert", "shaders/sprite.frag")
        self.gfx.create_fullscreen_quad()

        # Generamos la primera textura con gradiente
        self._upload_sky_texture(self._tex_w, self._tex_h)

    def _upload_sky_texture(self, w: int, h: int):
        if not self.gfx:
            return

        img = ImageData(w, h, channels=3)
        rows = np.zeros((h, 3), dtype=np.uint8)
        for j in range(h):
            v = 1.0 - (j + 0.5) / h
            sky = self.camera.get_sky_gradient(v)
            rows[j] = np.clip(np.array([sky.x, sky.y, sky.z]) * 255.0, 0, 255).astype(np.uint8)
        img.pixels[:] = rows[:, None, :]
        self.gfx.update_texture(w, h, img.get_bytes())

    def update(self, dt: float):
        pass  # sin animación en modo normal

    def render(self):
        if self.gfx:
            self.gfx.draw()

    def on_resize(self, width: int, height: int):
        if height == 0:
            height = 1
        if self.ctx:
            self.ctx.viewport = (0, 0, width, height)
        self.camera.aspect = width / height
        self.camera.update_matrices()

        # Ajustamos resolución de la textura de fondo
        self._tex_w = max(320, width // 2)
        self._tex_h = max(180, height // 2)
        if self.gfx is not None:
            self._upload_sky_texture(self._tex_w, self._tex_h)

    def on_mouse_click(self, u: float, v: float, button: int, modifiers: int):
        # Raycasting CPU para logs
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
