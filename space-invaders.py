import pygame
import math
import random
from pygame import mixer

# Initialise a Pygame
pygame.init()

# Creating The Game Screen
screen = pygame.display.set_mode((800, 600))

# Background
Background = pygame.image.load('Background.jpg')

# Adding Background Sound
mixer.music.load('Music.mp3')
mixer.music.play(-1)

# Captions And Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)

# Creating Player
playerImg = pygame.image.load('Player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Creating Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('Enemy.png'))
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(1)
    EnemyY_change.append(40)

# Creating bullet
# ready - you can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load('Bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "Ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_scores(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('Game Over', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def Enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'Fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(EnemyX, EnemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(EnemyX - bulletX, 2)) + (math.pow(EnemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(Background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check wheather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state is 'Ready':
                    # bullet_sound = mixer.Sound('bull.mp3')
                    # bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 - 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game over
        if EnemyY[i] > 440:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break

        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 1
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -1
            EnemyY[i] += EnemyY_change[i]

        # Collision
        Collision = isCollision(EnemyX[i], EnemyY[i], bulletX, bulletY)
        if Collision:
            # coll_sound = mixer.Sound('bull.mp3')
            # coll_sound.play()
            bulletY = 480
            bullet_state = 'Ready'
            score_value += 1
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(50, 150)

        Enemy(EnemyX[i], EnemyY[i], i)

        # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'Ready'

    if bullet_state is 'Fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_scores(textX, textY)
    pygame.display.update()

# Created with the help of freeCodeCamp Youtube Video
