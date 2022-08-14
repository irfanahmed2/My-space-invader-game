import math
import pygame
import random
from pygame import mixer
# intializa the pygame
pygame.init()

# create the  screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('galaxy0.jpg')

#bk sound
mixer.music.load('bk.mp3')
mixer.music.play(-1)

#Title and toon
pygame.display.set_caption("Space Invaders")
Icon = pygame.image.load('1.png')
pygame.display.set_icon(Icon)


# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370  # setting the position of img on screen with x-axis
playerY = 480  # setting the position of img on screen with x-axis

playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX .append(random.randint(0, 800))
    enemyY .append(random.randint(50, 150))
    enemyX_change.append(0.1)
    enemyY_change.append(40)

# laser
laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserX_change = 3
laserY_change = 1
# ready - you can't see laser on screen
# fire - you can  see laser on screen
laser_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)


textx = 10
texty = 10

# game over text
def game_over_text():
 over_text = over_font.render('GAME OVER',True,(255,255,255))
 screen.blit(over_text,(200,250))



# show score function


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# creating function for enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# creating function for player
def player(x, y):
    screen.blit(playerImg, (x, y))  # to draw image And Setting the positions

# creating function for fire


def fire(x, y):
    global laser_state
    laser_state = 'fire'
    screen.blit(laserImg, (x+16, y+10))


def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt(
        math.pow(enemyX-laserX, 2) + math.pow(enemyY-laserY, 2))
    if distance < 27:
        return True
    else:
        return False


# using while loop  to show window
running = True
while running:
   # RGB RED,GREEN,BLUE
    screen.fill((0, 0, 0))
    # checking player movement mechanic
    #! playerY -= 0.2
    #   background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed check wheather it's right or left
    # using if/else condition
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if laser_state is 'ready':
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    laserX = playerX
                    fire(laserX, laserY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

           # Adding boundary of spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 725:
        playerX = 725

    playerX += playerX_change

    # adding boundary for enemy
    #
    for i in range(num_of_enemies):
        
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                 enemyY[j] = 2000 
            game_over_text()
            break       
        
        
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 725:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
            # collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            
            laserY = 480
            laser_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 725)
            enemyY[i] = random.randint(50, 150)
            print(score_value)
    # calling enemy function
        enemy(enemyX[i], enemyY[i], i)

   # laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = 'ready'

    if laser_state is 'fire':
        fire(laserX, laserY)
        laserY -= laserY_change
   # calling player function
    player(playerX, playerY)
    # show score funtion
    show_score(textx, texty)
   # to update
    pygame.display.update()
# code by irfan ahmed