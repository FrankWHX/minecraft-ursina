# this will import everything we need from ursina with just one line.
from ursina import *

app = Ursina()

player = Entity(
    model='cube',           # finds a 3d model by name
    color=color.gold,
    scale_y=1,
    position=(0, 0)  # 位置坐标：(x,y)
)


def update():                  # update gets automatically called by the engine.
    player.x += held_keys['d'] * .1
    player.x -= held_keys['a'] * .1
    player.y += held_keys['w'] * .1
    player.y -= held_keys['s'] * .1


app.run()                     # opens a window and starts the game.
