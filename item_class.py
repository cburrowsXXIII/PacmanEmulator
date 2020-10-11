import pygame
from settings import Settings
from enemy_class import Enemy

class Item:
    def __init__(self, app, item_type, location):
        self.setting = Settings()
        self.app = app
        self.type = item_type
        self.location = location


    def draw(self):
        if self.type == "coin":
            pygame.draw.circle(self.app.screen, self.setting.GREY,
                                (int(self.location.x*self.app.cell_width)+self.app.cell_width//2+self.setting.TOP_BOTTOM_BUFFER//2,
                                    int(self.location.y*self.app.cell_height)+self.app.cell_height//2+self.setting.TOP_BOTTOM_BUFFER//2), 2)
        elif self.type == "power":
            pygame.draw.circle(self.app.screen, self.setting.WHITE,
                                (int(self.location.x*self.app.cell_width)+self.app.cell_width//2+self.setting.TOP_BOTTOM_BUFFER//2,
                                    int(self.location.y*self.app.cell_height)+self.app.cell_height//2+self.setting.TOP_BOTTOM_BUFFER//2), 4)

    
    def eat_coin(self, index):
        self.app.coins.pop(index)
        self.app.current_score += 10


    def absorb_powerup(self, index):
        self.app.powerups.pop(index)
        self.app.current_score += 50
        for enemy in self.app.enemies:
            enemy.change_state("scatter")