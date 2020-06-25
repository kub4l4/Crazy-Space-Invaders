"""Testy modułu main."""

import unittest

import pygame

import main


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


class TestEnemyCreator(unittest.TestCase):
    def test_enemy_creator(self):
        main.enemy_creator()
        self.assertEqual(main.Enemy.num_of_enemies_generated, 1)


class TestEnemyMovement(unittest.TestCase):
    def test_enemy_movement(self):
        player = main.Player()
        main.n_enemy = main.Enemy(1)
        main.enemy_movement(pygame.display.set_mode(main.RESOLUTION), player)
        self.assertEqual(main.n_enemy.pos_y, -64)


if __name__ == '__main__':
    unittest.main()
