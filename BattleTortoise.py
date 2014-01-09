# Battle Tortoise
# by Adam Binks
#######################################################################################################
#######################################################################################################
#######################################################################################################

import random, pygame, sys, time, math
from pygame.locals import *
pygame.init()


def main():
    while True:
        winner, tortoiseHealth, enemyHealth = runGame()
        gameOverScreen(screen, winner, tortoiseHealth, enemyHealth)


def runGame():
    global screen, turn

    userInput = Input()
    tortoise = Tortoise()
    enemy = Enemy('BEAR', random.randint(3, 5), 50)
    skipTurnButton = Button('Skip turn', 0, (WINDOWWIDTH - 200, GAP), 1, 0, 1)
    testButton = Button('Tester!', 0, (WINDOWWIDTH - 200, 300), 1, 0, 1, 'And there you have it, a test. And it works...perfectly!')
    buttons = [skipTurnButton, testButton]
    turn = 'tortoise'
    fadeInAlpha = 255 # fade in from previous screen
    prevScreen = screen.copy()
    while True: # main game loop
        userInput.get()
        screen.blit(backgroundImg, (0,0))
        if turn == 'enemy':    # allows correct draw order for animations
            tortoise.simulate(turn, screen, userInput)
            turn = enemy.simulate(turn, screen)
        else:
            turn = enemy.simulate(turn, screen)
            tortoise.simulate(turn, screen, userInput)

        for button in buttons:
            button.simulate(screen, userInput)
        if skipTurnButton.isClicked:
            if turn == 'tortoise':
                turn = 'enemy'
        screen = updateLiveElements(screen, turn)
        
        if fadeInAlpha > 0:
            prevScreen.set_alpha(fadeInAlpha)
            screen.blit(prevScreen, (0, 0))
            fadeInAlpha -= 10

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

        
def genText(text, topLeftPos, colour, isTitle=0, isMega=0, centerPos=0, isPretty=0):
    if isTitle:
        font = BIGFONT
    elif isMega:
        font = MEGAFONT
    elif isPretty:
        font = PRETTYFONT
    else: font = BASICFONT
    surf = font.render(text, 1, colour)
    rect = surf.get_rect()
    if centerPos:
        rect.center = centerPos
    else:
        rect.topleft = topLeftPos
    return (surf, rect)


def updateLiveElements(screen, turn):
    if turn == 'tortoise':
        turnSurf, turnRect = genText(str('Make your move!'), (int(WINDOWWIDTH / 2), 50), WHITE, 1)
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

def loadAnimationFiles(folder, file, frames):
    animation = []
    for num in range(0, frames):
        num = str(num)
        num = num.zfill(4)
        img = pygame.image.load('assets/' + folder + '/' + file + '.' + num + '.png')
        animation.append(img)
    return animation


#######################################################################################################
#######################################################################################################



FPS = 60
FPSCLOCK = pygame.time.Clock()
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Battle tortoise')

loadingScreen = pygame.image.load('assets/loadingScreen.png').convert_alpha()
screen.blit(loadingScreen, (0, 0))
pygame.display.update()

BASICFONT = pygame.font.Font('freesansbold.ttf', 12)
PRETTYFONT = pygame.font.Font('fontTitle.ttf', 12)
BIGFONT   = pygame.font.Font('fontTitle.ttf', 25)
MEGAFONT  = pygame.font.Font('fontTitle.ttf', 42)

TORTOISESCREENPOS = (int(WINDOWWIDTH / 4),     int((WINDOWHEIGHT / 3) * 2))
ENEMYSCREENPOS =    (int((WINDOWWIDTH / 3) * 2), int(WINDOWHEIGHT / 8))
GAP = 5
STATHOOPSIZE = 30
TOOLTIPWORDSPERLINE = 6  # subtract 1!
FLASHREDTIME = 0.2
ATTACKANIMTIME = 20000 # in milliseconds
ENEMYWAITFRAMES = 20 # pause after turn begins before enemy attacks
BLOCKEFFECTIVENESS = 4 # smaller number = more effective
RANDOMDAMAGEMARGIN = 4
MISSCHANCE = 2

backgroundImg = pygame.image.load('beachBackground.png').convert()
tortoiseIdleImg = pygame.image.load('tortoiseIdle1.png').convert_alpha()
tortoiseIdleHitImg = pygame.image.load('tortoiseIdle1Hit.png').convert_alpha()
tortoiseBlockImg = pygame.image.load('tortoiseBlock1.png').convert_alpha()
tortoiseBlockHitImg = pygame.image.load('tortoiseBlock1Hit.png').convert_alpha()


