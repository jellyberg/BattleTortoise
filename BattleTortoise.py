# Battle Tortoise
# by Adam Binks
#######################################################################################################
#######################################################################################################
#######################################################################################################

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
BIGFONT   = pygame.font.Font('fontTitle.ttf', 25)
MEGAFONT  = pygame.font.Font('fontTitle.ttf', 42)

TORTOISESCREENPOS = (int(WINDOWWIDTH / 4),     int((WINDOWHEIGHT / 3) * 2))
ENEMYSCREENPOS =    (int((WINDOWWIDTH / 3) * 2), int(WINDOWHEIGHT / 8))
GAP = 5
FLASHREDTIME = 0.2
ATTACKANIMTIME = 2000 # in milliseconds

backgroundImg = pygame.image.load('beachBackground.png').convert()
tortoiseIdleImg = pygame.image.load('tortoiseIdle1.png').convert_alpha()
tortoiseIdleHitImg = pygame.image.load('tortoiseIdle1Hit.png').convert_alpha()
tortoiseBlockImg = pygame.image.load('tortoiseBlock1.png').convert_alpha()
tortoiseBlockHitImg = pygame.image.load('tortoiseBlock1Hit.png').convert_alpha()
bearIdleImg = pygame.image.load('bearIdle1.png').convert_alpha()
bearIdleHitImg = pygame.image.load('bearIdle1Hit.png').convert_alpha()

# Colours     R    G    B  ALPHA
WHITE     = (255, 255, 255, 255)
BLACK     = (  0,   0,   0, 255)
RED       = (255,   0,   0, 255)
DARKRED   = (220,   0,   0, 255)
BLUE      = (  0,   0, 255, 255)
YELLOW    = (255, 250,  17, 255)
GREEN     = (  0, 255,   0, 255)
ORANGE    = (255, 165,   0, 255)
DARKGREEN = (  0, 155,   0, 255)
DARKGREY  = ( 60,  60,  60, 255)
LIGHTGREY = (180, 180, 180, 255)
BROWN     = (139,  69,  19, 255)

# KEYBINDINGS
BLOCKKEY = K_SPACE

# ALL MOBS STATS
TORTOISE = {'health': 100, 'strength': 3, 'idleImg': tortoiseIdleImg, 'blockImg': tortoiseBlockImg, 
            'idleHitImg': tortoiseIdleHitImg, 'blockHitImg': tortoiseBlockHitImg}
BEAR = {'health': 100, 'strength': 5, 'idleImg': bearIdleImg, 'idleHitImg': bearIdleHitImg, 
        'attacks' : ['scratch', 'claw', 'bite']}

BLOCKEFFECTIVENESS = 4 # smaller number = more effective
RANDOMDAMAGEMARGIN = 4
MISSCHANCE = 2
    

#######################################################################################################
#######################################################################################################
#######################################################################################################


