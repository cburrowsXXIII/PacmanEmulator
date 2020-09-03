import pygame, sys
from settings import *
from player_class import Player
from enemy_class import Enemy

pygame.init()
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.walls = []
        self.enemies = []
        self.coins = []
        self.enemy_pos = []
        self.player_pos = None

        #debugging variables
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 30

        self.load()
        self.player = Player(self, self.player_pos)
        self.make_enemies()

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
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

#######################HELPER FUNCTIONS####################################

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH,MAZE_HEIGHT))

        #opening walls file and creating walls list with coords
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.player_pos = vec(xidx, yidx)
                    elif char in ["2", "3", "4", "5"]:
                        self.enemy_pos.append(vec(xidx, yidx))
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height, self.cell_width, self.cell_height))

    def draw_text(self, words, screen, pos, font_size, font_colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, font_size)
        text = font.render(words, False, font_colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)


######################DEBUGGING FUNCTIONS##################################

    def draw_grid(self):
        for i in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY,(i*self.cell_width, 0), (i*self.cell_width, HEIGHT))
        for i in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY,(0, i*self.cell_height), (WIDTH, i*self.cell_height))

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
        self.screen.fill(BLACK)
        self.draw_text('HIGH SCORE', self.screen, [25, 0], START_FONT_SIZE, WHITE,
                       START_FONT)
        self.draw_text('START [ENTER]', self.screen, [WIDTH // 2, HEIGHT // 2], START_FONT_SIZE, ORANGE, START_FONT, centered=True)
        self.draw_text('SETTINGS [SPACE]', self.screen, [WIDTH // 2, HEIGHT // 2  + 80], START_FONT_SIZE, LILAC, START_FONT,
                       centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH // 2, HEIGHT // 2 + 200], START_FONT_SIZE, AQUA,
                       START_FONT, centered=True)
        pygame.display.update()

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

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        # self.draw_grid()
        self.draw_coins()
        self.draw_text('HIGH SCORE: 0', self.screen, [25, 0], START_FONT_SIZE, WHITE,
                       START_FONT)
        self.draw_text('SCORE: {}'.format(self.player.current_score), self.screen, [WIDTH - 125, 0], START_FONT_SIZE, WHITE,
                       START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, WHITE, (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2, int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 2)

    def make_enemies(self):
        for idx, pos in enumerate(self.enemy_pos):
            self.enemies.append(Enemy(self, pos, idx))