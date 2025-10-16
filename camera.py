# camera.py
import glm
from ray import Ray
import math

class Camera:
    def __init__(self, fov_deg: float = 60.0, aspect: float = 16/9.0, near: float = 0.1, far: float = 100.0):
        self.fov_deg = float(fov_deg)
        self.aspect = float(aspect)
        self.near = float(near)
        self.far = float(far)

        # Posición / orientación inicial
        self.position = glm.vec3(0.0, 1.0, 3.0)
        self.target   = glm.vec3(0.0, 1.0, 0.0)
        self.up       = glm.vec3(0.0, 1.0, 0.0)

        # Control de orientación (en grados)
        self.yaw = -90.0   # mirando hacia -Z
        self.pitch = 0.0

        # Velocidades
        self.speed = 3.0         # unidades por segundo
        self.sensitivity = 0.15  # grados por pixel (aprox)

        # Matrices
        self.view = glm.lookAt(self.position, self.target, self.up)
        self.proj = glm.perspective(glm.radians(self.fov_deg), self.aspect, self.near, self.far)
        self.inv_view = glm.inverse(self.view)

        # Colores del cielo
        self.sky_top = glm.vec3(0.55, 0.75, 0.95)
        self.sky_bottom = glm.vec3(0.90, 0.95, 1.00)

    # -------- Matrices / cielo --------
    def update_matrices(self):
        # Dirección forward a partir de yaw/pitch
        dir_x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        dir_y = math.sin(math.radians(self.pitch))
        dir_z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        forward = glm.normalize(glm.vec3(dir_x, dir_y, dir_z))
        self.target = self.position + forward

        self.view = glm.lookAt(self.position, self.target, self.up)
        self.proj = glm.perspective(glm.radians(self.fov_deg), self.aspect, self.near, self.far)
        self.inv_view = glm.inverse(self.view)

    def set_sky_colors(self, top, bottom):
        self.sky_top = glm.vec3(*top)
        self.sky_bottom = glm.vec3(*bottom)

    def get_sky_gradient(self, h: float) -> glm.vec3:
        h = max(0.0, min(1.0, h))
        return (1.0 - h) * self.sky_bottom + h * self.sky_top

    # -------- Raycast --------
    def raycast(self, u: float, v: float) -> Ray:
        x_ndc = 2.0 * u - 1.0
        y_ndc = 2.0 * v - 1.0
        tan_half_fov = math.tan(math.radians(self.fov_deg) * 0.5)
        dir_cam = glm.normalize(glm.vec3(
            x_ndc * self.aspect * tan_half_fov,
            y_ndc * tan_half_fov,
            -1.0
        ))
        dir_world = glm.normalize(glm.mat3(self.inv_view) * dir_cam)
        return Ray(self.position, dir_world)

    # -------- Movimiento / mirada --------
    def move(self, forward_amt: float, right_amt: float, up_amt: float, dt: float):
        """
        forward_amt: +1 W / -1 S
        right_amt:   +1 D / -1 A
        up_amt:      +1 E / -1 Q
        """
        # Forward en el plano XZ para strafing
        fx = math.cos(math.radians(self.yaw))
        fz = math.sin(math.radians(self.yaw))
        forward = glm.normalize(glm.vec3(fx, 0.0, fz))
        right = glm.normalize(glm.cross(forward, self.up))

        self.position += forward * (forward_amt * self.speed * dt)
        self.position += right   * (right_amt   * self.speed * dt)
        self.position += self.up * (up_amt      * self.speed * dt)
        self.update_matrices()

    def look(self, dyaw_pixels: float, dpitch_pixels: float):
        """
        dyaw_pixels, dpitch_pixels: delta del mouse en píxeles (aprox).
        """
        self.yaw += dyaw_pixels * self.sensitivity
        self.pitch = max(-89.0, min(89.0, self.pitch + dpitch_pixels * self.sensitivity))
        self.update_matrices()