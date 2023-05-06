import random
import re
class Board:
    def __init__(self, board_dimension, nums_bombs):
        self.board_dimension = board_dimension
        self.nums_bombs = nums_bombs
        self.board = self.make_new_board()
        self.assign_values_board()
        self.dug = set()
        
    def make_new_board(self):
        board = [[None for _ in range(self.board_dimension)] for _ in range(self.board_dimension)]
        bomb_planted = 0
        while bomb_planted < self.nums_bombs:
            loc = random.randint(0, self.board_dimension**2 - 1)
            row = loc // self.board_dimension
            col = loc % self.board_dimension
            if board[row][col] == "*":
                continue
            
            board[row][col] = "*"
            bomb_planted += 1
        return board
    def assign_values_board(self):
        for r in range(self.board_dimension):
            for c in range(self.board_dimension):
                if self.board[r][c] == "*":
                    continue
                self.board[r][c] = self.get_nums_neigh_bombs(r, c)

    def get_nums_neigh_bombs(self,row,col):
        number_neigh_bombs = 0
        for r in range(max(0, row-1), min(self.board_dimension-1, row+1)+1):
            for c in range(max(0,col-1),min(self.board_dimension-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == "*":
                    number_neigh_bombs += 1
        return number_neigh_bombs
    
    def dig(self,row,col):
        self.dug.add((row, col))
        if self.board[row][col] == "*" :
            return False 
        elif self.board[row][col] > 0 :
            return True
        for r in range(max(0, row-1),min(self.board_dimension-1, row+1)+1):
            for c in range(max(0,col-1),min(self.board_dimension-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.board_dimension)] for _ in range(self.board_dimension)]
        for row in range(self.board_dimension):
            for col in range(self.board_dimension):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' ' 
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.board_dimension):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.board_dimension)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.board_dimension)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep            
                   
def play(board_dimension=10, nums_bombs=10):
    board = Board(board_dimension,nums_bombs)
    safe = True
    while len(board.dug) < board.board_dimension ** 2 - nums_bombs:
        print(board)
        user_input = re.split(',(\\s)*',input("Where do you want to dig. Enter format like row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.board_dimension or col < 0 or col >= board_dimension:
            print("Invalid value")
            continue
        
        safe = board.dig(row,col)
        if not safe:
            break
        
    if safe :
        print("CONGRATS!!!")
    else:
        print("GAME OVER HAHAHAH!!!")
            
        board.dug = [(r,c) for r in range(board.board_dimension) for c in range(board.board_dimension)]
        print(board)
        
        
if __name__ == "__main__":
    play()    