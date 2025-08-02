import pygame as pg
import random as r
import math as m
from pygame import FULLSCREEN
from Drawable import drawable
from Drawable import polygon
from Powers import power
SPAWN_ENEMIES=pg.USEREVENT+1
MENU=pg.USEREVENT+2
REGENERATION=pg.USEREVENT+3
pg.init()
Fonta=pg.font.Font("BeVietnamPro-Medium.ttf",20)
Fonte=pg.font.Font("BeVietnamPro-Medium.ttf",40)
Fonti=pg.font.Font("BeVietnamPro-Medium.ttf",30)
win=pg.display.set_mode(flags=pg.FULLSCREEN)
WIDTH=win.get_width()
LENGTH=win.get_height()
play=True
Clock=pg.time.Clock()
mousemode="Up"
lvlstart=False
lvl=0
level=drawable(Fonta.render(f"Level:{lvl}",True,(255,255,255)))
money=10000000000
moneyt=Fonta.render(f"${money}",True,(255,255,255))
lives=100
maxhealth=100
regen=1
healthmultiplier=1.25
livest=Fonta.render(f"{lives}",True,(255,255,255))
buyone=True
price=100
buycount=0
addthingy=10
powers={}
jonpowers=[]
lottery=[]
common=[]
uncommon=[]
rare=[]
epic=[]
legendary=[]
rarities=[common,uncommon,rare,epic,legendary]
with open("Powers.csv",'r') as file:
    for line in file:
        for char in range(len(line)):
            if line[char]==',':
                name=line[0:char]
                amount=int(line[char+1:])
                if amount==1:
                    legendary.append(name)
                elif 2<=amount<25:
                    epic.append(name)
                elif 25<=amount<=35:
                    rare.append(name)
                elif 35<amount<=60:
                    uncommon.append(name)
                elif amount>60:
                    common.append(name)
                for x in range(int(line[char+1:-1])):
                    lottery.append(name)
                powers.update({name:power(name)})
                # powers.append(power(line[0:char]))
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
powerpedia=drawable(pg.transform.scale(pg.image.load("powers.png"),(200,200)))
powerpedia.rect.x = WIDTH / 4 - 50
powerpedia.rect.bottom = 3*LENGTH / 4 + 50
grid=drawable(pg.transform.scale(pg.image.load("P.png"),(1000,1000)))
grid.rect.centerx=WIDTH/2
grid.rect.centery=LENGTH/2
winimg=drawable(pg.transform.scale(pg.image.load("Win.png"),(150,150)))
winimg.rect.centerx=WIDTH/2
winimg.rect.centery=LENGTH/2-10
# winscreen=drawable(pg.transform.scale(pg.image.load("Victory.jpg"),(WIDTH,LENGTH)))
damageimg=drawable(pg.transform.scale(pg.image.load("Damage.png"),(125,125)))
damageimg.rect.x=grid.rect.x+90
damageimg.rect.y=grid.rect.y+100
healthimg=drawable(pg.transform.scale(pg.image.load("Health.png"),(125,125)))
healthimg.rect.x=grid.rect.x+265
healthimg.rect.y=grid.rect.y+100
regenerationimg=drawable(pg.transform.scale(pg.image.load("Regeneration.png"),(125,125)))
regenerationimg.rect.x=grid.rect.x+442
regenerationimg.rect.y=grid.rect.y+100
betterluckimg=drawable(pg.transform.scale(pg.image.load("Better_Luck.png"),(125,125)))
betterluckimg.rect.x=grid.rect.x+616
betterluckimg.rect.y=grid.rect.y+100
criticalclickimg=drawable(pg.transform.scale(pg.image.load("Critical_Click.png"),(125,125)))
criticalclickimg.rect.x=grid.rect.x+785
criticalclickimg.rect.y=grid.rect.y+100
doublemoneyimg=drawable(pg.transform.scale(pg.image.load("Double_Money.png"),(125,125)))
doublemoneyimg.rect.x=grid.rect.x+90
doublemoneyimg.rect.y=grid.rect.y+265
daggerimg=drawable(pg.transform.scale(pg.image.load("Dagger.png"),(100,100)))
daggerimg.rect.x=grid.rect.x+275
daggerimg.rect.y=grid.rect.y+280
swordimg=drawable(pg.transform.scale(pg.image.load("Sword.png"),(125,125)))
swordimg.rect.x=grid.rect.x+435
swordimg.rect.y=grid.rect.y+265
bowimg=drawable(pg.transform.scale(pg.image.load("Bow.png"),(125,125)))
bowimg.rect.x=grid.rect.x+620
bowimg.rect.y=grid.rect.y+265
lifestealimg=drawable(pg.transform.scale(pg.image.load("Life_Steal.png"),(125,125)))
lifestealimg.rect.x=grid.rect.x+790
lifestealimg.rect.y=grid.rect.y+265
moneyperroundimg=drawable(pg.transform.scale(pg.image.load("Money_Per_Round.png"),(125,125)))
moneyperroundimg.rect.x=grid.rect.x+90
moneyperroundimg.rect.y=grid.rect.y+425
shieldimg=drawable(pg.transform.scale(pg.image.load("Shield.png"), (125, 125)))
shieldimg.rect.x=grid.rect.x+265
shieldimg.rect.y=grid.rect.y+425
shockwaveimg=drawable(pg.transform.scale(pg.image.load("Shockwave.png"), (150, 150)))
shockwaveimg.rect.x=grid.rect.x+605
shockwaveimg.rect.y=grid.rect.y+410
bouncybulletsimg=drawable(pg.transform.scale(pg.image.load("Bouncy_Bullets.png"), (150, 150)))
bouncybulletsimg.rect.x=grid.rect.x+780
bouncybulletsimg.rect.y=grid.rect.y+410
eatimg=drawable(pg.transform.scale(pg.image.load("Eat.png"), (125, 125)))
eatimg.rect.x=grid.rect.x+90
eatimg.rect.y=grid.rect.y+580
raygunimg=drawable(pg.transform.scale(pg.image.load("Raygun.png"), (125, 125)))
raygunimg.rect.x=grid.rect.x+270
raygunimg.rect.y=grid.rect.y+580
bombimg=drawable(pg.transform.scale(pg.image.load("Bomb.png"), (125, 125)))
bombimg.rect.x=grid.rect.x+450
bombimg.rect.y=grid.rect.y+580
swampimg=drawable(pg.transform.scale(pg.image.load("Swamp.png"), (125, 125)))
swampimg.rect.x=grid.rect.x+615
swampimg.rect.y=grid.rect.y+580
lightningimg=drawable(pg.transform.scale(pg.image.load("Lightning.png"), (125, 140)))
lightningimg.rect.x=grid.rect.x+785
lightningimg.rect.y=grid.rect.y+575
freezeimg=drawable(pg.transform.scale(pg.image.load("Freeze.png"), (125, 125)))
freezeimg.rect.x=grid.rect.x+90
freezeimg.rect.y=grid.rect.y+745
nukeimg=drawable(pg.transform.scale(pg.image.load("Nuke.png"), (125, 125)))
nukeimg.rect.x=grid.rect.x+265
nukeimg.rect.y=grid.rect.y+745
whiteholeimg=drawable(pg.transform.scale(pg.image.load("White_Hole.png"), (125, 125)))
whiteholeimg.rect.x=grid.rect.x+435
whiteholeimg.rect.y=grid.rect.y+740
dragonbreathimg=drawable(pg.transform.scale(pg.image.load("Dragon_Breath.png"), (125, 125)))
dragonbreathimg.rect.x=grid.rect.x+615
dragonbreathimg.rect.y=grid.rect.y+740
forcefieldimg=drawable(pg.transform.scale(pg.image.load("Force_Field.png"), (125, 125)))
forcefieldimg.rect.x=grid.rect.x+790
forcefieldimg.rect.y=grid.rect.y+740
grabilities=[grid,winimg,damageimg,healthimg,regenerationimg,betterluckimg, criticalclickimg, doublemoneyimg, daggerimg, swordimg, bowimg, lifestealimg, moneyperroundimg, shieldimg, shockwaveimg, bouncybulletsimg, eatimg, raygunimg, bombimg, swampimg, lightningimg, freezeimg, nukeimg, whiteholeimg, dragonbreathimg, forcefieldimg]
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
    global lives
    global livest
    global maxhealth
    global regen
    global healthmultiplier
    theone=r.randint(0,len(lottery)-1)
    powers[lottery[theone]].upgrade()
    jonpowers.append(lottery[theone])
    if lottery[theone]=="Win":
        victory()
    if lottery[theone]=="Health":
        lives=int(lives*healthmultiplier)
        maxhealth=int(maxhealth*healthmultiplier)
        livest = Fonta.render(f"{lives}", True, (255, 255, 255))
    if lottery[theone]=="Better_Luck":
        for ability in powers:
            for y in range(getraritymp(ability)):
                lottery.append(ability)
    lottery.pop(theone)
