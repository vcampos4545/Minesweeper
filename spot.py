import pygame
pygame.font.init()
from constants import ROWS, COLS, WHITE, BLACK, RED, BLUE, GREY

class Spot:
    def __init__(self, i, j, width):
        self.i = i
        self.j = j
        self.x = j * width
        self.y = i * width
        self.w = width
        self.neighbors = []
        self.num_mines = 0
        self.mine = False
        self.flag = False
        self.revealed = False

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.i < ROWS - 1: # DOWN
            if grid[self.i + 1][self.j].mine:
                self.num_mines += 1
            self.neighbors.append(grid[self.i + 1][self.j])

        if self.i > 0: # UP
            if grid[self.i - 1][self.j].mine:
                self.num_mines += 1
            self.neighbors.append(grid[self.i - 1][self.j])

        if self.j < COLS - 1: # RIGHT
            if grid[self.i][self.j + 1].mine:
                self.num_mines += 1
            self.neighbors.append(grid[self.i][self.j + 1])

        if self.j > 0: # LEFT
            if grid[self.i][self.j - 1].mine:
                self.num_mines += 1
            self.neighbors.append(grid[self.i][self.j - 1])

        if self.i < ROWS - 1 and self.j < COLS - 1: # DOWN RIGHT
            if grid[self.i + 1][self.j + 1].mine:
                self.num_mines += 1
            self.neighbors.append(grid[self.i + 1][self.j + 1])

        if self.i < ROWS - 1 and self.j > 0: # DOWN LEFT
            if grid[self.i + 1][self.j - 1].mine:
                self.num_mines += 1
            self.neighbors.append(grid[self.i + 1][self.j - 1])

        if self.i > 0 and self.j < COLS - 1: # UP RIGHT
            if grid[self.i - 1][self.j + 1].mine:
                self.num_mines += 1
            self.neighbors.append(grid[self.i - 1][self.j + 1])

        if self.i > 0 and self.j > 0: # UP LEFT
            if grid[self.i - 1][self.j - 1].mine:
                self.num_mines += 1
            self.neighbors.append(grid[self.i - 1][self.j - 1])

    def draw(self, win):
        if self.revealed:
            if self.mine:
                pygame.draw.rect(win, RED, (self.x, self.y, self.w, self.w))

            else:
                pygame.draw.rect(win, WHITE, (self.x, self.y, self.w, self.w))
                if self.num_mines > 0:
                    font = pygame.font.Font('freesansbold.ttf',10)
                    display = font.render(str(self.num_mines),True,BLACK)
                    textRect = display.get_rect()
                    textRect.center = (self.x + self.w//2,self.y + self.w//2)
                    win.blit(display,textRect)
        else:
            if self.flag:
                pygame.draw.rect(win, BLUE, (self.x, self.y, self.w, self.w))
            else:
                pygame.draw.rect(win, GREY, (self.x, self.y, self.w, self.w))

    def reveal(self):
        self.revealed = True
        #If revealed spot is a mine end game
        if self.mine:
            print('Game Over')
            return -1
        
        if self.num_mines == 0:
            for n in self.neighbors:
                if not n.revealed:
                    n.reveal()
        return 0

    def all_flags(self):
        count = 0
        for n in self.neighbors:
            if n.flag:
                count += 1
        
        if count == self.num_mines:
            return True
        return False
