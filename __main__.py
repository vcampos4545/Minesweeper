import pygame
import random
from spot import Spot
from constants import *

class Game:
    def __init__(self):
        self.grid = None #2d array of rows of Spot objects
        self.loop = True #Loop boolean

    def run(self):
        WIN = pygame.display.set_mode((WIDTH,HEIGHT))

        while self.loop:
            #INPUTS/LOGIC
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.loop = False
                if pygame.mouse.get_pressed()[0]: #Left click
                    row, col = pygame.mouse.get_pos()[1]//GRID_WIDTH, pygame.mouse.get_pos()[0]//GRID_WIDTH
                    if self.grid:
                        outcome = self.grid[row][col].reveal()
                        if outcome == -1:
                            self.reveal_grid()
                    else:
                        self.create_board(row, col)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE: #Space bar pressed
                        row, col = pygame.mouse.get_pos()[1]//GRID_WIDTH, pygame.mouse.get_pos()[0]//GRID_WIDTH
                        if self.grid:
                            spot = self.grid[row][col]
                            #Toggle flag if not revealed
                            if not spot.revealed:
                                if spot.flag:
                                    spot.flag = False
                                else:
                                    spot.flag = True
                            #Reveal neighbors if all mines flagged and revealed
                            elif spot.revealed and spot.all_flags():
                                for n in spot.neighbors:
                                    if not n.flag:
                                        outcome = n.reveal()
                                        if outcome == -1:
                                            self.reveal_grid()
                #DRAW
                self.draw(WIN)
        
    def draw(self, WIN):
        #Fill background
        WIN.fill(GREY)
        #Draw all spots
        if self.grid:
            for row in self.grid:
                for spot in row:
                    spot.draw(WIN)
        #Draw gridlines
        for i in range(ROWS):
            pygame.draw.line(WIN, BLACK, (0, i * GRID_WIDTH), (WIDTH, i * GRID_WIDTH))
        for i in range(COLS):
            pygame.draw.line(WIN, BLACK, (i * GRID_WIDTH, 0), (i * GRID_WIDTH, WIDTH))
        #Update display
        pygame.display.update()
        

    def reveal_grid(self):
        for row in self.grid:
            for spot in row:
                spot.revealed = True

    def create_board(self, mouse_row, mouse_col, rows=ROWS, cols=COLS):
        #Create 2d array of Spots
        self.grid = []
        for i in range(rows):
            temp = []
            for j in range(cols):
                temp.append(Spot(i, j, GRID_WIDTH))
            self.grid.append(temp)

        #Create Mines out of spots
        n = 0
        while n < NUM_MINES:
            i,j = random.randint(0,rows-1), random.randint(0,cols-1)
            dist = int(((mouse_row-i)**2 + (mouse_col-j)**2)**(1/2))
            if not self.grid[i][j].mine and dist > 2:
                n += 1
                self.grid[i][j].mine = True

        #Update neighbors of each spot and give number of mines around
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid)

game = Game()
game.run()
