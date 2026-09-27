import pygame
from player import Player
Files = ["A", "B", "C", "D", "E", "F", "G", "H"]
Ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
increment = 75
initial_x = 340
initial_y = 60
padding = 10
class chess_piece:
    def __init__(self, type ,name, ASCII_value, Player:Player,file, rank,selected = False):
        self.name = name
        self.ASCII_value = ASCII_value
        self.player = Player
        self.color = Player.color
        self.player_number = Player.player_number
        self.rank = rank
        self.file = file
        self.type = type
        self.selected = selected
        self.special = False
        self.valid_moves = []
        self.attacked_squares = []
        self.pseudo_legal_moves = []
     
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