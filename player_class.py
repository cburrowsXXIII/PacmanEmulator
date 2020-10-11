import pygame
from settings import Settings
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.setting = Settings()
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        
        self.speed = 2
        self.lives = 3

    def update(self):
        # Movement Rules
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                if self.direction.x == self.stored_direction.x or self.direction.y == self.stored_direction.y:
                    self.direction = self.stored_direction
                else:
                    for turn in self.app.turns:
                        if self.grid_pos == turn and self.can_move(self.stored_direction):
                            self.direction = self.stored_direction
                            
            self.able_to_move = self.can_move(self.direction)
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0]-self.setting.TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-self.setting.TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1
        self.on_item()

    def draw(self):
        pygame.draw.circle(self.app.screen, self.setting.PLAYER_COLOUR, (int(self.pix_pos.x),
                                                            int(self.pix_pos.y)), self.app.cell_width//2-2)

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, self.setting.PLAYER_COLOUR, (30 + 20*x, self.setting.HEIGHT - 15), 7)

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.app.cell_width)+self.setting.TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos[1]*self.app.cell_height) +
                   self.setting.TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)

        print(self.grid_pos, self.pix_pos)

    def time_to_move(self):
        if int(self.pix_pos.x+self.setting.TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+self.setting.TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self, direction):
        for wall in self.app.walls:
            if vec(self.grid_pos+direction) == wall:
                return False
        return True

    def on_item(self):
        #Coin handler
        for idx, coin in enumerate(self.app.coins):
            if self.grid_pos == coin.location:
                if int(self.pix_pos.x+self.setting.TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                    if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                        coin.eat_coin(idx)                        
                if int(self.pix_pos.y+self.setting.TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                    if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                        coin.eat_coin(idx)
        ##Power up handler
        for idx, powerup in enumerate(self.app.powerups):
            if self.grid_pos == powerup.location:
                if int(self.pix_pos.x+self.setting.TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                    if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                        powerup.absorb_powerup(idx)                        
                if int(self.pix_pos.y+self.setting.TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                    if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                        powerup.absorb_powerup(idx)
        
