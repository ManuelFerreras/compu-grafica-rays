# cube.py
# Cubo con OBB: la colisión rota/escala/traslada junto con el modelo.

import glm
from hit import HitBoxOBB, HitResult

def _euler_xyz_to_mat(rx_deg: float, ry_deg: float, rz_deg: float) -> glm.mat4:
    rx = glm.radians(rx_deg)
    ry = glm.radians(ry_deg)
    rz = glm.radians(rz_deg)
    Rx = glm.rotate(glm.mat4(1.0), rx, glm.vec3(1,0,0))
    Ry = glm.rotate(glm.mat4(1.0), ry, glm.vec3(0,1,0))
    Rz = glm.rotate(glm.mat4(1.0), rz, glm.vec3(0,0,1))
    # Convención: R = Rz * Ry * Rx (podés cambiarla si preferís otra)
    return Rz * Ry * Rx

class Cube:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="cube"):
        self.name = name
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)     # grados
        self.scale    = glm.vec3(*scale)

        # OBB local: AABB unitario en espacio local [-0.5, 0.5] y usamos la model matrix
        self.obb = HitBoxOBB(get_model_matrix=self.get_model_matrix)

    def get_model_matrix(self) -> glm.mat4:
        T = glm.translate(glm.mat4(1.0), self.position)
        R = _euler_xyz_to_mat(self.rotation.x, self.rotation.y, self.rotation.z)
        S = glm.scale(glm.mat4(1.0), self.scale)
        return T * R * S

    def check_hit(self, origin: glm.vec3, direction: glm.vec3) -> HitResult:
        return self.obb.check_hit(origin, direction)
