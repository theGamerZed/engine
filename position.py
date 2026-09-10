Files = ["A", "B", "C", "D", "E", "F", "G", "H"]
Ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
increment = 75
initial_x = 340
initial_y = 60
padding = 10
def determine_chess_coordinates(x, y):
    if not (initial_x <= x < initial_x + 8 * increment) or not (initial_y <= y < initial_y + 8 * increment):
        return None, None
    file_index = (x - initial_x) // increment
    rank_index = (y - initial_y) // increment
    return Files[file_index], Ranks[rank_index]

def determine_square_coordinates(file, rank):
    file_index = Files.index(file)
    rank_index = Ranks.index(rank)
    x = initial_x + (file_index * increment)
    y = initial_y + (rank_index * increment)
    return x, y

def determine_piece_in_square(x, y, player_pieces):
    coords = determine_chess_coordinates(x, y)
    for piece in player_pieces:
        if piece.file == coords[0] and piece.rank == coords[1]:
            return piece
    return None

def move_piece_to_square(piece, file, rank, all_pieces):
    x, y = determine_square_coordinates(file, rank)
    if is_valid_square(x, y, all_pieces):
        piece.rank = rank
        piece.file = file
    else:
        print(f"Invalid move for {piece.name} to square {file}{rank}.")

def is_valid_square(x, y, pieces):
    if not determine_piece_in_square(x, y, pieces):
        return True
    # elif determine_piece_in_square(x, y, pieces).player != piece.player:
    #     return True
    return False