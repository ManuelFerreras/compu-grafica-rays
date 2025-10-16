# scene_cpu.py
from typing import List
from camera import Camera
from cube import Cube
from graphics import Graphics
from raytracer import RayTracer

class SceneCPU:
    def __init__(self, camera: Camera):
        self.camera: Camera = camera
        self.objects: List[Cube] = []
        self.ctx = None
        self.gfx: Graphics | None = None

        # render interno reducido
        self.render_scale = 0.33
        self.fb_width = 320
        self.fb_height = 180

        self._acc = 0.0
        self._render_dt = 0.15
        self._needs_redraw = True

        self.ROTATE = True

    def start(self):
        print("[Scene] start(): MODO CPU (Raytracer por software)")
        self.objects = [
            Cube(position=(0.0, 1.0, 0.0),   scale=(1.0, 1.0, 1.0), name="Cube_A"),
            Cube(position=(2.0, 1.0, 0.0),   scale=(1.0, 1.0, 1.0), name="Cube_B_rotY"),
            Cube(position=(-2.0, 1.0, 0.0),  scale=(1.2, 1.2, 0.8), name="Cube_C_scaled"),
        ]
        self.objects[1].rotation.y = 25.0

        self._raytracer = RayTracer(self.camera, self.objects)

        # Sprite pipeline (quad) para mostrar la textura renderizada por CPU
        self.gfx = Graphics(self.ctx)
        self.gfx.load_program_from_files("shaders/sprite.vert", "shaders/sprite.frag")
        self.gfx.create_fullscreen_quad()

        # Primer frame rápido
        self._resize_internal(self.fb_width, self.fb_height)
        self._render_to_texture()

    def _resize_internal(self, w: int, h: int):
        self.fb_width = max(160, int(w))
        self.fb_height = max(90, int(h))

    def _render_to_texture(self):
        img = self._raytracer.render(self.fb_width, self.fb_height)
        self.gfx.update_texture(self.fb_width, self.fb_height, img.get_bytes())
        self._needs_redraw = False

    def update(self, dt: float):
        if self.ROTATE:
            self.objects[1].rotation.y = (self.objects[1].rotation.y + 20.0 * dt) % 360.0
            self._needs_redraw = True

        self._acc += dt
        if self._needs_redraw and self._acc >= self._render_dt:
            self._render_to_texture()
            self._acc = 0.0

    def render(self):
        if self.gfx:
            self.gfx.draw()

    def on_resize(self, width: int, height: int):
        if height == 0:
            height = 1
        self.camera.aspect = width / height
        self.camera.update_matrices()
        self._resize_internal(width * self.render_scale, height * self.render_scale)
        self._needs_redraw = True

    def on_mouse_click(self, u: float, v: float, button: int, modifiers: int):
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
