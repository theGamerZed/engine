Files = ["A", "B", "C", "D", "E", "F", "G", "H"]
Ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
increment = 75
initial_x = 340
initial_y = 60

def determine_square(x, y):
    file_index = (x//increment) 
    rank_index = (y//increment) 
    return Files[file_index], Ranks[rank_index]

def determine_piece_in_square(x, y, player_pieces):
    for piece in player_pieces:
        file = determine_square(x - initial_x, y - initial_y)[0]
        rank = determine_square(x - initial_x, y - initial_y)[1]
        if piece.x <= x <= piece.x + increment and piece.y <= y <= piece.y + increment:
            #print(f"Piece {piece.name} is in square ({file}{rank})")
            print(piece)
            return piece
    return None
