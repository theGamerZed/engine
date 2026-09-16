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
    if  piece.file == target_file and  piece.rank == target_rank:
        print("same square")
        return False
    else:
        if piece.type == "knight":
            return True
        else:
            file_index = Files.index(piece.file)
            rank_index = Ranks.index(piece.rank)
            target_file_index = Files.index(target_file)
            target_rank_index = Ranks.index(target_rank)
            if (piece.type == "bishop" or piece.type == "queen" or piece.type == "king") and piece.diagonal:
                file_diff = file_index - target_file_index
                rank_diff = rank_index - target_rank_index
                if abs(rank_diff) == abs(file_diff):
                    file_step = 1 if target_file_index > file_index else -1
                    rank_step = 1 if target_rank_index > rank_index else -1
                    steps = abs(file_diff)
                    for i in range(1, steps):
                        curr_file_idx = file_index + (i * file_step)
                        curr_rank_idx = rank_index + (i * rank_step)
                        found = determine_piece_in_square(Files[curr_file_idx], Ranks[curr_rank_idx], all_pieces)
                        if found is not None:
                            print(f"unauth pieces on the way: {found.name}")
                            return False
                        else:
                            print(f"auth diag {curr_file_idx, curr_rank_idx}")
            elif (piece.type == "pawn" or piece.type == "queen" or piece.type == "king" or piece.type == "rook"):
                delta_rank = int(piece.rank) - int(target_rank)
                delta_file = int(Files.index(piece.file)) - int(Files.index(target_file))
                if piece.forward and delta_file == 0:
                    if rank_index - target_rank_index > 0 and piece.forward:
                        for r in range(rank_index - 1, target_rank_index, -1): # -1 to ignore the current piece's rank and start verification from the piece in front
                            print(rank_index,target_rank_index)
                            found = determine_piece_in_square(piece.file,Ranks[r],all_pieces)
                            if found == None:
                                print("authorized!!!")
                            else:
                                print(f"unauth pieces on the way: {found.name}")
                                return False
                    elif rank_index - target_rank_index < 0 and piece.forward:
                        print(rank_index,target_rank_index)
                        for r in range(rank_index + 1 , target_rank_index, 1): # +1 to ignore the current piece's rank and start verification from the piece in front
                            found = determine_piece_in_square(piece.file,Ranks[r],all_pieces)
                            if found == None:
                                print("authorized!!!")
                            else:
                                print(f"unauth pieces on the way: {found.name}")
                                return False
                if piece.sideward and delta_rank == 0:
                    if file_index - target_file_index > 0 and piece.sideward:
                        for f in range(file_index - 1, target_file_index, -1): # -1 to ignore the current piece's file and start verification from the square next to current piece
                            found = determine_piece_in_square(Files[f],piece.rank,all_pieces)
                            if  found == None:
                                print("auth")
                            else:
                                print(f"unauth pieces on the way: {found.name}")
                                return False
                    elif file_index - target_file_index < 0 and piece.sideward:
                        for f in range(file_index + 1, target_file_index, 1): # +1 to ignore the current piece's file and start verification from the square next to current piece
                            found = determine_piece_in_square(Files[f],piece.rank,all_pieces)
                            if  found == None:
                                print("auth")
                            else:
                                print(f"unauth pieces on the way: {found.name}")
                                return False
