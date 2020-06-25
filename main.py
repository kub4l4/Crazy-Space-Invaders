""" Moduł zawiera wszytskie klasy funkcje potrzebne do korzystania z gry. """

import math
import random
import sys
import time

import pygame

RESOLUTION_WIDTH = 1080
RESOLUTION_HEIGHT = 720
RESOLUTION = (RESOLUTION_WIDTH, RESOLUTION_HEIGHT)

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
POS_Y_ENEMY_WIN = 600

TXT_COLOR = (255, 255, 255)

AVAILABLE_ON_START_BULLET = 1
INCREASE_AVAILABLE_BULLET = 1

TIME_ON_START_TO_CREATE_NEW_ENEMY = 1
TIME_DECREASE_TO_CREATE_ENEMY = -0.01

ENEMY_START_SPEED = 5
ENEMY_START_POS = 10

NUMBER_OF_LEVELS = 10
SLEEP_TIME_AFTER_NEXT_LEVEL = 2

GO_TO_MENU = 1
GO_TO_GAME = 2
GO_TO_GAME_OVER = 3
GO_TO_WINNER = 4


class Assets:
    """Przechowuje zasoby."""
    game_state = GO_TO_MENU

    @staticmethod
    def load():
        """Wczytuje zasoby z dysku."""
        Assets.IMG_PLAYER = pygame.image.load('img/player.png')
        Assets.IMG_BULLET = pygame.image.load('img/bullet.png')
        Assets.IMG_ENEMY_DEFAULT = pygame.image.load('img/enemy1.png')
        Assets.IMG_ENEMY_TYPE1 = pygame.image.load('img/enemy1.png')
        Assets.IMG_ENEMY_TYPE2 = pygame.image.load('img/enemy2.png')
        Assets.IMG_ENEMY_TYPE3 = pygame.image.load('img/enemy3.png')

        Assets.IMG_MENU = pygame.image.load('img/menu.png')
        Assets.IMG_BACKGROUND = pygame.image.load('img/background.jpg')

        Assets.FONT = pygame.font.Font('font/ARMY_RUST.ttf', 50)
        Assets.MENU_FONT = pygame.font.Font('font/ARMY_RUST.ttf', 128)
        Assets.START_FONT = pygame.font.Font('font/ARMY_RUST.ttf', 50)

        Assets.TITLE1 = Assets.MENU_FONT.render("MILITARY", True, TXT_COLOR)
        Assets.TITLE2 = Assets.MENU_FONT.render("WAR", True, TXT_COLOR)
        Assets.START_TEXT = Assets.START_FONT.render("Press space bar to start", True, TXT_COLOR)
        Assets.EXIT_TEXT = Assets.START_FONT.render("Press e to exit", True, TXT_COLOR)


class Player:
    """Przechowuje informacje o graczu."""

    def __init__(self):
        """Inicjuje wsztskie zmienne o graczu."""
        self.size = 64
        self.img = Assets.IMG_PLAYER
        self.pos_x = RESOLUTION_WIDTH / 2
        self.pos_y = RESOLUTION_HEIGHT - 5 * RESOLUTION_HEIGHT / 100 - self.size
        self.pos_x_change = 0
        self.pos_x_speed = 1
        self.score = 0

    def movement(self, screen, key):
        """Funkcja przemieszcza gracza w zależności o wciśniętego przycisku."""
        if key[0] and key[1] or not key[0] and not key[1]:
            self.pos_x_change = 0
        elif key[1]:
            self.pos_x_change += self.pos_x_speed
        elif key[0]:
            self.pos_x_change -= self.pos_x_speed

        self.pos_x += self.pos_x_change
        if self.pos_x <= POS_X_MIN:
            self.pos_x = POS_X_MIN
        elif self.pos_x >= RESOLUTION_WIDTH - self.size:
            self.pos_x = RESOLUTION_WIDTH - self.size
        self.update(screen)

    def update(self, screen):
        """Pokazuje na ekranie zdjęcie gracza w określonym miejscu."""
        screen.blit(self.img, (int(self.pos_x), int(self.pos_y)))

    def update_score(self, screen):
        """Pokazuje na ekranie gry aktualną ilość punktów."""
        score = Assets.FONT.render("Score : %d" % self.score, True, TXT_COLOR)
        screen.blit(score, POS_SCORE)


