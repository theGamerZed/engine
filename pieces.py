import pygame
from player import Player
from constants import Files,Ranks,increment,initial_x,initial_y
class ChessPiece:
    def __init__(self, type ,name, ASCII_value, player:Player,file, rank,selected = False):
        self.name = name
        self.ASCII_value = ASCII_value
        self.player = player
        self.color = player.color
        self.player_number = player.player_number
        self.rank = rank
        self.file = file
        self.type = type
        self.selected = selected
        self.special = False
        self.valid_moves = []
        self.attacked_squares = []
        self.pseudo_legal_moves = []
        self.move_history = []

        if self.type == "king":
            self.safe_squares = []
     
    def render_piece(self,font,screen):
        piece = font.render(self.ASCII_value, True, self.color)
        coordinates = determine_square_coordinates(self.file, self.rank)
        screen.blit(piece, coordinates)

def determine_square_coordinates(file, rank):
    file_index = Files.index(file)
    rank_index = Ranks.index(rank)
    x = initial_x + (file_index * increment)
    y = initial_y + (rank_index * increment)
    return x, y