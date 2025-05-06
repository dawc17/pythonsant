import numpy as np
import pygame
import sys

gridX = int(input("How many pixels wide should the grid be? "))
gridY = int(input("How many pixels tall should the grid be? "))
cell_size = 10

pygame.init()
window = pygame.display.set_mode((gridX * cell_size, gridY * cell_size))
pygame.display.set_caption("Langton's Ant")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

grid = np.zeros((gridY, gridX), dtype=int)

class Ant:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.direction = 0 # 0=north, 1=east, 2=south, 3=west
    
    def turnLeft(self):
        self.direction = (self.direction - 1) % 4

    def turnRight(self):
        self.direction = (self.direction + 1) % 4

    def moveForward(self):
        if self.direction == 0:
            self.yPos -= 1
        elif self.direction == 1:
            self.xPos += 1
        elif self.direction == 2:
            self.yPos += 1
        elif self.direction == 3:
            self.xPos -= 1

startX = gridX // 2
startY = gridY // 2

ant = Ant(startX, startY)

running = True
step = 0
while running:
    clock.tick(1000000)  # Limit to 60 frames per second

    # Event handler to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # Safety check: stop if ant goes off grid
    if not (0 <= ant.xPos < gridX and 0 <= ant.yPos < gridY):
        print("Ant went out of bounds.")

    # Langton's ant logic
    currentColor = grid[ant.yPos][ant.xPos]

    if currentColor == 0:
        ant.turnRight()
        grid[ant.yPos][ant.xPos] = 1
    else:
        ant.turnLeft()
        grid[ant.yPos][ant.xPos] = 0

    ant.moveForward()
    step += 1

    # --- Drawing the grid ---
    for y in range(gridY):
        for x in range(gridX):
            color = BLACK if grid[y][x] == 0 else WHITE
            pygame.draw.rect(window, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    # Draw the ant (on top)
    if 0 <= ant.xPos < gridX and 0 <= ant.yPos < gridY:
        pygame.draw.rect(window, RED, (ant.xPos * cell_size, ant.yPos * cell_size, cell_size, cell_size))

    pygame.display.flip()

pygame.quit()
sys.exit()
