import pygame
import random
from settings import *



class Enemy:
    def __init__(self, app, pos,idx):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.character_id = idx
        self.colour = self.set_colour()
        self.direction = vec(1, 0)
        self.personality = self.set_personality()

    def update(self):
        self.pix_pos += self.direction
        if self.time_to_move():
            self.move()

        #grid pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def set_colour(self):
        if self.character_id == 0:
            return RED
        if self.character_id == 1:
            return AQUA
        if self.character_id == 2:
            return LILAC
        if self.character_id == 3:
            return YELLOW

    def set_personality(self):
        if self.character_id == 0:
            return "speedy"
        if self.character_id == 1:
            return "slow"
        if self.character_id == 2:
            return "random"
        if self.character_id == 3:
            return "scared"

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True
        return False

    def move(self):
        # if self.personality == "random":
        #     self.direction = self.get_random_direction()
        self.direction = self.get_random_direction()

    def get_random_direction(self):
        while True:
            number = random.randint(-2,1)
            if number == -2:
                xdir, ydir = 1,0
            elif number == -1:
                xdir, ydir = 0,1
            elif number == 0:
                xdir, ydir = -1,0
            else:
                xdir, ydir = 0,-1
            next_pos = vec(self.grid_pos.x + xdir, self.grid_pos.y + ydir)
            if next_pos not in self.app.walls:
                break
        return vec(xdir,ydir)

