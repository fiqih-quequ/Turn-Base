import random
import pygame
from abc import ABC, abstractmethod


pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_icon(pygame.image.load("img/Icons/wall2.png"))
pygame.display.set_caption('Dampak Genshin')

#backsound
pygame.mixer.music.load('music/backsound.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

#define game variables
gameOver = 0
currentEntity = 1
totalEntity = 3
actionCooldown = 0
actionWaitTime = 90
attack = False
potion = False
potionHeal = 15
clicked = False 
#entity variables
heroChoice = None #0: knight, 1: priestess, 2: hashashin

#define font
font = pygame.font.SysFont('Times New Roman', 26)
fontButton = pygame.font.SysFont('Times New Roman', 18)

#define color
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

#load images
#background img
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
background_img1 = pygame.image.load('img/Background/background1.png').convert_alpha()
#panel img
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
#sword img
sword_img = pygame.image.load('img/Icons/window.png').convert_alpha()
sword_img = pygame.transform.scale(sword_img, (45, 35))
#button img
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
#victory and defeat img
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
#hero icon
knight_icon = pygame.image.load('img/icons/knight.png')
priestess_icon = pygame.image.load('img/icons/priest.png')
hashashin_icon = pygame.image.load('img/icons/asasin.png')


#function for drawing text
def drawText(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))

#function draw background
def drawBg(background_img):
    screen.blit(background_img, (0,0))

#function draw panel
def drawPanel():
    #draw panel retangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #draw knight stats
    #draw knight name 
    drawText(f'{heroes[heroChoice].name}', font, white, 110, screen_height - bottom_panel + 10)
    #draw knight HP
    drawText(f'HP: {heroes[heroChoice].getHP()}', font, red, 200, screen_height - bottom_panel + 10)
    #draw bandit stats
    for count, i in enumerate(banditList):
        drawText(f'{i.name}', font, white, 520, (screen_height - bottom_panel + 10) + count * 60 )
        drawText(f'HP: {i.getHP()}', font, red, 610, (screen_height - bottom_panel + 10) + count * 60)

#abstract class entity
class Entity(ABC):
    def __init__(self, x, y, name, maxHP, strength, potions):
        self.name = name
        self.__maxHP = maxHP
        self.__hp = maxHP
        self.__strenght = strength
        self.__startPotions = potions
        self.__potions = potions
        self.alive = True
        self.animationList = []
        self.frameIndex = 0
        self.action = 0 #0: idle, 1: attack, 2: hurt, 3: death
        self.updateTime = pygame.time.get_ticks()
        # Do NOT load images here! Let child classes handle it.
        self.image = None
        self.rect = None

    def updateFrame(self):
        #handle animation
        animationCooldown = 100
        #update image
        self.image = self.animationList[self.action][self.frameIndex]
            #check if enough time is passed since the last update
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
        if self.alive == True:
            #if the animation has run out the restart back to the start
            if self.frameIndex >= len(self.animationList[self.action]):
                self.idle()
        else:
            if self.frameIndex >= len(self.animationList[self.action]):
                self.frameIndex = len(self.animationList[self.action]) - 1

    
    def idle(self):
        self.action = 0
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()
    
    def hurt(self):
        self.action = 2
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()
    
    def death(self):
        self.action = 3
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()

    def reset(self):
        self.action = 0
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()
        self.alive = True
        self.setPotions(self.getStartPotions())
        self.setHP(self.getMaxHP())

    def draw(self):
        screen.blit(self.image, self.rect) 

    def getMaxHP(self):
        return self.__maxHP
    
    def setMaxHP(self, newMaxHP):
        self.__maxHP = newMaxHP
    
    def getHP(self):
        return self.__hp
    
    def setHP(self, newHP):
        self.__hp = newHP
    
    def getStrenght(self):
        return self.__strenght
    
    def setStrenght(self, newStrenght):
        self.__strenght = newStrenght

    def getStartPotions(self):
        return self.__startPotions

    def setStartPotions(self, newStartPotions):
        self.__startPotions = newStartPotions
    
    def getPotions(self):
        return self.__potions

    def setPotions(self, newPotions):
        self.__potions = newPotions
     
    @abstractmethod
    def attack(self):
        pass
    
#hero class inheritance from entity
class Hero(Entity):
    def __init__(self, x, y, name, maxHP, strength, potions):
        super().__init__(x, y, name, maxHP, strength, potions)
    

    def attack(self, target):
        if heroChoice == 0:
            rand = random.randint(-5, 5)
        elif heroChoice == 1:
            rand = random.randint(-4, 3)
        else:
            rand = random.randint(-3, 6)
        damage = self.getStrenght() + rand
        targetHP = target.getHP()
        targetHP -= damage 
        target.setHP(targetHP)
        target.hurt()
        #check if target has died
        if target.getHP() < 1:
            target.setHP(0)
            target.alive = False
            target.death()
        damageText = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damageTextGroup.add(damageText)
        #set variable to attack animation
        self.action = 1
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()