class Tortoise :
    startingHealth = 100
    SCREENPOSX, SCREENPOSY = TORTOISESCREENPOS
    incomingDamage = 0

    def __init__(self):
        self.img = TORTOISE['idleImg']
        self.rect = Rect((TORTOISESCREENPOS), (self.img.get_size()))
        self.health = TORTOISE['health']
        self.attacks = ['bite', 'headbutt']
        self.strength = 3
        self.isBlocking = False
        self.initUI()
        self.timeOfLastHit = time.time() - 100

    def simulate(self, turn, screen, userInput):
        #SIMULATE
        self.block(turn, userInput)
        self.takeDamage()
        self.handleImg()
        #DRAW
        screen.blit(self.img, self.rect)
        self.updateUI(screen, userInput, turn)
        self.attack(screen)
        self.lastHealth = self.health

    def initUI(self):
        # HEALTH BAR
        self.lastHealth = 0
        self.healthBar = pygame.Surface((100, 10))
        self.healthBar.fill(BLACK)
        self.healthBarRed = pygame.Surface((98, 8))
        self.healthBarRed.fill(RED)
        self.healthText = Button('Tortoise\'s health:', 0, (5, WINDOWHEIGHT - 35))

        # DAMAGE NUMBERS
        self.damageNums = []
        self.dmgNumPos = (self.rect.centerx, self.rect.top - 10)

        # ATTACK LIST
        self.attackButtons = []
        self.attackTitle = Button('Attacks:', 0, (GAP, GAP), 0, 'IsTitle', 0)
        self.attackButtons.append(self.attackTitle)
        dummy = Button('test', 0, (0, 0), 0, 0, 0)
        for i in range(len(self.attacks)):
            pos = (GAP, GAP * (i + 2) + self.attackTitle.rect.height + (i * dummy.rect.height))
            self.attackButtons.append(Button(self.attacks[i].title(), 0, (pos), 'isClickable', 0, 0))
        self.clickedButtons = []


        
    def updateUI(self, screen, userInput, turn):
        # HEALTH BAR
        if self.health != self.lastHealth:
            if self.health < 0: self.health = 0
            self.healthBar.blit(self.healthBarRed, (1, 1))
            self.healthBarGreen = pygame.Surface((int((self.healthBarRed.get_width() / TORTOISE['health']) * self.health), \
                                                 int(self.healthBarRed.get_height())))
            self.healthBarGreen.fill(GREEN)
            self.healthBar.blit(self.healthBarGreen, (1, 1))
        screen.blit(self.healthBar, (5, WINDOWHEIGHT - 15))
        self.healthText.simulate(screen, None)
        self.lastHealth = self.health

        # DAMAGE NUMBERS
        for num in self.damageNums:
            num.simulate(screen)

        # ATTACK LIST
        i = -1
        for button in self.attackButtons:
            button.simulate(screen, userInput)
            if button.isClickable and button.isClicked and i not in self.clickedButtons and turn == 'tortoise':
                self.clickedButtons.append(i)
            i += 1

    def attack(self, screen):
        global turn
        if self.clickedButtons:
            # ANIMATE
            screenFreeze = screen.copy()
            frames = int(ATTACKANIMTIME / FPS)
            startx, starty = self.rect.topleft
            enemyx, enemyy = ENEMYSCREENPOS
            endx, endy = (enemyx - 50, enemyy - 5)
            endPos = endx, endy
            xstep = int((endx - startx) / frames)
            ystep = int((endy - starty) / frames)
            while self.rect.topleft != endPos:
                self.rect.move_ip(xstep, ystep)
                screen.blit(screenFreeze, self.rect)
                screen.blit(self.img, self.rect)
                pygame.display.update()
                checkForQuit()

                if self.rect.left == endx or self.rect.top  == endy:
                    print('Topleft: ' + str(self.rect.topleft) + ', endPos: ' + str(endPos))


            # ATTACK TEXT
            attackText = DamageNum('Tortoise uses ' + self.attacks[(self.clickedButtons[0])] + '!', self.dmgNumPos, GREEN)
            self.damageNums.append(attackText)
            # DEAL DAMAGE
            damage = self.clickedButtons[0] * self.strength + random.randint(MISSCHANCE, RANDOMDAMAGEMARGIN)
            Enemy.incomingDamage = damage
            self.clickedButtons = []
            #turn = 'enemy'

    def takeDamage(self):
        damage = Tortoise.incomingDamage
        if damage > 0:
            if self.isBlocking:
                damage -= int(damage / BLOCKEFFECTIVENESS)
            self.health -= damage
            Tortoise.incomingDamage = 0
            dmgNum = DamageNum(damage, self.dmgNumPos, RED)
            self.damageNums.append(dmgNum)
            self.timeOfLastHit = time.time()
        elif damage < 0:
            dmgNum = DamageNum('MISS!', self.dmgNumPos, GREEN)
            self.damageNums.append(dmgNum)

    def block(self, turn, userInput):
        if turn == 'enemy':
            for key in userInput.pressedKeys[:]:
                if key.key == BLOCKKEY:
                    self.isBlocking = True
                    return
        self.isBlocking = False
        self.img = TORTOISE['idleImg']

    def handleImg(self):
        if time.time() - FLASHREDTIME < self.timeOfLastHit:
            if self.isBlocking:
                self.img = TORTOISE['blockHitImg']
                return
            else:
                self.img = TORTOISE['idleHitImg']
                return
        elif self.isBlocking:
            self.img = TORTOISE['blockImg']
        else:
            self.img = TORTOISE['idleImg']


