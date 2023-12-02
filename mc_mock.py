from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from enum import IntEnum
import random

# 创建一个全屏窗口
app = Ursina(borderless=True, fullscreen=True, show_ursina_splash=True)

# 设置窗口和场景的属性
window.fps_counter.enabled = False
window.exit_button.visible = False
scene.fog_color = color.white
scene.fog_density = 0.02

# 载入图片资源  1=绿地 2=泥土 3=木板 4=砖块 5=石头
grass_texture = load_texture("Assets/Textures/Grass_Block.png")
dirt_texture = load_texture("Assets/Textures/Dirt_Block.png")
wood_texture = load_texture("Assets/Textures/Wood_Block.png")
brick_texture = load_texture("Assets/Textures/Brick_Block.png")
stone_texture = load_texture("Assets/Textures/Stone_Block.png")
tree_texture = load_texture("Assets/Textures/Tree_Block.png")
leaf_texture = load_texture("Assets/Textures/Leaf_Block.png")
sky_texture = load_texture("Assets/Textures/Skybox.png")
arm_texture = load_texture("Assets/Textures/Arm_Texture.png")


# 载入声音
punch_sound = Audio("Assets/SFX/Punch_Sound.wav", loop=False, autoplay=False)
error_sound = Audio("Assets/SFX/Snap_Sound.wav", loop=False, autoplay=False)


# 方块皮肤的枚举
class BlockPick(IntEnum):
    GRASS_TEXTURE = 1
    DIRT_TEXTURE = 2
    WOOD_TEXTURE = 3
    BRICK_TEXTURE = 4
    STONE_TEXTURE = 5
    TREE_TEXTURE = 6
    LEAF_TEXTURE = 7


# 设置默认方块的图片序号
block_pick = BlockPick.GRASS_TEXTURE

# 地图大小
map_size = 50

# 复活点坐标
map_revive_poit = Vec3(floor(map_size / 2), 50, floor(map_size / 2))
"""复活点坐标"""

# 保存地图数据的字典(x=右 y=高 z=前)  map_dict = { "x|y|z": block_pick, "x|y|z": block_pick }
map_dict = {}

# 是否创建树，默认为不创建
is_create_tree = False


def save_map():
    """保存地图到磁盘上"""
    f = open("data/map.db", "w")
    data_format = "{}:{}\n"
    for k, v in map_dict.items():
        f.write(data_format.format(k, v))
    f.close()


def load_map():
    """从磁盘上加载地图"""
    f = open("data/map.db", "r")
    lines = f.readlines()
    for line in lines:
        # 使用“:”将该行分割为一个列表
        list = line.split(":")

        # 列表的第一位是“x|y|z”格式的坐标字符串，因此使用“｜”分割为坐标的列表
        line_position = list[0].split("|")

        # 列表的第二位是方块的皮肤索引，使用strip()移除换行符后再转为int类型
        line_block_pick = int(list[1].strip())

        # 使用该行值创建方块，注意：通过split方法转换的列表中的数据为字符串，需要通过float转为数字
        Block(
            position=Vec3(
                float(line_position[0]),
                float(line_position[1]),
                float(line_position[2]),
            ),
            block_pick=BlockPick(line_block_pick),
        )
    f.close()

    # 如果磁盘上未加载到地图，则创建新地图
    if len(map_dict) == 0:
        create_map()
        print("创建新地图完成")


def create_map():
    """使用柏林噪声创建地图"""
    noise = PerlinNoise(octaves=3, seed=20231202)
    scale = 24
    for z in range(map_size):
        for x in range(map_size):
            y = floor(noise([x / scale, z / scale]) * 8)

            # 创建草地
            current_position = Vec3(x, y, z)
            Block(position=current_position)

            # 创建草地下面的石头
            behind_position = Vec3(x, y - 1, z)
            Block(position=behind_position, block_pick=BlockPick.STONE_TEXTURE)

            if (random.randint(1, 100)) == 1:
                create_tree(Vec3(x, y + 1, z))

    # 创建复活点
    Block(position=map_revive_poit, block_pick=BlockPick.STONE_TEXTURE)


def create_tree(creata_position):
    Block(position=creata_position, block_pick=BlockPick.TREE_TEXTURE)
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 1,
            creata_position.z,
        ),
        block_pick=BlockPick.TREE_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 2,
            creata_position.z,
        ),
        block_pick=BlockPick.TREE_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 3,
            creata_position.z,
        ),
        block_pick=BlockPick.TREE_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 4,
            creata_position.z,
        ),
        block_pick=BlockPick.TREE_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 5,
            creata_position.z,
        ),
        block_pick=BlockPick.TREE_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 6,
            creata_position.z,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x + 1,
            creata_position.y + 5,
            creata_position.z,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x - 1,
            creata_position.y + 5,
            creata_position.z,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 5,
            creata_position.z + 1,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 5,
            creata_position.z - 1,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x + 1,
            creata_position.y + 4,
            creata_position.z,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x - 1,
            creata_position.y + 4,
            creata_position.z,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 4,
            creata_position.z + 1,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 4,
            creata_position.z - 1,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x + 2,
            creata_position.y + 4,
            creata_position.z,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x - 2,
            creata_position.y + 4,
            creata_position.z,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 4,
            creata_position.z + 2,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x,
            creata_position.y + 4,
            creata_position.z - 2,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x + 1,
            creata_position.y + 4,
            creata_position.z + 1,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x - 1,
            creata_position.y + 4,
            creata_position.z + 1,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x + 1,
            creata_position.y + 4,
            creata_position.z - 1,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )
    Block(
        position=Vec3(
            creata_position.x - 1,
            creata_position.y + 4,
            creata_position.z - 1,
        ),
        block_pick=BlockPick.LEAF_TEXTURE,
    )


