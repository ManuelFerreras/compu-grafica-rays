# ray.py

import glm

class Ray:
    def __init__(self, origin, direction):
        self.__origin = glm.vec3(*origin) if not isinstance(origin, glm.vec3) else glm.vec3(origin)
        d = glm.vec3(*direction) if not isinstance(direction, glm.vec3) else glm.vec3(direction)
        self.__direction = glm.normalize(d)

    @property
    def origin(self) -> glm.vec3:
        return self.__origin

    @property
    def direction(self) -> glm.vec3:
        return self.__direction

    def at(self, t: float) -> glm.vec3:
        # P(t) = origin + t * direction
        return self.__origin + t * self.__direction
