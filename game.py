def double(val):
    if val is None:
        return None
    return val * 2

def merge(tiles):
    if tiles[0] == tiles[1]:
        tiles[0], tiles[1] = double(tiles[0]), None
    if tiles[1] == tiles[2]:
        tiles[1], tiles[2] = double(tiles[1]), None
    if tiles[2] == tiles[3]:
        tiles[2], tiles[3] = double(tiles[2]), None
    for t in range(3):
        if tiles[t] == None:
            tiles[t], tiles[t + 1] = tiles[t + 1], tiles[t]
    return tiles

class Game(object):
    def __init__(self, board=None):
        if board is None:
            self.board = [[None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None]]
        else:
            self.board = board
    
    def move_left(self):
        row_1 = merge(self.board[0])
        row_2 = merge(self.board[1])
        row_3 = merge(self.board[2])
        row_4 = merge(self.board[3])
        return [row_1, row_2, row_3, row_4]

    def move_right(self):
        row_1 = merge(self.board[0][::-1])
        row_2 = merge(self.board[1][::-1])
        row_3 = merge(self.board[2][::-1])
        row_4 = merge(self.board[3][::-1])
        return [row_1[::-1], row_2[::-1], row_3[::-1], row_4[::-1]]

    def move_up(self):
        row_1 = merge([self.board[0][0], self.board[1][0], self.board[2][0], self.board[3][0]])
        row_2 = merge([self.board[0][1], self.board[1][1], self.board[2][1], self.board[3][1]])
        row_3 = merge([self.board[0][2], self.board[1][2], self.board[2][2], self.board[3][2]])
        row_4 = merge([self.board[0][3], self.board[1][3], self.board[2][3], self.board[3][3]])
        return [[row_1[0], row_2[0], row_3[0], row_4[0]],
                      [row_1[1], row_2[1], row_3[1], row_4[1]],
                      [row_1[2], row_2[2], row_3[2], row_4[2]],
                      [row_1[3], row_2[3], row_3[3], row_4[3]]]

    def move_down(self):
        row_1 = merge([self.board[0][0], self.board[1][0], self.board[2][0], self.board[3][0]][::-1])
        row_2 = merge([self.board[0][1], self.board[1][1], self.board[2][1], self.board[3][1]][::-1])
        row_3 = merge([self.board[0][2], self.board[1][2], self.board[2][2], self.board[3][2]][::-1])
        row_4 = merge([self.board[0][3], self.board[1][3], self.board[2][3], self.board[3][3]][::-1])
        return [[row_1[0], row_2[0], row_3[0], row_4[0]][::-1],
                      [row_1[1], row_2[1], row_3[1], row_4[1]][::-1],
                      [row_1[2], row_2[2], row_3[2], row_4[2]][::-1],
                      [row_1[3], row_2[3], row_3[3], row_4[3]][::-1]]

        

