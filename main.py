import time
import math
import random
import pygame

# Intialize the pygame
pygame.init()

# Create the screen
screen_resolutionX = 800
screen_resolutionY = 600
screen = pygame.display.set_mode((screen_resolutionX, screen_resolutionY))

# Background
background = pygame.image.load('background.jpg')

# Caption
pygame.display.set_caption("Strzelanka")

# Player
player_size = 64
playerImg = pygame.image.load('player.png')
playerX = screen_resolutionX / 2
playerY = screen_resolutionY - 5 * screen_resolutionY / 100 - player_size
playerX_change = 0
playerX_speed = 5

# Enemy
enemyID = []
gamelvl = 1
enemysize = 64
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = [1, 5, 10, 16, 25, 40, 30000, 300000, 3000000, 30000000, 300000000, 3000000000, 30000000000]
num_of_enemies_generated = 0

enemyY_speed = 40
enemyX_speed = 1
enemyImg.append(pygame.image.load('enemy.png'))
enemyX.append(1)
enemyY.append(70)
enemyX_change.append(enemyX_speed)
enemyY_change.append(40)
enemyID.append(0)
# for i in range(num_of_enemies):


# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = screen_resolutionY - 5 * screen_resolutionY / 100 - player_size
bulletY_speed = 20
bulletY_change = 0
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# time
gamelvl_time_start = time.time()
gamelvl_time = 15

enemy_latest_get_time = time.time()
enemy_next_get_time = 1

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (screen_resolutionX / 2, screen_resolutionY / 2))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= playerX_speed
            if event.key == pygame.K_RIGHT:
                playerX_change += playerX_speed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Next enemy creator
    if num_of_enemies[gamelvl] >= num_of_enemies_generated:
        if enemy_latest_get_time + enemy_next_get_time < time.time():
            enemy_latest_get_time = time.time()
            num_of_enemies_generated += 1
            enemyID.append(num_of_enemies_generated)
            enemyImg.append(pygame.image.load('enemy.png'))
            enemyX.append(1)
            enemyY.append(70)
            enemyX_change.append(enemyX_speed)
            enemyY_change.append(enemyY_speed)

    # Next_level
    if gamelvl_time_start + gamelvl_time < time.time() or not enemyID:
        gamelvl_time_start = time.time()
        gamelvl += 1
        gamelvl_time = 10
        enemyX_speed += 1
        enemy_next_get_time -= 0.05
        print("Next lvl")

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= screen_resolutionX - player_size:
        playerX = screen_resolutionX - player_size
    print(enemyID)
    # Enemy Movement
    for i in enemyID:
        # Game Over
        if enemyY[i] > screen_resolutionY - 5 * screen_resolutionY / 100 - 2 * player_size:
            for j in enemyID:
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX[i] = 0
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > screen_resolutionX - player_size:
            enemyX[i] = screen_resolutionX - player_size
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = screen_resolutionY - 5 * screen_resolutionY / 100 - player_size
            bullet_state = "ready"
            enemyID.remove(i)
            score_value += 1

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = screen_resolutionY - 5 * screen_resolutionY / 100 - player_size
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_speed

    player(playerX, playerY)
    pygame.display.update()