#######################################################################################################


class Enemy:
    screenPos = ENEMYSCREENPOS
    incomingDamage = 0
    
    def __init__(self, creature, strength, startingHealth):
        adjectives = ['merry', 'angry', 'maddened', 'lazy', 'hungry', 'vicious',
                      'psychotic', 'insane', 'misunderstood', 'raging', 'mad', 'terrifying']
        adjNum = random.randint(0, len(adjectives) - 1)
        self.name = adjectives[adjNum].title() + ' ' + creature.title()
        self.creature = creature
        self.strength = strength
        self.startingHealth = startingHealth
        self.health = startingHealth
        if creature == 'BEAR':
            self.img = BEAR['idleImg']
            self.attacks = BEAR['attacks']
        self.rect = Rect((Enemy.screenPos), (self.img.get_size()))
        self.genAttacks()
        self.initUI()
        self.timeOfLastHit = time.time() - 100

    def simulate(self, turn, screen):
        self.handleImg()
        self.draw(screen)
        if turn == 'enemy':
            self.attack()
        else:
            self.takeDamage()
        self.updateUI(screen)
        if turn == 'enemy':
            return 'tortoise'
        else:
            return 'tortoise'

    def handleImg(self):
        if self.creature == 'BEAR':
            if time.time() - FLASHREDTIME < self.timeOfLastHit:
                self.img = BEAR['idleHitImg']
                return
            self.img = BEAR['idleImg']

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def initUI(self):
        # HEALTH BAR
        self.lastHealth = 0
        self.healthBar = pygame.Surface((100, 10))
        self.healthBar.fill(BLACK)
        self.healthBarRed = pygame.Surface((98, 8))
        self.healthBarRed.fill(RED)
        self.healthText = Button(self.name + '\'s health:', 0, (WINDOWWIDTH - 5, WINDOWHEIGHT - 35), 0, 0, 1)
        self.healthText.rect.right = 1000 # WINDOWWIDTH - 5

        # DAMAGE NUMBERS
        self.damageNums = []
        self.dmgNumPos = (self.rect.centerx, self.rect.bottom + 40)
        self.dmgTextPos = (self.rect.left, self.rect.bottom + 40)
        
    def updateUI(self, screen):
        # HEALTH BAR
        if self.health != self.lastHealth:
            self.healthBar.blit(self.healthBarRed, (1, 1))
            self.healthBarGreen = pygame.Surface((int((self.healthBarRed.get_width() / self.startingHealth) * self.health), \
                                                 int(self.healthBarRed.get_height())))
            self.healthBarGreen.fill(GREEN)
            self.healthBar.blit(self.healthBarGreen, (1, 1))
        screen.blit(self.healthBar, (WINDOWWIDTH - 5 - self.healthBar.get_width(), WINDOWHEIGHT - 15))
        self.healthText.simulate(screen, None)

        # DAMAGE NUMBERS
        for num in self.damageNums:
            num.simulate(screen)

    def genAttacks(self):
        self.numAttacks = len(self.attacks)

    def attack(self):
        attackNum = random.randint(0, self.numAttacks - 1)
        damage = attackNum * self.strength + random.randint(MISSCHANCE, RANDOMDAMAGEMARGIN)
        Tortoise.incomingDamage = damage
        attackText = DamageNum(self.name + ' uses ' + self.attacks[attackNum] + '!', self.dmgTextPos, GREEN)
        self.damageNums.append(attackText)

    def takeDamage(self):
        damage = Enemy.incomingDamage
        if damage > 0:
            self.health -= damage
            Enemy.incomingDamage = 0
            dmgNum = DamageNum(damage, self.dmgNumPos, RED)
            self.damageNums.append(dmgNum)
            self.timeOfLastHit = time.time()
        elif damage < 0:
            dmgNum = DamageNum('MISS!', self.dmgNumPos, GREEN)
            self.damageNums.append(dmgNum)
        if self.health < 0:
            self.health = 0


