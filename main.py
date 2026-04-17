import arcade 
import math
import time
from coords import COORDS, COORDS_SNIPERS

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shooter"



    

class Animate(arcade.Sprite):
    i = 0
    time = 0
    def update_animation(self, delta_time):
        self.time += delta_time
        if self.time >= 0.1:
            self.time = 0
            if self.i == len(self.textures)-1:
                self.i = 0
            else:
                self.i += 1
            self.set_texture(self.i)

class Sniper (Animate):
    def __init__(self, window):
        super().__init__("animate/sniper/sniper_angle.png", 1)
        self.lifes=3
        self.sniper_left = arcade.load_texture("animate/sniper/sniper_forward.png", flipped_horizontally=True)
        self.sniper_right = arcade.load_texture("animate/sniper/sniper_forward.png", flipped_horizontally=False)
        self.sniper_left_angle = arcade.load_texture("animate/sniper/sniper_angle.png", flipped_horizontally= True)
        self.sniper_right_angle = arcade.load_texture("animate/sniper/sniper_angle.png", flipped_horizontally= False)
        self.window= window
        self.reloaded_time = time.time ()
        
    def shot (self, direction_x, direction_y):
        if time.time () - self.reloaded_time > 3:
            x= self.center_x
            y= self.center_y
            new_bullet = Sniper_bullet (self.window, direction_x, direction_y, x,y)
            self.window.sniper_bullets.append(new_bullet)
            self.reloaded_time = time.time ()
        
    def update (self):
        if self.window.bill.center_y  < self.center_y:
            if self.window.bill.center_x < self.center_x:
                self.texture = self.sniper_right_angle
                self.shot(-10, -10)
            else:
                self.texture = self.sniper_left_angle
                self.shot(10,-10)
        else:
            if self.window.bill.center_x < self.center_x:
                self.texture = self.sniper_right
            else:
                self.texture = self.sniper_left
               

class Runman (Animate):
    def __init__(self, window):
        super().__init__("animate/runman/frame-01.gif", 2)
        self.lifes = 3
        self.left_textures = []
        self.right_textures = []
        self.window= window
        for i in range (1,10):
            self.left_textures.append(arcade.load_texture(f"animate/runman/frame-0{i}.gif", flipped_horizontally=True))
            self.right_textures.append(arcade.load_texture(f"animate/runman/frame-0{i}.gif", flipped_horizontally=False))
        self.side = False

    def set_side(self):
        if self.side:
            self.textures = self.left_textures
        else:
            self.textures=self.right_textures

    def update (self):
        if self.window.bill.center_x > self.center_x:
            self.side = True
        else:
            self.side = False
        self.set_side()
        if abs(self.center_x-self.window.bill.center_x) < 600:
            if self.window.bill.center_x < self.center_x:
                self.change_x = -1
            else:
                self.change_x = 1
        else:
            self.change_x=0     

class Bullet (arcade.Sprite):
    def __init__(self, window):
        super().__init__("bullet.png", 0.05)
        self.change_x = -25
        self.window = window 
        if self.window.bill.side:
            self.change_x = -25
        else:
            self.change_x = 25
        self.shoot_sound = arcade.load_sound("sounds/shoot.wav")

    def update(self):
        self.center_x += self.change_x
        distance_x = self.center_x - self.window.bill.center_x
        distance_y = self.center_y - self.window.bill.center_y
        distance = math.hypot ( distance_x, distance_y)
        print(self.window.bill.side)

        if distance > 300:
            self.remove_from_sprite_lists()
            
