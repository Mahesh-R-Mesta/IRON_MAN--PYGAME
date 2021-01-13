import pygame
import os
import random
import time
width=1000
height=700
pygame.font.init()

win= pygame.display.set_mode((width,height))
pygame.display.set_caption("Iron Man")
fire = pygame.transform.scale(pygame.image.load(os.path.join("img","g_fire.png")),(80,50))
fires=[]

first_suit = [pygame.transform.scale(pygame.image.load(os.path.join("suit","fin1 ({}).gif".format(i))),(width,height)) for i in range(1,174)]

skys=pygame.transform.scale(pygame.image.load(os.path.join("img","sky.png")),(width,height-50))

i_man =[pygame.transform.scale(pygame.image.load(os.path.join("irons","{}.png".format(i))),(150,150)) for i in range(1,14)]
mask =[pygame.mask.from_surface(i_man[i]) for i in range(1,13)]

bg=pygame.transform.scale(pygame.image.load(os.path.join("img","city.png")),(3557,height))

robo1=pygame.transform.scale(pygame.image.load(os.path.join("img","robo2.png")),(70,80))
mask_v1=pygame.mask.from_surface(robo1)

robo2 = pygame.transform.scale(pygame.image.load(os.path.join("img","robo1.png")),(70,70))
mask_v2 = pygame.mask.from_surface(robo2)

logo=pygame.transform.scale(pygame.image.load(os.path.join("img","logo.png")),(50,50))

blast = pygame.transform.scale(pygame.image.load(os.path.join("img","fire2.ico")),(130,130))
small_blast =pygame.transform.scale(pygame.image.load(os.path.join("img","fire2.ico")),(50,50))
missile_fire = pygame.transform.scale(pygame.image.load(os.path.join("img","jet.png")),(50,20)) 
kill_all = pygame.transform.scale(pygame.image.load(os.path.join("img","missile.png")),(50,50))
enemies_fire=[]
kill_all_missile=[]
Life=10
i=1
j=0
scr_x=0
run=True
x_pos=10
y_pos=height/2
kill_com=False
get_cor=[]

class velocity():
    def __init__(self,vel,maxi):
        self.vel=vel
        self.maxi=maxi
        
    def gofast(self):
        self.vel+=1
        if self.vel >=self.maxi:
            self.vel=self.maxi
        return self.vel
            
    def stop(self):
        self.vel=1

up_vel = velocity(1,6)
down_vel = velocity(1,6)
for_vel = velocity(1,6)
back_vel = velocity(1,6)
clock = pygame.time.Clock()
class shoot():
    def __init__ (self,imgs,x,y,win):
        self.x=x
        self.y=y
        self.IMG=imgs
        self.WIN=win
        self.mask=pygame.mask.from_surface(self.IMG)
    def update(self):
        self.WIN.blit(self.IMG,(self.x,self.y))
    def update_myhero(self,img,x1,y1):
        self.IMG=img
        self.x=x1
        self.y=y1
        self.WIN.blit(img,(x1,y1))
        self.mask=pygame.mask.from_surface(img)
class counter():
    def __init__ (self,k,maxi):
        self.K=k
        self.maxi=maxi
    def up(self):
        if self.maxi > self.K:
            return False
        else:
            self.K=0
            return True
class enemy():
    def __init__(self,v_img,x,y,win):
        self.v_img=v_img
        self.x=x
        self.y=y
        self.win=win
        self.mask=pygame.mask.from_surface(v_img)
    def update_e(self):
        self.win.blit(self.v_img,(self.x,self.y))
def LifeB(Life,win):
    b_bar=pygame.Surface((100,10))
    b_bar.fill((255,255,255))
    f_bar=pygame.Surface((Life,10))
    f_bar.fill((0,255,0))
    win.blit(b_bar,(70,35))
    win.blit(f_bar,(70,35))
def collide(obj1,obj2):
    x1=obj1.x - obj2.x
    y1=obj1.y - obj2.y
    return obj2.mask.overlap(obj1.mask,(x1,y1))!=None
    
