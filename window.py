# window.py
import pyglet
import moderngl
from pyglet.window import key, mouse

class AppWindow(pyglet.window.Window):
    def __init__(self, width=1280, height=720, caption="Ray Project", resizable=True):
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
        self.scene = scene
        if self.scene:
            self.scene.ctx = self.ctx
            self.scene.on_resize(self.width, self.height)
            self.scene.start()

    def on_draw(self):
        self.clear()
        self.ctx.clear(*self.clear_color)
        if self.scene:
            self.scene.render()

    def update(self, dt: float):
        if not self.scene:
            return

        # ---- Movimiento cámara: WASD + Q/E ----
        f = (1 if self.keys[key.W] else 0) - (1 if self.keys[key.S] else 0)   # forward/back
        r = (1 if self.keys[key.D] else 0) - (1 if self.keys[key.A] else 0)   # right/left
        u = (1 if self.keys[key.E] else 0) - (1 if self.keys[key.Q] else 0)   # up/down
        if f or r or u:
            self.scene.camera.move(float(f), float(r), float(u), dt)

        self.scene.update(dt)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        if hasattr(self, "ctx") and self.ctx is not None:
            self.ctx.viewport = (0, 0, width, height)
        if self.scene:
            self.scene.on_resize(width, height)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.scene:
            u = x / self.width
            v = y / self.height
            self.scene.on_mouse_click(u, v, button, modifiers)

        # Para mouse-look con botón derecho, inicializamos el delta
        if button == mouse.RIGHT:
            self._last_drag_x = x
            self._last_drag_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        # Reset del drag cuando soltamos botón derecho
        if button == mouse.RIGHT:
            self._last_drag_x = None
            self._last_drag_y = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """
        Mouse look: si el botón derecho está presionado, rotamos la cámara
        con el delta del mouse (dx,dy). Mantiene el control de luz por click derecho:
        - Click derecho simple: reorienta la luz
        - Click derecho + arrastrar: rota la cámara
        """
        if not self.scene:
            return

        if buttons & mouse.RIGHT:
            self.scene.camera.look(dx, dy)