#######################################################################################################
        

class Button:
    def __init__(self, text, style, screenPos, isClickable=0, isTitle=0, screenPosIsTopRight=0):
        self.text, self.style, self.screenPos, self.isClickable, self.posIsTopRight = \
        (text, style, screenPos, isClickable, screenPosIsTopRight)
        if isTitle:
            self.textSurf = BIGFONT.render(self.text, 1, LIGHTGREY)
        else:
            self.textSurf = BASICFONT.render(self.text, 1, WHITE)
        # CREATE BASIC SURF
        self.padding = 6 # will be controlled by 'style' eventually
        self.buttonSurf = pygame.Surface((self.textSurf.get_width() + self.padding, self.textSurf.get_height() + self.padding))
        self.buttonSurf.fill(BLUE)
        self.buttonSurf.blit(self.textSurf, (int(self.padding /2), int(self.padding /2)))
        self.currentSurf = self.buttonSurf
        self.rect = Rect(self.screenPos, self.buttonSurf.get_size())
        # CREATE ADDITIONAL SURFS
        if isClickable:
            # MOUSE HOVER
            self.hoverSurf = pygame.Surface(self.buttonSurf.get_size())
            self.hoverSurf.fill(RED)
            self.hoverSurf.blit(self.textSurf, (int(self.padding /2), int(self.padding /2)))
            # MOUSE CLICK
            self.clickSurf = pygame.Surface(self.buttonSurf.get_size())
            self.clickSurf.fill(DARKRED)
            self.clickSurf.blit(self.textSurf, (int(self.padding /2), int(self.padding /2)))
            self.isClicked = False

    def simulate(self, screen, userInput):
        if self.isClickable: self.handleClicks(userInput)
        self.draw(screen)

    def draw(self, screen):
        if self.posIsTopRight:
            self.rect.topright = self.screenPos
        else:
            self.rect.topleft = self.screenPos
        screen.blit(self.currentSurf, self.rect)

    def handleClicks(self, userInput=None):
        self.isClicked = False
        if self.rect.collidepoint(userInput.mousePos):
            if userInput.mousePressed == True:
                self.currentSurf = self.clickSurf
            else:
                self.currentSurf = self.hoverSurf
        else:
            self.currentSurf = self.buttonSurf
        if userInput.mouseUnpressed == True and self.rect.collidepoint(userInput.mousePos):
            self.isClicked = True


#######################################################################################################


class DamageNum:
    def __init__(self, number, roughPos, roughColor):
        self.num = number
        roughx, roughy = roughPos
        self.x = roughx + random.randint(-10, 10)
        self.y = roughy
        r, g, b, a = roughColor
        self.color = pygame.Color(r, g, b, a)

    def simulate(self, screen):
        if self.color.a > 0:
            self.surf, self.rect = genText(str(self.num), (self.x, self.y), self.color)
            surf2 = pygame.Surface((self.surf.get_width() + 10, self.surf.get_height() + 10))
            surf2.fill(YELLOW)
            surf2.blit(self.surf, (0, 0))
            surf2.set_alpha(self.color.a)
            screen.blit(surf2, self.rect)
            self.color.a -= 5
            self.y -= 1

        
#######################################################################################################


