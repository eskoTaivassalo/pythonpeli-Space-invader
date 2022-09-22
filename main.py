import pygame 
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('8752.jpg')

# background music
mixer.music.load('pelitausta1.wav')
mixer.music.play(-1)

# caption and icon
pygame.display.set_caption("Avaruusammuntapeli")
icon = pygame.image.load('nuclear-bomb.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('spaceship.png')
playerX = 375
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ghost.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet

# ready-- et näe luotia
# fire-- luoti liikkuu kohti vihollista

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# superbullet

superBulletImg = pygame.image.load('bullet.png')
superBulletX = 0
superBulletY = 480
superBulletX_change = 0
superBulletY_change = 2
superBullet_state = False



# score

score_value = 0
font = pygame.font.Font('Delinda Agatha.ttf',44)              # dafont.com siellä ne fontit on

textX = 10
textY = 10

#Game over
over_font = pygame.font.Font('Delinda Agatha.ttf',64)
running = True



def show_score(x, y) :
    score = font.render("Score : " + str(score_value), True, (0, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (0, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def fire_super_bullet(x,y):
    global superBullet_state
    superBullet_state = "fire"
    screen.blit(superBulletImg, (x + 25, y + 10))



def isCollision(enemyX, enemyY, bulletX, bulletY):  # tulee kaavasta D= neliöj. (x2-x1) toiseen + (y2-y1) toiseen
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
def isSuperCollision(enemyX, enemyY, superBulletX, superBulletY):  # tulee kaavasta D= neliöj. (x2-x1) toiseen + (y2-y1) toiseen
    distance = math.sqrt((math.pow(enemyX - superBulletX, 2)) + (math.pow(enemyY - superBulletY, 2)))

    if distance < 27:
        return True
    else:
        return False




# game loop
running = True
while running:
    # red- green- blue(rgb)
    screen.fill((112, 123, 241,))
    # background-image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('piu.wav')
                    bullet_sound.play()
                    # get the current coordinate of the spaceshit
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
            if event.key == pygame.K_DOWN:

                superBullet_state = "ready"
                superBullet_sound = mixer.Sound('superase.wav')
                superBullet_sound.play()
                superBulletX = playerX
                fire_super_bullet(playerX, playerY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    # checking for boundaries of ship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:

            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()


            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('pum.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        superCollision = isSuperCollision(enemyX[i], enemyY[i], superBulletX, superBulletY)
        if superCollision:
            superExplosion_sound = mixer.Sound('superosuma.wav')
            superExplosion_sound.play()
            superBulletY = 480
            superBullet_state = "ready"
            score_value += 10
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)



        enemy(enemyX[i], enemyY[i], i)

    # bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # superBullet movement
    if superBulletY <= 0:
      superBulletY = 480
      superBullet_state = "ready"

    if superBullet_state == "fire":
      fire_super_bullet(superBulletX, superBulletY)
      superBulletY -= superBulletY_change


    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