def guid_missile(x_m,y_m,x_e,y_e):
    if (x_e>x_m):
        x1=2
    if (x_e<x_m):
        x1=-2
    if (y_e>y_m):
        y1=+2
    if (y_e<y_m):
        y1=-2
    if (y_e==y_m and y_e==y_m):
        y1=0
        x1=0
    return x1,y1

def enemy_collide(ene):
    ene.v_img=blast
    ene.y=ene.y-(robo1.get_height()/2)
    ene.x=ene.x-(robo1.get_width()/2)
    ene.update_e()


IRON_MAN = shoot(i_man[1],x_pos,y_pos,win) #Creating My Iron Man

d1=counter(0,15)
d2=counter(0,30)
enemies=[]
fps=60

def updateall():
    pygame.display.update()
surf=pygame.Surface((width,200))
surf.fill((168,178,179))
for suit in first_suit:
    clock.tick(10)
    win.blit(skys,(0,0))
    win.blit(surf,(0,height-200))
    win.blit(suit,(0,0))
    updateall()
while run:
    clock.tick(fps)
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run=False
    win.fill((0, 47, 75))
    win.blit(skys,(0,0))
    win.blit(bg,(-scr_x,0))
    i=i+1
    if i >=13:
        i=1
    keys =pygame.key.get_pressed()
    if keys[pygame.K_UP] and y_pos >=0:
        y_pos-=up_vel.gofast()
    else:
        up_vel.stop()
    if keys[pygame.K_DOWN] and y_pos + i_man[1].get_height() <=height:
        y_pos+=down_vel.gofast()
    else:
        down_vel.stop()
    if keys[pygame.K_RIGHT] and x_pos + i_man[1].get_width()<=width:
        x_pos+=for_vel.gofast()
    else:
        for_vel.stop()
    if keys[pygame.K_LEFT] and x_pos >=0:
        x_pos-=back_vel.gofast()
    else:
        back_vel.stop()
    if keys[pygame.K_SPACE]:
        if d1.up():
            s1=shoot(fire,(x_pos+(i_man[1].get_width()/2)),(y_pos+(i_man[1].get_height()/2)),win)
            fires.append(s1)
            d1.K=0
    if keys[pygame.K_a]:
        if d2.up():
            kill_com=True
            d2.K=0
    if Life==0:
        run=False
    d1.K+=1
    d2.K+=1
    for fire1 in fires:
        fire1.x+=8
        fire1.update()
        if fire1.x >=width:
            fires.remove(fire1)
    if random.randrange(0,50) == 0:
        enem=enemy(robo1,width+50,random.randrange(robo1.get_height(),height-robo1.get_height()),win)
        enemies.append(enem)
    for ene in enemies:
        ene.update_e()
        ene.x-=4
        if collide(IRON_MAN,ene):
            enemy_collide(ene)
            enemies.remove(ene)
            Life-=1
        if ene.x < 0:
            enemies.remove(ene)
        for fire1 in fires:
            if collide(fire1,ene):
                enemy_collide(ene)
                enemies.remove(ene)
                fires.remove(fire1)
        if random.randrange(0,100)==0:
            ene_shoot = shoot(missile_fire,ene.x,ene.y+(robo1.get_height()/2),win)
            enemies_fire.append(ene_shoot)
    win.blit(logo,(10,10))
    kill_com=False
    IRON_MAN.update_myhero(i_man[i],x_pos,y_pos)
    LifeB(Life*10,win)
    for ene_s in enemies_fire:
        ene_s.x-=8
        ene_s.update()
        if ene_s.x <=0:
            enemies_fire.remove(ene_s)
        if collide(IRON_MAN,ene_s):
            ene_s.IMG = small_blast
            ene_s.x = ene_s.x - small_blast.get_width()/2
            ene_s.y = ene_s.y - small_blast.get_height()/2
            ene_s.update()
            enemies_fire.remove(ene_s)
            Life-=1
    scr_x+=1
    if scr_x ==(3557+350):
        scr_x = -width
    updateall()
pygame.quit()
