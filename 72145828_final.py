import random
import pyxel
import math

# ====== create EnemyList ======
enemy_list = []
enemy2_list = []
enemy3_list = []
# ====== gravity set ======
gravity = -0.7
# ====== create Fire ======
fire_list = []
# ====== create Fruit =====
fruit_list = []

# ====== 敵の出現するペース =====
enemy_pace = 20
enemy2_pace = 30
enemy3_pace = 50

# ====== constants ========
SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player:
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.health = 5
        self.amo = 5
        self.shot = False

    def move(self, x, y):
        self.pos.x = x
        self.pos.y = y
        
        if y <= 0:
            self.pos.y = 0
        elif y >= 184:
            self.pos.y = 184
            
    def reload(self):
        self.amo = 5
            
class Enemy:
    def __init__(self):
        self.pos = Vec2(184, random.randint(0,170))
        self.speed = 2
        self.dir = 1
        self.time = 0
            
    def move(self, x, y):
        self.pos.x = x
        self.pos.y = y

class Enemy2:
    def __init__(self):
        self.pos = Vec2(184, random.randint(0,184))
        self.speed = 1.5
    
    def move(self, x, y):
        self.pos.x = x
        self.pos.y = y
        
class Enemy3:
    def __init__(self):
        self.originy = random.randint(0, 184)
        self.pos = Vec2(184, self.originy)
        self.speed = 2
        angle = math.radians(random.randint(120, 210))
        self.dirx = math.cos(angle)
        self.diry = math.sin(angle) 
        self.flag = False
        self.randpos = random.randint(30,150)
        self.health = 3
    
    def move(self, x, y):
        self.pos.x = x
        self.pos.y = y
        
        if ((self.originy + 30 <= self.pos.y) 
            or (self.originy - 30 >= self.pos.y)):
            self.diry *= -1
        
class Fire:
    def __init__(self, x, y):
        self.pos = Vec2(x + 8, y + 4)
        self.speed = 2
    
    def move(self, x, y):
        self.x = x
        self.y = y
    
class Fruit:
    def __init__(self):
        self.pos = Vec2(192, random.randint(0,192))
        self.speed = 1.5
    
    def move(self, x, y):
        self.x = x
        self.y = y
        
        
# =======　以下Appクラス ========

