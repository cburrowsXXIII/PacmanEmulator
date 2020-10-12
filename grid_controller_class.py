from math import sin, cos, pi
import pygame
vec = pygame.math.Vector2

class Grid_controller:
    def __init__(self):
        self.bg_color = (4, 16, 189)
        self.fg_color = (0, 255, 255)
        self.alt_color = (255,0,0)
        self.color = fg_color
        self.TOP_BOTTOM_BUFFER = 50
        self.WIDTH = 610
        self.HEIGHT = 670
        self.w = WIDTH - TOP_BOTTOM_BUFFER
        self.h = HEIGHT - TOP_BOTTOM_BUFFER
        self.vertex_count = 6
    
    def draw_regular_polygon(surface, color, vertex_count, radius, position):
        n, r = vertex_count, radius
        x, y = position
        pygame.draw.polygon(surface, color, [
            (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
            for i in range(n)
        ])   


    def draw_hexagonal_grid(self):
        row = 0
        file_row = 0
        odd = 40
        x_offset = 10
        y_offset = 20
        coords = []
        walls=[]
        coord_rows = []
        for x in range(w + 1):
            if x == 0 or x % 34 == 0:
                for y in range(h + 1):
                    if y == 0 or y % odd == 0:
                        if row % 2 == 0:
                            coord_rows.append((x + x_offset, y))
                        else:
                            coord_rows.append((x + x_offset, y + y_offset))
                row += 1
                coords.append(coord_rows)
                coord_rows = []

        with open("test.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        if xidx % 2 == 0:
                            walls.append((xidx *34+10,yidx * 40))
                        else:
                            walls.append((xidx * 34 + 10, yidx * 40 + 20))
        
        for wall in walls:
            draw_regular_polygon(root, color, vertex_count,
                            22, wall)

    # print(walls)
    # pygame.init()
    # root = pygame.display.set_mode((w, h))
    # print(coords)
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             exit()

    #         # Use UP / DOWN arrow keys to increase / decrease the vertex count
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_UP:
    #                 vertex_count += 1
    #             elif event.key == pygame.K_DOWN:
    #                 vertex_count = max(3, vertex_count - 1)

    #     root.fill(bg_color)
    #     

    #     pygame.display.flip()