Files = ["A", "B", "C", "D", "E", "F", "G", "H"]
Ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
increment = 75

def determine_square(x, y):
    file_index = (x//increment) 
    rank_index = (y//increment) 

    #print(f"File: {Files[file_index]}, Rank: {Ranks[rank_index]}")
    
    return Files[file_index], Ranks[rank_index]