class App:
    def __init__(self):
        pyxel.init(200,200)
        pyxel.load("res.pyxres")
        pyxel.mouse(True)
        self.scene = SCENE_TITLE
        # ====== create Player ======
        self.player = Player()
        self.score = 0
        
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()
            
    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY

    def update_play_scene(self):    
        # ======= ctrl Player ======
        self.player.move(10, pyxel.mouse_y)
            
        # ====== ctrl Enemy ====== 
        if pyxel.frame_count % enemy_pace == 0:
            enemy_list.append(Enemy())
            
        enemy_count = len(enemy_list)
        for i in range(enemy_count):
            if 0 < enemy_list[i].pos.x < 200:
                enemy_list[i].pos.x += -enemy_list[i].speed * enemy_list[i].time * enemy_list[i].dir
                enemy_list[i].pos.y += -0.5 * gravity * enemy_list[i].time * enemy_list[i].time * enemy_list[i].dir      
                enemy_list[i].time += 0.05
                enemy_list[i].move(enemy_list[i].pos.x, enemy_list[i].pos.y)
                
            elif ((enemy_list[i].pos.x - 16 <= self.player.pos.x <= enemy_list[i].pos.x + 16)
                and (enemy_list[i].pos.y - 16 <= self.player.pos.y <= enemy_list[i].pos.y + 16)):
                self.player.health -= 1
                pyxel.play(2, 2)
                del enemy_list[i] 
            else:
                del enemy_list[i]
                break
        
        # ====== ctrl Enemy2 ====== 
        if pyxel.frame_count % enemy2_pace == 0:
            enemy2_list.append(Enemy2())
            
        enemy2_count = len(enemy2_list)
        for i in range(enemy2_count):
            if 0 < enemy2_list[i].pos.x < 200:
                enemy2_list[i].pos.x -= enemy2_list[i].speed
                enemy2_list[i].speed += 0.1
                    
                enemy2_list[i].move(enemy2_list[i].pos.x, enemy2_list[i].pos.y)
            
            elif ((enemy2_list[i].pos.x <= self.player.pos.x <= enemy2_list[i].pos.x + 16)
                and (enemy2_list[i].pos.y <= self.player.pos.y <= enemy2_list[i].pos.y + 16)):
                self.player.health -= 1
                pyxel.play(2, 2)
                del enemy2_list[i]
                
            else:
                del enemy2_list[i]
                break
        
        # ====== ctrl Enemy3 ======
        if pyxel.frame_count % enemy3_pace == 0:
            enemy3_list.append(Enemy3())
            
        enemy3_count = len(enemy3_list)
        for i in range(enemy3_count):      
            if 0 < enemy3_list[i].pos.x < 200:
                enemy3_list[i].pos.x += enemy3_list[i].speed * enemy3_list[i].dirx
                enemy3_list[i].pos.y += enemy3_list[i].speed * enemy3_list[i].diry  
                enemy3_list[i].move(enemy3_list[i].pos.x, enemy3_list[i].pos.y)
                #形態変化
                if enemy3_list[i].pos.x <= enemy3_list[i].randpos:
                    enemy3_list[i].flag = True
            elif ((enemy3_list[i].pos.x <= self.player.pos.x <= enemy3_list[i].pos.x + 32)
                and (enemy3_list[i].pos.y <= self.player.pos.y <= enemy3_list[i].pos.y + 32)):
                self.player.health -= 3
                pyxel.play(3, 3)
                del enemy3_list[i]
            else:
                del enemy3_list[i]
                break

        # ====== ctrl Fire ====== 
        if self.player.amo > 0:    
            if pyxel.btnp(pyxel.KEY_SPACE):
                fire_list.append(Fire(self.player.pos.x, self.player.pos.y))
                self.player.amo -= 1
                self.player.shot = True
                pyxel.play(1,5)
            
            if pyxel.btnr(pyxel.KEY_SPACE):
                self.player.shot = False

        if pyxel.btnp(pyxel.KEY_R):
            self.player.reload()        
            self.player.shot = False
            pyxel.play(1,4)
                
        fire_count = len(fire_list)
        for i in range(fire_count):
            if 0 < fire_list[i].pos.x < 150:
                fire_list[i].pos.x += fire_list[i].speed      
                fire_list[i].move(10 + 16, self.player.pos.y + 16)
                
                enemy_count = len(enemy_list)
                for j in range(enemy_count):
                    if ((enemy_list[j].pos.x < fire_list[i].pos.x < enemy_list[j].pos.x + 16)
                        and (enemy_list[j].pos.y < fire_list[i].pos.y < enemy_list[j].pos.y + 16)):
                        del enemy_list[j]
                        del fire_list[i]
                        self.score += 1
                        break
                    
                enemy2_count = len(enemy2_list)
                for j in range(enemy2_count):
                    if ((enemy2_list[j].pos.x < fire_list[i].pos.x < enemy2_list[j].pos.x + 16)
                        and (enemy2_list[j].pos.y < fire_list[i].pos.y < enemy2_list[j].pos.y + 16)):
                        del enemy2_list[j]
                        del fire_list[i]
                        self.score += 1
                        break
                
                enemy3_count = len(enemy3_list)
                for j in range(enemy3_count):
                    if ((enemy3_list[j].pos.x < fire_list[i].pos.x < enemy3_list[j].pos.x + 32)
                        and (enemy3_list[j].pos.y < fire_list[i].pos.y < enemy3_list[j].pos.y + 32)):
                        enemy3_list[j].health -= 1
                        del fire_list[i]
                    if enemy3_list[j].health <0:
                        del enemy3_list[j]
                        self.score += 3
            else:
                del fire_list[i]
                break 
            
        # ======= ctrl Fruit ======
        if pyxel.frame_count % 300 == 0:
            fruit_list.append(Fruit())
            
        fruit_count = len(fruit_list)
        for i in range(fruit_count):
            if 0 < fruit_list[i].pos.x < 200:
                fruit_list[i].pos.x -= fruit_list[i].speed
                fruit_list[i].move(fruit_list[i].pos.x, fruit_list[i].pos.y)
                
                if ((self.player.pos.x  <= fruit_list[i].pos.x <= self.player.pos.x + 16)
                    and (self.player.pos.y <= fruit_list[i].pos.y <= self.player.pos.y + 16)):
                    self.player.health += 5
                    pyxel.play(1, 1)
                    del fruit_list[i]
            else:
                del fruit_list[i]
                break
        
        # ======= GAME OVER ======
        if self.player.health <= 0:
            self.scene = SCENE_GAMEOVER

    def update_gameover_scene(self):
        enemy_list.clear()
        enemy2_list.clear()
        enemy3_list.clear()
        fire_list.clear()
        fruit_list.clear()
        
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
            self.player.health = 5
            self.player.amo = 5
            self.score = 0
            
            enemy_list.clear()
            enemy2_list.clear()
            enemy3_list.clear()
            fire_list.clear()
            fruit_list.clear()  
            
    def draw(self):
        pyxel.cls(7)
        
        if self.scene == SCENE_TITLE:
            pyxel.text(70, 20, "Shooting Dragon", pyxel.frame_count % 16)
            pyxel.text(70, 180, "- PRESS ENTER -", 13)
            
        elif self.scene == SCENE_PLAY:
            # ======= show Player ======
            if self.player.shot == True:
                pyxel.blt(self.player.pos.x, self.player.pos.y, 0, 16, 0, 16, 16, 7)
            else:
                pyxel.blt(self.player.pos.x, self.player.pos.y, 0, 0, 0, 16, 16, 7)

            # ======= show Enemy =======
            for new_enemy in enemy_list:
                pyxel.blt(new_enemy.pos.x, new_enemy.pos.y, 1, 0, 0, 16, 16, 7)
            
            # ======= show Enemy2 =======
            for new_enemy2 in enemy2_list:
                pyxel.blt(new_enemy2.pos.x, new_enemy2.pos.y, 1, 0, 0, 16, 16, 7)
            
            # ======= show Enemy3 =======
            for new_enemy3 in enemy3_list:
                if new_enemy3.flag == False:
                    pyxel.blt(new_enemy3.pos.x, new_enemy3.pos.y, 1, 0, 16, 16, 16, 7)
                if new_enemy3.flag == True:
                    pyxel.blt(new_enemy3.pos.x, new_enemy3.pos.y, 1, 0, 32, 32, 32, 7)

            # ======= show Fire =======
            for fire in fire_list:
                pyxel.blt(fire.pos.x, fire.pos.y, 0, 40, 0, 8, 8, 7)
                
            for fruit in fruit_list:
                pyxel.blt(fruit.pos.x, fruit.pos.y, 0, 0, 32, 8, 8, 7)
                
            if self.player.amo == 0:
                pyxel.text(65, 100, "press R to RELOAD!!", 8)
            
            pyxel.text(80,10, "score:" + str(self.score), 0)
            pyxel.text(80,20, "health:"+ str(self.player.health), 8)
            pyxel.text(85, 180, "amo:" + str(self.player.amo), 5)
            pyxel.text(65, 190, "press R to reload", 13)
        
        elif self.scene == SCENE_GAMEOVER:
            pyxel.text(80, 20, "GAME OVER", 8)
            pyxel.text(70, 180, "- PRESS ENTER -", 13)
            
App()