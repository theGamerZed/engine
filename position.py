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

def piece_move(piece,target_file,target_rank,all_pieces):
    attacked_squares = determine_attacked_squares(piece,all_pieces)
    if [target_file,target_rank] in attacked_squares:
        return True
    return False

def capture_piece(current_piece :chess_piece, target_piece :chess_piece, all_pieces: list):
    if [target_piece.file,target_piece.rank] in current_piece.attacked_squares:

        current_piece.file = target_piece.file
        current_piece.rank = target_piece.rank

        current_piece_index = all_pieces.index(target_piece)
        all_pieces.pop(current_piece_index)
        print(f"{current_piece.name} captured {target_piece.name} on square {target_piece.file,target_piece.rank}")
        return True
    else :
        return False

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

def is_king_checked(king:chess_piece, all_pieces:list) -> bool:
    for piece in all_pieces:
        if piece.player != king.player:
            attacked_squares = determine_attacked_squares(piece,all_pieces)
            if [king.file, king.rank] in attacked_squares:
                return True
    return False
  
def move_to_selected_square(selected_piece:chess_piece,highlighter_target,all_pieces:list):
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

def trial_move(piece:chess_piece, king:chess_piece, target_file : str, target_rank : str, all_pieces:list):
    if not is_path_free(piece, target_file, target_rank, all_pieces):
        return False
    if not is_valid_square(target_file,target_rank,piece.player,all_pieces):
        return False
    
    delta_file = Files.index(piece.file) - Files.index(target_file)
    if piece.type == "king" and abs(delta_file) == 2:
        castling_rook = None
        rook_file = "H" if delta_file < 0 else "A"
        rook_rank = "1" if piece.player_number == 1 else "8"
        for p in all_pieces:
            if (p.type == "rook" and p.file == rook_file and p.rank == rook_rank and piece.player == p.player):
                castling_rook = p
                print(f"castling rook is {castling_rook.name}: at {castling_rook.file,castling_rook.rank}")
                break
        start_index = Files.index(piece.file)
        end_index = Files.index(target_file)
        step = -1 if start_index > end_index else 1
        print(start_index,end_index,step)
        if castling_rook is not None:
            if not piece.move_history and not castling_rook.move_history:
                for f in Files[start_index:end_index + step:step]: # test if any of the kings moving squares is attacked 
                    print(f"tested squares are {f,target_rank}")
                    for el in all_pieces:
                        if el.player_number != piece.player_number:
                            if [f,target_rank] in el.attacked_squares:
                                print(el.name)
                                return False
                castle(piece,castling_rook,target_file)
                switch_turn(piece.player)
                return True 
            else:
                print("king already moved") if  piece.move_history else print(f"rook at {castling_rook.file,castling_rook.rank} already moved")
                return False
        else:
            return False
    else:
        prev_file = piece.file
        prev_rank = piece.rank
        prev_test_capture = None
        opposite_piece = determine_piece_in_square(target_file,target_rank,all_pieces)
        if opposite_piece is not None and not (piece.player == opposite_piece.player):
            prev_test_capture = opposite_piece
            if not capture_piece(piece, opposite_piece,all_pieces):
                return False
        else:
            piece.file = target_file
            piece.rank = target_rank
        # Recalculate hypothetical position
        determine_attacked_squares(piece,all_pieces)
        # Did this move expose our king?
        if is_king_checked(king, all_pieces):
            print("Move rejected: king is checked.")
            # for p in all_pieces:
            #     print( f"{p.name} : {p.attacked_squares}")
            revert_move(piece, prev_file, prev_rank,all_pieces,prev_test_capture)
            return False 
        else:  
            # if move is 'valid' switch player
            move = [target_file,target_rank]
            piece.move_history.append(move)
            switch_turn(piece.player)
            print(piece.move_history)
            return True

def revert_move(piece:chess_piece,prev_file : str,prev_rank : str, all_pieces:list, capture = None):
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
    return False