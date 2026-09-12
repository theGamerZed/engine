from position import determine_chess_coordinates, determine_piece_in_square, determine_square_coordinates, move_piece_to_square,move_to_selected_square
from position import Files,Ranks
from box import BOX
import pygame
import pieces
#initialise player pieces
all_player_pieces = []
def initial_player_pieces(color,player):
    if player == 2:
        rook_1 = pieces.chess_piece("black_Rook", "♜", (color), player, "A", "8")
        all_player_pieces.append(rook_1)
        knight_1 = pieces.chess_piece("black_Knight", "♞", (color), player, "B", "8")
        all_player_pieces.append(knight_1)
        bishop_1 = pieces.chess_piece("black_Bishop", "♝", (color), player, "C", "8")
        all_player_pieces.append(bishop_1)
        queen = pieces.chess_piece("black_Queen", "♛", (color), player, "D", "8")
        all_player_pieces.append(queen)
        king = pieces.chess_piece("black_King", "♚", (color), player, "E", "8")
        all_player_pieces.append(king)
        bishop_2 = pieces.chess_piece("black_Bishop", "♝", (color), player, "F", "8")
        all_player_pieces.append(bishop_2)
        knight_2 = pieces.chess_piece("black_Knight", "♞", (color), player, "G", "8")
        all_player_pieces.append(knight_2)
        rook_2 = pieces.chess_piece("black_Rook", "♜", (color), player, "H", "8")
        all_player_pieces.append(rook_2)
        for file in range(Files.index("A"), Files.index("H")+1): #+1 to include the last file "H"
            pawn = pieces.chess_piece("black_Pawn", "♟", (color), player, Files[file], "7")
            all_player_pieces.append(pawn)
    elif player == 1:
        rook_1 = pieces.chess_piece("white_Rook", "♜", (color), player, "A", "1")
        all_player_pieces.append(rook_1)
        knight_1 = pieces.chess_piece("white_Knight", "♞", (color), player, "B", "1")
        all_player_pieces.append(knight_1)
        bishop_1 = pieces.chess_piece("white_Bishop", "♝", (color), player, "C", "1")
        all_player_pieces.append(bishop_1)
        queen = pieces.chess_piece("white_Queen", "♛", (color), player, "D", "1")
        all_player_pieces.append(queen)
        king = pieces.chess_piece("white_King", "♚", (color), player, "E", "1")
        all_player_pieces.append(king)
        bishop_2 = pieces.chess_piece("white_Bishop", "♝", (color), player, "F", "1")
        all_player_pieces.append(bishop_2)
        knight_2 = pieces.chess_piece("white_Knight", "♞", (color), player, "G", "1")
        all_player_pieces.append(knight_2)
        rook_2 = pieces.chess_piece("white_Rook", "♜", (color), player, "H", "1")
        all_player_pieces.append(rook_2)
        for file in range(Files.index("A"), Files.index("H")+1): #+1 to include the last file "H"
            pawn = pieces.chess_piece("white_Pawn", "♟", (color), player, Files[file], "2")
            all_player_pieces.append(pawn)

    return all_player_pieces
player_1_params = ((255, 255, 255), 1) #white pieces, player 1
player_2_params = ((0, 0, 0), 2)       #black pieces, player 2
player_1_pieces = initial_player_pieces(player_1_params[0], player_1_params[1])
player_2_pieces = initial_player_pieces(player_2_params[0], player_2_params[1])
# Global variables
screen = pygame.display.set_mode((1280, 720))
pygame.font.init()
font = pygame.font.SysFont("Noto Sans Symbols 2", 50 )
initial_selected_piece = ["E", "2"]  # Example initial selected piece, replace with actual logic to determine selected piece
selected_square = BOX(initial_selected_piece[0], initial_selected_piece[1], (0,250,0))
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
                    selected_piece = determine_piece_in_square(event.pos[0],event.pos[1],all_player_pieces)
                    if selected_piece is not None:
                        selected_piece.selected = True
                        selected_square.current_piece = selected_piece
                        #move_piece_to_square(selected_piece,"E", "5",all_player_pieces,selected_piece.selected)
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
                move_to_selected_square(selected_square,all_player_pieces)
                # for piece in all_player_pieces:
                #     if piece.name == "white_king":
                #         move_piece_to_square(piece,"E","7",all_player_pieces,piece.selected)

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

    for piece in player_1_pieces + player_2_pieces:
            piece.render_piece(font, screen)
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(2)  # limits FPS to 60