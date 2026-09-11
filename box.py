
import pygame
from position import Files, Ranks
from position import determine_square_coordinates
class BOX:
    def __init__(self, file:str , rank:str , color,):
        self.file = file
        self.rank = rank
        self.color = color
    def render_box(self, screen):
        coordinates = determine_square_coordinates(self.file, self.rank)
        pygame.draw.rect(screen, self.color, pygame.Rect(coordinates[0], coordinates[1], 75, 75),3)
    def move_up(self):
        current_rank_index = Ranks.index(self.rank)
        if current_rank_index - 1 < 0:
            print("out of bounds")
        else:
            self.rank = Ranks[current_rank_index - 1]
    def move_down(self):
        current_rank_index = Ranks.index(self.rank)
        if current_rank_index + 1 >= len(Ranks):
            print("out of bounds")
        else:
            self.rank = Ranks[current_rank_index + 1]
    def move_left(self):
            current_file_index = Files.index(self.file)
            if current_file_index - 1 < 0:
                print("out of bounds")
            else:
                self.file = Files[current_file_index - 1]
    def move_right(self):
        current_file_index = Files.index(self.file)
        if current_file_index + 1 >= len(Files):
            print("out of bounds")
        else:
            self.file = Files[current_file_index + 1]