tortoiseIdle = loadAnimationFiles('tortoiseIdle', 'tortoiseIdle', 119)
tortoiseAttack = loadAnimationFiles('tortoiseAttack', 'tortoiseAttack', 179)
bearIdle = loadAnimationFiles('bearIdle', 'bear_idle', 120)
bearAttack = loadAnimationFiles('bearAttack', 'bear_attack', 180)



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
CREAM     = (255, 255, 204,   0)

# KEYBINDINGS
BLOCKKEY = K_SPACE

# ALL MOBS STATS
TORTOISE = {'health': 100, 'strength': 3, 'idleAnim': tortoiseIdle, 'attackAnim': tortoiseAttack, 
            'blockImg': tortoiseBlockImg, 'idleHitImg': tortoiseIdleHitImg, 'blockHitImg': tortoiseBlockHitImg}
BEAR     = {'health': 100, 'strength': 5, 'idleAnim': bearIdle, 'attackAnim': bearAttack,  
            'attacks' : ['scratch', 'claw', 'bite']}


    

#######################################################################################################
#######################################################################################################
#######################################################################################################


class Tortoise :
    startingHealth = 100
    SCREENPOSX, SCREENPOSY = TORTOISESCREENPOS
    incomingDamage = 0

    def __init__(self):
        self.img = TORTOISE['idleAnim'][0]
        self.rect = Rect((TORTOISESCREENPOS), (self.img.get_size()))
        self.health = TORTOISE['health']
        self.attacks = ['bite', 'headbutt']
        self.strength = 3
        self.intelligence = 5
        self.hoopStats = [self.strength, self.intelligence]
        self.hoopStatsNames = ['strength', 'intelligence']
        self.isBlocking = False
        self.initUI()
        self.timeOfLastHit = time.time() - 100
        self.idleAnimNum = 0
        self.attackAnimNum = -1

    def simulate(self, turn, screen, userInput):
        #SIMULATE
        self.block(turn, userInput)
        self.takeDamage()
        self.handleImg()
        #DRAW
        self.updateUI(screen, userInput, turn)
        self.attack(screen)
        screen.blit(self.img, self.rect)
        self.lastHealth = self.health

    def initUI(self):
        # HEALTH BAR
        self.lastHealth = 0
        self.healthBar = pygame.Surface((100, 10))
        self.healthBar.fill(BLACK)
        self.healthBarRed = pygame.Surface((98, 8))
        self.healthBarRed.fill(RED)
        self.healthText = Button('Tortoise\'s health:', 0, (5, WINDOWHEIGHT - 35))

        # STAT HOOPS
        self.statHoop = pygame.Surface((STATHOOPSIZE, STATHOOPSIZE))
        self.halfhoop = int(STATHOOPSIZE / 2)
        pygame.draw.circle(self.statHoop, LIGHTGREY, (self.halfhoop, self.halfhoop), self.halfhoop)
        pygame.draw.circle(self.statHoop, BLUE, (self.halfhoop, self.halfhoop), self.halfhoop, 2)
        self.statHoop.set_colorkey(BLACK)
        self.statHoopLabels = []
        for statName in self.hoopStatsNames:
            statName = statName.capitalize()
            surf, rect = genText(statName, (0, 0), DARKGREY, 0, 0, 0, 1)
            surf = pygame.transform.rotate(surf, 90)
            rect = surf.get_rect()
            self.statHoopLabels.append([surf, rect])

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

        # STAT HOOPS
        for i in range(0, len(self.hoopStats)):
            x = (i + 1) * GAP + STATHOOPSIZE * i
            y = WINDOWHEIGHT - 80
            screen.blit(self.statHoop, (x, y))
            num = self.hoopStats[i]
            numSurf, numRect = genText(str(num), (0, 0), BLACK, 1, 0, (x + self.halfhoop, y + self.halfhoop))
            screen.blit(numSurf, numRect)
            self.statHoopLabels[i][1].bottomleft = (x + GAP * 2, y - GAP)
            screen.blit(self.statHoopLabels[i][0], self.statHoopLabels[i][1])


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
            endy +=  random.randint(100, 150)
            startPos = startx, starty
            endPos = endx, endy
            xstep = ((endx - startx) / frames)
            ystep = ((endy - starty) / frames)
            truex, truey = self.rect.topleft
            # go to enemy
            self.attackAnimNum = -223
            while (int(truex), int(truey)) != endPos and (int(truex + 0.5), int(truey + 0.5)) != endPos and (int(truex - 0.5), int(truey - 0.5)) != endPos:
                truex, truey= truex + xstep, truey + ystep
                self.rect.topleft = (int(truex), int(truey))
                screen.blit(screenFreeze, (0, 0))
                screen.blit(self.img, self.rect)
                pygame.display.update()
                checkForQuit()
                # ANIMATE
                if self.attackAnimNum > -1 and self.attackAnimNum < 180:
                    self.img = TORTOISE['attackAnim'][self.attackAnimNum]
                else:
                    self.img = TORTOISE['idleAnim'][self.idleAnimNum]
                    self.idleAnimNum += 1
                    if self.idleAnimNum > 118: self.idleAnimNum = 0
                self.attackAnimNum += 1
            # return to startPos
            while (int(truex), int(truey)) != startPos and (int(truex + 0.5), int(truey + 0.5)) != startPos and (int(truex - 0.5), int(truey - 0.5)) != startPos:
                truex, truey= truex - xstep, truey - ystep
                self.rect.topleft = (int(truex), int(truey))
                screen.blit(screenFreeze, (0, 0))
                screen.blit(self.img, self.rect)
                pygame.display.update()
                checkForQuit()

            # ATTACK TEXT
            attackText = DamageNum('Tortoise uses ' + self.attacks[(self.clickedButtons[0])] + '!', self.dmgNumPos, GREEN)
            self.damageNums.append(attackText)
            # DEAL DAMAGE
            damage = self.clickedButtons[0] * self.strength + random.randint(MISSCHANCE, RANDOMDAMAGEMARGIN)
            Enemy.incomingDamage = damage
            self.clickedButtons = []
            turn = 'enemy'

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

    def handleImg(self):
        # if time.time() - FLASHREDTIME < self.timeOfLastHit:
        #     if self.isBlocking:
        #         self.img = TORTOISE['blockHitImg']
        #         return
        #     else:
        #         self.img = TORTOISE['idleHitImg']
        #         return
        if self.isBlocking:
            self.img = TORTOISE['blockImg']
        else:
            self.img = TORTOISE['idleAnim'][self.idleAnimNum]
            self.idleAnimNum += 1
            if self.idleAnimNum == 119: self.idleAnimNum = 0


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
            self.img = BEAR['idleAnim'][0]
            self.attacks = BEAR['attacks']
        self.rect = Rect((Enemy.screenPos), (self.img.get_size()))
        self.genAttacks()
        self.initUI()
        self.timeOfLastHit = time.time() - 100
        self.pauseBeforeAttack = ENEMYWAITFRAMES
        self.idleAnimNum = 0
        self.attackAnimNum = -1

    def simulate(self, turn, screen):
        self.handleImg()
        self.takeDamage()
        self.updateUI(screen)
        if turn == 'enemy':
            if self.pauseBeforeAttack == 0:
                self.attack(screen)
                return 'tortoise'
            self.draw(screen)
            self.pauseBeforeAttack -= 1
            return 'enemy'
        else:
            self.pauseBeforeAttack = ENEMYWAITFRAMES
            self.draw(screen)
            return 'tortoise'


    def handleImg(self):
        if self.creature == 'BEAR':
            # if time.time() - FLASHREDTIME < self.timeOfLastHit:
            #     self.img = BEAR['idleHitImg']
            #     return
            if self.attackAnimNum < 180 and self.attackAnimNum > 1:
                self.img = BEAR['attackAnim'][self.attackAnimNum]
            else:
                self.img = BEAR['idleAnim'][self.idleAnimNum]
                self.idleAnimNum += 1
                if self.idleAnimNum == 120: self.idleAnimNum = 0

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

    def attack(self, screen):
        screenFreeze = screen.copy()
        frames = int(ATTACKANIMTIME / FPS)
        startx, starty = self.rect.topleft
        enemyx, enemyy = TORTOISESCREENPOS
        endx, endy = (enemyx + 40, enemyy - 200 + random.randint(-50, 50))
        startPos = startx, starty
        endPos = endx, endy
        xstep = ((endx - startx) / frames)
        ystep = ((endy - starty) / frames)
        truex, truey = self.rect.topleft
        # go to enemy
        self.attackAnimNum = -250
        while (int(truex), int(truey)) != endPos and (int(truex + 0.5), int(truey + 0.5)) != endPos and (int(truex - 0.5), int(truey - 0.5)) != endPos:
            truex, truey = truex + xstep, truey + ystep
            self.rect.topleft = (int(truex), int(truey))
            screen.blit(screenFreeze, (0, 0))
            # ANIMATE
            if self.attackAnimNum > -1 and self.attackAnimNum < 120:
                self.img = BEAR['attackAnim'][self.attackAnimNum]
            else:
                self.img = BEAR['idleAnim'][self.idleAnimNum]
                self.idleAnimNum += 1
                if self.idleAnimNum > 119: self.idleAnimNum = 0
            self.attackAnimNum += 1
            screen.blit(self.img, self.rect)
            pygame.display.update()
            checkForQuit()
        # return to startPos
        while (int(truex), int(truey)) != startPos and (int(truex + 0.5), int(truey + 0.5)) != startPos and (int(truex - 0.5), int(truey - 0.5)) != startPos:
            truex, truey = truex - xstep, truey - ystep
            self.rect.topleft = (int(truex), int(truey))
            screen.blit(screenFreeze, (0, 0))
            # ANIMATE
            if self.attackAnimNum > -1 and self.attackAnimNum < 180:
                self.img = BEAR['attackAnim'][self.attackAnimNum]
                self.attackAnimNum += 1
            screen.blit(self.img, self.rect)
            pygame.display.update()
            checkForQuit()
        #  DEAL DAMAGE
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
    def __init__(self, text, style, screenPos, isClickable=0, isTitle=0, screenPosIsTopRight=0, tooltip=None):
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
        self.hasTooltip = False
        if tooltip:
            self.hasTooltip = True
            self.tooltip = Tooltip(tooltip, (self.rect.left + GAP, self.rect.top))

    def simulate(self, screen, userInput):
        if self.isClickable or self.hasTooltip: self.handleClicks(userInput)
        if self.hasTooltip: self.tooltip.simulate(screen, self.isHovered)
        self.draw(screen)

    def draw(self, screen):
        if self.posIsTopRight:
            self.rect.topright = self.screenPos
        else:
            self.rect.topleft = self.screenPos
        screen.blit(self.currentSurf, self.rect)

    def handleClicks(self, userInput=None):
        self.isClicked = False
        self.isHovered = False
        if self.rect.collidepoint(userInput.mousePos):
            if userInput.mousePressed == True:
                self.currentSurf = self.clickSurf
            else:
                self.currentSurf = self.hoverSurf
                self.isHovered = True
        else:
            self.currentSurf = self.buttonSurf
        if userInput.mouseUnpressed == True and self.rect.collidepoint(userInput.mousePos):
            self.isClicked = True


