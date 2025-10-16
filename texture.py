# texture.py

import numpy as np

class ImageData:
    def __init__(self, width: int, height: int, channels: int = 3):
        assert channels in (3,4)
        self.width = int(width)
        self.height = int(height)
        self.channels = channels
        self.pixels = np.zeros((self.height, self.width, self.channels), dtype=np.uint8)

    def fill_rgb(self, r, g, b):
        self.pixels[..., 0] = np.uint8(r)
        self.pixels[..., 1] = np.uint8(g)
        self.pixels[..., 2] = np.uint8(b)

    def get_bytes(self) -> bytes:
        return self.pixels.tobytes()
