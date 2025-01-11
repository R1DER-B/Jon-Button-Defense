import pygame as pg
import random as r
from pygame import FULLSCREEN
from Drawable import drawable
from Drawable import polygon
from Powers import power
SPAWN_ENEMIES=pg.USEREVENT+1
MENU=pg.USEREVENT+2
pg.init()
Fonta=pg.font.Font("BeVietnamPro-Medium.ttf",20)
Fonte=pg.font.Font("BeVietnamPro-Medium.ttf",40)
Fonti=pg.font.Font("BeVietnamPro-Medium.ttf",30)
win=pg.display.set_mode(flags=pg.FULLSCREEN)
test=0
WIDTH=win.get_width()
LENGTH=win.get_height()
play=True
Clock=pg.time.Clock()
mousemode="Up"
lvlstart=False
lvl=0
level=drawable(Fonta.render(f"Level:{lvl}",True,(255,255,255)))
money=1000000000000000000000
moneyt=Fonta.render(f"${money}",True,(255,255,255))
lives=100
livest=Fonta.render(f"{lives}",True,(255,255,255))
buyone=True
price=100
buycount=0
addthingy=10
powers={}
lottery=[]
with open("Powers.csv",'r') as file:
    for line in file:
        for char in range(len(line)):
            if line[char]==',':
                name=line[0:char]
                for x in range(int(line[char+1:-1])):
                    lottery.append(name)
                powers.update({name:power(name)})
                # powers.append(power(line[0:char]))
print(powers)
print(len(powers))
print(len(lottery))
Jon=pg.image.load("Jon_2_0.png")
Jon.set_colorkey((255,0,0))
Jonr=Jon.get_rect(center=((WIDTH/2,LENGTH/2)))
Jon=drawable(Jon,Jonr)
Drag=drawable(pg.Surface((0,0)),pg.Rect(0,0,0,0))
heart=drawable(pg.transform.scale(pg.image.load("Heart.svg.png"),(32,32)))
heart.rect.y=LENGTH-heart.rect.width
Lvlbtn=drawable(pg.transform.scale(pg.image.load("levelbutton.png"),(64,64)))
Lvlbtn.rect.right=WIDTH
exit=drawable(pg.transform.scale((pg.image.load("exit.png")),(150,68)))
exit.rect.x = WIDTH / 4
exit.rect.y = LENGTH / 4
shop=drawable(pg.transform.scale((pg.image.load("shop.png")),(64,64)))
shop.rect.x=WIDTH/4*3-shop.rect.width
shop.rect.y=LENGTH/4
gasha=drawable(pg.image.load("Gashapon.png"))
gasha.rect.center = (WIDTH/2, LENGTH/2)
blortton=drawable(pg.transform.scale(pg.image.load("blurange.png"),(131,58)))
blortton.rect.x=WIDTH-blortton.rect.width-20
blortton.rect.y=20
coin=drawable(pg.transform.scale(pg.image.load("coin.png"),(30,33)))
coin.surface.set_colorkey((255,255,255))
coinbag=[]
# winscreen=drawable(pg.transform.scale(pg.image.load("Victory.jpg"),(WIDTH,LENGTH)))
winscreen=drawable(pg.image.load("Victory.jpg"))
winscreen.rect.centerx=WIDTH/2
reinforcements=0
enemies=[]
pg.time.set_timer(SPAWN_ENEMIES, 1000)
def polylist(center,size,sides):
    points=[]
    Transformer=pg.math.Vector2(0,size)
    for i in range(sides):
        points.append(pg.math.Vector2(center[0]+Transformer.x,center[1]+Transformer.y))
        Transformer.rotate_ip(360/sides)
    return points
def draw(*objs):
    win.fill((0,0,0))
    win.blit(moneyt,(WIDTH-moneyt.get_width(),LENGTH-moneyt.get_height()))
    win.blit(livest,(heart.rect.width,LENGTH-livest.get_height()))
    for obj in objs:
        if obj!= None:
            obj.draw(win)
    pg.display.update()
def drag_box(p1, p2):
    # function that returns a Rectangle based on two points
    top=p2[1] if p1[1] > p2[1] else p1[1]
    left=p2[0] if p1[0] > p2[0] else p1[0]
    width=abs(p1[0]-p2[0])
    height=abs(p1[1]-p2[1])
    return pg.Rect(left, top, width, height)
