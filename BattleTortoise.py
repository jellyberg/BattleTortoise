# Battle Tortoise
# by Adam Binks

import random, pygame, sys, time
from pygame.locals import *
pygame.init()

FPS = 30
FPSCLOCK = pygame.time.Clock()
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Battle tortoise')

BASICFONT = pygame.font.Font('freesansbold.ttf', 12)
BIGFONT   = pygame.font.Font('freesansbold.ttf', 36)

TORTOISESCREENPOS = (int(WINDOWWIDTH / 4),     int((WINDOWHEIGHT / 3) * 2))
ENEMYSCREENPOS =    (int((WINDOWWIDTH / 3) * 2), int(WINDOWHEIGHT / 30))

backgroundImg = pygame.image.load('beachBackground.png')
tortoiseIdleImg = pygame.image.load('tortoiseIdle1.png')
tortoiseBlockImg = pygame.image.load('tortoiseBlock1.png')
bearIdleImg = pygame.image.load('bearIdle1.png')

# Colours     R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
DARKRED   = (255,  10,  10)
BLUE      = (  0,   0, 255)
GREEN     = (  0, 255,   0)
ORANGE    = (255, 165,   0)
DARKGREEN = (  0, 155,   0)
DARKGREY  = ( 60,  60,  60)
LIGHTGREY = (180, 180, 180)
BROWN     = (139,  69,  19)

# KEYBINDINGS
BLOCKKEY = K_SPACE

# ALL MOBS STATS
TORTOISE = {'health': 100, 'strength': 3, 'idleImg': tortoiseIdleImg, 'blockImg': tortoiseBlockImg}
BEAR = {'health': 100, 'strength': 5, 'idleImg': bearIdleImg, 'attacks' : ['scratch', 'claw', 'bite']}
             




class Tortoise :
    startingHealth = 100
    SCREENPOSX, SCREENPOSY = TORTOISESCREENPOS
    incomingDamage = 0

    def __init__(self):
        self.health = TORTOISE['health']
        self.img = TORTOISE['idleImg']
        self.attacks = self.generateAttacksList
        self.isBlocking = False
        self.initUI()

    def generateAttacksList(self):
        return['bite', 'headbutt']

    def simulate(self, turn, screen, userInput):
        self.block(turn, userInput)
        self.handleImg()
        self.draw(screen)
        self.lastHealth = self.health

    def draw(self, screen):
        screen.blit(self.img, TORTOISESCREENPOS)
        self.updateUI(screen)

    def initUI(self):
        self.lastHealth = 0
        self.healthBar = pygame.Surface((100, 10))
        self.healthBar.fill(BLACK)
        self.healthBarRed = pygame.Surface((98, 8))
        self.healthBarRed.fill(RED)
        self.healthText = Button('Tortoise health:', 0, (5, WINDOWHEIGHT - 35))
        
    def updateUI(self, screen):
        # HEALTH BAR
        if self.health != self.lastHealth:
            self.healthBar.blit(self.healthBarRed, (1, 1))
            self.healthBarGreen = pygame.Surface((int((self.healthBarRed.get_width() / TORTOISE['health']) * self.health), \
                                                 int(self.healthBarRed.get_height())))
            self.healthBarGreen.fill(GREEN)
            self.healthBar.blit(self.healthBarGreen, (1, 1))
        screen.blit(self.healthBar, (5, WINDOWHEIGHT - 15))
        self.healthText.simulate(screen, None)

    def block(self, turn, userInput):
        if turn == 'enemy':
            for key in userInput.pressedKeys[:]:
                if key.key == BLOCKKEY:
                    self.isBlocking = True
                    return
        self.isBlocking = False

    def handleImg(self):
        if self.isBlocking == True:
            self.img = TORTOISE['blockImg']
        else:
            self.img = TORTOISE['idleImg']
                    