class Sniper_bullet (Bullet):
    def __init__(self, window, direction_x, direction_y, x,y):
        super().__init__(window)
        self.set_position(x,y + 10)
        self.change_x = direction_x
        self.change_y = direction_y
        
    def update (self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        
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
        self.is_moving = False
        self.left_down_textures = arcade.load_texture(f"bill_textures/BillLayingDown.png", flipped_horizontally= True)
        self.right_down_textures = arcade.load_texture(f"bill_textures/BillLayingDown.png", flipped_horizontally= False)
        self.side = False
        for i in range (6):
            self.left_textures.append(arcade.load_texture(f"go_bill/{i}.gif", flipped_horizontally=True))
            self.right_textures.append(arcade.load_texture(f"go_bill/{i}.gif", flipped_horizontally=False))
        self.jump_sound = arcade.load_sound("animate/sounds/jump.wav")

    def update (self):
        self.center_x += self.change_x
        self.center_y += self.change_y
    def set_side(self):
        if self.side:
            self.textures = self.left_textures
        else:
            self.textures = self.right_textures
    def to_down (self):
        if self.side:
            self.texture = self.left_down_textures
        else:
            self.texture = self.right_down_textures  
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
        self.lines = arcade.SpriteList ()
        self.lines_for_level = []
        self.runmans_for_level= []
        self.snipers_for_level= []
        self.snipers = arcade.SpriteList ()
        self.runmans_engine = []
        self.draw_lines_for_level = arcade.SpriteList()
        self.bullets = arcade.SpriteList ()
        self.sniper_bullets = arcade.SpriteList ()
        self.down_pressed = False
        self.enemies = arcade.SpriteList()
        self.setup ()
        self.bill = Bill ()
        self.engine = arcade.PhysicsEnginePlatformer(self.bill, self.lines, 1)      

    def append_line (self, side):
        self.append_runman(side)
        self.append_sniper(side)
        if side:
            for i in range(len(self.lines_for_level[self.index_texture+side])):
                self.lines.pop() 

        for new_line in self.lines_for_level[self.index_texture]:
            self.lines.append(new_line)    
            
    def append_sniper(self,side):
        if side:
            for i in range(len(self.snipers_for_level[self.index_texture+side])):
                self.snipers.pop()
        for new_sniper in self.snipers_for_level[self.index_texture]:
            self.snipers.append(new_sniper)

    def append_runman(self, side):
        #self.enemies.clear()
        self.runmans_engine.clear()
        if side:
            for i in range(len(self.runmans_for_level[self.index_texture+side])):
                self.enemies.pop()

        for new_runman in self.runmans_for_level[self.index_texture]:
            self.enemies.append(new_runman)
            self.runmans_engine.append(arcade.PhysicsEnginePlatformer(new_runman, self.lines, 1))
            
        
    def setup (self):
        for i in range (0, 801, 100):
            low_line = Line()
            low_line.set_position(i,20)
            self.lines.append(low_line)
            low_line.visible=False
    
        for i, lines in enumerate (COORDS):
            self.lines_for_level.append ([])
            self.runmans_for_level.append ([])
            for x,y in lines:
                other_line = Line ()
                other_line.set_position (x,y)
                self.lines_for_level[i].append(other_line)
               #runmans
                self.runman=Runman(self)
                self.runman.center_x = x
                self.runman.center_y = y + 50
                self.runmans_for_level [i].append(self.runman)
                
        for i, lines in enumerate (COORDS_SNIPERS):
            self.snipers_for_level.append ([])
            for x,y in lines:
                sniper = Sniper(self)
                sniper.set_position(x,y)
                self.snipers_for_level[i].append(sniper)
                
        self.append_line(0)       

    def on_draw (self):
        self.clear ()
        arcade.draw_texture_rectangle (SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_list[self.index_texture])
        self.bill.draw ()
        self.lines.draw()
        self.bullets.draw()
        self.enemies.draw()
        self.snipers.draw()
        self.sniper_bullets.draw()

    def update (self,dt):
        self.enemies.update_animation(dt)
        self.enemies.update()
        self.bullets.update()
        self.bill.update ()
        self.sniper_bullets.update ()
        self.snipers.update()
        if self.bill.is_moving:
            self.bill.update_animation(dt)
        self.lines.update()
        self.engine.update()
        if self.bill.back_left():
            if self.index_texture != len(self.bg_list) -1:
                self.index_texture += 1
                self.append_line(-1)
        elif self.bill.back_right():
            if self.index_texture != 0:
                self.index_texture -= 1
                self.append_line(1)
        for runman in self.runmans_engine:
            runman.update()
        #self.runman.update() 

    def on_key_press(self, key, modifiers):
        if arcade.key.A == key:
           self.bill.change_x= -5
           self.bill.side = True
           self.bill.is_moving = True
           self.bill.set_side()
        if arcade.key.D == key:
            self.bill.change_x = 5
            self.bill.side = False
            self.bill.is_moving = True
            self.bill.set_side()
        if arcade.key.F == key:
            self.bill.to_down ()
            self.down_pressed = True   
        if arcade.key.G== key:
            arcade.play_sound(self.bill.jump_sound)
            if self.engine.can_jump():
                self.engine.jump(15)
        if arcade.key.SPACE == key:
            bullet = Bullet(self)
            arcade.play_sound(bullet.shoot_sound)
            bullet.center_x = self.bill.center_x + 10
            #bullet.change_x = 25
            bullet.center_y = self.bill.center_y + 10
            self.bullets.append(bullet)
    
            if self.down_pressed == True:
                bullet.center_y = self.bill.center_y -15
            else:
                bullet.center_y = self.bill.center_y +10
        

    def on_key_release(self, key, modifiers):
        if arcade.key.A == key or arcade.key.D == key or arcade.key.F == key or arcade.key.SPACE == key:
           self.bill.change_x= 0
           self.bill.is_moving = False
           self.bill.set_texture(0)
           self.down_pressed = False

window = My_game (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)  
arcade.run ()  

#hw: left right shot for sniper_bullet and fix sound 