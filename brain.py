# Example file showing a basic pygame "game loop"
import pygame
from cmath import rect
from turtle import color

class box:
    def __init__(self,name,id):
        self.name = name  
        self.id = id

    def identify(self):
        return f"{self.name} (ID: {self.id})"
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
board_width = 600
center_x = screen.get_width() / 2
center_y = screen.get_height() / 2
padding = 5
increment = 75
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                print(f"Left click at {event.pos}")

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((102,51, 0))

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(center_x - 300, center_y - 300, board_width, board_width))

    for x in range(340, 340 + board_width, increment):
        for y in range(60, 60 + board_width, increment):
            if ((x-340) +(y-60)) % (increment * 2) == 0: #check if the sum of the x and y offsets is even to determine the color of the square
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)
            pygame.draw.rect(screen, color, pygame.Rect(x, y, increment, increment))
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
