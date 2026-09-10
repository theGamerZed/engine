from position import determine_chess_coordinates, determine_piece_in_square, determine_square_coordinates, move_piece_to_square,Files
import pygame
import pieces

# Global variables
pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont("Noto Sans Symbols 2", 50 )
clock = pygame.time.Clock()
board_width = 600
center_x = screen.get_width() / 2
center_y = screen.get_height() / 2
player_1_color = (255, 255, 255)
player_2_color = (0, 0, 0)
player_1 = 1
player_2 = 2
increment = 75
initial_x = 340
initial_y = 60
running = True
clicked_square = {}
def initial_player_pieces(color,player):
    all_player_pieces = []
    if player == 2:
        rook_1 = pieces.chess_piece("black_Rook", "♜", (color), player, font, screen, "A", "8")
        all_player_pieces.append(rook_1)
        knight_1 = pieces.chess_piece("black_Knight", "♞", (color), player, font, screen, "B", "8")
        all_player_pieces.append(knight_1)
        bishop_1 = pieces.chess_piece("black_Bishop", "♝", (color), player, font, screen, "C", "8")
        all_player_pieces.append(bishop_1)
        queen = pieces.chess_piece("black_Queen", "♛", (color), player, font, screen, "D", "8")
        all_player_pieces.append(queen)
        king = pieces.chess_piece("black_King", "♚", (color), player, font, screen, "E", "8")
        all_player_pieces.append(king)
        bishop_2 = pieces.chess_piece("black_Bishop", "♝", (color), player, font, screen, "F", "8")
        all_player_pieces.append(bishop_2)
        knight_2 = pieces.chess_piece("black_Knight", "♞", (color), player, font, screen, "G", "8")
        all_player_pieces.append(knight_2)
        rook_2 = pieces.chess_piece("black_Rook", "♜", (color), player, font, screen, "H", "8")
        all_player_pieces.append(rook_2)
        rook_1.render_piece()
        knight_1.render_piece()
        bishop_1.render_piece()
        queen.render_piece()
        king.render_piece()
        bishop_2.render_piece()
        knight_2.render_piece()
        rook_2.render_piece()
        for file in range(Files.index("A"), Files.index("H")+1): #+1 to include the last file "H"
            pawn = pieces.chess_piece("black_Pawn", "♟", (color), player, font, screen, Files[file], "7")
            pawn.render_piece()
            all_player_pieces.append(pawn)
    elif player == 1:
        rook_1 = pieces.chess_piece("white_Rook", "♜", (color), player, font, screen, "A", "1")
        all_player_pieces.append(rook_1)
        knight_1 = pieces.chess_piece("white_Knight", "♞", (color), player, font, screen, "B", "1")
        all_player_pieces.append(knight_1)
        bishop_1 = pieces.chess_piece("white_Bishop", "♝", (color), player, font, screen, "C", "1")
        all_player_pieces.append(bishop_1)
        queen = pieces.chess_piece("white_Queen", "♛", (color), player, font, screen, "D", "1")
        all_player_pieces.append(queen)
        king = pieces.chess_piece("white_King", "♚", (color), player, font, screen, "E", "1")
        all_player_pieces.append(king)
        bishop_2 = pieces.chess_piece("white_Bishop", "♝", (color), player, font, screen, "F", "1")
        all_player_pieces.append(bishop_2)
        knight_2 = pieces.chess_piece("white_Knight", "♞", (color), player, font, screen, "G", "1")
        all_player_pieces.append(knight_2)
        rook_2 = pieces.chess_piece("white_Rook", "♜", (color), player, font, screen, "H", "1")
        all_player_pieces.append(rook_2)
        rook_1.render_piece()
        knight_1.render_piece()
        bishop_1.render_piece()
        queen.render_piece()
        king.render_piece()
        bishop_2.render_piece()
        knight_2.render_piece()
        rook_2.render_piece()
        for file in range(Files.index("A"), Files.index("H")+1): #+1 to include the last file "H"
            pawn = pieces.chess_piece("white_Pawn", "♟", (color), player, font, screen, Files[file], "2")
            pawn.render_piece()
            all_player_pieces.append(pawn)

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
            elif x <= clicked_square["x"] <= x+increment and y <= clicked_square["y"] <= y+increment: # check if current square is clicked ...
                pygame.draw.rect(screen, "green", pygame.Rect(x, y, increment, increment),3)
                current_file , current_rank = determine_chess_coordinates(clicked_square["x"], clicked_square["y"])
                chess_piece = determine_piece_in_square(clicked_square["x"], clicked_square["y"], player_1_pieces + player_2_pieces)
                print(f"current_file: {current_file}, current_rank: {current_rank}, chess_piece: {chess_piece.name if chess_piece else 'None'}")
                file, rank = ["E", "5"] # Example target square, replace with actual logic to determine target square
                move_piece_to_square(chess_piece, file, rank, font) if chess_piece else None
    player_1_pieces = initial_player_pieces(player_1_color, player_1)
    player_2_pieces = initial_player_pieces(player_2_color, player_2)

        # Pieces
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(2)  # limits FPS to 60