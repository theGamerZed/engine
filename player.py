class Player:
    def __init__ (self,player_number,turn,color):
        self.player_number = player_number
        self.turn = turn
        self.color = color

#initialise player pieces
player_1 = Player(1,True,(255, 255, 255))   #white pieces, player 1
player_2 = Player(2,False,(0, 0, 0) )       #black pieces, player 2    

PLAYERS = [player_1,player_2]

def switch_turn(player):
    current_player_index = PLAYERS.index(player)
    for p in PLAYERS:
        if p == PLAYERS[current_player_index]:
            p.turn = False
        else:
            p.turn = True