# enemies.append(polygon((255, 255, 255), polylist((0, 0), 20, (r.randint(3, 10)))))
def spawnenemy(enemies):
    if r.randint(0, 1) == 1:
        #    pick a random y and start on the left or right side of the screen
        x = (0 if r.randint(0, 1) == 1 else WIDTH)
        y = r.randint(0, LENGTH)
    else:
        #    pick a random x and start on the top or bottom side of the screen
        y = (0 if r.randint(0, 1) == 1 else LENGTH)
        x = r.randint(0, WIDTH)
    enemies.append(polygon((255, 255, 255), polylist((x, y), lvl+9, (r.randint(3, 3+lvl)))))
# with open("Powers.csv","r") as fower:
#     for line in fower:
#         print(line)
# bowser = "Hi my name is, Bowser"
# mario=""
# for char in bowser:
#     if char == ',':
#         print(mario)
#     else:
#         mario+=char
def roll(powers, lottery):
    theone=r.randint(0,len(lottery)-1)
    powers[lottery[theone]].upgrade()
    print(lottery[theone])
    if lottery[theone]=="Win":
        victory()
    lottery.pop(theone)
def victory():
    global play
    global menu
    global gacha
    win.fill((0, 0, 0))
    winscreen.draw(win)
    Jon.draw(win)
    pg.display.update()
    pg.time.wait(5000)
    menu=False
    gacha=False
    play=False
