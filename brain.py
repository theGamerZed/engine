from position import determine_square
import pygame
import pieces
from cmath import rect
from turtle import color

# Global variables
pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont("Noto Sans Symbols 2", 50 )
clock = pygame.time.Clock()
board_width = 600
center_x = screen.get_width() / 2
center_y = screen.get_height() / 2
player_1_color = (0, 0, 0)
player_2_color = (255, 255, 255)
player_1 = 1
player_2 = 2
increment = 75
initial_x = 340
initial_y = 60
running = True
clicked_square = {}
def initial_player_pieces(color,player):
    all_player_pieces = []
    if player == 1:
        piece_file = initial_x 
        pawn_rank  = initial_y + increment
        piece_rank = initial_y

        rook_1 = pieces.chess_piece("White_Rook", "♜", (color), player, font,screen, x=piece_file + 10, y=initial_y)
        all_player_pieces.append(rook_1)
        knight_1 = pieces.chess_piece("White_Knight", "♞", (color), player, font,screen, x=piece_file + 85, y=initial_y)
        all_player_pieces.append(knight_1)
        bishop_1 = pieces.chess_piece("White_Bishop", "♝", (color), player, font,screen, x=piece_file + 160, y=initial_y)
        all_player_pieces.append(bishop_1)
        queen = pieces.chess_piece("White_Queen", "♛", (color), player, font,screen, x=piece_file + 235, y=initial_y)
        all_player_pieces.append(queen)
        king = pieces.chess_piece("White_King", "♚", (color), player, font,screen, x=piece_file + 310, y=initial_y)
        all_player_pieces.append(king)
        bishop_2 = pieces.chess_piece("White_Bishop", "♝", (color), player, font,screen, x=piece_file + 385, y=initial_y)
        all_player_pieces.append(bishop_2)
        knight_2 = pieces.chess_piece("White_Knight", "♞", (color), player, font,screen, x=piece_file + 460, y=initial_y)
        all_player_pieces.append(knight_2)
        rook_2 = pieces.chess_piece("White_Rook", "♜", (color), player, font,screen, x=piece_file + 535, y=initial_y)
        all_player_pieces.append(rook_2)
        rook_1.render_piece(font)
        knight_1.render_piece(font)
        bishop_1.render_piece(font)
        queen.render_piece(font)
        king.render_piece(font)
        bishop_2.render_piece(font)
        knight_2.render_piece(font)
        rook_2.render_piece(font)
        for x in range(initial_x, initial_x + board_width, increment):
            pawn = pieces.chess_piece("Black_Pawn", "♟", (color), player, font,screen, x=x + 10, y=pawn_rank)
            pawn.render_piece(font)
            all_player_pieces.append(pawn)
    elif player == 2:
        piece_file = initial_x
        pawn_rank  = board_width - increment
        piece_rank = board_width

        rook_1 = pieces.chess_piece("Black_Rook", "♜", (color), player, font,screen, x=piece_file + 10, y=piece_rank)
        all_player_pieces.append(rook_1)
        knight_1 = pieces.chess_piece("Black_Knight", "♞", (color), player, font,screen, x=piece_file + 85, y=piece_rank)
        all_player_pieces.append(knight_1)
        bishop_1 = pieces.chess_piece("Black_Bishop", "♝", (color), player, font,screen, x=piece_file + 160, y=piece_rank)
        all_player_pieces.append(bishop_1)
        queen = pieces.chess_piece("Black_Queen", "♛", (color), player, font,screen, x=piece_file + 235, y=piece_rank)
        all_player_pieces.append(queen)
        king = pieces.chess_piece("Black_King", "♚", (color), player, font,screen, x=piece_file + 310, y=piece_rank)
        all_player_pieces.append(king)
        bishop_2 = pieces.chess_piece("Black_Bishop", "♝", (color), player, font,screen, x=piece_file + 385, y=piece_rank)
        all_player_pieces.append(bishop_2)
        knight_2 = pieces.chess_piece("Black_Knight", "♞", (color), player, font,screen, x=piece_file + 460, y=piece_rank)
        all_player_pieces.append(knight_2)
        rook_2 = pieces.chess_piece("Black_Rook", "♜", (color), player, font,screen, x=piece_file + 535, y=piece_rank)
        all_player_pieces.append(rook_2)
        rook_1.render_piece(font)
        knight_1.render_piece(font)
        bishop_1.render_piece(font)
        queen.render_piece(font)
        king.render_piece(font)
        bishop_2.render_piece(font)
        knight_2.render_piece(font)
        rook_2.render_piece(font)
        for x in range(initial_x, initial_x + board_width, increment):
                pawn = pieces.chess_piece("Black_Pawn", "♟", (color), player, font,screen, x=x + 10, y=pawn_rank)
                pawn.render_piece(font)

    return all_player_pieces

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                clicked_square = {"x": event.pos[0], "y": event.pos[1]}

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((102,51, 0))

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(center_x - 300, center_y - 300, board_width, board_width))

    for x in range(initial_x, initial_x + board_width, increment):
        for y in range(initial_y, initial_y + board_width, increment):

            if ((x-initial_x) + (y-initial_y)) % (increment * 2) == 0:
                color = (51, 104, 75)
            else:
                color = (190, 202, 193)

            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(x, y, increment, increment)
            )

            if not clicked_square: 
                a = 0 
            elif (x <= clicked_square["x"] <= x+increment and y <= clicked_square["y"] <= y+increment ): # check if current square is clicked ... 
                pygame.draw.rect(screen, "green", pygame.Rect(x, y, increment, increment),3)
                normal_x = clicked_square["x"] - initial_x #normalize the clicked square coordinates to the board's coordinate system
                normal_y = clicked_square["y"] - initial_y #same here!!!!
                #print(normal_x, normal_y, clicked_square["y"])
                determine_square(normal_x, normal_y)
        # Pieces
    player_1_pieces = initial_player_pieces(player_1_color, player_1)
    player_2_pieces = initial_player_pieces(player_2_color, player_2)

    # print(player_1_pieces[0].name)
    # print(player_2_pieces)
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(10)  # limits FPS to 60