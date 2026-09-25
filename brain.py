from position import determine_chess_coordinates, determine_piece_in_square,move_to_selected_square,determine_attacked_squares
from position import Files,Ranks
from box import BOX
from player import Player,player_2,player_1
import pygame
import pieces
# helper functions
all_player_pieces = []
def initialize_player_pieces(player: Player):
    if player.player_number == 2:
        rook_1 = pieces.chess_piece("rook","black_Rook_1", "♜", player_2, "A", "8")
        all_player_pieces.append(rook_1)
        knight_1 = pieces.chess_piece("knight","black_Knight_1", "♞", player_2, "B", "8")
        all_player_pieces.append(knight_1)
        bishop_1 = pieces.chess_piece("bishop","black_Bishop_1", "♝", player_2, "C", "8")
        all_player_pieces.append(bishop_1)
        black_queen = pieces.chess_piece("queen","black_Queen", "♛", player_2, "D", "8")
        all_player_pieces.append(black_queen)
        black_king = pieces.chess_piece("king","black_King", "♚", player_2, "E", "8")
        all_player_pieces.append(black_king)
        bishop_2 = pieces.chess_piece("bishop","black_Bishop_2", "♝", player_2, "F", "8")
        all_player_pieces.append(bishop_2)
        knight_2 = pieces.chess_piece("knight", "black_Knight_2", "♞", player_2, "G", "8")
        all_player_pieces.append(knight_2)
        rook_2 = pieces.chess_piece("rook","black_Rook_2", "♜", player_2, "H", "8")
        all_player_pieces.append(rook_2)
        for file in range(Files.index("A"), Files.index("H")+1): #+1 to include the last file "H"
            pawn = pieces.chess_piece("pawn","black_Pawn", "♟", player_2, Files[file], "7")
            all_player_pieces.append(pawn)
        return black_king
    elif player.player_number == 1:
        rook_1 = pieces.chess_piece("rook","white_Rook_1", "♜", player_1, "A", "1")
        all_player_pieces.append(rook_1)
        knight_1 = pieces.chess_piece("knight","white_Knight_1", "♞", player_1, "B", "1")
        all_player_pieces.append(knight_1)
        bishop_1 = pieces.chess_piece("bishop", "white_Bishop_1", "♝", player_1, "C", "1")
        all_player_pieces.append(bishop_1)
        white_queen = pieces.chess_piece("queen", "white_Queen", "♛", player_1, "D", "1")
        all_player_pieces.append(white_queen)
        white_king = pieces.chess_piece("king", "white_King", "♚", player_1, "E", "1")
        all_player_pieces.append(white_king)
        bishop_2 = pieces.chess_piece("bishop", "white_Bishop_2", "♝", player_1, "F", "1")
        all_player_pieces.append(bishop_2)
        knight_2 = pieces.chess_piece("knight", "white_Knight_2", "♞", player_1, "G", "1")
        all_player_pieces.append(knight_2)
        rook_2 = pieces.chess_piece("rook", "white_Rook_2", "♜", player_1, "H", "1")
        all_player_pieces.append(rook_2)
        for file in range(Files.index("A"), Files.index("H")+1): #+1 to include the last file "H"
            pawn = pieces.chess_piece("pawn", "white_Pawn", "♟", player_1, Files[file], "2")
            all_player_pieces.append(pawn)

        return white_king
white_king = initialize_player_pieces(player_1)
black_king = initialize_player_pieces(player_2)
#all_player_pieces.append(white_king)
#all_player_pieces.append(black_king)
# Global variables
screen = pygame.display.set_mode((1280, 720))
pygame.font.init()
font = pygame.font.SysFont("Noto Sans Symbols 2", 50 )
initial_selected_piece = ["E", "2"]  # Example initial selected piece, replace with actual logic to determine selected piece
selected_square = BOX(initial_selected_piece[0], initial_selected_piece[1], (0,250,0))
selected_square.current_piece = determine_piece_in_square(initial_selected_piece[0],initial_selected_piece[1],all_player_pieces)
if selected_square.current_piece is not None:
    selected_square.current_piece.selected = True
else:
    print("No piece found on this square")
clock = pygame.time.Clock()
board_width = 600
center_x = screen.get_width() / 2
center_y = screen.get_height() / 2
increment = 75
initial_x = 340
initial_y = 60
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                current_file, current_rank = determine_chess_coordinates(event.pos[0], event.pos[1])
                if current_file is not None and current_rank is not None:
                    selected_square.file = Files[Files.index(current_file)]
                    selected_square.rank = Ranks[Ranks.index(current_rank)]
                    selected_piece = determine_piece_in_square(current_file,current_rank,all_player_pieces)
                    if selected_piece is not None:
                        selected_piece.selected = True
                        selected_square.current_piece = selected_piece                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                selected_square.move_up()
            elif event.key == pygame.K_DOWN:
                    selected_square.move_down()
            elif event.key == pygame.K_LEFT:
                selected_square.move_left()
            elif event.key == pygame.K_RIGHT:
                selected_square.move_right()
            elif event.key == pygame.K_RETURN:
                move_to_selected_square(selected_square.current_piece,selected_square,all_player_pieces)
                
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
            pygame.draw.rect(screen,color,pygame.Rect(x, y, increment, increment))

    selected_square.render_box(screen) # render the selected square once on top of the board

    for piece in all_player_pieces:
            piece.render_piece(font, screen)
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(2)  # limits FPS to 60