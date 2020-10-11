import pygame, sys
from settings import Settings
from player_class import Player
from enemy_class import Enemy
from item_class import *

pygame.init()
vec = pygame.math.Vector2
setting = Settings()

class App:
    def __init__(self):
        print(vars(setting))
        self.screen = pygame.display.set_mode((setting.WIDTH, setting.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = setting.MAZE_WIDTH//setting.COLS
        self.cell_height = setting.MAZE_HEIGHT//setting.ROWS

        #load from environment file
        self.walls = []
        self.coins = []
        self.powerups = []
        self.turns = []
        self.enemies = []
        self.enemies_to_respawn = []
        self.scatter_targets = []
        self.e_pos = []
        self.p_pos = None        
        self.respawn = None  
        self.load()     
        

        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()
        self.current_score = 0
        self.level = 1
        

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(setting.fps)
        pygame.quit()
        sys.exit()

#######################HELPER FUNCTIONS####################################

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (setting.MAZE_WIDTH, setting.MAZE_HEIGHT))

        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as  a vector
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char in "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "U":
                        self.powerups.append(Item(self, "power", vec(xidx, yidx)))
                    elif char == "R":
                        self.respawn = vec(xidx, yidx)
                        print(self.respawn)
                    elif char in ["C", "T", "b", "p", "i", "c"]:
                        self.coins.append(Item(self, "coin", vec(xidx, yidx)))
                        if char in ["b", "p", "i", "c"]:
                            self.scatter_targets.append(vec(xidx, yidx))
                        if char == "T":
                            self.turns.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, setting.BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))
    
    def draw_text(self, words, screen, pos, font_size, font_colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, font_size)
        text = font.render(words, False, font_colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)
    
    def reset(self, condition):
        if condition == "hard reset":
            self.current_score = 0
        self.player.lives = 3
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.direction = vec(1, 0)
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        self.turns = []
        self.powerups = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C' or char == "T":
                        self.coins.append(Item(self, "coin", vec(xidx, yidx)))
                        if char == "T":
                            self.turns.append(vec(xidx, yidx))
                    elif char == "U":
                        self.powerups.append(Item(self, "power", vec(xidx, yidx)))
        self.state = "playing"


######################DEBUGGING FUNCTIONS##################################

    def draw_grid(self):
        for i in range(setting.WIDTH//self.cell_width):
            pygame.draw.line(self.background, setting.GREY,(i*self.cell_width, 0), (i*self.cell_width, setting.HEIGHT))
        for i in range(setting.HEIGHT//self.cell_height):
            pygame.draw.line(self.background, setting.GREY,(0, i*self.cell_height), (setting.WIDTH, i*self.cell_height))

#######################START FUNCTIONS####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(setting.BLACK)
        self.draw_text('HIGH SCORE', self.screen, [25, 0], setting.START_FONT_SIZE, setting.WHITE,
                       setting.START_FONT)
        self.draw_text('START [ENTER]', self.screen, [setting.WIDTH // 2, setting.HEIGHT // 2], setting.START_FONT_SIZE, setting.ORANGE, setting.START_FONT, centered=True)
        self.draw_text('SETTINGS [SPACE]', self.screen, [setting.WIDTH // 2, setting.HEIGHT // 2  + 80], setting.START_FONT_SIZE, setting.LILAC, setting.START_FONT,
                       centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [setting.WIDTH // 2, setting.HEIGHT // 2 + 200], setting.START_FONT_SIZE, setting.AQUA,
                       setting.START_FONT, centered=True)
        pygame.display.update()

#######################LEVEL CHANGER FUNCTIONS####################################

    def new_level(self):
        self.level += 1
        self.reset("new level")
        self.state = "playing"


#######################PLAYING FUNCTIONS####################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()        
        self.enemy_collision_handler()
        self.enemy_respawn_handler()
                

    def playing_draw(self):
        self.screen.fill(setting.BLACK)
        self.screen.blit(self.background, (setting.TOP_BOTTOM_BUFFER // 2, setting.TOP_BOTTOM_BUFFER // 2))
        # self.draw_grid()
        self.draw_items()
        self.draw_text('HIGH SCORE: 0', self.screen, [25, 0], setting.START_FONT_SIZE, setting.WHITE,
                       setting.START_FONT)
        self.draw_text('SCORE: {}'.format(self.current_score), self.screen, [setting.WIDTH - 135, 0], setting.START_FONT_SIZE, setting.WHITE,
                       setting.START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()  

########################### GAME OVER FUNCTIONS ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset("hard reset")
                self.state = "start"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(setting.BLACK)
        again_text = "CONTINUE [SPACE]"
        self.draw_text("GAME OVER", self.screen, [setting.WIDTH//2, 100],  52, RED, "arial", centered=True)
        self.draw_text(again_text, self.screen, [
                       setting.WIDTH//2, setting.HEIGHT//2],  36, (190, 190, 190), "arial", centered=True)
        
        pygame.display.update()



########################### EVENT HANDLERS ################################

    def draw_items(self):
        if len(self.coins) > 0:
            for coin in self.coins:
                coin.draw()
            
            for powerup in self.powerups:
                powerup.draw()            
        else:
            self.state = "next level"

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx, self.scatter_targets[idx]) )
    
    def enemy_collision_handler(self):
        for idx, enemy in enumerate(self.enemies):
            if enemy.grid_pos == self.player.grid_pos and enemy.state == "chase":
                self.remove_life()
            elif enemy.grid_pos == self.player.grid_pos and enemy.state == "scatter":
                enemy.respawn_wait_time = 100 * self.level
                self.enemies_to_respawn.append(enemy)
                self.enemies.pop(idx)                              
                self.current_score += 100

    def enemy_respawn_handler(self):
        if len(self.enemies_to_respawn) > 0:
            for idx, enemy in enumerate(self.enemies_to_respawn):
                if enemy.respawn_wait_time == 0:
                    enemy.respawn()
                    self.enemies.append(enemy)
                    self.enemies_to_respawn.pop(idx)
                else:
                    enemy.respawn_wait_time -= 1

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0
    
    