class Input:
    def __init__(self):
        Input.pressedKeys = []
        Input.mousePressed = False
        Input.mouseUnpressed = False
        Input.mousePos = (0, 0)
        
    def get(self):
        Input.mouseUnpressed = False
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
                Input.mouseUnpressed = False
            elif event.type == MOUSEBUTTONUP:
                Input.mousePressed = False
                Input.mouseUnpressed = True

    

#######################################################################################################
#######################################################################################################
#######################################################################################################



def main():
    while True:
        winner, tortoiseHealth, enemyHealth = runGame()
        gameOverScreen(screen, winner, tortoiseHealth, enemyHealth)


def runGame():
    global screen, turn
    
    userInput = Input()
    tortoise = Tortoise()
    enemy = Enemy('BEAR', random.randint(3, 5), 50)
    skipTurnButton = Button('Skip turn', 0, (WINDOWWIDTH - GAP, GAP), 1, 0, 1)
    buttons = [skipTurnButton]
    turn = 'tortoise'
    while True: # main game loop
        userInput.get()
        screen.blit(backgroundImg, (0,0))
        tortoise.simulate(turn, screen, userInput)
        turn = enemy.simulate(turn, screen)

        for button in buttons:
            button.simulate(screen, userInput)
        if skipTurnButton.isClicked:
            if turn == 'tortoise':
                turn = 'enemy'
        screen = updateLiveElements(screen, turn)
        
        
        pygame.display.update()
        checkForQuit()
        FPSCLOCK.tick(FPS)

        if tortoise.health < 1:
            winner = 'enemy'
            pygame.time.wait(200)
            break
        elif enemy.health < 1:
            winner = 'tortoise'
            pygame.time.wait(200)
            break

    return(winner, tortoise.health, enemy.health)


def gameOverScreen(screen, winner, tortoiseHealth, enemyHealth):
    newScreen = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    userInput = Input()
    if winner == 'tortoise':
        loser = 'enemy'
        verb = 'won'
        mainColour = GREEN
        accentColour = DARKGREEN
    elif winner == 'enemy':
        loser = 'tortoise'
        verb = 'lost'
        mainColour = RED
        accentColour = DARKRED

    newScreen.fill(mainColour)
    titleSurf, titleRect = genText('You ' + verb + '!', None, WHITE, False, True, (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 3)))
    newScreen.blit(titleSurf, titleRect)
    newScreen.set_alpha(5)

    for i in range(60): # ANIMATE TRANSITION:
        screen.blit(newScreen, (0, 0))
        pygame.display.update()
        checkForQuit()
        FPSCLOCK.tick()

    base = screen.copy()
    playAgain = Button('Play again', None, (int(WINDOWWIDTH / 2) - 10, int(WINDOWHEIGHT / 3) * 2), 1, 0, 1)
    quit = Button('Quit', None, (int(WINDOWWIDTH / 2) + 10, int(WINDOWHEIGHT / 3) * 2), 1, 0, 0)

    while True:
        userInput.get()
        playAgain.simulate(screen, userInput)
        if playAgain.isClicked:
            return
        quit.simulate(screen, userInput)
        if quit.isClicked:
            terminate()
        checkForQuit()
        pygame.display.update()
        FPSCLOCK.tick()
    pygame.time.wait(2000)

        
def genText(text, topLeftPos, colour, isTitle=0, isMega=0, centerPos=0):
    if isTitle:
        font = BIGFONT
    elif isMega:
        font = MEGAFONT
    else: font = BASICFONT
    surf = font.render(text, 1, colour)
    rect = surf.get_rect()
    if centerPos:
        rect.center = centerPos
    else:
        rect.topleft = topLeftPos
    return (surf, rect)


def updateLiveElements(screen, turn):
    turnSurf, turnRect = genText(str('Turn: ' + turn), (int(WINDOWWIDTH / 2), 50), WHITE, 1)
    turnRect.centerx = int(WINDOWWIDTH / 2)
    screen.blit(turnSurf, turnRect)
    return screen
    

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
