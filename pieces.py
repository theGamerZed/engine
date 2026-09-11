import pygame

from position import determine_square_coordinates
class chess_piece:
    def __init__(self, name, ASCII_value, color, player,file, rank):
        self.name = name
        self.ASCII_value = ASCII_value
        self.color = color
        self.player = player
        self.rank = rank
        self.file = file

    def render_piece(self,font,screen):
        piece = font.render(self.ASCII_value, True, self.color)
        coordinates = determine_square_coordinates(self.file, self.rank)
        screen.blit(piece, coordinates)

