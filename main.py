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
        SCREEN.blit(Player.img, ((int)(x), (int)(y)))


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
        SCREEN.blit(self.img, ((int)(self.positionX), (int)(self.positionY)))


class Bullet:
    img = pygame.image.load('img/bullet.png')
    positionX = 0
    positionY = Screen.resolutionY - 5 * Screen.resolutionY / 100 - Player.size
    positionYSpeed = 5
    positionYChange = 0
    state = "ready"

    def fire(x, y):
        Bullet.state = "fire"
        SCREEN.blit(Bullet.img, (x + 16, y + 10))


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
    SCREEN.blit(over_text, ((int)(Screen.resolutionX / 2), (int)(Screen.resolutionY / 2)))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
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
                Player.positionXChange -= Player.positionXSpeed
            if event.key == pygame.K_RIGHT:
                Player.positionXChange += Player.positionXSpeed
            if event.key == pygame.K_SPACE:
                if Bullet.state == "ready":
                    # Get the current x cordinate of the spaceship
                    Bullet.positionX = Player.positionX
                    Bullet.fire(Bullet.positionX, Bullet.positionY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Player.positionXChange = 0


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
    for enemyName in Level.enemy_list:
        # Game Over
        if enemyName.positionY > Screen.resolutionY - 5 * Screen.resolutionY / 100 - 2 * Player.size:
            for j in Level.enemy_list:
                j.positionY = 2000
            game_over_text()
            global running
            running = False
            break

        enemyName.positionX += enemyName.positionXChange
        if enemyName.positionX < 0:
            enemyName.positionX = 0
            enemyName.positionXChange = -enemyName.positionXChange
            enemyName.positionY += enemyName.positionYChange
        elif enemyName.positionX > Screen.resolutionX - Player.size:
            enemyName.positionX = Screen.resolutionX - Player.size
            enemyName.positionXChange = -enemyName.positionXChange
            enemyName.positionY += enemyName.positionYChange

        # Collision
        collision = is_collision(enemyName.positionX, enemyName.positionY, Bullet.positionX, Bullet.positionY)
        if collision:
            Bullet.positionY = Screen.resolutionY - 5 * Screen.resolutionY / 100 - Player.size
            Bullet.state = "ready"
            Level.enemy_list.remove(enemyName)
            Score.value += 1
        Enemy.update(enemyName, enemyName.positionX, enemyName.positionY)

    print(Level.enemy_list)


def bullet_movement():
    if Bullet.positionY <= 0:
        Bullet.positionY = Screen.resolutionY - 5 * Screen.resolutionY / 100 - Player.size
        Bullet.state = "ready"

    if Bullet.state == "fire":
        Bullet.fire(Bullet.positionX, Bullet.positionY)
        Bullet.positionY -= Bullet.positionYSpeed


def game():
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(BACKGROUND, (0, 0))
    buttons()
    enemy_creator()
    next_level()
    player_movement()
    enemy_movement()
    bullet_movement()
    pygame.display.update()


# menu()
running = True
while running:
    game()