class Enemy:
    screenPos = ENEMYSCREENPOS
    incomingDamage = 0
    
    def __init__(self, creature, strength, startingHealth):
        adjectives = ['merry', 'angry', 'maddened', 'lazy', 'hungry', 'vicious',
                      'psychotic', 'insane', 'misunderstood', 'raging']
        adjNum = random.randint(0, len(adjectives) - 1)
        self.name = adjectives[adjNum] + creature.lower()
        self.creature = creature
        self.strength = strength
        self.startingHealth = startingHealth
        self.health = startingHealth
        if creature == 'BEAR':
            self.img = BEAR['idleImg']
            self.attacks = BEAR['attacks']

    def simulate(self, turn, screen):
        self.handleImg()
        self.draw(screen)
        self.attack

    def handleImg(self):
        if self.creature == 'BEAR':
            img = BEAR['idleImg']

    def draw(self, screen):
        screen.blit(self.img, Enemy.screenPos)

    def genAttacks(self):
        self.numAttacks = len(self.attacks)

    def attack(self):
        attackNum = random.randint(0, self.numAttacks - 1)
        damage = attackNum * self.strength


        
class Button:
    def __init__(self, text, style, screenPos, isClickable=0, isTitle=0):
        self.text, self.style, self.screenPos, self.isClickable = \
        (text, style, screenPos, isClickable)
        if isTitle:
            self.textSurf = BIGFONT.render(self.text, 1, LIGHTGREY)
        else:
            self.textSurf = BASICFONT.render(self.text, 1, WHITE)

        self.rect = Rect(self.screenPos, self.textSurf.get_size())
            
        self.buttonSurf = pygame.Surface(self.textSurf.get_size())
        self.buttonSurf.fill(BLUE)
        self.buttonSurf.blit(self.textSurf, (0, 0))
        self.currentSurf = self.buttonSurf

        if isClickable:
            self.hoverSurf = pygame.Surface(self.buttonSurf.get_size())
            self.hoverSurf.fill(DARKRED)
            self.hoverSurf.blit(self.textSurf, (0, 0))

            self.clickSurf = pygame.Surface(self.buttonSurf.get_size())
            self.clickSurf.fill(BLACK)
            self.clickSurf.blit(self.textSurf, (0, 0))
            self.isClicked = False
            

    def simulate(self, screen, userInput):
        if self.isClickable: self.handleClicks(userInput)
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.currentSurf, self.screenPos)

    def handleClicks(self, userInput=None):
        self.isClicked = False
        if self.rect.collidepoint(userInput.mousePos):
            if userInput.mousePressed == True:
                self.currentSurf = self.clickSurf
                self.isClicked = True
            else:
                self.currentSurf = self.hoverSurf
        else:
            self.currentSurf = self.buttonSurf



class Input:
    def __init__(self):
        Input.pressedKeys = []
        Input.mousePressed = False
        Input.mousePos = (0, 0)
        
    def get(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.event.post(event)
            elif event.type == KEYDOWN:
                Input.pressedKeys.append(event)
            elif event.type == KEYUP:
                for key in Input.pressedKeys:
                    if event.key == key.key:
                        Input.pressedKeys.remove(key)
            elif event.type == MOUSEMOTION:
                Input.mousePos = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                Input.mousePressed = True
            elif event.type == MOUSEBUTTONUP:
                Input.mousePressed = False
                        
    



def main():
    runGame()


def runGame():
    userInput = Input()
    tortoise = Tortoise()
    enemy = Enemy('BEAR', random.randint(3, 5), 50)
    button1 = Button('A groovy button.', 0, (50, 50), 1, 0)
    UIelements = [button1]
    while True: # main game loop
        userInput.get()
        turn = 'enemy'
        screen.blit(backgroundImg, (0,0))
        tortoise.simulate(turn, screen, userInput)
        enemy.simulate(turn, screen)

        for element in UIelements:
            element.simulate(screen, userInput)
        
        
        pygame.display.update()
        checkForQuit()
        FPSCLOCK.tick(FPS)

        

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def terminate():
    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()
