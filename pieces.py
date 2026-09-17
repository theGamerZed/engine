import pygame

from position import determine_square_coordinates
class chess_piece:
    def __init__(self, type ,name, ASCII_value, color, player,file, rank,selected = False):
        self.name = name
        self.ASCII_value = ASCII_value
        self.color = color
        self.player = player
        self.rank = rank
        self.file = file
        self.type = type
        self.selected = selected
        self.special = False
        if self.type == "king" or self.type == "queen" :
            self.forward = True
            self.sideward = True
            self.diagonal = True
        elif self.type == "bishop":
            self.forward = False
            self.sideward = False
            self.diagonal = True
        elif self.type == "knight":
            self.special = True
            self.forward = False
            self.sideward = False
            self.diagonal = False
        elif self.type == "pawn":
            self.forward = True
            self.sideward = False
            self.diagonal = False
        elif self.type == "rook":
            self.forward = True
            self.sideward = True
            self.diagonal = False
        

    def render_piece(self,font,screen):
        piece = font.render(self.ASCII_value, True, self.color)
        coordinates = determine_square_coordinates(self.file, self.rank)
        screen.blit(piece, coordinates)
