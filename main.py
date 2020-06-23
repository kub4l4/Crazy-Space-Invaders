import time

import math

import random

import pygame

pygame.init()


class Screen:
    resolutionX = 1080
    resolutionY = 720


SCREEN = pygame.display.set_mode((Screen.resolutionX, Screen.resolutionY))
MENU = pygame.image.load('img/menu.png')
BACKGROUND = pygame.image.load('img/background.jpg')
pygame.display.set_caption("Military War")

# SCREEN POSITIONS
POS_TITLE1 = (100, 50)
POS_TITLE2 = (130, 125)
POS_START_TXT = (300, 600)
POS_SCORE = (800, 650)
POS_X_MIN = 0
POS_Y_MIN = 0
POS_DEAD_TXT = (300, 400)
POS_WIN_TXT = (300, 600)
POS_SCORE_TXT = (300, 480)
POS_NEXT_LVL_TXT = (100, 300)
POS_BULLET_TXT = (50, 650)

# FONTS
FONT = pygame.font.Font('font/ARMY_RUST.ttf', 50)
MENU_FONT = pygame.font.Font('font/ARMY_RUST.ttf', 128)
START_FONT = pygame.font.Font('font/ARMY_RUST.ttf', 50)

TXT_COLOR = (255, 255, 255)

# TXT
TITLE1 = MENU_FONT.render("MILITARY", True, TXT_COLOR)
TITLE2 = MENU_FONT.render("WAR", True, TXT_COLOR)
START_TEXT = START_FONT.render("Press space bar to start", True, TXT_COLOR)
EXIT_TEXT = START_FONT.render("Press e to exit", True, TXT_COLOR)
key = [False, False]

AVAILABLE_START_BULLET = 1


class Init:
    stan = 1
    running = 1


class Player:
    def __init__(self):
        self.size = 64
        self.img = pygame.image.load('img/player.png')
        self.pos_x = Screen.resolutionX / 2
        self.pos_y = Screen.resolutionY - 5 * Screen.resolutionY / 100 - self.size
        self.pos_x_change = 0
        self.pos_x_speed = 5
        self.score = 0

    def update(self):
        SCREEN.blit(self.img, (int(self.pos_x), int(self.pos_y)))

    def update_score(self):
        score = FONT.render("Score : " + str(self.score), True, TXT_COLOR)
        SCREEN.blit(score, POS_SCORE)


class Bullet:
    list = []
    max = AVAILABLE_START_BULLET
    size = 32

    def __init__(self, poz_x):
        self.img = pygame.image.load('img/bullet.png')
        self.pos_x = poz_x
        self.pos_y = Screen.resolutionY - 5 * Screen.resolutionY / 100 - Player1.size
        self.pos_y_speed = 5
        self.pos_y_change = 0

    def fire(self):
        SCREEN.blit(self.img, (int(self.pos_x) + 16, int(self.pos_y) + 10))
        self.pos_y -= self.pos_y_speed


class Level:
    now = 0
    numOfEnemies = [1, 2]
    numOfEnemiesGenerated = 0
    startTime = time.time()
    periodTime = 10


class Enemy:
    list = []
    lastTime = 0
    Time = time.time()
    periodTime = 1

    def __init__(self, enemy_type):
        self.size = 64
        self.img = pygame.image.load('img/enemy1.png')
        self.pos_x = random.randrange(700)
        self.pos_y = -64
        self.pos_x_speed = 1
        self.pos_y_speed = 70

        if enemy_type == 1:
            self.enemy_type1()
        elif enemy_type == 2:
            self.enemy_type2()
        elif enemy_type == 3:
            self.enemy_type3()

    def enemy_type1(self):
        self.size = 64
        self.img = pygame.image.load('img/enemy1.png')
        self.pos_x_speed = 3

    def enemy_type2(self):
        self.size = 64
        self.img = pygame.image.load('img/enemy2.png')
        self.pos_x_speed = 4

    def enemy_type3(self):
        self.size = 64
        self.img = pygame.image.load('img/enemy3.png')
        self.pos_x_speed = 5

    def update(self):
        Bullet.lastTime = time.time()
        SCREEN.blit(self.img, (int(self.pos_x), int(self.pos_y)))

    def down_left(self):
        self.pos_x = POS_X_MIN
        self.pos_x_speed = -self.pos_x_speed
        self.pos_y += self.pos_y_speed

    def down_right(self):
        self.pos_x = Screen.resolutionX - Player1.size
        self.pos_x_speed = -self.pos_x_speed
        self.pos_y += self.pos_y_speed


def menu():
    SCREEN.blit(MENU, (0, 0))
    SCREEN.blit(TITLE1, POS_TITLE1)
    SCREEN.blit(TITLE2, POS_TITLE2)
    SCREEN.blit(START_TEXT, POS_START_TXT)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Init.running = 0
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Init.stan = 2


def game_over_text():
    dead_txt = FONT.render("GAME OVER", True, TXT_COLOR)
    SCREEN.blit(dead_txt, POS_DEAD_TXT)

    dead_txt = FONT.render("SCORE: " + str(Player1.score), True, TXT_COLOR)
    SCREEN.blit(dead_txt, POS_SCORE_TXT)
    SCREEN.blit(EXIT_TEXT, POS_START_TXT)