def add_block_to_map_dict(position, block_pick):
    """保存创建方块的参数到地图字典变量中"""
    # print("添加地图到字典的位置：", position)
    dict_key = get_map_dict_key(position)
    map_dict[dict_key] = block_pick


def delete_block_from_map_dict(position):
    """从地图字典变量中移除要删除的方块"""
    dict_key = get_map_dict_key(position)

    # 如果dict_key在地图字典map_dict中存在时，再进行删除
    if dict_key in map_dict:
        map_dict.pop(dict_key)


def get_map_dict_key(position):
    """获取地图字典变量的Key"""
    map_dict_key_format = "{}|{}|{}"
    return map_dict_key_format.format(int(position.x), int(position.y), int(position.z))


# 当按下键盘或鼠标按键时，ursina会执行该方法
def input(key):
    # 通过按1～5按键设置不同的方块皮肤
    global block_pick
    global is_create_tree
    if key == "1":
        block_pick = BlockPick(1)
    elif key == "2":
        block_pick = BlockPick(2)
    elif key == "3":
        block_pick = BlockPick(3)
    elif key == "4":
        block_pick = BlockPick(4)
    elif key == "5":
        block_pick = BlockPick(5)
    elif key == "6":
        block_pick = BlockPick(6)
    elif key == "7":
        block_pick = BlockPick(7)
    elif key == "8":
        is_create_tree = True
    elif key == "escape":
        # 按下esc键时，保存地图数据并推出
        save_map()
        quit()
    elif key == "o":
        save_map()

    print("键盘按下：", key)


# ursina在每一帧都会调用该方法
def update():
    if held_keys["left mouse"] or held_keys["right mouse"]:
        hand.active()
    else:
        hand.passive()

    # print("我的位置：", player.position)
    if (
        player.position.x < 0
        or player.position.z < 0
        or player.position.x > map_size - 1
        or player.position.z > map_size - 1
    ):
        print("溢出位置：", player.position)
        player.set_position(map_revive_poit)
        print("复活位置：", player.position)


def get_texture(block_pick):
    if block_pick == BlockPick.GRASS_TEXTURE:
        current_texture = grass_texture
    elif block_pick == BlockPick.DIRT_TEXTURE:
        current_texture = dirt_texture
    elif block_pick == BlockPick.WOOD_TEXTURE:
        current_texture = wood_texture
    elif block_pick == BlockPick.BRICK_TEXTURE:
        current_texture = brick_texture
    elif block_pick == BlockPick.STONE_TEXTURE:
        current_texture = stone_texture
    elif block_pick == BlockPick.TREE_TEXTURE:
        current_texture = tree_texture
    elif block_pick == BlockPick.LEAF_TEXTURE:
        current_texture = leaf_texture
    else:
        current_texture = grass_texture
    return current_texture


# 设置方块的样式
class Block(Button):
    def __init__(self, position=Vec3(0, 0, 0), block_pick=BlockPick.GRASS_TEXTURE):
        """加载方块"""

        # 将创建方块的位置写入到地图字典中
        add_block_to_map_dict(position, block_pick)

        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Block",
            origin_y=0.5,
            texture=get_texture(block_pick),
            color=color.color(0, 0, random.uniform(0.9, 1)),
            # highlight_color=color.green,
            scale=0.5,
        )

    def input(self, key):
        global is_create_tree
        if self.hovered:
            if key == "left mouse down":
                creata_position = self.position + mouse.normal
                print(
                    "我的位置=",
                    player.position,
                    " 创建位置=",
                    creata_position,
                )

                # 是否允许创建方块，默认为允许
                is_allow_create = True

                # 当创建的方块在我的脚下时，设置为不能创建
                if (
                    (
                        creata_position.x == floor(player.position.x)
                        or creata_position.x == ceil(player.position.x)
                    )
                    and (
                        creata_position.y == floor(player.position.y) + 1
                        or creata_position.y == floor(player.position.y) + 2
                    )
                    and (
                        creata_position.z == floor(player.position.z)
                        or creata_position.z == ceil(player.position.z)
                    )
                ):
                    is_allow_create = False
                    print("不能在脚下创建方块")

                # 当创建的方块已经存在时，设置为不能创建
                dict_key = get_map_dict_key(creata_position)
                if dict_key in map_dict:
                    is_allow_create = False
                    print("方块已存在，不能创建")

                # 如果允许创建时，创建方块
                if is_allow_create:
                    if is_create_tree:
                        create_tree(creata_position)
                        is_create_tree = False
                    else:
                        Block(position=creata_position, block_pick=block_pick)
                    punch_sound.play()
                else:
                    error_sound.play()

            if key == "right mouse down":
                # 如果要移除的方块是石头时，不能移除，发出警告音
                if self.texture.name == "Stone_Block.png":
                    error_sound.play()
                else:
                    punch_sound.play()
                    print("即将移除方块：", self.texture.name, self.position)

                    # 从地图字典中要删除要移除的方块
                    delete_block_from_map_dict(self.position)

                    # 移除方块
                    destroy(self)


# 天空
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=sky_texture,
            scale=300,
            double_sided=True,
        )


# 手势
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model="Assets/Models/Arm",
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6),
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)


# 加载数据
load_map()


# 实例化玩家
player = FirstPersonController(speed=5, jump_height=3)

# 设置出生点为复活坐标
player.set_position(map_revive_poit)

# 实例化天空
sky = Sky()

# 实例化手
hand = Hand()

# 运行
app.run()
