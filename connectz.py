from collections import namedtuple
import sys

import constants as state
from errors import *

PLAYER_ONE = '1'
PLAYER_TWO = '2'


class GameBoard(object):
    def __init__(self, no_of_rows, no_of_columns, counters_to_win=4):
        self.max_rows = no_of_rows
        self.max_columns = no_of_columns
        self.counters_to_win = counters_to_win
        self.grid = [[] for _ in range(no_of_columns)]

        self.Direction = namedtuple('Direction', ['x', 'y', 'direction'])

    def add_to_column(self, col_index, player):
        try:
            self.grid[col_index].append(player)
        except IndexError:
            raise ColumnError

        row_length = len(self.grid[col_index])
        row_index = row_length-1  # reset to index base 0

        if row_length > self.max_rows:
            raise RowError

        return self.check_for_win(col_index, row_index, player)

    def check_for_win(self, col_number, row_index, player):
        # iterate over every direction (except up), if we hit a grid boundary (IndexError) continue
        # if we find X in a row, return True
        # else return False
        win = False
        for d in [
            self.Direction(0, -1, 'left'),
            self.Direction(0, 1, 'right'),
            self.Direction(-1, 0, 'down'),
            self.Direction(1, -1, 'upleft'),
            self.Direction(1, 1, 'upright'),
            self.Direction(-1, -1, 'downleft'),
            self.Direction(-1, 1, 'downright')
        ]:
            try:
                win = self.win_checker(row_index, col_number, d.x, d.y, player)
            except IndexError:
                continue

            if win:
                break

        return win

    def win_checker(self, row, col, d_row, d_col, player, number_of_rows_left=0):
        if number_of_rows_left >= self.counters_to_win:
            return True

        if row < 0 or col < 0:
            raise IndexError  # let's pretend we are using arrays and are not going to wrap back around

        if not self.grid[col][row] == player:
            return False

        elif self.grid[col][row] == player:
            return self.win_checker(row+d_row, col+d_col, d_row, d_col, player, number_of_rows_left+1)


def connectz(args):
    if not len(args) == 2:
        return state.INCORRECT_ARGUMENTS

    file_name = args[1]
    try:
        with open(file_name, 'r') as f:
            game = f.read().splitlines()

    except IOError:
        return state.FILE_DOESNT_EXIST

    game_rules = tuple(game.pop(0).replace(" ", ""))

    try:
        game_moves = [int(i) for i in game]
        x, y, counters_to_win = [int(i) for i in game_rules]
    except ValueError:
        return state.INVALID_FILE

    if counters_to_win > x and counters_to_win > y:
        return state.ILLEGAL_GAME

    gb = GameBoard(x, y, counters_to_win)

    is_game_over = False

    for idx, column_to_place in enumerate(game_moves):
        if is_game_over:
            return state.ILLEGAL_CONTINUE

        # Odd moves are always player one and even moves are player 2
        if idx % 2 == 0:
            player = PLAYER_ONE
        else:
            player = PLAYER_TWO

        col = column_to_place - 1  # set this index to base 0 so we can use it in an array

        try:
            is_game_over = gb.add_to_column(col, player)
        except RowError:
            return state.ILLEGAL_ROW
        except ColumnError:
            return state.ILLEGAL_COLUMN

    if is_game_over:
        return player  # todo this should return a state

    if x * y == len(game):
        # all game slots have been used.
        return state.DRAW

    return state.INCOMPLETE


def main():
    args = sys.argv
    # specification was to print to stdout
    # we can print to stdout while keeping our unit tests intact. alternative is to test stdout directly.
    print(connectz(args))


if __name__ == "__main__":
    main()
