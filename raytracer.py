# raytracer.py

import numpy as np
from texture import ImageData

class RayTracer:
    def __init__(self, camera, objects):
        self.camera = camera
        self.objects = objects
        self.color_hit = np.array([210, 50, 60], dtype=np.uint8)

    def render(self, width: int, height: int) -> ImageData:
        img = ImageData(width, height, channels=3)

        sky_rows = np.zeros((height, 3), dtype=np.uint8)
        for j in range(height):
            v = 1.0 - (j + 0.5) / height
            sky = self.camera.get_sky_gradient(v)
            sky_rows[j] = np.clip(np.array([sky.x, sky.y, sky.z]) * 255.0, 0, 255).astype(np.uint8)
        img.pixels[:] = sky_rows[:, None, :]

        for j in range(height):
            v = 1.0 - (j + 0.5) / height
            for i in range(width):
                u = (i + 0.5) / width
                ray = self.camera.raycast(u, v)

                closest_t = float('inf')
                hit_any = False
                for obj in self.objects:
                    res = obj.check_hit(ray.origin, ray.direction)
                    if res.hit and res.t_near < closest_t:
                        closest_t = res.t_near
                        hit_any = True

                if hit_any:
                    img.pixels[j, i] = self.color_hit

        return img