#######################################################################################################


class Tooltip:
    def __init__(self, text, pos):
        self.pos = pos
        self.x, self.y = pos
        self.alpha = 255
        # GET TEXT OBJS
        self.textObjs, self.textHeight = self.genTextObjs(text)
        self.textWidth = self.getLongestTextLine(self.textObjs)
        # CREAT SURF
        self.surf = pygame.Surface((self.textWidth + GAP * 3, self.textHeight + GAP * 2))
        pygame.draw.rect(self.surf, CREAM, (GAP, 0, self.surf.get_width() - GAP, self.surf.get_height()))
        pygame.draw.polygon(self.surf, CREAM, [(0, 5), (GAP, 3), (GAP, 7)])
        for i in range(len(self.textObjs)):
            self.surf.blit(self.textObjs[i][0], self.textObjs[i][1])
        

    def simulate(self, screen, isHovered):
        if isHovered:
            if self.alpha < 255: self.alpha += 20
        else:
            self.alpha -= 20
        self.surf.set_alpha(self.alpha)
        screen.blit(self.surf, self.pos)


    def genTextObjs(self, text):
        wordList = text.split()
        extraWords = wordList[:]
        numLines = int(math.ceil(len(wordList) / TOOLTIPWORDSPERLINE))
        newText = [] # a list of strings, each line having one string
        textObjs = [] # a list of two item lists, each list having a surf and rect object for a line
        # GENERATE LIST OF STRINGS
        for lineNum in range(0, numLines):
            line = ''
            for wordNum in range(0, TOOLTIPWORDSPERLINE - 1):
                currentWord = wordList[lineNum * (TOOLTIPWORDSPERLINE - 1) + wordNum]
                line = line + currentWord + ' '
                extraWords.remove(currentWord)
            newText.append(line)
        lastLine = ' '.join(extraWords)
        newText.append(lastLine)
        # CONVERT STRINGS TO TEXT SURFS AND RECTS
        testText, testRect = genText(newText[0], (0, 0), BLACK, 0, 0, 0, 0)
        textHeight = testText.get_height()
        totalHeight = textHeight * len(newText) + GAP * len(newText)
        for lineNum in range(len(newText)):
            surf, rect = genText(newText[lineNum], (GAP * 2, textHeight * lineNum + GAP * lineNum), DARKGREY,0,0,0,0)
            textObjs.append([surf, rect])
        return textObjs, totalHeight


    def getLongestTextLine(self, textObjs):
        longestLineWidth = 0
        for i in range(len(textObjs)):
            if textObjs[i][1].width > longestLineWidth:
                longestLineWidth = textObjs[i][1].width
        return longestLineWidth




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







if __name__ == '__main__':
    main()
