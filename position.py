from player import switch_turn
from pieces import chess_piece
Files = ["A", "B", "C", "D", "E", "F", "G", "H"]
Ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
increment = 75
initial_x = 340
initial_y = 60
padding = 10
def determine_chess_coordinates(x:int, y:int):
    if not (initial_x <= x < initial_x + 8 * increment) or not (initial_y <= y < initial_y + 8 * increment):
        return None, None
    file_index = (x - initial_x) // increment
    rank_index = (y - initial_y) // increment
    return Files[file_index], Ranks[rank_index]

def determine_square_coordinates(file:str, rank:str):
    file_index = Files.index(file)
    rank_index = Ranks.index(rank)
    x = initial_x + (file_index * increment)
    y = initial_y + (rank_index * increment)
    return x, y

def determine_piece_in_square(file : str, rank : str, player_pieces :list):
    for piece in player_pieces:
        if piece.file == file and piece.rank == rank:
            return piece
    return None

def is_valid_square(file : str, rank : str, current_player, all_pieces):
    piece = determine_piece_in_square(file,rank,all_pieces)
    if not piece:
        return True
    elif piece.player != current_player:
        return True
    return False

def is_path_free(piece:chess_piece,target_file: str, target_rank : str,all_pieces:list):
    rank_index = Ranks.index(piece.rank)
    target_rank_index = Ranks.index(target_rank)
    file_index = Files.index(piece.file)
    target_file_index = Files.index(target_file)
    delta_rank = int(piece.rank) - int(target_rank)
    delta_file = int(file_index) - int(target_file_index)
    if piece.type == "king" and (abs(delta_rank) > 1 or  abs(delta_file) > 1):
        return False
    if piece.type == "pawn":
        if (piece.player_number == 1 and delta_rank > 0 and piece.type == "pawn") or (piece.player_number == 2 and delta_rank < 0 and piece.type == "pawn"):
            return False
        if abs(delta_file) == 1 and abs(delta_rank) < 2: # might be relevant later when doing captures ... dunno 
            enemy_piece = determine_piece_in_square(target_file,target_rank,all_pieces)
            if enemy_piece is not None and (piece.player is not  enemy_piece.player):
               return True
        if abs(delta_rank) > 0:
            enemy_piece = determine_piece_in_square(target_file,target_rank,all_pieces)
            if enemy_piece: 
                return False
        if (piece.player_number == 1 and piece.rank =="2") or (piece.player_number == 2 and piece.rank == "7"):
            if abs(delta_rank) > 2:
                return False
        else:
            if abs(delta_rank) > 1:
                return False
    if abs(delta_file) == abs(delta_rank):
        if piece.diagonal:
            file_step = 1 if target_file_index > file_index else -1 # vary both file and rank separately to avoid issues that stem from directional changes
            rank_step = 1 if target_rank_index > rank_index else -1
            steps = abs(delta_file)
            for i in range(1, steps):
                curr_file_idx = file_index + (i * file_step)
                curr_rank_idx = rank_index + (i * rank_step)
                found = determine_piece_in_square(Files[curr_file_idx], Ranks[curr_rank_idx], all_pieces)
                if found is not None:
                    return False
        else:
            return False
    elif  delta_file == 0 and delta_rank != 0 :
        rank_step = 1 if target_rank_index > rank_index else -1
        
        steps = abs(delta_rank)
        if piece.forward:
            for r in range(rank_index + rank_step, target_rank_index , rank_step):
                found = determine_piece_in_square(piece.file,Ranks[r],all_pieces)
                if found is not None:
                    return False
        else:
            return False
    elif  delta_file != 0 and delta_rank == 0 :
        file_step = 1 if file_index < target_file_index else -1 # vary both file and rank separately to avoid issues that stem from directional changes
        steps = abs(delta_file)
        if piece.sideward:
            for f in range(file_index + file_step, target_file_index, file_step):
                found = determine_piece_in_square(Files[f],piece.rank,all_pieces)
                if found is not None:
                    return False
        else:
            return False
    else:
        if piece.special:
            if (abs(delta_file) == 2 and abs(delta_rank) == 1) or (abs(delta_file) == 1 and abs(delta_rank) == 2):
                return True
            else:
                return False
        else:
            return False
    return True

def capture_piece(current_piece :chess_piece, target_piece :chess_piece, all_pieces: list):
    current_piece.file = target_piece.file
    current_piece.rank = target_piece.rank
    current_piece_index = all_pieces.index(target_piece)
    all_pieces.pop(current_piece_index)
    print(f"{current_piece.name} captured {target_piece.name} on square {target_piece.file,target_piece.rank}")
    return True
def determine_attacked_squares(piece :chess_piece, all_pieces: list):

    if piece.type == "pawn":
        piece.attacked_squares = pawn_attacks(piece)

    elif piece.type == "knight":
        piece.attacked_squares = knight_attacks(piece)

    elif piece.type == "bishop":
        piece.attacked_squares = sliding_attacks(piece,all_pieces,[(1, 1), (1, -1), (-1, 1), (-1, -1)])

    elif piece.type == "rook":
        piece.attacked_squares = sliding_attacks(piece,all_pieces,[(1, 0), (-1, 0), (0, 1), (0, -1)])

    elif piece.type == "queen":
        piece.attacked_squares = sliding_attacks(piece,all_pieces,[(1, 1), (1, -1), (-1, 1), (-1, -1),(1, 0), (-1, 0), (0, 1), (0, -1)])

    elif piece.type == "king":
        piece.attacked_squares = king_attacks(piece)

    return piece.attacked_squares    
