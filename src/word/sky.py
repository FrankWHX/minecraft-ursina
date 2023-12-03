from ursina import *


# 天空
class Sky(Entity):
    def __init__(self, texture):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=texture,
            scale=300,
            double_sided=True,
        )
