from typing import Literal
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

def determine_piece_in_square(file : str, rank : str, all_pieces : list[chess_piece]):
    for piece in all_pieces:
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

def is_path_free(piece:chess_piece,target_file: str, target_rank : str,all_pieces : list[chess_piece]):
    valid = True
    if piece.type == "pawn":
        valid = pawn_move(piece,target_file,target_rank,all_pieces,[(0,1),(0,2),(0,-1),(0,-2)])
    elif piece.type == "king":
        delta_file = Files.index(piece.file) - Files.index(target_file)
        if abs(delta_file) > 2 : return False
        if abs(delta_file) == 2 :
            castling_rook = None
            rook_file = "H" if delta_file < 0 else "A"
            rook_rank = "1" if piece.player_number == 1 else "8"
            for p in all_pieces:
                if (p.type == "rook" and p.file == rook_file and p.rank == rook_rank):
                    castling_rook = p
                    break
            if castling_rook is not None:
                if is_path_free (castling_rook,piece.file,piece.rank,all_pieces):
                    return True
                else:
                    return False
            else: return False
        elif abs(delta_file) == 1 :
            valid = piece_move(piece,target_file,target_rank,all_pieces)
    else: # for all pieces except king and pawns
        valid = piece_move(piece,target_file,target_rank,all_pieces)
    return valid

def pawn_move(piece, target_file, target_rank, all_pieces, directions):

    file_index = Files.index(piece.file)
    rank_index = Ranks.index(piece.rank)

    target_file_index = Files.index(target_file)
    target_rank_index = Ranks.index(target_rank)

    delta_rank = rank_index - target_rank_index
    delta_file = file_index - target_file_index
    
    square = [target_file,target_rank]
    attacked_squares = determine_attacked_squares(piece,all_pieces)
    potential_enemy_piece = determine_piece_in_square(target_file,target_rank,all_pieces) 
    if square in attacked_squares:
        print(square)
        if potential_enemy_piece is not None and not (potential_enemy_piece.player == piece.player):
            print("pawn capture")
            return True

    coord = (delta_file, delta_rank)
    if coord not in directions:
        return False
        
    if piece.player_number == 1:
        forward = 1
        starting_rank = "2"
    else:
        forward = -1
        starting_rank = "7"

    if delta_rank not in (forward, forward * 2): # test for backward movement
        return False
    
    if delta_file == 0 and delta_rank == forward:
        return True

    if delta_file == 0 and delta_rank == forward * 2:
        if piece.rank != starting_rank:
            return False
        
        intermediate_rank_index = rank_index - forward
        intermediate_rank = Ranks[intermediate_rank_index]
        occupying_piece = determine_piece_in_square( piece.file, intermediate_rank, all_pieces)

        if occupying_piece is not None:
            return False
        return True

    return False

def determine_pawn_moves(pawn: chess_piece, all_pieces: list[chess_piece]):
    moves = []

    direction = -1 if pawn.player == 1 else 1
    current_file_index = Files.index(pawn.file)
    current_rank_index = Ranks.index(pawn.rank)
    # One square forward
    new_rank_index = current_rank_index + direction
    if 0 <= new_rank_index < len(Ranks):
        new_square = [ Files[current_file_index], Ranks[new_rank_index] ]
        if determine_piece_in_square(new_square[0],new_square[1], all_pieces) is None:
            moves.append(new_square)
            # Two squares forward
            if  (pawn.player_number == 1 and pawn.rank == "2") or(pawn.player_number == 2 and pawn.rank == "7") :
                double_rank_index = current_rank_index + (2 * direction)
                double_square = [ Files[current_file_index], Ranks[double_rank_index] ]
                if determine_piece_in_square(double_square[0],double_square[1], all_pieces ) is None:
                    moves.append(double_square)
    print(moves)
    return moves

def piece_move(piece,target_file,target_rank,all_pieces):
    attacked_squares = determine_attacked_squares(piece,all_pieces)
    if [target_file,target_rank] in attacked_squares:
        return True
    return False

def capture_piece(current_piece :chess_piece, target_piece :chess_piece,all_pieces : list[chess_piece]):
    current_piece.rank = target_piece.rank
    current_piece.file = target_piece.file

    current_piece_index = all_pieces.index(target_piece)
    all_pieces.pop(current_piece_index)
    print(f"{current_piece.name} captured {target_piece.name} on square {target_piece.file,target_piece.rank}")
    return True

def determine_attacked_squares(piece :chess_piece,all_pieces : list[chess_piece]):
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

            if (0 <= new_file < len(Files) and 0 <= new_rank < len(Ranks) ):
                attacked.append([ Files[new_file], Ranks[new_rank] ])

    return attacked

