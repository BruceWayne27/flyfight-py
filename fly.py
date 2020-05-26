import pygame
import random
import math

#初始化界面
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('BruceWayne27')
icon = pygame.image.load('ufo64.png')
pygame.display.set_icon(icon)
bgImg = pygame.image.load('bg.jpg')
#飞机
playerImg = pygame.image.load('player64.png')
playerX = 350
playerY = 500
playerStep = 0
#添加音乐
pygame.mixer.music.load('bg.mp3')
pygame.mixer.music.play(-1)

#射中音效
hitsound = pygame.mixer.Sound('hit.wav')

#Score
score = 0
font =pygame.font.Font('freesansbold.ttf',32)
def show_score():
    text = f"Score:{score}"
    score_render=font.render(text,True,(0,255,0))
    screen.blit(score_render,(10,10))

Gameover=False
overfont =pygame.font.Font('freesansbold.ttf',64)
def check_is_over():
    if Gameover:
        text = "Game Over"
        render = overfont.render(text,True,(255,255,0))
        screen.blit(render, (200, 260))
#敌人
number_of_enemies = 10
class Enemy():
    def __init__(self):
        self.img = pygame.image.load('ufo64.png')
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 260)
        self.step = random.randint(2, 5)
    def reset(self):#重置敌人
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 200)
#计算距离
def distance(bx,by,ex,ey):
    a = bx -ex
    b = by -ey
    return math.sqrt(a*a + b*b)
#子弹
class Bullet():
    def __init__(self):
        self.img = pygame.image.load('bullet.png')
        self.x = playerX +26
        self.y = playerY + 10
        self.step = 10
    def hit(self):
        global score
        for e in enemies:
            if(distance(self.x , self.y , e.x , e.y) < 30):
                #射中
                hitsound.play()
                bullets.remove(self)
                e.reset()#重置敌人
                score += 1


bullets = []#保存现有的子弹
enemies = []
for i in range(number_of_enemies):
    enemies.append(Enemy())

def show_bullets():
    for b in bullets:
        screen.blit(b.img,(b.x,b.y))
        b.hit()#是否击中目标
        b.y -= b.step
        if b.y < 0:
            bullets.remove(b)
def show_enemy():
    global Gameover
    for e in enemies:
        screen.blit(e.img,(e.x,e.y))
        e.x += e.step
        if (e.x > 736 or e.x < 0) :
            e.step*=-1
            e.y += 50
            if(e.y > 450):
                Gameover=True
                enemies.clear()
#def process_events():

def move_player():
    global playerX
    playerX += playerStep
    # 防止飞机出界
    if playerX > 736:
        playerX = 736
    if playerX < 0:
        playerX = 0

#游戏主循环

running = True
while running:
    screen.blit(bgImg,(0,0))
    show_score()
    #process_events()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # 键盘事件控制 方向键
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerStep = 3
            elif event.key == pygame.K_LEFT:
                playerStep = -3
            elif event.key==pygame.K_SPACE:
                #发射子弹
                #print("bbb")
                bullets.append(Bullet())

        if event.type == pygame.KEYUP:
            playerStep = 0

    screen.blit(playerImg,(playerX,playerY))
    move_player()
    show_enemy()
    show_bullets()
    check_is_over()
    pygame.display.update()