class Bullet:
    """Przechowuje informacje o wszytskich pociskach."""
    list = []
    max = AVAILABLE_ON_START_BULLET
    size = 32

    def __init__(self, player1):
        """Inicjuje wsztskie zmienne o pocisku."""
        self.img = Assets.IMG_BULLET
        self.pos_x = player1.pos_x
        self.pos_y = RESOLUTION_HEIGHT - 5 * RESOLUTION_HEIGHT / 100 - player1.size
        self.pos_y_speed = 5
        self.pos_y_change = 0

    def fire(self, screen):
        """Zmienia położenie pocisku i pokazuje na ekranie zdjęcie pocisku w określonym miejscu."""
        self.pos_y -= self.pos_y_speed
        screen.blit(self.img, (int(self.pos_x) + 16, int(self.pos_y) + 10))

    @staticmethod
    def update_avaible(screen):
        """Pokazuje na ekranie gry aktualnie dostępną ilość pocisków."""
        bullet_txt = Assets.FONT.render(
            "Bullets : %d" % (Bullet.max - len(Bullet.list)), True, TXT_COLOR)
        screen.blit(bullet_txt, POS_BULLET_TXT)


class Enemy:
    """Przechowuje informacje o wszytskich wrogach."""
    list = []
    lastTime = 0
    periodTime = TIME_ON_START_TO_CREATE_NEW_ENEMY
    num_of_enemies_per_lvl = [4, 8]
    num_of_enemies_generated = 0
    current_lvl = 0

    def __init__(self, enemy_type):
        """Inicjuje wsztskie zmienne o wrogach."""
        self.size = 64
        self.img = Assets.IMG_ENEMY_DEFAULT
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
        """Zmienia zmienne obiektu jeśli TYPE=1."""
        self.size = 64
        self.img = Assets.IMG_ENEMY_TYPE1
        self.pos_x_speed = 3

    def enemy_type2(self):
        """Zmienia zmienne obiektu jeśli TYPE=2."""
        self.size = 64
        self.img = Assets.IMG_ENEMY_TYPE2
        self.pos_x_speed = 4

    def enemy_type3(self):
        """Zmienia zmienne obiektu jeśli TYPE=3."""
        self.size = 64
        self.img = Assets.IMG_ENEMY_TYPE3
        self.pos_x_speed = 5

    def update(self, screen):
        """Pokazuje na ekranie zdjęcie przeciwnika w określonym miejscu."""
        screen.blit(self.img, (int(self.pos_x), int(self.pos_y)))

    def down_change_direction(self):
        """Zmienia kierunek porusznia się wroga i przenosi go niżej."""
        self.pos_x_speed = -self.pos_x_speed
        self.pos_y += self.pos_y_speed


def menu(screen):
    """funkcja definiująca menu gry."""
    screen.blit(Assets.IMG_MENU, (POS_X_MIN, POS_Y_MIN))
    screen.blit(Assets.TITLE1, POS_TITLE1)
    screen.blit(Assets.TITLE2, POS_TITLE2)
    screen.blit(Assets.START_TEXT, POS_START_TXT)

    pygame.display.update()
    start_button()


def game_over_text(screen, player1):
    """fukcja pokazuje tekst po przegraniu."""
    dead_txt = Assets.FONT.render('GAME OVER', True, TXT_COLOR)
    screen.blit(dead_txt, POS_DEAD_TXT)

    dead_txt = Assets.FONT.render('SCORE: %d' % player1.score, True, TXT_COLOR)
    screen.blit(dead_txt, POS_SCORE_TXT)
    screen.blit(Assets.EXIT_TEXT, POS_START_TXT)


def game_win_text(screen, player1):
    """fukcja pokazuje tekst po wygraniu."""
    dead_txt = Assets.FONT.render("WINNER", True, TXT_COLOR)
    screen.blit(dead_txt, POS_DEAD_TXT)

    dead_txt = Assets.FONT.render('SCORE: %d' % player1.score, True, TXT_COLOR)
    screen.blit(dead_txt, POS_SCORE_TXT)
    screen.blit(Assets.EXIT_TEXT, POS_START_TXT)


def buttons(key, player1):
    """obsługa przycisków w trakcie gry."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key[0] = True
            if event.key == pygame.K_RIGHT:
                key[1] = True
            if event.key == pygame.K_SPACE:
                if len(Bullet.list) < Bullet.max:
                    Bullet.list.append(Bullet(player1))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key[0] = False
            if event.key == pygame.K_RIGHT:
                key[1] = False
    return key


def exit_button():
    """Obsługa przycisków po skończeniu gry."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                sys.exit(0)