def pawn_attacks(piece: chess_piece):
    attacked = []
    file_index = Files.index(piece.file)
    rank_index = Ranks.index(piece.rank)
    if piece.player.player_number == 1:       # White
        rank_step = -1
    else:                       # Black
        rank_step = 1
    target_rank_index = rank_index + rank_step
    if 0 <= target_rank_index < len(Ranks):
        # diagonal left
        if file_index - 1 >= 0:
            attacked.append([
                Files[file_index - 1],
                Ranks[target_rank_index]
            ])
        # diagonal right
        if file_index + 1 < len(Files):
            attacked.append([
                Files[file_index + 1],
                Ranks[target_rank_index]
            ])

    return attacked      

def knight_attacks(piece: chess_piece):
    attacked = []

    file_index = Files.index(piece.file)
    rank_index = Ranks.index(piece.rank)

    offsets = [
        (1, 2),
        (2, 1),
        (2, -1),
        (1, -2),
        (-1, -2),
        (-2, -1),
        (-2, 1),
        (-1, 2)
    ]

    for file_step, rank_step in offsets:
        new_file = file_index + file_step
        new_rank = rank_index + rank_step

        if (0 <= new_file < len(Files) and 0 <= new_rank < len(Ranks)):
            attacked.append([
                Files[new_file],
                Ranks[new_rank]
            ])

    return attacked

def king_attacks(piece: chess_piece):
    attacked = []

    file_index = Files.index(piece.file)
    rank_index = Ranks.index(piece.rank)

    for file_step in [-1, 0, 1]:
        for rank_step in [-1, 0, 1]:

            if file_step == 0 and rank_step == 0:
                continue

            new_file = file_index + file_step
            new_rank = rank_index + rank_step

            if (
                0 <= new_file < len(Files)
                and 0 <= new_rank < len(Ranks)
            ):
                attacked.append([
                    Files[new_file],
                    Ranks[new_rank]
                ])

    return attacked

def sliding_attacks(piece: chess_piece, all_pieces:list , directions :list):
    attacked = []

    file_index = Files.index(piece.file)
    rank_index = Ranks.index(piece.rank)

    for file_step, rank_step in directions:

        current_file = file_index + file_step
        current_rank = rank_index + rank_step

        while (
            0 <= current_file < len(Files)
            and 0 <= current_rank < len(Ranks)
        ):

            square = [
                Files[current_file],
                Ranks[current_rank]
            ]

            attacked.append(square)

            occupying_piece = determine_piece_in_square(
                square[0],
                square[1],
                all_pieces
            )

            if occupying_piece is not None:
                break

            current_file += file_step
            current_rank += rank_step

    return attacked

def generate_pseudo_legal_moves(all_pieces:list) -> None:
    for p in all_pieces:
        p.pseudo_legal_moves = []
    for piece in all_pieces:
        for file in Files:
            for rank in Ranks:
                if is_path_free(piece,file,rank,all_pieces) and is_valid_square(file,rank,piece.player,all_pieces):
                    square = [file,rank]
                    if square not in piece.pseudo_legal_moves:
                        piece.pseudo_legal_moves.append(square)
    return None

def is_king_checked(king:chess_piece, all_pieces:list) -> bool:
    for piece in all_pieces:
        if piece.player != king.player:
            attacked_squares = determine_attacked_squares(piece,all_pieces)
            if [king.file, king.rank] in attacked_squares:
                return True

    return False
def move_to_selected_square(selected_piece,highlighter_target,all_pieces):
    if not selected_piece.player.turn:
        print(f"not Player: {selected_piece.player.player_number} turn")
        return
    else:
        current_king = next(
            piece for piece in all_pieces
                if piece.type == "king" and piece.player == selected_piece.player
            )
    trial_move(selected_piece,current_king,highlighter_target.file,highlighter_target.rank,all_pieces)
    return None

def trial_move(piece:chess_piece, king:chess_piece, target_file : str, target_rank : str, all_pieces:list) -> bool:
    prev_file = piece.file
    prev_rank = piece.rank
    prev_test_capture = None

    if not is_path_free(piece, target_file, target_rank, all_pieces):
        return False
    if not is_valid_square(target_file,target_rank,piece.player,all_pieces):
        return False
    opposite_piece = determine_piece_in_square(target_file,target_rank,all_pieces)
    if opposite_piece is not None:
        prev_test_capture = opposite_piece
        capture_piece(piece, opposite_piece,all_pieces)
    else:
        piece.file = target_file
        piece.rank = target_rank
        # Recalculate hypothetical position
    determine_attacked_squares(piece,all_pieces)
    # Did this move expose our king?
    if is_king_checked(king, all_pieces):
        print("Move rejected: piece is pinned.")
        for p in all_pieces:
            print( f"{p.name} : {p.pseudo_legal_moves}")
        revert_move(piece, prev_file, prev_rank,all_pieces,prev_test_capture)
        return False 
    else:  
        switch_turn(piece.player)
        return True

def revert_move(piece:chess_piece,prev_file : str,prev_rank : str,all_pieces:list,capture = None):
    piece.file = prev_file
    piece.rank = prev_rank
    generate_pseudo_legal_moves(all_pieces)

    if capture is not None:
        all_pieces.append(capture)
