from enum import Enum
import numpy as np

class Player(Enum):
    X = 1
    O = 2
    EMPTY = 0

# this is the game of ultimate tic tac toe with 9 x 9 grid
class Game:
    board = [[Player.EMPTY for i in range(9)] for j in range(9)]
    to_move = Player.X
    # matrix for grid won or not
    min_grid_win_info = [[None for i in range(3)] for j in range(3)]
    move_history = []
    
    def __init__(self):
        self.board = [[Player.EMPTY for i in range(9)] for j in range(9)]
        self.to_move = Player.X
        # matrix for grid won or not
        self.min_grid_win_info = [[None for i in range(3)] for j in range(3)]
        self.move_history = []

    def print_board(self):
        print("move: ", len(self.move_history))
        if (len(self.move_history) > 0):
            print("last move was", self.move_history[-1])
        else:
            print("no move history")
        for i in range(9):

            print(i, end=' ')
            for j in range(9):
                to_print = self.board[i][j]
                if to_print == Player.X:
                    to_print = 'X'
                elif to_print == Player.O:
                    to_print = 'O'
                else:
                    to_print = 'E'
                print(to_print, end=' ')
            print()
        print(" ", end=' ')
        for i in range(9):
            print(i, end=' ')
        print()
        print('next player is', self.to_move)
        print('mini board')
        for i in range(3):
            for j in range(3):
                to_print = self.min_grid_win_info[i][j]
                if to_print == Player.X:
                    to_print = 'X'
                elif to_print == Player.O:
                    to_print = 'O'
                elif to_print == Player.EMPTY:
                    to_print = 'T'
                else:
                    to_print = 'E'
                print(to_print, end=' ')
            print()
        print()

    def is_move_allowed(self, x, y):
        if self.board[y][x] != Player.EMPTY:
            return False
        if x < 0 or x >= 9 or y < 0 or y >= 9:
            return False
        if self.min_grid_win_info[y // 3][x // 3] != None:
            return False

        # check for last move location to get space allowed
        if len(self.move_history) > 0:
            last_move_x, last_move_y = self.move_history[-1]
            last_move_x = last_move_x % 3
            last_move_y = last_move_y % 3
            if (x // 3 == last_move_x and y // 3 == last_move_y):
                return True
            elif self.min_grid_win_info[last_move_y][last_move_x] != None:
                return True
            else:
                return

        return True

    # grid is [y][x]
    def make_move(self, x, y):
        if not self.is_move_allowed(x, y):
            raise Exception('Invalid move at location', x, y)
        self.board[y][x] = self.to_move
        res = self.check_grid_won(x, y)
        if res[0] == True:
            self.min_grid_win_info[y // 3][x // 3] = res[1]
        # check and update game state 
        self.to_move =  Player.O if self.to_move == Player.X else Player.X
        self.move_history.append((x, y))
    def get_all_valid_moves(self) -> list[tuple[int, int]]:
        # loop through small grid won they are not valid
        all_valid_moves = []
        # for i in range(3):
        #     for j in range(3):
        #         if self.min_grid_win_info[i][j] != None:
        #             continue
        #         else:
        #             for x in range(3):
        #                 for y in range(3):
        #                     if self.board[i * 3 + y][j * 3 + x] == Player.EMPTY:
        #                         all_valid_moves.append((j * 3 + x, i * 3 + y))
        for i in range(9):
            for j in range(9):
                if self.is_move_allowed(i, j):
                    all_valid_moves.append((i, j))
        return all_valid_moves

    # just check if small grid's location is won doesn't play the move itself
    def check_grid_won(self, x, y):
        # always need the row and col of the small grid but diagnal only needed if on certain tiles
        base_x_offset = x // 3 * 3
        base_y_offset = y // 3 * 3
        x_offset = x % 3
        y_offset = y % 3
        # check row        
        row_won = 0
        for i in range(3):
            if self.board[base_y_offset + i][base_x_offset + x_offset] == self.to_move:
                row_won += 1
        if row_won == 3:
            return (True, self.to_move)
        # check col
        col_won = 0
        for i in range(3):
            if self.board[base_y_offset + y_offset][base_x_offset + i] == self.to_move:
                col_won += 1
        if col_won == 3:
            return (True, self.to_move)
        # on left diagonal
        if (x_offset == y_offset):
            l_diag_won = 0
            for i in range(3):
                if self.board[base_y_offset + i][base_x_offset + i] == self.to_move:
                    l_diag_won += 1
            if l_diag_won == 3:
                return (True, self.to_move)
                    
        # on right diagonal
        if (x_offset == 2 - y_offset):
            r_diag_won = 0
            for i in range(3):
                if self.board[base_y_offset + i][base_x_offset + 2 - i] == self.to_move:
                    r_diag_won += 1
            if r_diag_won == 3:
                return (True, self.to_move)
        filled = 0
        for i in range(3):
            for j in range(3):
                if self.board[base_y_offset + i][base_x_offset + j] != Player.EMPTY:
                    filled += 1
        if filled == 9:
            return (True, Player.EMPTY)

        return (False, Player.EMPTY)
    
    def undo_move(self):
        if len(self.move_history) == 0:
            raise Exception('No move to undo')
        x, y = self.move_history.pop()
        # undo the mini grid won state information if the grid is no longer won
        self.board[y][x] = Player.EMPTY
        res = self.check_grid_won(x, y)
        if res[0] == True:
            # undo the state change of this being won
            self.min_grid_win_info[y // 3][x // 3] = res[1]
        else:
            self.min_grid_win_info[y // 3][x // 3] = None
        self.to_move = Player.O if self.to_move == Player.X else Player.X


    def is_game_over_and_winner(self):
        # check row for mini grid won
        for i in range(3):
            row_won = 0
            row_player = self.min_grid_win_info[i][0]
            if row_player == Player.EMPTY or row_player == None:
                continue
            if self.min_grid_win_info[i][0] != None:
                row_won = 1
                for j in range(1, 3):
                    if self.min_grid_win_info[i][j] != row_player:
                        break
                    else:
                        row_won += 1
                if (row_won == 3):
                    return (True, row_player)
            
        
        # check col for mini grid won
        for i in range(3):
            col_won = 0
            col_player = self.min_grid_win_info[0][i]
            if col_player == Player.EMPTY or col_player == None:
                continue
            if self.min_grid_win_info[0][i] != None:
                col_won = 1
                for j in range(1, 3):
                    if self.min_grid_win_info[j][i] != col_player:
                        break
                    else:
                        col_won += 1
                if (col_won == 3):
                    return (True, col_player)
                
        # check diagonal for mini grid won
        l_diag_player = self.min_grid_win_info[0][0]
        if l_diag_player != None and l_diag_player != Player.EMPTY:
            l_diag_won = 0
            for i in range(3):
                if self.min_grid_win_info[i][i] != l_diag_player:
                    break
                else:
                    l_diag_won += 1
            if (l_diag_won == 3):
                return (True, l_diag_player)
        r_diag_player = self.min_grid_win_info[0][2]
        if r_diag_player != None and r_diag_player != Player.EMPTY:
            r_diag_won = 0
            for i in range(3):
                if self.min_grid_win_info[i][2 - i] != r_diag_player:
                    break
                else:
                    r_diag_won += 1
            if (r_diag_won == 3):
                return (True, r_diag_player)
        filled = 0
        for i in range(3):
            for j in range(3):
                if self.min_grid_win_info[i][j] != None:
                    filled += 1
        if filled == 9:
            return (True, Player.EMPTY)
        return (False, Player.EMPTY)

    def convert_board_to_np_array(self):
        board = np.zeros((9, 9, 2), dtype=np.int8)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == self.to_move:
                    board[i][j][0] = 1
                elif self.board[i][j] != Player.EMPTY and self.board[i][j] != self.to_move:
                    board[i][j][1] = 1
        return board

        
      