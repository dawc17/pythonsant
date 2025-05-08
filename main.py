import numpy as np
import pygame
import sys
import random

gridX = int(input("How many pixels wide should the grid be? "))
gridY = int(input("How many pixels tall should the grid be? "))
cell_size = 10
button_panel_height = 60

pygame.init()
window_height = gridY * cell_size + button_panel_height
window = pygame.display.set_mode((gridX * cell_size, window_height))
pygame.display.set_caption("Langton's Ant Extended")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 200)
DARK_BLUE = (0, 0, 150)
ORANGE = (255, 165, 0)
DARK_ORANGE = (200, 100, 0)
GRAY = (200, 200, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)

grid = np.zeros((gridY, gridX), dtype=int)
button_font = pygame.font.Font(None, 28)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font, action=None, action_args=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.action = action
        self.action_args = action_args if action_args is not None else []
        self.is_hovered = False
        self.text_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered and self.action:
                self.action(*self.action_args)
    
    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

class Ant:
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.direction = random.randint(0, 3)
        self.randomize_ruleset()

    def randomize_ruleset(self):
        self.ruleset = {
            0: random.choice(['L', 'R']),
            1: random.choice(['L', 'R'])
        }

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
        
        self.xPos = self.xPos % gridX
        self.yPos = self.yPos % gridY

ants_list = []
paused = False

def add_new_ant():
    global ants_list
    if len(ants_list) < 10:
        new_x = random.randint(0, gridX - 1)
        new_y = random.randint(0, gridY - 1)
        new_ant = Ant(new_x, new_y)
        ants_list.append(new_ant)
        print(f"Added ant at ({new_x}, {new_y}) with rules {new_ant.ruleset}. Total ants: {len(ants_list)}")

def remove_ant_from_list():
    global ants_list
    if ants_list:
        removed_ant = ants_list.pop()
        print(f"Removed ant from ({removed_ant.xPos}, {removed_ant.yPos}). Total ants: {len(ants_list)}")

def toggle_pause():
    global paused
    paused = not paused
    pause_play_button.update_text("Play" if paused else "Pause")
    print(f"Simulation {'paused' if paused else 'resumed'}")

def randomize_all_ants_rulesets():
    global ants_list
    if not ants_list:
        print("No ants to randomize rules for.")
        return
    for ant in ants_list:
        ant.randomize_ruleset()
    print("Randomized rulesets for all active ants.")

add_new_ant()

button_y_pos = gridY * cell_size + (button_panel_height - 40) // 2
button_height = 40
button_width = 110
spacing = 15

pause_play_button = Button(
    spacing, button_y_pos, button_width, button_height,
    "Pause", GREEN, DARK_GREEN, button_font, toggle_pause
)
add_ant_button = Button(
    spacing * 2 + button_width, button_y_pos, button_width, button_height,
    "Add Ant", BLUE, DARK_BLUE, button_font, add_new_ant
)
remove_ant_button = Button(
    spacing * 3 + button_width * 2, button_y_pos, button_width + 20, button_height,
    "Remove Ant", RED, (200, 0, 0), button_font, remove_ant_from_list
)
randomize_rules_button = Button(
    spacing * 4 + button_width * 3 + 20, button_y_pos, button_width + 40, button_height,
    "Randomize Rules", ORANGE, DARK_ORANGE, button_font, randomize_all_ants_rulesets
)

buttons = [pause_play_button, add_ant_button, remove_ant_button, randomize_rules_button]

ant_speed = 10
time_since_last_move = 0

running = True
step = 0
while running:
    dt = clock.tick(60) / 1000.0
    if not paused:
        time_since_last_move += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ant_speed += 1
                if ant_speed > 100: ant_speed = 100
                print(f"Ant speed: {ant_speed} steps per second (approx)")
            elif event.key == pygame.K_DOWN:
                ant_speed -= 1
                if ant_speed < 1: ant_speed = 1
                print(f"Ant speed: {ant_speed} steps per second (approx)")
            elif event.key == pygame.K_SPACE:
                toggle_pause()
        
        for button in buttons:
            button.handle_event(event)
    
    if not running:
        break

    if not paused:
        update_interval = 1.0 / ant_speed if ant_speed > 0 else float('inf')
        
        while time_since_last_move >= update_interval and ants_list:
            for ant in ants_list:
                currentColor = grid[ant.yPos][ant.xPos]
                
                action_to_take = ant.ruleset.get(currentColor)

                if action_to_take == 'R':
                    ant.turnRight()
                elif action_to_take == 'L':
                    ant.turnLeft()

                if currentColor == 0:
                    grid[ant.yPos][ant.xPos] = 1
                else:
                    grid[ant.yPos][ant.xPos] = 0

                ant.moveForward()
            step += 1
            time_since_last_move -= update_interval
            if ant_speed == 0:
                break

    window.fill(BLACK)

    for y_idx in range(gridY):
        for x_idx in range(gridX):
            color = BLACK if grid[y_idx][x_idx] == 0 else WHITE
            pygame.draw.rect(window, color, (x_idx * cell_size, y_idx * cell_size, cell_size, cell_size))

    for ant_obj in ants_list:
        if 0 <= ant_obj.xPos < gridX and 0 <= ant_obj.yPos < gridY:
            pygame.draw.rect(window, RED, (ant_obj.xPos * cell_size, ant_obj.yPos * cell_size, cell_size, cell_size))

    pygame.draw.rect(window, GRAY, (0, gridY * cell_size, gridX * cell_size, button_panel_height))

    for button in buttons:
        button.draw(window)

    pygame.display.flip()

pygame.quit()
sys.exit()
