"""Testy modułu main."""

import unittest

import pygame

import main


class EnemyTest(unittest.TestCase):
    """Klasa dokonująca klasy Enemy."""
    def setUp(self):
        pygame.init()
        main.Assets.load()
        self.n_enemy = main.Enemy(1)

    def test_down_change_direction(self):
        self.n_enemy.pos_x_speed = -self.n_enemy.pos_x_speed
        self.assertEqual(self.n_enemy.pos_x_speed, -3)

    def test_down_change_direction2(self):
        self.n_enemy.pos_y += self.n_enemy.pos_y_speed
        self.assertEqual(self.n_enemy.pos_y, 6)


class BulletTest(unittest.TestCase):
    """Klasa dokonująca klasy Bullet."""
    def setUp(self):
        pygame.init()
        main.Assets.load()
        player1 = main.Player()
        self.n_bullet = main.Bullet(player1)

    def test_fire(self):
        self.n_bullet.pos_y -= self.n_bullet.pos_y_speed
        self.assertEqual(self.n_bullet.pos_y, 615)


class TestCollision(unittest.TestCase):
    """Klasa dokonująca testów funkcji is_collision."""
    def setUp(self):
        self.enemy_x = 150
        self.enemy_y = 300
        self.bullet_x = 140
        self.bullet_y = 300
        self.size = 64

    def test1(self):
        self.assertEqual(main.is_collision(
            self.enemy_x, self.enemy_y, self.bullet_x, self.bullet_y, self.size), True)


class TestEnemy_creator(unittest.TestCase):
    """Klasa dokonująca testów funkcji enemy_creator."""
    def setUp(self):
        pygame.init()
        main.Assets.load()
        main.enemy_creator()

    def test1(self):
        self.assertEqual(main.Enemy.num_of_enemies_generated, 1)


class TestEnemyMovement(unittest.TestCase):
    """Klasa dokonująca testów funkcji enemy_movement."""
    def setUp(self):
        pygame.init()
        main.Assets.load()
        screen = pygame.display.set_mode(main.RESOLUTION)
        player = main.Player()
        main.n_enemy = main.Enemy(1)
        main.enemy_movement(screen, player)

    def test1(self):
        self.assertEqual(main.n_enemy.pos_y, -64)


if __name__ == '__main__':
    unittest.main()
