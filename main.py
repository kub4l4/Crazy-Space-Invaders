import time
import math
import random
import pygame

pygame.init()


class Screen:
    resolutionX = 800
    resolutionY = 600


SCREEN = pygame.display.set_mode((Screen.resolutionX, Screen.resolutionY))
FONT = pygame.font.Font('freesansbold.ttf', 32)
BACKGROUND = pygame.image.load('img/background.jpg')
END_FONT = pygame.font.Font('freesansbold.ttf', 64)
pygame.display.set_caption("Strzelanka")


class Player:
    size = 64
    img = pygame.image.load('img/player.png')
    positionX = Screen.resolutionX / 2
    positionY = Screen.resolutionY - 5 * Screen.resolutionY / 100 - size
    positionXChange = 0
    positionXSpeed = 5

    def update(x, y):
        SCREEN.blit(Player.img, (int(x), int(y)))


class Level:
    gamelvl = 0
    numOfEnemies = [20, 30, 10]
    numOfEnemiesGenerated = 0
    enemy_list = []


class Enemy:
    def __init__(self, typ_potwora):
        if typ_potwora == 1:
            self.potwor1()
        elif typ_potwora == 2:
            self.potwor2()
        elif typ_potwora == 3:
            self.potwor3()

    def potwor1(self):
        self.size = 64
        self.img = pygame.image.load('img/enemy.png')
        self.positionX = 50
        self.positionY = 50
        self.positionXChange = 1
        self.positionYChange = 40

    def potwor2(self):
        self.size = 64
        self.img = pygame.image.load('img/enemy.png')
        self.positionX = 50
        self.positionY = 50
        self.positionXChange = 4
        self.positionYChange = 40

    def potwor3(self):
        self.size = 64
        self.img = pygame.image.load('img/enemy.png')
        self.positionX = 50
        self.positionY = 50
        self.positionXChange = 8
        self.positionYChange = 40

    def update(self, posX, posY):
        SCREEN.blit(self.img, (int(self.positionX), int(self.positionY)))


class Bullet:
    list = []

    def __init__(self, poz_x):
        self.img = pygame.image.load('img/bullet.png')
        self.positionX = poz_x
        self.positionY = Screen.resolutionY - 5 * Screen.resolutionY / 100 - Player.size
        self.positionYSpeed = 3
        self.positionYChange = 0


    def fire(self):
        SCREEN.blit(self.img, (self.positionX + 16, self.positionY + 10))


class Score:
    # name = input("Podaj nick gracza")
    value = 0

    def update(self, x, y):
        score = FONT.render("Score : " + str(self.value), True, (255, 255, 255))
        SCREEN.blit(score, (x, y))


class Czas:
    gamelvl_time_start = time.time()
    gamelvl_time = 15

    enemy_latest_get_time = time.time()
    enemy_next_get_time = 1


def menu():
    nick = Score()


def game_over_text():
    over_text = END_FONT.render("GAME OVER", True, (255, 255, 255))
    SCREEN.blit(over_text, (int(Screen.resolutionX / 2), int(Screen.resolutionY / 2)))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


def buttons():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            break

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key[0] = True
            if event.key == pygame.K_RIGHT:
                key[1] = True
            if event.key == pygame.K_SPACE:
                Bullet.list.append(Bullet(Player.positionX))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key[0] = False
            if event.key == pygame.K_RIGHT:
                key[1] = False

        if key[0] and key[1] or not key[0] and not key[1]:
            Player.positionXChange = 0
        elif key[1]:
            Player.positionXChange += Player.positionXSpeed
        elif key[0]:
            Player.positionXChange -= Player.positionXSpeed


def enemy_creator():
    if Level.numOfEnemies[Level.gamelvl] > Level.numOfEnemiesGenerated:
        if Czas.enemy_latest_get_time + Czas.enemy_next_get_time < time.time():
            Czas.enemy_latest_get_time = time.time()
            if Level.gamelvl == 0:
                Level.enemy_list.append(Enemy(1))
            if Level.gamelvl == 1:
                Level.enemy_list.append(Enemy(2))
            if Level.gamelvl == 2:
                Level.enemy_list.append(Enemy(3))
            Level.numOfEnemiesGenerated += 1


def next_level():
    if Czas.gamelvl_time_start + Czas.gamelvl_time < time.time() and not Level.enemy_list:
        Czas.gamelvl_time_start = time.time()
        Level.gamelvl += 1
        Czas.gamelvl_time = 10
        Czas.enemy_next_get_time -= 0.05
        print("Next lvl")


def player_movement():
    Player.positionX += Player.positionXChange
    if Player.positionX <= 0:
        Player.positionX = 0
    elif Player.positionX >= Screen.resolutionX - Player.size:
        Player.positionX = Screen.resolutionX - Player.size
    Player.update(Player.positionX, Player.positionY)


def enemy_movement():
    for nEnemy in Level.enemy_list:
        # Game Over
        if nEnemy.positionY > Screen.resolutionY - 5 * Screen.resolutionY / 100 - 2 * Player.size:
            for j in Level.enemy_list:
                j.positionY = 2000
            game_over_text()
            global running
            running = False
            break

        nEnemy.positionX += nEnemy.positionXChange
        if nEnemy.positionX < 0:
            nEnemy.positionX = 0
            nEnemy.positionXChange = -nEnemy.positionXChange
            nEnemy.positionY += nEnemy.positionYChange
        elif nEnemy.positionX > Screen.resolutionX - Player.size:
            nEnemy.positionX = Screen.resolutionX - Player.size
            nEnemy.positionXChange = -nEnemy.positionXChange
            nEnemy.positionY += nEnemy.positionYChange

        Enemy.update(nEnemy, nEnemy.positionX, nEnemy.positionY)

    print(Bullet.list)


def bullet_movement():
    for nBullet in Bullet.list:
        if nBullet.positionY <= 0:
            Bullet.list.remove(nBullet)
        else:
            nBullet.fire()
            nBullet.positionY -= nBullet.positionYSpeed


def collision():
    for nEnemy in Level.enemy_list:
        for nBullet in Bullet.list:
            if is_collision(nEnemy.positionX, nEnemy.positionY, nBullet.positionX, nBullet.positionY):
                Bullet.positionY = Screen.resolutionY - 5 * Screen.resolutionY / 100 - Player.size
                Level.enemy_list.remove(nEnemy)
                Bullet.list.remove(nBullet)
                Score.value += 1

def game():
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(BACKGROUND, (0, 0))
    buttons()
    enemy_creator()
    next_level()
    player_movement()
    enemy_movement()
    bullet_movement()
    collision()
    pygame.display.update()


# menu()
key = [False, False]
running = True
while running:
    game()
