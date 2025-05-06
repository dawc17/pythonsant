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

ant_speed = 100  
time_since_last_move = 0

running = True
step = 0
while running:
    dt = clock.tick(60) / 1000.0  
    time_since_last_move += dt

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ant_speed += 100
            elif event.key == pygame.K_DOWN and ant_speed > 1:
                ant_speed -= 100
            print(f"Ant speed: {ant_speed} steps per second")

    update_interval = 1.0 / ant_speed 
    
    while time_since_last_move >= update_interval:
        if not (0 <= ant.xPos < gridX and 0 <= ant.yPos < gridY):
            ant.xPos = ant.xPos % gridX
            ant.yPos = ant.yPos % gridY
            print(f"Ant wrapped around to position ({ant.xPos}, {ant.yPos})")

        # ant logic
        currentColor = grid[ant.yPos][ant.xPos]

        if currentColor == 0:
            ant.turnRight()
            grid[ant.yPos][ant.xPos] = 1
        else:
            ant.turnLeft()
            grid[ant.yPos][ant.xPos] = 0

        ant.moveForward()
        step += 1
        time_since_last_move -= update_interval

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