def start_button():
    """Obsługa przycisków w menu."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Assets.game_state = GO_TO_GAME


def enemy_creator():
    """Tworzenie nowych przeciwników w zależności od poziumu."""
    if Enemy.num_of_enemies_per_lvl[Enemy.current_lvl] > Enemy.num_of_enemies_generated:
        if Enemy.lastTime + Enemy.periodTime < time.time():
            Enemy.lastTime = time.time()
            if Enemy.current_lvl == 0:
                Enemy.list.append(Enemy(1))
            if Enemy.current_lvl == 1:
                Enemy.list.append(Enemy(1))
                Enemy.list.append(Enemy(2))
            if Enemy.current_lvl >= 2:
                Enemy.list.append(Enemy(1))
                Enemy.list.append(Enemy(2))
                Enemy.list.append(Enemy(3))
            Enemy.num_of_enemies_generated += 1


def enemy_movement(screen, player1):
    """Funkcja zmieniająca współrzędne wszytskich przeniwników."""
    for n_enemy in Enemy.list:
        if n_enemy.pos_y < ENEMY_START_POS:
            n_enemy.pos_y = n_enemy.pos_y + ENEMY_START_SPEED
        else:
            n_enemy.pos_x += n_enemy.pos_x_speed
            if n_enemy.pos_x < POS_X_MIN:
                n_enemy.pos_x = POS_X_MIN
                n_enemy.down_change_direction()
            elif n_enemy.pos_x > RESOLUTION_WIDTH - player1.size:
                n_enemy.pos_x = RESOLUTION_WIDTH - player1.size
                n_enemy.down_change_direction()
        n_enemy.update(screen)


def bullet_movement(screen):
    """Funkcja zmieniająca współrzędne wszytskich pocisków."""
    for n_bullet in Bullet.list:
        if n_bullet.pos_y <= POS_Y_MIN - Bullet.size:
            Bullet.list.remove(n_bullet)
        else:
            n_bullet.fire(screen)


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y, size):
    """Funkcja sprawdzająca czy pocisk uderzył w przeciwnika"""
    distance = math.hypot(enemy_x - bullet_x, enemy_y - bullet_y)
    if distance < size / 2:
        return True
    return False


def collision(player1):
    """Funkcja usuwa obiekt przeciwnika i pocisk, jeśli is_collision zwróci prawdę."""
    for n_enemy in Enemy.list:
        for n_bullet in Bullet.list:
            if is_collision(
                    n_enemy.pos_x, n_enemy.pos_y, n_bullet.pos_x, n_bullet.pos_y, n_enemy.size):
                Enemy.list.remove(n_enemy)
                Bullet.list.remove(n_bullet)
                player1.score += 1


def next_level(screen):
    """
    Funkcja sprawdza, czy gracz może już wejść na wyższy poziom.

    Sprawdza, czy wszyscy przeciwnicy zostali pokonani.
    Jeśli tak to generuje kolejny level oraz dodaje dodatkowy pocisk dla gracza.
    """
    if not Enemy.list:
        Enemy.current_lvl += 1
        Bullet.max += INCREASE_AVAILABLE_BULLET
        Enemy.periodTime -= TIME_DECREASE_TO_CREATE_ENEMY
        Enemy.num_of_enemies_per_lvl.append(
            (Enemy.num_of_enemies_per_lvl[Enemy.current_lvl] + random.randint(
                Enemy.current_lvl, Enemy.current_lvl * Enemy.current_lvl)))
        next_level_txt = Assets.MENU_FONT.render(
            "Level: %d completed!" % Enemy.current_lvl, True, TXT_COLOR)
        screen.blit(next_level_txt, POS_NEXT_LVL_TXT)
        pygame.display.update()
        time.sleep(SLEEP_TIME_AFTER_NEXT_LEVEL)


def ending_condition():
    """Sprawdza waruneki końca gry."""
    for n_enemy in Enemy.list:
        if n_enemy.pos_y > POS_Y_ENEMY_WIN:
            Assets.game_state = GO_TO_GAME_OVER
            break
    if Enemy.current_lvl == NUMBER_OF_LEVELS:
        Assets.game_state = GO_TO_WINNER


def game(screen, key, player1):
    """Obsługuje czas grania w gre."""
    screen.blit(Assets.IMG_BACKGROUND, (POS_X_MIN, POS_Y_MIN))
    key = buttons(key, player1)
    collision(player1)
    player1.update_score(screen)
    Bullet.update_avaible(screen)
    enemy_creator()
    player1.movement(screen, key)
    enemy_movement(screen, player1)
    bullet_movement(screen)
    pygame.display.update()
    next_level(screen)
    ending_condition()


def main():
    """Funkcja główna."""

    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Military War")
    Assets.load()
    player1 = Player()
    key = [False, False]
    while True:
        if Assets.game_state == GO_TO_MENU:
            menu(screen)

        if Assets.game_state == GO_TO_GAME:
            game(screen, key, player1)

        if Assets.game_state == GO_TO_GAME_OVER:
            screen.blit(Assets.IMG_MENU, (POS_X_MIN, POS_Y_MIN))
            screen.blit(Assets.TITLE1, POS_TITLE1)
            screen.blit(Assets.TITLE2, POS_TITLE2)
            game_over_text(screen, player1)
            exit_button()
            pygame.display.update()

        if Assets.game_state == GO_TO_WINNER:
            screen.blit(Assets.IMG_MENU, (POS_X_MIN, POS_Y_MIN))
            screen.blit(Assets.TITLE1, POS_TITLE1)
            screen.blit(Assets.TITLE2, POS_TITLE2)
            game_win_text(screen, player1)
            exit_button()
            pygame.display.update()


if __name__ == "__main__":
    main()
