"""
This module describes the Enemy class and provides all functionality for enemy objects created by the controller.
The enemies each have unique personalities in how they chase the player:
The red ghost directly chases the player using A* pathfinding and has a higher speed.
The blue ghost periodically chases the player and otherwise just wanders the maze randomly
The pink ghost uses A* to find the next place that the player will be
The yellow ghost does the same yet switches to flee occasionally

    pydoc -w enemy_class

"""

import pygame
import random
from settings import Settings

vec = pygame.math.Vector2


class Enemy:
    """
    Provides attributes and methods for all Enemy objects within Pacman game.
    """
    def __init__(self, app, pos, id, scatter_target):
        self.setting = Settings()
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.enemy_id = id
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = None 
        self.scatter_target = scatter_target
        self.state = "chase"
        self.scatter_timer = 0
        self.scatter_time_limit = 300
        self.respawn_wait_time = 0
        self.reached_base = False
        self.clyde_timer = 0
        self.speedy_timer = 0

    def update(self):
        """
        Function updates the enemy every frame
        """
        self.speed = self.set_speed()
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0]-self.setting.TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-self.setting.TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1

    def draw(self):
        """
        Function draws the enemy
        """
        pygame.draw.circle(self.app.screen, self.colour,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_speed(self):
        """
        Function sets speed characteristic
        """
        if self.personality in ["speedy", "scared"] and self.state != "scatter":
            if self.speedy_timer >= 200:
                speed = 1
            speed = 2
        else:
            speed = 1
        return speed

    def set_target(self):
        """
        Function sets target for each enemy based on their personalities for CHASE state and uses SCATTER state when player has consumed powerup
        """
        #SCATTER Handler
        if self.state == "scatter": 
            self.has_scattered = True           
            self.colour = self.setting.BLUE
            self.scatter_timer += 1
            if self.scatter_timer >= self.scatter_time_limit:
                self.scatter_timer = 0
                self.state = "chase"
            if self.grid_pos == self.scatter_target:
                self.reached_base = True
            if  self.reached_base == False:
                return self.app.player.grid_pos
            return self.scatter_target
        #CHASE Handler    
        elif self.state == "chase":
            self.reached_base = False
            self.scatter_timer = 0
            self.colour = self.set_colour()    
            if self.personality == "speedy" or self.personality == "slow" or self.personality == "clyde":
                return self.app.player.grid_pos
            else:
                if self.app.player.grid_pos[0] > self.setting.COLS//2 and self.app.player.grid_pos[1] > self.setting.ROWS//2:
                    return vec(1, 1)
                if self.app.player.grid_pos[0] > self.setting.COLS//2 and self.app.player.grid_pos[1] < self.setting.ROWS//2:
                    return vec(1, self.setting.ROWS-2)
                if self.app.player.grid_pos[0] < self.setting.COLS//2 and self.app.player.grid_pos[1] > self.setting.ROWS//2:
                    return vec(self.setting.COLS-2, 1)
                else:
                    return vec(self.setting.COLS-2, self.setting.ROWS-2)

    def time_to_move(self):
        """
        Determines if an enemy can physically move
        """
        if int(self.pix_pos.x+self.setting.TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+self.setting.TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        """
        Handles the enemy move mechanics based on personalities
        """
        if self.personality == "clyde":
            self.clyde_timer += 1
            if self.clyde_timer >= 200:
                self.direction = self.get_random_direction()
                if self.clyde_timer >= 400:
                    self.clyde_timer = 0
            else:
                self.direction = self.get_path_direction(self.target)
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.speedy_timer += 1
            if self.speedy_timer >= 400 - 100 * self.app.level:
                self.speedy_timer = 0
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        """
        One of the steps in the multifunction A* algorithm. Focused on finding the next cell
        """
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        """
        One of the steps in the multifunction A* algorithm. Focused on finding the next cell in the path list
        """
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target[0]), int(target[1])])
        return path[1]

    def BFS(self, start, target):
        """
        Provides all remaining A* functionality
        """
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        """
        Function used for yellow ghosts occasional random movement
        """
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def get_pix_pos(self):
        """
        Gets the current position on the grid that the enemy is situated in
        """
        return vec((self.grid_pos.x*self.app.cell_width)+self.setting.TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos.y*self.app.cell_height)+self.setting.TOP_BOTTOM_BUFFER//2 +
                   self.app.cell_height//2)

    def set_colour(self):
        """
        Sets the enemy colour based on their personalities
        """
        if self.enemy_id == 0:
            return self.setting.RED
        if self.enemy_id == 1:
            return self.setting.ORANGE
        if self.enemy_id == 2:
            return self.setting.LILAC
        if self.enemy_id == 3:
            return self.setting.AQUA

    def set_personality(self):
        """
        Initialises the enemy personality based on their ID
        """
        if self.enemy_id == 0:
            return "speedy"
        elif self.enemy_id == 1:
            return "slow"
        elif self.enemy_id == 2:
            return "clyde"
        else:
            return "scared"

    def change_state(self, state):
        """
        Function communicates with the controller for when a powerup has been selected
        """
        if self.state == "scatter":
            self.scatter_time_limit += 200
        self.state = state

    def respawn(self):
        """
        Handles enemy respawn after death
        """
        self.state = "chase"
        self.grid_pos = vec(self.starting_pos)
        self.pix_pos = self.get_pix_pos()
    

