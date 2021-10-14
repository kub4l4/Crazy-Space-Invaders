# Crazy SpaceInvaders

School project - python
## 1. Project topic
The theme of the project is a Space Invaders game in a different style. As in the original version, the player moves left and right, shooting at his opponents. Contrary to the standard version, enemies fly from above to the screen in a random position. After moving down to a certain height, they start moving right until they hit the end of the screen. This is the moment when the enemy flies down and starts moving to the left.
Hitting an enemy with a missile scores a point. After hitting all monsters, the player moves to the next level. With each level, the possible difficulty of the game increases and the number of missile available to the player increases. Up to level 3, the number of monsters remains constant. From 3 levels on, the number of monsters is generated in a way that increases the possible difficulty of the game.
The game ends when the player passes a certain number of levels or when the opponent reaches a certain point on the screen.
![Image of Yaktocat](https://raw.githubusercontent.com/kub4l4/Crazy-Space-Invaders/master/screen.png)

## 2. Code
The program code was written in one python module, using libraries:
```python
import math
import random
import sys
import time
import pygame
```
This was changed in later stages - the player, projectile, and opponent are objects.<br/>
Enemy class example:
```python
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
```
## 3. Test
The selected classes have been tested in the `main_test.py` file:<br/>

Example:
```python
class BulletTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        main.Assets.load()

    def setUp(self):
        player1 = main.Player()
        self.n_bullet = main.Bullet(player1)

    def test_fire(self):
        self.n_bullet.pos_y -= self.n_bullet.pos_y_speed
        self.assertEqual(self.n_bullet.pos_y, 615)


class EnemyTest(unittest.TestCase):
    def setUp(self):
        self.n_enemy = main.Enemy(1)

    def test_down_change_direction(self):
        self.n_enemy.pos_x_speed = -self.n_enemy.pos_x_speed
        self.assertEqual(self.n_enemy.pos_x_speed, -3)

    def test_down_change_direction2(self):
        self.n_enemy.pos_y += self.n_enemy.pos_y_speed
        self.assertEqual(self.n_enemy.pos_y, 6)


class TestCollision(unittest.TestCase):
    def test_is_collision(self):
        self.assertTrue(main.is_collision(100, 400, 125, 400, 64))
```
## 3. Summary
The implementation of the project made me realize that learning many methods and libraries allows me to implement better and more efficient programs. Additionally, systematized my knowledge gained during laboratory classes.
