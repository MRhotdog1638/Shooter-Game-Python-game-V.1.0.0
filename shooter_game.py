# Importing all the plugins
from pygame import *
mixer.init()
font.init()
from random import randint, random

#Adding and playing the music
mixer.music.load("Assets/Sounds/space.ogg")
mixer.music.play()
fire = mixer.Sound("Assets/Sounds/fire.ogg")

#Adding the main window
mw = display.set_mode((700, 500))
#Adding the caption for the main window
display.set_caption("Space Shooters")

#Adding the background
bg = transform.scale(image.load("Assets/Pictures/galaxy.jpg"), (700, 500))

#Adding the variable to see if the game should still be running
gameOn = True

#Adding the FPS
clock = time.Clock()
FPS = 60

missed = 0

shot = 0

lost = False

won = False

cooldown = 10

lrboss = 0

bossTimeon = False

bosshealth = 50

stylecounter = font.SysFont("Arial", 36)
styletext = font.SysFont("Arial", 150)

lostText = styletext.render("You lost!", 1, (255, 0, 0))
wonText = styletext.render("You won!", 1, (0, 255, 0))




#Adding the main GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self, Pimage, Px, Py, Pw, Ph, Pspeed):
        super().__init__()
        self.width = Pw
        self.height = Ph
        self.image = transform.scale(image.load(Pimage), (Pw, Ph))
        self.speed = Pspeed
        self.rect = self.image.get_rect()
        self.rect.x = Px
        self.rect.y = Py
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class BulletSprite(GameSprite):
    def update(self):
        self.rect.y += self.speed * -1
        if self.rect.y < 0:
            self.kill()
        if bossTimeon == True:
            if sprite.collide_rect(boss, self):
                global bosshealth
                bosshealth -= 1
                self.kill()


bulletGroup = sprite.Group()

#Adding the PlayerSprite (based on the GameSprite)
class PlayerSprite(GameSprite):
    #Adding the player movement code
    def move(self):
        pressedKeys = key.get_pressed()
        if pressedKeys[K_LEFT] and self.rect.x > -10:
            self.rect.x -= self.speed
        if pressedKeys[K_RIGHT] and self.rect.x < 645:
            self.rect.x += self.speed
    def fire(self):
        bullet = BulletSprite("Assets/Pictures/bullet.png", self.rect.centerx, self.rect.top, 20, 50, 15)
        bulletGroup.add(bullet)
            

#Adding the EnemySprite (also based on the GameSprite)
class EnemySprite(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            global missed
            missed += 1
        if bossTimeon == True:
            self.kill()

bulletBossGroup = sprite.Group()

class BossSprite(GameSprite):
    def shoot(self):
        bulletBoss = BulletBossSprite("Assets/Pictures/bulletBoss.png", self.rect.centerx, self.rect.bottom, 40, 100, 3)
        bulletBossGroup.add(bulletBoss)
    def move(self):
        if lrboss > -1 and lrboss < 101:
            self.rect.x += 5
        if lrboss > 99 and lrboss < 201:
            self.rect.x -= 5
        

class BulletBossSprite(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.kill()
        if sprite.collide_rect(player, self):
            global lost
            lost = True
            self.kill()
        


#Adding the player himself
player = PlayerSprite("Assets/Pictures/rocket.png", 350, 435, 65, 65, 5)
enemyGroup = sprite.Group()
for i in range(5):
    enemy = EnemySprite("Assets/Pictures/ufo.png", randint(0, 600), randint(0, 200), 130, 65, 2)
    enemyGroup.add(enemy)





#Adding the Gameloop
while gameOn:

    mw.blit(bg, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            gameOn = False
        if lost == False and won == False:
            if cooldown == 0:
                if e.type == KEYDOWN:
                    if e.key == K_UP:
                        player.fire()
                        fire.play()
                        cooldown = 10

    if lost == False and won == False:
    #Showing the background

    
        lostCounter = stylecounter.render("Missed:" + str(missed), 1, (255, 255, 255))
        shotCounter = stylecounter.render("Enemys shot:" + str(shot), 1, (255, 255, 255))
        Bosshealthbar = stylecounter.render("HEALTH:" + str(bosshealth), 1, (255, 255, 255))


        if bossTimeon == False:
            mw.blit(lostCounter, (10, 20))
            mw.blit(shotCounter, (10, 40))

        #Adding the player movement
        player.move()

        enemyGroup.update()

        #Making the player appear
        player.reset()


        enemyGroup.draw(mw)

        bulletGroup.update()
        bulletGroup.draw(mw)

        if bossTimeon == True:
            if lrboss == 201:
                lrboss = 0
            elif lrboss < 201:
                lrboss += 1
            boss.reset()
            boss.move()
            bulletBossGroup.update()
            bulletBossGroup.draw(mw)
            if randint(0, 60) == 1:
                boss.shoot()
            mw.blit(Bosshealthbar, (10, 10))

        collidesB = sprite.groupcollide(enemyGroup, bulletGroup, True, True)

        for c in collidesB:
            shot += 1
            enemy = EnemySprite("Assets/Pictures/ufo.png", randint(0, 600), 0, 130, 65, 2)
            enemyGroup.add(enemy)
        
        if missed > 2:
            lost = True

        if bossTimeon == False:
            if shot > 30:
                boss = BossSprite("Assets/Pictures/ufo.png", -100, 0, 400, 200, 2)
                bossTimeon = True
        
        if bosshealth == 0:
            won = True

        
        if cooldown > 0:
            cooldown -= 1


    
    elif lost == True:

        mw.blit(lostText, (100, 200))
    
    elif won == True:

        mw.blit(wonText, (50, 200))

    #Showing everything
    display.update()

    #Adding the FPS
    clock.tick(FPS)