def sliding_attacks(piece: chess_piece, all_pieces : list[chess_piece] , directions :list):
    attacked = []

    file_index = Files.index(piece.file)
    rank_index = Ranks.index(piece.rank)

    for file_step, rank_step in directions:

        current_file = file_index + file_step
        current_rank = rank_index + rank_step

        while ( 0 <= current_file < len(Files) and 0 <= current_rank < len(Ranks) ):
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

def is_king_checked(king:chess_piece, all_pieces : list[chess_piece]) -> list[chess_piece] | Literal[False]:
    checking_pieces = []
    for piece in all_pieces:
        if piece.player != king.player:
            attacked_squares = determine_attacked_squares(piece,all_pieces)     
            if [king.file, king.rank] in attacked_squares:
                checking_pieces.append(piece)
    if checking_pieces:
        return checking_pieces
    return False

def is_checkmate(king: chess_piece, all_pieces :list ):
    safe_squares = generate_safe_squares(king,all_pieces)
    attacker_list = is_king_checked(king,all_pieces)
    print(f"safe squares are {safe_squares} for {king.name}")
    if not safe_squares and attacker_list:
        print(attacker_list)
        if not is_piece_capturable(king, attacker_list,all_pieces):
            print("not capturable")
            if not can_block_check(king,attacker_list,all_pieces):
                print("no piece can block ... checkmate")
    return False

def can_block_check( king: chess_piece, attacking_pieces: list[chess_piece], all_pieces: list[chess_piece] ):

    if len(attacking_pieces) != 1:
        return False

    checker = attacking_pieces[0]

    if checker.type in ["knight", "pawn", "king"]:
        return False

    king_file_index = Files.index(king.file)
    king_rank_index = Ranks.index(king.rank)

    checker_file_index = Files.index(checker.file)
    checker_rank_index = Ranks.index(checker.rank)

    delta_file = checker_file_index - king_file_index
    delta_rank = checker_rank_index - king_rank_index

    # Determine direction
    if delta_file == 0:
        file_step = 0
        rank_step = 1 if delta_rank > 0 else -1

    elif delta_rank == 0:
        file_step = 1 if delta_file > 0 else -1
        rank_step = 0

    elif abs(delta_file) == abs(delta_rank):
        file_step = 1 if delta_file > 0 else -1
        rank_step = 1 if delta_rank > 0 else -1

    else:
        return False

    blocking_squares = []

    current_file_index = king_file_index + file_step
    current_rank_index = king_rank_index + rank_step

    while ( current_file_index != checker_file_index or current_rank_index != checker_rank_index ):
        blocking_squares.append([ Files[current_file_index], Ranks[current_rank_index] ])
        current_file_index += file_step
        current_rank_index += rank_step

    print("Blocking squares:", blocking_squares)

    for blocking_piece in all_pieces:

        if blocking_piece.player != king.player:
            continue

        if blocking_piece.type == "king":
            continue

        # candidate_piece_moves = determine_attacked_squares( blocking_piece, all_pieces )
        if blocking_piece.type == "pawn":
            candidate_piece_moves = determine_pawn_moves( blocking_piece, all_pieces )
        else: 
            candidate_piece_moves = determine_attacked_squares( blocking_piece, all_pieces )

        for square in blocking_squares:
                if square in candidate_piece_moves:
                    if trial_move( blocking_piece, king, square[0], square[1], all_pieces ):
                        print(f"{blocking_piece.name} on {blocking_piece.file,blocking_piece.rank}can block the check")
                        return True
    return False