def game_win_text():
    dead_txt = FONT.render("WINNER", True, TXT_COLOR)
    SCREEN.blit(dead_txt, POS_DEAD_TXT)

    dead_txt = FONT.render("SCORE: " + str(Player1.score), True, TXT_COLOR)
    SCREEN.blit(dead_txt, POS_SCORE_TXT)
    SCREEN.blit(EXIT_TEXT, POS_START_TXT)


def update_bullets():
    bullet_txt = FONT.render("Bullets : " + str(Bullet.max - len(Bullet.list)), True, TXT_COLOR)
    SCREEN.blit(bullet_txt, POS_BULLET_TXT)


def buttons():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key[0] = True
            if event.key == pygame.K_RIGHT:
                key[1] = True
            if event.key == pygame.K_SPACE:
                if len(Bullet.list) < Bullet.max:
                    Bullet.list.append(Bullet(Player1.pos_x))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key[0] = False
            if event.key == pygame.K_RIGHT:
                key[1] = False
        if key[0] and key[1] or not key[0] and not key[1]:
            Player1.pos_x_change = 0
        elif key[1]:
            Player1.pos_x_change += Player1.pos_x_speed
        elif key[0]:
            Player1.pos_x_change -= Player1.pos_x_speed


def enemy_creator():
    if Level.numOfEnemies[Level.now] > Level.numOfEnemiesGenerated:
        if Enemy.lastTime + Enemy.periodTime < time.time():
            Enemy.lastTime = time.time()
            if Level.now == 0:
                Enemy.list.append(Enemy(1))
            if Level.now == 1:
                Enemy.list.append(Enemy(1))
                Enemy.list.append(Enemy(2))
            if Level.now >= 2:
                Enemy.list.append(Enemy(1))
                Enemy.list.append(Enemy(2))
                Enemy.list.append(Enemy(3))
                print(Level.numOfEnemies)
            Level.numOfEnemiesGenerated += 1


def player_movement():
    Player1.pos_x += Player1.pos_x_change
    if Player1.pos_x <= POS_X_MIN:
        Player1.pos_x = POS_X_MIN
    elif Player1.pos_x >= Screen.resolutionX - Player1.size:
        Player1.pos_x = Screen.resolutionX - Player1.size
    Player1.update()


def enemy_movement():
    for n_enemy in Enemy.list:
        if n_enemy.pos_y < 10:
            n_enemy.pos_y = n_enemy.pos_y + 5
        else:
            n_enemy.pos_x += n_enemy.pos_x_speed
            if n_enemy.pos_x < POS_X_MIN:
                n_enemy.down_left()
            elif n_enemy.pos_x > Screen.resolutionX - Player1.size:
                n_enemy.down_right()
        n_enemy.update()


def bullet_movement():
    for n_bullet in Bullet.list:
        if n_bullet.pos_y <= POS_Y_MIN - Bullet.size:
            Bullet.list.remove(n_bullet)
        else:
            n_bullet.fire()


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    return False


def collision():
    for n_enemy in Enemy.list:
        for n_bullet in Bullet.list:
            if is_collision(n_enemy.pos_x, n_enemy.pos_y, n_bullet.pos_x, n_bullet.pos_y):
                Bullet.positionY = Screen.resolutionY - 5 * Screen.resolutionY / 100 - Player1.size
                Enemy.list.remove(n_enemy)
                Bullet.list.remove(n_bullet)
                Player1.score += 1


def next_level():
    if not Enemy.list:
        Level.startTime = time.time()
        Level.now += 1
        Level.periodTime = 5
        Bullet.max += 1
        Enemy.periodTime -= 0.1
        Level.numOfEnemies.append(
            (Level.numOfEnemies[Level.now] + random.randint(Level.now, Level.now * Level.now)))
        next_level_txt = MENU_FONT.render("Level: " + str(Level.now) + " completed!", True, TXT_COLOR)
        SCREEN.blit(next_level_txt, POS_NEXT_LVL_TXT)
        pygame.display.update()
        time.sleep(2)


def ending_condition():
    for n_enemy in Enemy.list:
        if n_enemy.pos_y > Screen.resolutionY - 5 * Screen.resolutionY / 100 - 2 * Player1.size:
            Init.stan = 3
            break
    if Level.now == 10:
        Init.stan = 4


def game():
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(BACKGROUND, (POS_X_MIN, POS_Y_MIN))
    buttons()
    collision()
    Player1.update_score()
    update_bullets()
    enemy_creator()
    player_movement()
    enemy_movement()
    bullet_movement()
    pygame.display.update()
    next_level()
    ending_condition()


def exit_button():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Init.running = 0
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                exit(0)


while Init.running == 1:
    if Init.stan == 1:
        Player1 = Player()
        menu()

    if Init.stan == 2:
        game()

    if Init.stan == 3:
        SCREEN.blit(MENU, (0, 0))
        SCREEN.blit(TITLE1, POS_TITLE1)
        SCREEN.blit(TITLE2, POS_TITLE2)
        game_over_text()
        exit_button()
        pygame.display.update()

    if Init.stan == 4:
        SCREEN.blit(MENU, (0, 0))
        SCREEN.blit(TITLE1, POS_TITLE1)
        SCREEN.blit(TITLE2, POS_TITLE2)
        game_win_text()
        exit_button()
        pygame.display.update()
