# hit.py
# AABB (igual que antes) + OBB transformando rayo a espacio local con inv(model_matrix).

import glm
from dataclasses import dataclass
from typing import Tuple, Optional, Callable

@dataclass
class HitResult:
    hit: bool
    t_near: float = float('inf')
    t_far: float = float('-inf')

class Hit:
    def check_hit(self, origin: glm.vec3, direction: glm.vec3) -> HitResult:
        raise NotImplementedError

class HitBox(Hit):
    """AABB en espacio de MUNDO."""
    def __init__(self, min_v: Tuple[float,float,float], max_v: Tuple[float,float,float]):
        self.min = glm.vec3(*min_v)
        self.max = glm.vec3(*max_v)

    def check_hit(self, origin: glm.vec3, direction: glm.vec3) -> HitResult:
        return _slab_intersect(origin, direction, self.min, self.max)

class HitBoxOBB(Hit):
    """
    OBB: usamos un AABB en ESPACIO LOCAL, y transformamos el rayo con inv(model_matrix).
    get_model_matrix: Callable[[], glm.mat4]
    """
    def __init__(
        self,
        get_model_matrix: Callable[[], glm.mat4],
        local_min: Tuple[float,float,float] = (-0.5, -0.5, -0.5),
        local_max: Tuple[float,float,float] = ( 0.5,  0.5,  0.5),
    ):
        self.get_model_matrix = get_model_matrix
        self.local_min = glm.vec3(*local_min)
        self.local_max = glm.vec3(*local_max)

    def check_hit(self, origin: glm.vec3, direction: glm.vec3) -> HitResult:
        # 1) Mundo -> Local (usando inv(model))
        M = self.get_model_matrix()
        invM = glm.inverse(M)

        # Transformamos origen como punto (w=1)
        o_local4 = invM * glm.vec4(origin, 1.0)
        o_local = glm.vec3(o_local4.x, o_local4.y, o_local4.z)

        # Para la dirección: transformamos un punto en la dirección y restamos
        p_world = origin + direction
        p_local4 = invM * glm.vec4(p_world, 1.0)
        p_local = glm.vec3(p_local4.x, p_local4.y, p_local4.z)

        d_local = glm.normalize(p_local - o_local)

        # 2) Intersección Slab en el AABB local
        local_res = _slab_intersect(o_local, d_local, self.local_min, self.local_max)
        if not local_res.hit:
            return HitResult(hit=False)

        # 3) Convertimos el punto de impacto a mundo para medir t en mundo
        t_local = local_res.t_near
        hit_local = o_local + d_local * t_local
        hit_world4 = M * glm.vec4(hit_local, 1.0)
        hit_world = glm.vec3(hit_world4.x, hit_world4.y, hit_world4.z)

        # t mundial: proyectamos el vector (hit - origin) sobre la dirección (normalizada)
        w_dir = glm.normalize(direction)
        t_world = glm.dot(hit_world - origin, w_dir)
        return HitResult(hit=True, t_near=float(t_world), t_far=local_res.t_far)

# ---------- helper: método Slab (ray vs AABB) ----------
def _slab_intersect(origin: glm.vec3, direction: glm.vec3, vmin: glm.vec3, vmax: glm.vec3) -> HitResult:
    tmin = float('-inf')
    tmax = float('inf')

    for axis in ('x','y','z'):
        o = getattr(origin, axis)
        d = getattr(direction, axis)
        a_min = getattr(vmin, axis)
        a_max = getattr(vmax, axis)

        if abs(d) < 1e-8:
            if o < a_min or o > a_max:
                return HitResult(hit=False)
        else:
            t1 = (a_min - o) / d
            t2 = (a_max - o) / d
            t_near = min(t1, t2)
            t_far  = max(t1, t2)
            tmin = max(tmin, t_near)
            tmax = min(tmax, t_far)
            if tmin > tmax:
                return HitResult(hit=False)

    if tmax < 0:
        return HitResult(hit=False)
    t_first = tmin if tmin >= 0 else tmax
    return HitResult(hit=True, t_near=t_first, t_far=tmax)
