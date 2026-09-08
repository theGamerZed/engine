import pygame
import pieces
from cmath import rect
from turtle import color

# Global variables
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
board_width = 600
center_x = screen.get_width() / 2
center_y = screen.get_height() / 2
padding = 5
increment = 75
initial_x = 340
initial_y = 60
running = True
clicked_square = {}
font = pygame.font.SysFont("Noto Sans Symbols 2", 50 )
def initial_player_pieces(color,player):
    if player == 1:
        x = initial_x 
        pawn_rank  = initial_y + increment
        piece_rank = initial_y

        rook_1 = pieces.chess_piece("White_Rook", "♜", (color), player, font)
        knight_1 = pieces.chess_piece("White_Knight", "♞", (color), player, font)
        bishop_1 = pieces.chess_piece("White_Bishop", "♝", (color), player, font)
        queen = pieces.chess_piece("White_Queen", "♛", (color), player, font)
        king = pieces.chess_piece("White_King", "♚", (color), player, font)
        bishop_2 = pieces.chess_piece("White_Bishop", "♝", (color), player, font)
        knight_2 = pieces.chess_piece("White_Knight", "♞", (color), player, font)
        rook_2 = pieces.chess_piece("White_Rook", "♜", (color), player, font)
        screen.blit(rook_1.render_piece(font), (x + 10, piece_rank))
        screen.blit(knight_1.render_piece(font), (x + 85, piece_rank))
        screen.blit(bishop_1.render_piece(font), (x + 160, piece_rank))
        screen.blit(queen.render_piece(font), (x + 235, piece_rank))
        screen.blit(king.render_piece(font), (x + 310, piece_rank))
        screen.blit(bishop_2.render_piece(font), (x + 385, piece_rank))
        screen.blit(knight_2.render_piece(font), (x + 460, piece_rank))
        screen.blit(rook_2.render_piece(font), (x + 535, piece_rank))
    elif player == 2:
        x = initial_x
        pawn_rank  = board_width - increment
        piece_rank = board_width

        rook_1 = pieces.chess_piece("Black_Rook", "♜", (color), player, font)
        knight_1 = pieces.chess_piece("Black_Knight", "♞", (color), player, font)
        bishop_1 = pieces.chess_piece("Black_Bishop", "♝", (color), player, font)
        queen = pieces.chess_piece("Black_Queen", "♛", (color), player, font)
        king = pieces.chess_piece("Black_King", "♚", (color), player, font)
        bishop_2 = pieces.chess_piece("Black_Bishop", "♝", (color), player, font)
        knight_2 = pieces.chess_piece("Black_Knight", "♞", (color), player, font)
        rook_2 = pieces.chess_piece("Black_Rook", "♜", (color), player, font)
        screen.blit(rook_1.render_piece(font), (x + 10, piece_rank))
        screen.blit(knight_1.render_piece(font), (x + 85, piece_rank))
        screen.blit(bishop_1.render_piece(font), (x + 160, piece_rank))
        screen.blit(queen.render_piece(font), (x + 235, piece_rank))
        screen.blit(king.render_piece(font), (x + 310, piece_rank))
        screen.blit(bishop_2.render_piece(font), (x + 385, piece_rank))
        screen.blit(knight_2.render_piece(font), (x + 460, piece_rank))
        screen.blit(rook_2.render_piece(font), (x + 535, piece_rank))

    
    for x in range(initial_x, initial_x + board_width, increment):
        pawn = pieces.chess_piece("Black_Pawn", "♟", (color), player, font)
        screen.blit(pawn.render_piece(font), (x + 10, pawn_rank))

    
    
    return None

  
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                clicked_square = {"x": event.pos[0], "y": event.pos[1]}
                #print(clicked_square["x"])
                #print(pygame.font.get_fonts())

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((102,51, 0))

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(center_x - 300, center_y - 300, board_width, board_width))

    for x in range(initial_x, initial_x + board_width, increment):
        for y in range(initial_y, initial_y + board_width, increment):
            if ((x-initial_x) +(y-initial_y)) % (increment * 2) == 0: #check if the sum of the x and y offsets is even to determine the color of the square
                color = (51, 104, 75)
            else:
                color = (190, 202, 193)
            pygame.draw.rect(screen, color, pygame.Rect(x, y, increment, increment))
            initial_player_pieces((0, 0, 0), 1)
            initial_player_pieces((255, 255, 255), 2)

            if not clicked_square:
                a = 0
            elif (x <= clicked_square["x"] <= x+increment and y <= clicked_square["y"] <= y+increment ): # check if current square is clicked ... 
                pygame.draw.rect(screen, "green", pygame.Rect(x, y, increment, increment),3)
                
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