def victory():
    global play
    global menu
    global gacha
    print(lottery)
    win.fill((0, 0, 0))
    winscreen.draw(win)
    Jon.draw(win)
    pg.display.update()
    print(jonpowers)
    print(str(buycount)+" gachas")
    pg.time.wait(5000)
    pg.event.post(pg.event.Event(pg.QUIT, {}))
def getrarity(ability):
    for rarity in rarities:
        for name in rarity:
            if name==ability:
                if rarity==legendary:
                    return (255,180,0)
                elif rarity==epic:
                    return (255,0,255)
                elif rarity==rare:
                    return (0,0,255)
                elif rarity==uncommon:
                    return (0,255,0)
                elif rarity==common:
                    return (100,100,100)
def getraritymp(ability):
    ttlpwrs=lottery.count(ability)+jonpowers.count(ability)
    for rarity in rarities:
        for name in rarity:
            if name==ability:
                if rarity==legendary:
                     return m.ceil(ttlpwrs*2-jonpowers.count(ability))
                elif rarity==epic:
                    return m.ceil(ttlpwrs*1.2-jonpowers.count(ability))
                elif rarity==rare:
                    return m.ceil(ttlpwrs*1.1-jonpowers.count(ability))
                else:
                    return 0
def abilitytext(ability, image):
    if image.rect.y>=WIDTH/2:
        box=pg.Rect(image.rect.right,image.rect.bottom,300,175)
    else:
        box = pg.Rect(image.rect.right, image.rect.top, 350, 175)
    pg.draw.rect(win,(255,255,255),box)
    if ability=="Win":
        text=["              .Win.", "", "           Instantly Wins The Game"]
    elif ability=="Damage":
        text=["         .Damage.", "", "          Increases Damage Output"]
    elif ability=="Health":
        text=["           .Health.", "", "              Increases Jon's Health"]
    elif ability=="Regeneration":
        text=["    .Regeneration.", "", "            Regenerates Jon's Lost", "                  Health Over Time"]
    elif ability=="Better_Luck":
        text=["      .Better Luck.", "", "             Increases The Chances", "              To Get Rare Abilities"]
    elif ability=="Critical_Click":
        text=["    .Critical Click.", "", "             Increases The Chances", "                   And Damage Of", "                     Critical Clicks"]
    elif ability=="Double_Money":
        text=["   .Double Money.", "", "                Doubles The Money", "                      Jon Obtains"]
    elif ability=="Dagger":
        text=["          .Dagger.", "", "                       Gives Jon A", "                 Throwable Dagger"]
    elif ability=="Sword":
        text=["           .Sword.", "", "                 Gives Jon A Sword", "             That Spins Around Him"]
    elif ability=="Bow":
        text=["             .Bow.", "", "              Gives Jon A Bow That", "              Spins Around Him And", "          Shoot Arrows Periodically"]
    elif ability=="Life_Steal":
        text=["        .Life Steal.", "", "            When Jon Hits Enemies", "         Restores Health Based Off", "                    Damage Done"]
    elif ability=="Money_Per_Round":
        text=["  .Cash Per Round.", "", "                  Obtains A Certain", "           Amount Of Money At The", "               Start Of Each Round"]
    elif ability=="Shield":
        text=["           .Shield.", "", "              Allows Jon To Take A", "            Certain Amount Of Hits", "           Without Taking Damage"]
    elif ability == "Shockwave":
        text = ["      .Shockwave.", "", "              Pushes Enemies Away"]
    elif ability == "Bouncy_Bullets":
        text = ["  .Bouncy Bullets.", "", "                   Allows Bullets To", "                   Bounce Off Walls"]
    elif ability == "Eat":
        text = ["              .Eat.", "", "             If An Enemy's Sides Are", "          Low Enough Then Jon Will", "          Eat Them And Take No", "                          Damage"]
    elif ability == "Raygun":
        text = ["          .Raygun.", "", "          Gives Jon A Raygun That", "          Fires A Laser Periodically"]
    elif ability == "Bomb":
        text = ["            .Bomb.", "", "           Spawns Bombs That Can", "     Detonate Upon Dragging Over"]
    elif ability == "Swamp":
        text = ["           .Swamp.", "", "               Spawns Swamps That", "      Damages And Slows Enemies", "                          Over Time"]
    elif ability == "Lightning":
        text = ["        .Lightning.", "", "               Allows Jon To Shoot", "                Lightning That Hits", "                   Multiple Enemies"]
    elif ability == "Freeze":
        text = ["           .Freeze.", "", "              Freezes Enemies In A", "           Zone To Keep Them From", "                            Moving"]
    elif ability == "Nuke":
        text = ["             .Nuke.", "", "             Wipes Out All Enemies", "                  On Screen After", "            A Long Period Of Time"]
    elif ability == "White_Hole":
        text = ["      .White Hole.", "", "         Spawms A White Hole", "              That Sucks Enemies In", "                        Dealing Damage"]
    elif ability == "Dragon_Breath":
        text = ["  .Dragon Breath.", "", "                    Jon Gains The", "            Ability To Breathe Fire", "          That Also Does Damage", "                       Over Time"]
    elif ability == "Force_Field":
        text = ["      .Force Field.", "", "           Slows Enemies, Reduces", "             Damage Taken, And", "        Deals Damage To Enemies", "                      In The Field"]
    for i in range(len(text)):
        if i==0:
            abtext = Fonte.render(text[i], True, getrarity(ability))
        else:
            abtext = Fonta.render(text[i],True,(0,0,0))
        win.blit(abtext, (box.x, box.y+25*i))
