"""
Items within the game include pellets (coins) and powerups 

    pydoc -w item

"""

import pygame
from settings import Settings
from enemy_class import Enemy


class Item:
    """
    Provides attributes and methods for all item objects within Pacman game.
    These items include pellets (coins) for points and powerups for killing ghost enemies

    """
    def __init__(self, app, item_type, location):
        self.setting = Settings()
        self.app = app
        self.type = item_type
        self.location = location

    
    def draw(self):
        """
        Depending on which type of item this function draws the relevent circle item using Pygame function draw.circle()
        """
        if self.type == "coin":
            pygame.draw.circle(self.app.screen, self.setting.GREY,
                                (int(self.location.x*self.app.cell_width)+self.app.cell_width//2+self.setting.TOP_BOTTOM_BUFFER//2,
                                    int(self.location.y*self.app.cell_height)+self.app.cell_height//2+self.setting.TOP_BOTTOM_BUFFER//2), 2)
        elif self.type == "power":
            pygame.draw.circle(self.app.screen, self.setting.WHITE,
                                (int(self.location.x*self.app.cell_width)+self.app.cell_width//2+self.setting.TOP_BOTTOM_BUFFER//2,
                                    int(self.location.y*self.app.cell_height)+self.app.cell_height//2+self.setting.TOP_BOTTOM_BUFFER//2), 4)

    
    def eat_coin(self, index):
        """
        Function controls events after pellet (coin) is collided with by player
        """
        self.app.coins.pop(index)
        self.app.current_score += 10


    def absorb_powerup(self, index):
        """
        Function controls the changes made upon a player colliding with a powerup
        """
        self.app.powerups.pop(index)
        self.app.current_score += 50
        for enemy in self.app.enemies:
            enemy.change_state("scatter")