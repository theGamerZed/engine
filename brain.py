from position import determine_chess_coordinates, determine_piece_in_square,move_to_selected_square,determine_attacked_squares
from constants import Files,Ranks,increment,initial_x,initial_y
from box import Box
from player import Player,player_2,player_1
from pieces import ChessPiece as ChessPieces
import pygame
import time
# helper functions
all_player_pieces = []
def initialize_player_pieces(player: Player):
    if player.player_number == 2:
        rook_1 = ChessPieces("rook","black_Rook_1", "♜", player_2, "A", "8")
        all_player_pieces.append(rook_1)
        knight_1 = ChessPieces("knight","black_Knight_1", "♞", player_2, "B", "8")
        all_player_pieces.append(knight_1)
        bishop_1 = ChessPieces("bishop","black_Bishop_1", "♝", player_2, "C", "8")
        all_player_pieces.append(bishop_1)
        black_queen = ChessPieces("queen","black_Queen", "♛", player_2, "D", "8")
        all_player_pieces.append(black_queen)
        black_king = ChessPieces("king","black_King", "♚", player_2, "E", "8")
        all_player_pieces.append(black_king)
        bishop_2 = ChessPieces("bishop","black_Bishop_2", "♝", player_2, "F", "8")
        all_player_pieces.append(bishop_2)
        # knight_2 = ChessPieces("knight", "black_Knight_2", "♞", player_2, "G", "8")
        # all_player_pieces.append(knight_2)
        # rook_2 = ChessPieces("rook","black_Rook_2", "♜", player_2, "H", "8")
        # all_player_pieces.append(rook_2)
        # for file in range(Files.index("A"), Files.index("H")+1): #+1 to include the last file "H"
        #     pawn = ChessPieces("pawn","black_Pawn", "♟", player_2, Files[file], "7")
        #     all_player_pieces.append(pawn)
        # return None
    elif player.player_number == 1:
        rook_1 = ChessPieces("rook","white_Rook_1", "♜", player_1, "A", "1")
        all_player_pieces.append(rook_1)
        knight_1 = ChessPieces("knight","white_Knight_1", "♞", player_1, "B", "1")
        all_player_pieces.append(knight_1)
        bishop_1 = ChessPieces("bishop", "white_Bishop_1", "♝", player_1, "C", "1")
        all_player_pieces.append(bishop_1)
        white_queen = ChessPieces("queen", "white_Queen", "♛", player_1, "D", "1")
        all_player_pieces.append(white_queen)
        white_king = ChessPieces("king", "white_King", "♚", player_1, "E", "1")
        all_player_pieces.append(white_king)
        bishop_2 = ChessPieces("bishop", "white_Bishop_2", "♝", player_1, "F", "1")
        all_player_pieces.append(bishop_2)
        knight_2 = ChessPieces("knight", "white_Knight_2", "♞", player_1, "G", "1")
        all_player_pieces.append(knight_2)
        rook_2 = ChessPieces("rook", "white_Rook_2", "♜", player_1, "H", "1")
        all_player_pieces.append(rook_2)
        for file in range(Files.index("A"), Files.index("H")+1): #+1 to include the last file "H"
            pawn = ChessPieces("pawn", "white_Pawn", "♟", player_1, Files[file], "5")
            all_player_pieces.append(pawn)
        return None
    
initialize_player_pieces(player_1)
initialize_player_pieces(player_2)
# Global variables
screen = pygame.display.set_mode((1280, 720))
pygame.font.init()
font = pygame.font.SysFont("Noto Sans Symbols 2", 50 )
initial_selected_piece = ["E", "2"]  # initial selected piece 
selection_box = Box(initial_selected_piece[0], initial_selected_piece[1], (0,250,0))
selection_box.current_piece = determine_piece_in_square(initial_selected_piece[0],initial_selected_piece[1],all_player_pieces)

clock = pygame.time.Clock()
board_width = 600
center_x = screen.get_width() / 2
center_y = screen.get_height() / 2
running = True
last_click_time = 0
double_click_threshold = 0.9
selected_piece = None

# Double-click tracking variables
last_clicked_file = None
last_clicked_rank = None

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_file, current_rank = determine_chess_coordinates(event.pos[0], event.pos[1])
            if current_file is not None and current_rank is not None:
                selected_piece = determine_piece_in_square(current_file,current_rank,all_player_pieces)
            if event.button == 1:  # Left click
                current_time = time.perf_counter()
                diff = current_time - last_click_time
                
                # Check if this click is on a valid board square
                click_is_valid = current_file is not None and current_rank is not None

                if 0 < diff < double_click_threshold and click_is_valid:
                    print("Double click detected - moving piece")
                    # Double click: move the currently selected piece to this square
                    if selection_box.current_piece is not None:
                        selection_box.file = Files[Files.index(current_file)]
                        selection_box.rank = Ranks[Ranks.index(current_rank)]
                        if move_to_selected_square(selection_box.current_piece, selection_box, all_player_pieces):
                            selection_box.full = False
                    last_click_time = 0  # Reset after detecting double-click

                else:
                    print("Single click - selecting piece")
                    # Single click: select the piece at this square immediately
                    if click_is_valid:
                        last_click_time = current_time
                        last_clicked_file = current_file
                        last_clicked_rank = current_rank
                        selection_box.file = Files[Files.index(current_file)]
                        selection_box.rank = Ranks[Ranks.index(current_rank)]
                        if selected_piece is not None and not selection_box.full:
                            selection_box.current_piece = selected_piece   
                            selection_box.full = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                selection_box.move_up()
            elif event.key == pygame.K_DOWN:
                    selection_box.move_down()
            elif event.key == pygame.K_LEFT:
                selection_box.move_left()
            elif event.key == pygame.K_RIGHT:
                selection_box.move_right()
            elif event.key == pygame.K_RETURN:
                if selection_box.current_piece is not None:
                    move_to_selected_square( selection_box.current_piece, selection_box, all_player_pieces )
                
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

    selection_box.render_box(screen) # render the selected square once on top of the board

    for piece in all_player_pieces:
            piece.render_piece(font, screen)
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(2)  # limits FPS to 60