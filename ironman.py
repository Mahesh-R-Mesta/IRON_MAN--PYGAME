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


bg=pygame.transform.scale(pygame.image.load(os.path.join("img","city.png")),(3557,height))

robo1=pygame.transform.scale(pygame.image.load(os.path.join("img","robo2.png")),(70,80))
mask_v1=pygame.mask.from_surface(robo1)

robo2 = pygame.transform.scale(pygame.image.load(os.path.join("img","enemy2.png")),(100,100))
enemy_2=[]
robo2_fire =pygame.transform.scale(pygame.image.load(os.path.join("img","missile.png")),(30,30))
ene2_fire=[]
main_ene=0
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
Level=1
Score=0
text_msg="IRON MAN"

msg=pygame.font.SysFont('comicsan',20)
label=pygame.font.SysFont("comicsan",35)
levelsp=label.render("Level:{}".format(Level),1,(255,255,255))
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
    if Life>0:
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
    
def enemy_collide(ene):
    ene.v_img=blast
    ene.y=ene.y-(robo1.get_height()/2)
    ene.x=ene.x-(robo1.get_width()/2)
    ene.update_e()

def navic(enemyLoc,HeroLoc):
    if (enemyLoc - HeroLoc)>0:
        return  int(-1*(enemyLoc-HeroLoc)*((25.0+(11*Level))/(width-80)))
    elif (HeroLoc-enemyLoc)>0:
        return   int((HeroLoc-enemyLoc)*((25.0+(11*Level))/(width-80)))
    elif (HeroLoc==enemyLoc):
        return 0
j=0
def msg_display(msg,text_msg,win,x,y,j,j1):
    if len(text_msg)==j:
        j=len(text_msg)
        j1+=1
    else:
        j+=1
    msg_dis = msg.render(text_msg[:j],1,(255,255,255))
    win.blit(msg_dis,(x,y))
    return j,j1

IRON_MAN = shoot(i_man[1],x_pos,y_pos,win) #Creating My Iron Man
s=0
s1=0
d1=counter(0,20)
d2=counter(0,30)
enemies=[]
fps=60

def updateall():
    pygame.display.update()

# --------suitUp_amimation---------- 
for suit in first_suit:
    clock.tick(10)
    win.blit(skys,(0,0))
    win.blit(surf,(0,height-200))
    win.blit(suit,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    updateall()

#-------------------------------
while run:
    clock.tick(fps)
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run=False
    win.fill((0, 47, 75))
    win.blit(skys,(0,0))
    win.blit(bg,(-scr_x,0))
    i=i+1
    if i >=10:
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
        i_man[i]=blast
        IRON_MAN.update()
        run=False
        lab9=label.render("You Lost..Still Love you",1,(255,255,255))
        win.blit(lab9,((width/2)-lab9.get_width()/2,height/2))
    d1.K+=1
    d2.K+=1
    for fire1 in fires[:]:
        fire1.x+=8
        fire1.update()
        if fire1.x >=width:
            fires.remove(fire1)
    if random.randrange(0, int((fps*2)/Level) ) == 0:
        enem=enemy(robo1,width+10,random.randrange(robo1.get_height(),height-robo1.get_height()),win)
        enemies.append(enem)
    for ene in enemies[:]:
        ene.update_e()
        ene.x-=4
        if collide(IRON_MAN,ene):
            enemy_collide(ene)
            enemies.remove(ene)
            Life-=1
        if ene.x < 0:
            enemies.remove(ene)
        for fire1 in fires[:]:
            if collide(fire1,ene):
                enemy_collide(ene)
                fires.remove(fire1)
                enemies.remove(ene)
                Score+=1
                break
            for e2 in enemy_2:
                if collide(fire1,e2):
                    e2.IMG=blast
                    e2.update()
                    enemy_2.remove(e2)
                    fires.remove(fire1)
                    Score+=5
        if random.randrange(0,fps*2)==0:
            ene_shoot = shoot(missile_fire,ene.x,ene.y+(robo1.get_height()/2),win)
            enemies_fire.append(ene_shoot)
    if random.randrange(0,1000/Level)==0 and main_ene<3+(Level-1) and len(enemy_2)==0:
        enemy_2.append(shoot(robo2,width,height-robo2.get_height(),win))
        main_ene+=1
        print("2nd Enemy IS COMMING")
    for ene_2 in enemy_2[:]:
        if ene_2.x > (width-100):
            ene_2.x-=1
            j1=0
        else:
            j1,s1=msg_display(msg,"Face My missile Iron Man..",win,ene_2.x-50,ene_2.y-30,j1,0)
            if len(ene2_fire)==0:
                ene2_fire.append(shoot(robo2_fire,ene_2.x,ene_2.y,win))
        ene_2.update()
    for fire_2 in ene2_fire:
        fire_2.x-=9
        fire_2.y+=navic(fire_2.y,IRON_MAN.y-30+i_man[1].get_height()/2)

        if IRON_MAN.x-100 > fire_2.x:
            fire_2.IMG=blast
            fire_2.y-=blast.get_height()/2
            fire_2.x-=blast.get_height()/2
            fire_2.update()
            ene2_fire.remove(fire_2)
            
        if collide(IRON_MAN,fire_2):
            fire_2.IMG=blast
            fire_2.update()
            ene2_fire.remove(fire_2)
            Life-=1

        
        fire_2.update()
    win.blit(logo,(10,10))
    kill_com=False
    IRON_MAN.update_myhero(i_man[i],x_pos,y_pos)
    LifeB(Life*10,win)
    levelsp=label.render("Level:{}".format(Level),1,(255,255,255))
    scores=label.render("Score:{}".format(Score),1,(255,255,255))

    win.blit(scores,(logo.get_width()+150,15))
    win.blit(levelsp,(20+logo.get_width(),10))
    if s<40:
        j,s=msg_display(msg,text_msg,win,IRON_MAN.x,IRON_MAN.y+30,j,s)
    for ene_s in enemies_fire[:]:
        ene_s.x-=7
        ene_s.update()
        if ene_s.x <=0:
            enemies_fire.remove(ene_s)
        if collide(IRON_MAN,ene_s):
            ene_s.IMG = blast
            ene_s.x = ene_s.x - blast.get_width()/2
            ene_s.y = ene_s.y - blast.get_height()/2
            ene_s.update()
            enemies_fire.remove(ene_s)
            Life-=1
    scr_x+=1
    if scr_x ==(3557+350):
        scr_x = -width
        text_msg="SUPER SONIC"
        Level+=1
        main_ene=0
    updateall()
pygame.quit()