while play:
    Clock.tick(60)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            play=False
        if event.type==pg.KEYUP:
            if event.key==pg.K_ESCAPE:
                pg.event.post(pg.event.Event(MENU,{}))
        if event.type==MENU:
            menu=True
            menutime=pg.time.get_ticks()
            while menu:
                menubox=pg.Rect(WIDTH/4,LENGTH/4,WIDTH/2,LENGTH/2)
                menuborder=pg.Rect(WIDTH/4-10,LENGTH/4-10,WIDTH/2+20,LENGTH/2+20)
                pg.draw.rect(win, (100,100,100), menuborder)
                pg.draw.rect(win,(255,255,255),menubox)
                Jon.draw(win)
                exit.draw(win)
                shop.draw(win)
                Title=Fonte.render("Jon 2: Button Defense",True,(0,0,0))
                win.blit(Title,(WIDTH/2-Title.get_width()/2,LENGTH*3/8))
                pg.display.update()
                for event in pg.event.get():
                    if event.type==pg.QUIT:
                        play=False
                        menu=False
                    if event.type==pg.KEYUP:
                        if event.key==pg.K_ESCAPE:
                            menu=False
                    if event.type==pg.MOUSEBUTTONDOWN:
                        mousepos=pg.mouse.get_pos()
                        if exit.rect.collidepoint(mousepos):
                            pg.event.post(pg.event.Event(pg.QUIT,{}))
                        if shop.rect.collidepoint(mousepos):
                            gacha=True
                            while gacha:
                                gachar=pg.Rect(0, 0, WIDTH, LENGTH)
                                pg.draw.rect(win, (100, 60, 200), gachar)
                                gasha.draw(win)
                                win.blit(moneyt,(WIDTH-moneyt.get_width(),LENGTH-moneyt.get_height()))
                                blortton.draw(win)
                                one = Fonti.render(f"1", True, ((0, 255, 0)) if buyone else (255, 255, 255))
                                ten = Fonti.render(f"10", True, ((255, 255, 255) if buyone else (0,255,0)))
                                win.blit(one, (WIDTH - blortton.rect.width + 15, 30))
                                win.blit(ten, (WIDTH - ten.get_width()-40, 30))
                                pricet = Fonta.render(f"One gacha costs ${price} and 10% off on 10 gachas cost ${int(9*(10*price+45*addthingy)/10)}",True, (255,255,255))
                                win.blit(pricet,(WIDTH/2-pricet.get_width()/2,gasha.rect.bottom))
                                pg.display.update()
                                for event in pg.event.get():
                                    if event.type == pg.QUIT:
                                        play = False
                                        menu = False
                                        gacha = False
                                    if event.type == pg.KEYUP:
                                        if event.key == pg.K_ESCAPE:
                                            gacha = False
                                            draw(Jon, Drag, *enemies, Lvlbtn, level, heart, *coinbag)
                                    if event.type == pg.MOUSEBUTTONDOWN:
                                        mousepos = pg.mouse.get_pos()
                                        if exit.rect.collidepoint(mousepos):
                                            pg.event.post(pg.event.Event(pg.QUIT, {}))
                                        if gasha.rect.collidepoint(mousepos):
                                            if buyone:
                                                if money >= price:
                                                    money-=price
                                                    buycount+=1
                                                    price+=addthingy
                                                    moneyt = Fonta.render(f"${money}", True, (255, 255, 255))
                                                    roll(powers,lottery)
                                            else:
                                                if money >= int(9*(10*price+45*addthingy)/10):
                                                    money -= int(9*(10*price+45*addthingy)/10)
                                                    buycount += 10
                                                    price += 10*addthingy
                                                    moneyt = Fonta.render(f"${money}", True, (255, 255, 255))
                                                    for x in range(10):
                                                        roll(powers, lottery)
                                            print(buycount)
                                        if blortton.rect.collidepoint(mousepos):
                                            buyone=not buyone
        if event.type==pg.MOUSEBUTTONDOWN:
            mousemode="Down"
            mousepos=pg.mouse.get_pos()
            if Jon.rect.collidepoint(mousepos) and lvlstart:
                # if Jon.mask.get_at(mousepos):
                money+=1
                moneyt=Fonta.render(f"${money}", True, (255, 255, 255))
            if Lvlbtn.rect.collidepoint(mousepos):
                # pg.time.set_timer(SPAWN_ENEMIES, 1000, loops=9)
                reinforcements=9
                lvlstart=True
                spawnenemy(enemies)
                lvl+=1
                level=drawable(Fonta.render(f"Level:{lvl}", True, (255, 255, 255)))
        if event.type==pg.MOUSEBUTTONUP:
            for enemy in enemies:
                damage=False
                for point in enemy.points:
                    if Drag.rect.collidepoint(point):
                        damage=True
                if damage:
                    if not enemy.damage():
                        copy=coin.copy()
                        copy.money=enemy.dollar
                        copy.rect.x=enemy.center[0]
                        copy.rect.y=enemy.center[1]
                        coinbag.append(copy)
                        enemies.remove(enemy)
            mousemode="Up"
            win.fill((0, 0, 0))
            # Drag.rect.size=(0,0)
            Drag=drawable(pg.Surface((0,0)),Drag.rect)
        if event.type==SPAWN_ENEMIES:
            if reinforcements>0:
                spawnenemy(enemies)
                reinforcements-=1
            # if r.randint(0, 1) == 1:
            #     #    pick a random y and start on the left or right side of the screen
            #     x = (0 if r.randint(0, 1) == 1 else WIDTH)
            #     y = r.randint(0, LENGTH)
            # else:
            #     #    pick a random x and start on the top or bottom side of the screen
            #     y = (0 if r.randint(0, 1) == 1 else LENGTH)
            #     x = r.randint(0, WIDTH)
            # enemies.append(polygon((255,255,255),polylist((x,y),20,(r.randint(3,10)))))
    if mousemode=="Down":
        Drag=drag_box(mousepos,pg.mouse.get_pos())
        # pg.draw.rect(win,(0,0,255),Drag)
        Drag=drawable(pg.Surface((Drag.width, Drag.height)),Drag)
        Drag.surface.fill((0,0,255))
        Drag.surface.set_alpha(100)
    else:
        Drag.rect.size=(0,0)
    for coim in coinbag:
        coim.move(10, Jon.rect.center)
        if coim.rect.colliderect(Jon.rect):
            coinbag.remove(coim)
            money+=2**powers["Double Money"].stacks*(copy.money+3)
            moneyt = Fonta.render(f"${money}", True, (255, 255, 255))
    for enemy in enemies:
        enemy.move(1,Jon.rect.center)
        if (enemy.mask.overlap(Jon.mask,(Jon.rect.x-enemy.center.x+enemy.rect.width/2,Jon.rect.y-enemy.center.y+enemy.rect.height/2))):
        # print(enemy.rect.x-Jon.rect.x,enemy.rect.y-Jon.rect.y)
            enemies.remove(enemy)
            lives-=len(enemy.points)
        livest = Fonta.render(f"{lives}", True, (255, 255, 255))
    if len(enemies)==0:
        lvlstart=False
    draw(Jon,Drag,*enemies,Lvlbtn,level,heart,*coinbag)
#TODO:
# GACHA in the menu
# IF DUPLICATES HAPPEN YOUR ABILITY UPGRADES
# LOSE LIVES=GAME OVER