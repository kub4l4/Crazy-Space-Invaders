import time
import math
import random
import pygame
from os import path

pygame.init()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(18):
    filename = 'Explosion{}.png'.format(i)
    img = pygame.image.load(path.join("explosion/", filename))
    # img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

class Screen:
    resolutionX = 800
    resolutionY = 600



screen = pygame.display.set_mode((Screen.resolutionX, Screen.resolutionY))
FONT = pygame.font.Font('freesansbold.ttf', 32)
BACKGROUND = pygame.image.load('background.jpg')
over_font = pygame.font.Font('freesansbold.ttf', 64)
pygame.display.set_caption("Strzelanka")



class Player:
    size = 64
    img = pygame.image.load('player.png')
    positionX = Screen.resolutionX / 2
    positionY = Screen.resolutionY - 5 * Screen.resolutionY / 100 - size
    positionXChange = 0
    positionXSpeed = 5

    def update(x, y):
        screen.blit(Player.img, (x, y))


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Level:
    gamelvl = 0
    numOfEnemies = [1, 5, 10, 16, 25, 40, 30000]
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
        self.potwor = 1
        self.size = 64
        self.img = pygame.image.load('enemy.png')
        self.positionX = 50
        self.positionY = 50
        self.positionXChange = 1
        self.positionYChange = 40

    def potwor2(self):
        self.potwor = 2
        '''Stwórz atrybuty o wartościach dla potwora typu 2'''

    def potwor3(self):
        self.potwor = 3
        '''Stwórz atrybuty o wartościach dla potwora typu 3'''

    def update(self, posX, posY):
        screen.blit(self.img, (self.positionX, self.positionY))


class Bullet:
    img = pygame.image.load('bullet.png')
    positionX = 0
    positionY = Screen.resolutionY - 5 * Screen.resolutionY / 100 - Player.size
    positionYSpeed = 5
    positionYChange = 0
    state = "ready"

    def fire(x, y):
        Bullet.state = "fire"
        screen.blit(Bullet.img, (x + 16, y + 10))


class Score:
    # name = input("Podaj nick gracza")
    value = 0

    def update(self, x, y):
        score = FONT.render("Score : " + str(self.value), True, (255, 255, 255))
        screen.blit(score, (x, y))


class Czas:
    gamelvl_time_start = time.time()
    gamelvl_time = 15

    enemy_latest_get_time = time.time()
    enemy_next_get_time = 1


def menu():
    nick = Score()

def explosion(x,y):
    img = pygame.image.load('explosion/boom (1).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (2).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (3).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (4).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (5).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (6).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (7).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (8).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (9).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (10).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (11).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (12).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (13).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (14).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (15).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (16).png')
    screen.blit(img, (x, y))
    pygame.display.update()
    img = pygame.image.load('explosion/boom (17).png')
    screen.blit(img, (x, y))




def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (Screen.resolutionX / 2, Screen.resolutionY / 2))


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
            Level.enemy_list.append(Enemy(1))
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
            expl = Explosion( (enemyName.positionX, enemyName.positionY), 'lg')
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
    screen.fill((0, 0, 0))
    screen.blit(BACKGROUND, (0, 0))
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
