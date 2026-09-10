
Files = ["A", "B", "C", "D", "E", "F", "G", "H"]
Ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
increment = 75
initial_x = 340
initial_y = 60
padding = 10
def determine_chess_coordinates(x, y):
    file_index = (x - initial_x) // increment
    rank_index = (y - initial_y) // increment
    #print("file_value: ", Files[file_index], "rank_value: ", Ranks[rank_index])
    return Files[file_index], Ranks[rank_index]

def determine_square_coordinates(file, rank):
    file_index = Files.index(file)
    rank_index = Ranks.index(rank)
    x = initial_x + (file_index * increment)
    y = initial_y + (rank_index * increment)
    return x, y

def determine_piece_in_square(x, y, player_pieces):
    for piece in player_pieces:
        piece_x, piece_y = determine_square_coordinates(piece.file, piece.rank)
        # print(piece_x, piece_y)
        if piece_x <= x <= piece_x + increment and piece_y <= y <= piece_y + increment:
            # print(f"Found piece {piece.name} at ({piece.file}{piece.rank})")
            return piece
    return None

def move_piece_to_square(piece, file, rank, font):
    piece.rank = rank
    piece.file = file
    piece.render_piece()