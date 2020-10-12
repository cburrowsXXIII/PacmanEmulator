import unittest
import pygame, sys
from app_class import *
from enemy_class import *
from item_class import *
from player_class import *

pygame.init()
vec = pygame.math.Vector2


class TestStringMethods(unittest.TestCase):
    
    def test_coin_creation(self):
        item = Item(self, "coin", [20,30])
        self.assertEqual(item.type, "coin")
    
    def test_enemy_creation(self):
        app = App()
        item = Item(self, "coin", [20,30])
        self.assertEqual(item.type, "coin")

    def test_player_creation(self):
        item = Item(self, "coin", [20,30])
        self.assertEqual(item.type, "coin")

    def test_get_pix_pos_enemy(self):
        item = Item(self, "coin", [20,30])
        self.assertEqual(item.type, "coin")
    
    def test_get_pix_pos_player(self):
        item = Item(self, "coin", [20,30])
        self.assertEqual(item.type, "coin")
    
    def test_reset(self):
        item = Item(self, "coin", [20,30])
        self.assertEqual(item.type, "coin")
    
    def test_hard_reset(self):
        item = Item(self, "coin", [20,30])
        self.assertEqual(item.type, "coin")
    
    def test_new_level(self):
        item = Item(self, "coin", [20,30])
        self.assertEqual(item.type, "coin")

if __name__ == '__main__':
    unittest.main()