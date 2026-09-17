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

def determine_piece_in_square(file, rank, player_pieces):
    for piece in player_pieces:
        if piece.file == file and piece.rank == rank:
            return piece
    return None

def detect_chess_piece (file, rank, player_pieces):
    for piece in player_pieces:
        if piece.file == file and piece.rank == rank:
            return piece

def move_piece_to_square(piece, file, rank, all_pieces,selected_status):
    if is_valid_square(file,rank, all_pieces) and selected_status :
        piece.rank = rank
        piece.file = file
    else:
        print(f"Invalid move for {piece.name} to square {file}{rank}.")

def is_valid_square(file, rank, pieces):
    if not determine_piece_in_square(file,rank,pieces):
        return True
    # elif determine_piece_in_square(x, y, pieces).player != piece.player:
    #     return True
    return False

def move_to_selected_square(selected_piece ,highlighter_target,all_pieces):
    if is_path_free(selected_piece,highlighter_target.file,highlighter_target.rank,all_pieces):
        if is_valid_square(highlighter_target.file, highlighter_target.rank, all_pieces) and highlighter_target.current_piece.selected:
            highlighter_target.current_piece.file = highlighter_target.file
            highlighter_target.current_piece.rank = highlighter_target.rank
        else:
            print(f"Invalid move for {highlighter_target.current_piece.name} to square {highlighter_target.file}{highlighter_target.rank}.")
    return None

def is_path_free(piece,target_file, target_rank,all_pieces):
    rank_index = Ranks.index(piece.rank)
    target_rank_index = Ranks.index(target_rank)
    file_index = Files.index(piece.file)
    target_file_index = Files.index(target_file)
    delta_rank = int(piece.rank) - int(target_rank)
    delta_file = int(file_index) - int(target_file_index)
    if piece.type == "king" and (abs(delta_rank) > 1 or  abs(delta_file) > 1):
        return False
    if piece.type == "pawn":
        if abs(delta_file) > 0: # might be relevant later when doing captures ... dunno 
            return False

        if piece.rank in ("2", "7"): # nifty trick alright !!!
            if abs(delta_rank) > 2:
                return False
        else:
            if abs(delta_rank) > 1:
                return False
    if abs(delta_file) == abs(delta_rank):
        if piece.diagonal:
            print(piece.type)
            file_step = 1 if target_file_index > file_index else -1 # vary both file and rank separately to avoid issues that stem from directional changes
            rank_step = 1 if target_rank_index > rank_index else -1
            steps = abs(delta_file)
            for i in range(1, steps):
                curr_file_idx = file_index + (i * file_step)
                curr_rank_idx = rank_index + (i * rank_step)
                found = determine_piece_in_square(Files[curr_file_idx], Ranks[curr_rank_idx], all_pieces)
                if found is not None:
                    print(f"found {found.name} at {found.file, found.rank}")
                    return False
        else:
            return False
    elif  delta_file == 0 and delta_rank is not 0 :
        if (piece.player == 1 and delta_rank > 0) or (piece.player == 2 and delta_rank < 0):
            return False
        if piece.forward:
            print(piece.type)
            for r in range(rank_index - 1, target_rank_index, -1):
                found = determine_piece_in_square(piece.file,Ranks[r],all_pieces)
                if found is not None:
                    print(f"found {found.name} at {found.file, found.rank}")
                    return False
        else:
            return False
    elif  delta_file is not 0 and delta_rank == 0 :
        print("sideward move")
        if piece.sideward:
            print(piece.type)
            for f in range(file_index - 1, target_file_index, -1):
                found = determine_piece_in_square(Files[f],piece.rank,all_pieces)
                if found is not None:
                    print(f"found {found.name} at {found.file, found.rank}")
                    return False
        else:
            return False
    else:
        if piece.special:
            if (abs(delta_file) == 2 and abs(delta_rank) == 1) or (abs(delta_file) == 1 and abs(delta_rank) == 2):
                print(piece.type)
            else:
                return False
    return True
