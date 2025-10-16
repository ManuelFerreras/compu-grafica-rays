# main.py

import pyglet
from window import AppWindow
from scene import Scene
from camera import Camera

WIDTH, HEIGHT = 960, 540

def main():
    # Creamos una cámara mínima con FOV vertical y aspecto correcto
    camera = Camera(fov_deg=60.0, aspect=WIDTH/HEIGHT)

    # Creamos una escena base
    scene = Scene(camera=camera)

    # Ventana Pyglet + ModernGL
    win = AppWindow(width=WIDTH, height=HEIGHT, caption="Proyecto de Computación Gráfica - Manuiel Ferreras - Matías Carbel", resizable=True)
    win.set_scene(scene)

    # Arranca el loop
    pyglet.app.run()

if __name__ == "__main__":
    main()