def move_to_selected_square(selected_piece:chess_piece,highlighter_target,all_pieces : list[chess_piece]):
    if not selected_piece.player.turn:
        print(f"not Player: {selected_piece.player.player_number} turn")
        return
    
    current_king = next(
            piece for piece in all_pieces                           
                if piece.type == "king" and piece.player == selected_piece.player
            )
    opposite_king = next(
            piece for piece in all_pieces                           
                if piece.type == "king" and not piece.player == selected_piece.player
            )
        
    if not trial_move(selected_piece,current_king,highlighter_target.file,highlighter_target.rank,all_pieces):
        return False
    enemy_piece = determine_piece_in_square( highlighter_target.file, highlighter_target.rank, all_pieces)

    delta_file = Files.index(selected_piece.file) - Files.index(highlighter_target.file)
    if selected_piece.type == "king" and abs(delta_file) == 2: # Handle Castling of the king 
        castling_rook = None
        rook_file = "H" if delta_file < 0 else "A"
        rook_rank = "1" if selected_piece.player_number == 1 else "8"
        
        for p in all_pieces:
            if (p.type == "rook" and p.file == rook_file and p.rank == rook_rank and selected_piece.player == p.player):
                castling_rook = p
                print(f"castling rook is {castling_rook.name}: at {castling_rook.file,castling_rook.rank}")
                break
        
        if castling_rook is None: # rook has been captured or something 
            return False
        if selected_piece.move_history or castling_rook.move_history: # if either the rook or king already moved before 
            return False
        
        start_index = Files.index(selected_piece.file)
        end_index = Files.index(highlighter_target.file)
        step = -1 if start_index > end_index else 1
        for f in Files[start_index : end_index + step: step]: # test if any of the kings moving squares is attacked 
            for el in all_pieces:
                if el.player_number != selected_piece.player_number:
                    if [f,highlighter_target.rank] in el.attacked_squares:
                        return False
                    
        castle(selected_piece,castling_rook,highlighter_target.file)
    elif enemy_piece is not None:
        print(f"{enemy_piece}, Real capture")
        capture_piece(selected_piece,enemy_piece,all_pieces)
        selected_piece.move_history.append(True)
    else:
        selected_piece.file = highlighter_target.file
        selected_piece.rank = highlighter_target.rank
        selected_piece.move_history.append(True) # to record pieces moves ... later serves as a test to determine if king or rook has moved
    switch_turn(selected_piece.player)
    is_checkmate(opposite_king,all_pieces)
    return None

def trial_move(piece, king, target_file, target_rank, all_pieces : list[chess_piece]):
    prev_file = piece.file
    prev_rank = piece.rank
    prev_test_capture = None

    if not is_path_free(piece, target_file, target_rank, all_pieces):
        return False
    if not is_valid_square(target_file,target_rank,piece.player,all_pieces):
        return False
    enemy_piece = determine_piece_in_square(target_file,target_rank,all_pieces)

    if enemy_piece is not None and not (piece.player == enemy_piece.player): # if the tried move is a capture ...
        prev_test_capture = enemy_piece
        capture_piece(piece, enemy_piece,all_pieces)
    else:                                                                     # if not then it is a normal move ...
        piece.file = target_file
        piece.rank = target_rank

    # Recalculate hypothetical position
    determine_attacked_squares(piece,all_pieces)
   
    if is_king_checked(king, all_pieces):  # Did this move expose our king?
        revert_move(piece, prev_file, prev_rank,all_pieces,prev_test_capture)
        return False
    
    revert_move(piece, prev_file, prev_rank,all_pieces,prev_test_capture)
    return True
        
def revert_move(piece:chess_piece,prev_file : str,prev_rank : str, all_pieces : list[chess_piece], capture = None ): # revert move in trail if it is illegal ... and un-capture any captured piece during tests 
    piece.file = prev_file
    piece.rank = prev_rank
    if capture is not None:
        all_pieces.append(capture)

def castle(king :chess_piece,rook: chess_piece, t_file:str):
    delta_file = Files.index(king.file) - Files.index(t_file)
    king.file = t_file

    offset = -1 if delta_file < 0 else 1
    new_rook_file = Files[Files.index(t_file) + offset]
    rook.file = new_rook_file

    king.move_history.append(True)
    rook.move_history.append(True)

    return False

def generate_safe_squares(king: chess_piece,all_pieces : list[chess_piece]):
    king_possible_squares = king_attacks(king)
    king.safe_squares = []
    for square in king_possible_squares:
        safe = True
        for piece in all_pieces:
            if piece.player != king.player:
                if square in piece.attacked_squares:
                    safe = False
                    break
        if safe:
            piece_on_square = determine_piece_in_square( square[0], square[1], all_pieces )
            if piece_on_square and piece_on_square.player == king.player: # king can't move to a friendly piece but can move to capture enemy piece
                safe = False
        if safe:
            king.safe_squares.append(square)

    return king.safe_squares

def promote_piece(pawn: chess_piece,all_pieces : list[chess_piece]):

    return False

def is_piece_capturable(king:chess_piece, enemy_pieces: list,all_pieces : list[chess_piece]):
    if not enemy_pieces:
        return False
    if len(enemy_pieces) > 1: # during a double check the king must move ...
        return False

    for enemy in enemy_pieces:
        for friend in all_pieces:
            if friend.player == enemy.player:
                continue

            square = [enemy.file, enemy.rank]
            attacked_squares = determine_attacked_squares( friend, all_pieces )

            if square in attacked_squares:
                if friend == king: #check if the king can safely capture this piece
                    return trial_move(friend,friend,square[0],square[1],all_pieces)
                else: # any other piece would sacrifice itself
                    return True
    return False
