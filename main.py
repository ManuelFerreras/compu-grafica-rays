# main.py
# Punto de entrada: crea la ventana, la escena y arranca el loop de Pyglet.

import pyglet
from window import AppWindow
from scene import Scene
from camera import Camera

# Resolución “estándar clase” (ajustable luego)
WIDTH, HEIGHT = 960, 540

def main():
    # Creamos una cámara mínima con FOV vertical y aspecto correcto
    camera = Camera(fov_deg=60.0, aspect=WIDTH/HEIGHT)

    # Creamos una escena base (sin objetos por ahora)
    scene = Scene(camera=camera)

    # Ventana Pyglet + ModernGL
    win = AppWindow(width=WIDTH, height=HEIGHT, caption="Ray Project – Etapa 1", resizable=True)
    win.set_scene(scene)   # Esto además llama scene.start()

    # Arranca el loop
    pyglet.app.run()

if __name__ == "__main__":
    main()
