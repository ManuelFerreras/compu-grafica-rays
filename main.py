# main.py
import pyglet
from window import AppWindow
from camera import Camera

# Elegí: "normal" | "cpu" | "gpu" (modo inicial)
SCENE_TYPE = "gpu"

def main():
    win = AppWindow(width=1280, height=720, caption=f"Ray Project ({SCENE_TYPE.upper()})")
    cam = Camera()

    if SCENE_TYPE == "normal":
        from scene_normal import SceneNormal
        scene = SceneNormal(cam)
    elif SCENE_TYPE == "cpu":
        from scene_cpu import SceneCPU
        scene = SceneCPU(cam)
    elif SCENE_TYPE == "gpu":
        from scene_gpu import SceneGPU
        scene = SceneGPU(cam)
    else:
        raise ValueError("SCENE_TYPE inválido. Usá: 'normal', 'cpu' o 'gpu'.")

    win.set_scene(scene)
    pyglet.app.run()

if __name__ == "__main__":
    main()