while play:
    Clock.tick(60)
    for event in pg.event.get():
        pg.time.set_timer(REGENERATION, 1000)
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
                powerpedia.draw(win)
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
                            print(jonpowers)
                            print(str(buycount)+" gachas")
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
                                            print(jonpowers)
                                            print(str(buycount)+" gachas")
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
                                        if blortton.rect.collidepoint(mousepos):
                                            buyone=not buyone
                        if powerpedia.rect.collidepoint(mousepos):
                            openpower=True
                            while openpower:
                                powerb = pg.Rect(0, 0, WIDTH, LENGTH)
                                pg.draw.rect(win, (160, 90, 30), powerb)
                                for obj in grabilities:
                                    obj.draw(win)
                                if winimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Win", winimg)
                                if damageimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Damage", damageimg)
                                if healthimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Health", healthimg)
                                if regenerationimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Regeneration", regenerationimg)
                                if betterluckimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Better_Luck", betterluckimg)
                                if criticalclickimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Critical_Click", criticalclickimg)
                                if doublemoneyimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Double_Money", doublemoneyimg)
                                if daggerimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Dagger", daggerimg)
                                if swordimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Sword", swordimg)
                                if bowimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Bow", bowimg)
                                if lifestealimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Life_Steal", lifestealimg)
                                if moneyperroundimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Money_Per_Round", moneyperroundimg)
                                if shieldimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Shield", shieldimg)
                                if shockwaveimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Shockwave", shockwaveimg)
                                if bouncybulletsimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Bouncy_Bullets", bouncybulletsimg)
                                if eatimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Eat", eatimg)
                                if raygunimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Raygun", raygunimg)
                                if bombimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Bomb", bombimg)
                                if swampimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Swamp", swampimg)
                                if lightningimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Lightning", lightningimg)
                                if freezeimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Freeze", freezeimg)
                                if nukeimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Nuke", nukeimg)
                                if whiteholeimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("White_Hole", whiteholeimg)
                                if dragonbreathimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Dragon_Breath", dragonbreathimg)
                                if forcefieldimg.rect.collidepoint(pg.mouse.get_pos()):
                                    abilitytext("Force_Field", forcefieldimg)
                                pg.display.update()
                                for event in pg.event.get():
                                    if event.type == pg.QUIT:
                                        play = False
                                        menu = False
                                        openpower = False
                                    if event.type == pg.KEYUP:
                                        if event.key == pg.K_ESCAPE:
                                            openpower = False
                                            draw(Jon, Drag, *enemies, Lvlbtn, level, heart, *coinbag)
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
                for x in range(jonpowers.count("Damage")+1):
                    if damage:
                        if not enemy.damage() and enemy in enemies:
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
        if event.type==REGENERATION:
            regenstacks=jonpowers.count("Regeneration")
            regen = int(healthmultiplier / 2 * regenstacks)
            lives+=regen
            if lives>=maxhealth:
                lives=maxhealth
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
            doublemoneystacks=int(jonpowers.count("Double_Money")*1.1)
            money+=int((copy.money*doublemoneystacks+3))
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
# IF DUPLICATES HAPPEN YOUR ABILITY UPGRADES
# LOSE LIVES=GAME OVER
# Luck will add to the rares and if the ability is maxed out it would reroll
# fix double money