#hero classes inheritance from hero   
class Knight(Hero):
    def __init__(self, x, y, name, maxHP, strength, potions):
        super().__init__(x, y, name, maxHP, strength, potions)
        # Load fire_knight animations (custom path)
        self.animationList = []
        # Idle
        tempList = []
        for i in range(1,9):
            img = pygame.image.load(f'img/Hero/fire_knight/01_idle/idle_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Attack
        tempList = []
        for i in range(9,19):
            img = pygame.image.load(f'img/Hero/fire_knight/08_sp_atk/sp_atk_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Hurt
        tempList = []
        for i in range(1,7):
            img = pygame.image.load(f'img/Hero/fire_knight/10_take_hit/take_hit_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Death
        tempList = []
        for i in range(1,14):
            img = pygame.image.load(f'img/Hero/fire_knight/11_death/death_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        self.image = self.animationList[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 

#hero classes inheritance from hero
class Priestess(Hero):
    def __init__(self, x, y, name, maxHP, strength, potions):
        super().__init__(x, y, name, maxHP, strength, potions)
        # Load fire_knight animations (custom path)
        self.animationList = []
        # Idle
        tempList = []
        for i in range(1,9):
            img = pygame.image.load(f'img/Hero/water_priestess/01_idle/idle_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Attack
        tempList = []
        for i in range(18,28):
            img = pygame.image.load(f'img/Hero/water_priestess/09_3_atk/3_atk_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Hurt
        tempList = []
        for i in range(1,8):
            img = pygame.image.load(f'img/Hero/water_priestess/13_take_hit/take_hit_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Death
        tempList = []
        for i in range(1,17):
            img = pygame.image.load(f'img/Hero/water_priestess/14_death/death_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        self.image = self.animationList[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 

#hero classes inheritance from hero
class Hashashin(Hero):
    def __init__(self, x, y, name, maxHP, strength, potions):
        super().__init__(x, y, name, maxHP, strength, potions)
        # Load fire_knight animations (custom path)
        self.animationList = []
        # Idle
        tempList = []
        for i in range(1,9):
            img = pygame.image.load(f'img/Hero/wind_hashashin/idle/idle_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Attack
        tempList = []
        for i in range(15,27):
            img = pygame.image.load(f'img/Hero/wind_hashashin/3_atk/3_atk_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Hurt
        tempList = []
        for i in range(1,7):
            img = pygame.image.load(f'img/Hero/wind_hashashin/take_hit/take_hit_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Death
        tempList = []
        for i in range(1,20):
            img = pygame.image.load(f'img/Hero/wind_hashashin/death/death_{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        self.image = self.animationList[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 

#bandit class inheritance from entity
class Bandit(Entity):
    def __init__(self, x, y, name, maxHP, strength, potions):
        super().__init__(x, y, name, maxHP, strength, potions)
        # Load Bandit animations (custom path)
        self.animationList = []
        # Idle
        tempList = []
        for i in range(8):
            img = pygame.image.load(f'img/Bandit/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Attack
        tempList = []
        for i in range(8):
            img = pygame.image.load(f'img/Bandit/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Hurt
        tempList = []
        for i in range(3):
            img = pygame.image.load(f'img/Bandit/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        # Death
        tempList = []
        for i in range(10):
            img = pygame.image.load(f'img/Bandit/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            tempList.append(img)
        self.animationList.append(tempList)
        self.image = self.animationList[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def attack(self, target):
        rand = random.randint(-4, 4)
        damage = self.getStrenght() + rand
        targetHP = target.getHP()
        targetHP -= damage
        target.setHP(targetHP)
        target.hurt()
        #check if target has died
        if target.getHP() < 1:
            target.setHP(0)
            target.alive = False
            target.death()
        damageText = DamageText(target.rect.centerx, target.rect.y + 220, str(damage), red)
        damageTextGroup.add(damageText)
        #set variable to attack animation
        self.action = 1
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()
        
#Health Bar class
class HealthBar():
    def __init__(self, x, y, hp, maxHP):
        self.hp = hp
        self.maxHP = maxHP
        self.x = x
        self.y = y
    
    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.maxHP
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

#button class
class Button():
    def __init__(self, surface, x, y, image, sizeButtonX, sizeButtonY):
        self.image = pygame.transform.scale(image, (sizeButtonX, sizeButtonY))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
    
    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouse over and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == 0:
                action = True
        #         self.clicked = True
        
        # if pygame.mouse.get_pressed()[0] == 0:
        #     self.clicked = False
        
        #draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

#damage text class inheritance from pygame.sprite.Sprite
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1  
        self.counter += 1
        if self.counter > 30:   
            self.kill()

damageTextGroup = pygame.sprite.Group()

knight = Knight(200, 150, 'Knight', 35, 8, 3)
priestiess = Priestess(200, 150, 'Priest', 27, 11, 4)
hashashin = Hashashin(200, 150, 'Asasin', 25, 15, 2)

heroes = [knight, priestiess, hashashin]

bandit1 = Bandit(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Bandit(700, 270, 'Bandit', 20, 6, 1)

banditList = []
banditList.append(bandit1)
banditList.append(bandit2)

bandit1HealthBar = HealthBar(525, screen_height - bottom_panel + 40, bandit1.getHP(), bandit1.getMaxHP())
bandit2HealthBar = HealthBar(525, screen_height - bottom_panel + 100, bandit2.getHP(), bandit2.getMaxHP())

#create button
potionButton = Button(screen, 165, screen_height - bottom_panel + 70, potion_img, 60, 60)
restartButton = Button(screen, 330, 120, restart_img, 135, 30)
knightButton = Button(screen, 20, 200, knight_icon,knight_icon.get_width(), knight_icon.get_height())
priestessButton = Button(screen, 300, 200, priestess_icon, priestess_icon.get_width(), priestess_icon.get_height())
hashashinButton = Button(screen, 570, 200, hashashin_icon, hashashin_icon.get_width(), hashashin_icon.get_height())

run = True
gameState = "menu"  
while run:

    clock.tick(fps)

    if gameState == "menu":
        drawBg(background_img1)
        drawText("Choose Your Hero", font, white, 300, 100)
        if knightButton.draw():
            heroChoice = 0
            gameState = "main"
        if priestessButton.draw():
            heroChoice = 1
            gameState = "main"
        if hashashinButton.draw():
            heroChoice = 2
            gameState = "main"
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        continue

    drawBg(background_img)
    drawPanel()

    heroesHealthBar = HealthBar(115, screen_height - bottom_panel + 40, heroes[heroChoice].getHP(), heroes[heroChoice].getMaxHP())
    heroesHealthBar.draw(heroes[heroChoice].getHP())
    bandit1HealthBar.draw(bandit1.getHP())
    bandit2HealthBar.draw(bandit2.getHP())

    #draw entity
    heroes[heroChoice].updateFrame()
    heroes[heroChoice].draw()
    for bandit in banditList:
        bandit.updateFrame()
        bandit.draw()

    #draw damage text
    damageTextGroup.update()
    damageTextGroup.draw(screen)

    #control player action
    #reset action variables
    attack = False
    potion = False
    target = None
    #make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(banditList):
        if bandit.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked == True and bandit.alive == True:
                attack = True
                target = banditList[count]

    
    if potionButton.draw():
        potion = True
    #draw number of potion
    drawText(f'{heroes[heroChoice].getPotions()}', fontButton, white, 211, screen_height - bottom_panel + 73)

    # game action
    if gameOver == 0:
        #player action
        if heroes[heroChoice].alive == True:
            if currentEntity == 1:
                actionCooldown += 1
                if actionCooldown >= actionWaitTime:
                    #look for player action
                    #attack
                    if attack == True and target != None:
                        heroes[heroChoice].attack(target)
                        currentEntity += 1
                        actionCooldown = 0
                    #potion
                    if potion == True and heroes[heroChoice].getPotions() != 0:
                        if heroes[heroChoice].getMaxHP() - heroes[heroChoice].getHP() > potionHeal:
                            healAmount = potionHeal
                        else:
                            healAmount = heroes[heroChoice].getMaxHP() - heroes[heroChoice].getHP()
                        heroes[heroChoice].setHP(heroes[heroChoice].getHP() + healAmount)
                        heroes[heroChoice].setPotions(heroes[heroChoice].getPotions() - 1)
                        damageText = DamageText(heroes[heroChoice].rect.centerx, heroes[heroChoice].rect.y, str(healAmount), green)
                        damageTextGroup.add(damageText)
                        currentEntity += 1
                        actionCooldown = 0
        else:
            gameOver = -1            

        #enemy action
        for count, bandit in enumerate(banditList):
            if currentEntity == 2 + count:
                if bandit.alive == True:
                    actionCooldown += 1
                    if actionCooldown >= actionWaitTime:
                        #check if bandit need heal
                        if (bandit.getHP() / bandit.getMaxHP()) <= 0.5 and bandit.getPotions() != 0:
                            if bandit.getMaxHP() - bandit.getHP() > potionHeal:
                                healAmount = potionHeal
                            else:
                                healAmount = bandit.getMaxHP() - bandit.getHP()
                            bandit.setHP(bandit.getHP() + healAmount)
                            bandit.setPotions(bandit.getPotions() - 1)
                            damageText = DamageText(bandit.rect.centerx, bandit.rect.y, str(healAmount), green)
                            damageTextGroup.add(damageText)
                            currentEntity += 1
                            actionCooldown = 0
                        #attack
                        else:
                            bandit.attack(heroes[heroChoice])
                            currentEntity += 1
                            actionCooldown = 0
                else:
                    currentEntity += 1
        
        #if all entity have had a turn then reset
        if currentEntity > totalEntity:
            currentEntity = 1

    # check alive bandit
    aliveBandit = 0
    for bandit in banditList:
        if bandit.alive == True:
            aliveBandit += 1
    if aliveBandit == 0:
        gameOver = 1

    #check if game is over 
    if gameOver != 0:
        if gameOver == 1:
            screen.blit(victory_img, (262, 50))
        else:
            screen.blit(defeat_img, (280,50))
        if restartButton.draw():
            heroes[heroChoice].reset()
            for bandit in banditList:
                bandit.reset()
            currentEntity = 1
            # actionCooldown 
            gameOver = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit