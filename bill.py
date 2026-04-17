import arcade 
import math
import time
from animate import*

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shooter"

class Line (arcade.Sprite):
    def __init__(self):
        super().__init__("line.png")

class Bill (Animate):
    def __init__(self):
        super().__init__("go_bill/0.gif", 2)
        self.center_x = 100
        self.center_y = 100
        self.left_textures = []
        self.right_textures = []
        self.is_walk = False
        self.right_down = arcade.load_texture(f"bill_textures/BillLayingDown.png")
        self.left_down = arcade.load_texture(f"bill_textures/BillLayingDown.png", flipped_horizontally= True)
        self.side = True
        for i in range (6):
            self.left_textures.append(arcade.load_texture(f"go_bill/{i}.gif", flipped_horizontally=True))
            self.right_textures.append(arcade.load_texture(f"go_bill/{i}.gif", flipped_horizontally=False))
    def update (self):
        self.center_x += self.change_x
        self.center_y += self.change_y
    def set_side(self):
        if self.side:
            self.textures = self.left_textures
        else:
            self.textures = self.right_textures
    def to_down(self):
        if self.side:
            self.texture = self.left_down
        else:
            self.texture = self.right_down    
    def back_left(self):
        if self.left > SCREEN_WIDTH:
            self.center_x = 0
            return True
        return False
    def back_right(self):
        if self.right < 0:
            self.center_x = SCREEN_WIDTH
            return True
        return False
#animate/background
class My_game (arcade.Window):
    def __init__ (self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.bg_list = []
        for i in range(1,16):
            self.bg_list.append(arcade.load_texture(f"background/Map{i}.png"))
        self.index_texture = 0
        self.bill = Bill ()
        self.lines = arcade.SpriteList()
        self.setup()
        self.engine = arcade.PhysicsEnginePlatformer(self.bill, self.lines, 1)
    def setup (self):
        for i in range (0,801,100):
            low_line = Line()
            low_line.set_position(i,20)
            self.lines.append(low_line)

    def on_draw (self):
        self.clear ()
        arcade.draw_texture_rectangle (SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_list[self.index_texture])
        self.bill.draw ()
        self.lines.draw()

    def update (self,dt):
        self.bill.update ()
        if self.bill.is_walk:
            self.bill.update_animation(dt)
        self.engine.update()
        if self.bill.back_left():
            self.index_texture += 1
        elif self.bill.back_right():
            if self.index_texture > 0:
                self.index_texture -= 1

    def on_key_press(self, key, modifiers):
        if arcade.key.A == key and not self.bill.is_walk: 
           self.bill.change_x= -5
           self.bill.side = True
           self.bill.is_walk = True
           self.bill.set_side()
        if arcade.key.D == key and not self.bill.is_walk:
            self.bill.change_x = 5
            self.bill.side = False
            self.bill.is_walk = True
            self.bill.set_side()
        if arcade.key.S == key:
            self.bill.to_down()
        if arcade.key.F == key:
            if self.engine.can_jump():
                self.engine.jump(15)   


    def on_key_release(self, key, modifiers):
        if arcade.key.A == key or arcade.key.D == key or arcade.key.S == key:
           self.bill.change_x= 0
           self.bill.set_texture(0)
           self.bill.is_walk = False

window = My_game (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)  
arcade.run ()  

#hw: Создать класс Runman, а также отрисовать его один обьект на сцене с анимациями