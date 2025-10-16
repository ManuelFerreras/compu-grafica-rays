# window.py
import pyglet
import moderngl
from pyglet.window import key, mouse

from camera import Camera

class AppWindow(pyglet.window.Window):
    def __init__(self, width=1280, height=720, caption="", resizable=True):
        super().__init__(width=width, height=height, caption=caption, resizable=resizable)
        self.ctx = moderngl.create_context()
        self.clear_color = (0.06, 0.06, 0.08, 1.0)
        self.scene = None

        # Estado de teclado continuo
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self._last_drag_x = None
        self._last_drag_y = None

        pyglet.clock.schedule_interval(self.update, 1/60)

    def set_scene(self, scene):
        """Setea una nueva escena y la inicializa correctamente."""
        if self.scene and hasattr(self.scene, "dispose"):
            try:
                self.scene.dispose()
            except Exception:
                pass

        self.scene = scene
        if self.scene:
            self.scene.ctx = self.ctx
            self.scene.start()
            self.scene.on_resize(self.width, self.height)

    def _switch_scene(self, mode: str):
        """
        Cambia de escena manteniendo la misma cámara para no perder la posición.
        mode: 'normal' | 'cpu' | 'gpu'
        """
        # Reusar la cámara actual si existe, sino crear una nueva
        cam = self.scene.camera if (self.scene and hasattr(self.scene, "camera")) else Camera()

        if mode == "normal":
            from scene_normal import SceneNormal
            new_scene = SceneNormal(cam)
        elif mode == "cpu":
            from scene_cpu import SceneCPU
            new_scene = SceneCPU(cam)
        elif mode == "gpu":
            from scene_gpu import SceneGPU
            new_scene = SceneGPU(cam)
        else:
            print(f"[UI] Modo desconocido: {mode}")
            return

        self.set_scene(new_scene)
        self.set_caption(f"{mode.upper()}")
        print(f"[UI] Cambiado a modo: {mode}")

    def on_draw(self):
        self.clear()
        self.ctx.clear(*self.clear_color)
        if self.scene:
            self.scene.render()

    def update(self, dt: float):
        if not self.scene:
            return

        # Movimiento cámara
        f = (1 if self.keys[key.W] else 0) - (1 if self.keys[key.S] else 0)
        r = (1 if self.keys[key.D] else 0) - (1 if self.keys[key.A] else 0)
        u = (1 if self.keys[key.E] else 0) - (1 if self.keys[key.Q] else 0)
        if (f or r or u) and hasattr(self.scene, "camera") and hasattr(self.scene.camera, "move"):
            self.scene.camera.move(float(f), float(r), float(u), dt)

        if hasattr(self.scene, "update"):
            self.scene.update(dt)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        if hasattr(self, "ctx") and self.ctx is not None:
            self.ctx.viewport = (0, 0, width, height)
        if self.scene:
            self.scene.on_resize(width, height)

    def on_key_press(self, symbol, modifiers):
        # F1/F2/F3: cambiar de escena en vivo
        if symbol == key.F1:
            self._switch_scene("normal")
        elif symbol == key.F2:
            self._switch_scene("cpu")
        elif symbol == key.F3:
            self._switch_scene("gpu")

    def on_mouse_press(self, x, y, button, modifiers):
        if self.scene:
            u = x / self.width
            v = y / self.height
            self.scene.on_mouse_click(u, v, button, modifiers)

        if button == mouse.RIGHT:
            self._last_drag_x = x
            self._last_drag_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.RIGHT:
            self._last_drag_x = None
            self._last_drag_y = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.scene:
            return
        if buttons & mouse.RIGHT:
            if hasattr(self.scene, "camera") and hasattr(self.scene.camera, "look"):
                self.scene.camera.look(dx, -dy)
