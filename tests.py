import constants as state
import unittest

from connectz import connectz
from connectz import GameBoard


class TestConnectZWithGames(unittest.TestCase):
    '''
    Supplied test cases
    '''

    def setUp(self):
        self.args = ['connectz']

    def tearDown(self):
        pass

    def test_draw(self):
        self.args.append('testcases/draw.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.DRAW)

    def test_p1_wins(self):
        self.args.append('testcases/player1_win.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.PLAYER_ONE_WIN)

    def test_p2_wins(self):
        self.args.append('testcases/player2_win.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.PLAYER_TWO_WIN)

    def test_illegal_column(self):
        self.args.append('testcases/illegal_column.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.ILLEGAL_COLUMN)

    def test_illegal_continue(self):
        self.args.append('testcases/illegal_continue.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.ILLEGAL_CONTINUE)

    def test_illegal_game(self):
        self.args.append('testcases/illegal_game.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.ILLEGAL_GAME)

    def test_illegal_row(self):
        self.args.append('testcases/illegal_row.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.ILLEGAL_ROW)

    def test_incomplete_game(self):
        self.args.append('testcases/incomplete.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.INCOMPLETE)

    def test_invalid_file(self):
        self.args.append('testcases/invalid_file.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.INVALID_FILE)

    def test_another_invalid_file(self):
        self.args.append('testcases/invalid_file_2.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.INVALID_FILE)

    def test_non_existant_file(self):
        self.args.append('testcases/xxxx.txt')
        result = connectz(self.args)
        self.assertEqual(result, state.FILE_DOESNT_EXIST)

    def test_returns_error_when_no_arguments_passed(self):
        result = connectz(self.args)
        self.assertEqual(result, state.INCORRECT_ARGUMENTS)


class TestGameBoard(unittest.TestCase):
    '''
    Logic test cases
    '''
    def setUp(self):
        self.p1 = 1
        self.p2 = 2

    def test_game_board_add_to_column_will_fill_up_column(self):
        gb = GameBoard(4, 4, 2)
        gb.add_to_column(1, self.p1)
        self.assertEqual(gb.grid[1][0], self.p1)

        gb.add_to_column(1, self.p1)
        self.assertEqual(gb.grid[1][1], self.p1)

    def test_non_win(self):
        gb = GameBoard(4, 4, 4)
        gb.grid = [[1, 1, 1], [2, 2, 2], [], []]
        game_state = gb.add_to_column(3, self.p1)
        self.assertEqual(game_state, False)

    def test_simple_vertical_win_for_p1(self):
        gb = GameBoard(4, 4, 4)
        gb.grid = [[1, 1, 1], [2, 2, 2], [], []]
        game_state = gb.add_to_column(0, self.p1)
        self.assertEqual(game_state, True)

    def test_simple_vertical_win_for_p2(self):
        gb = GameBoard(4, 4, 4)
        gb.grid = [[1, 1, 1], [2, 2, 2], [], []]
        game_state = gb.add_to_column(1, self.p2)
        self.assertEqual(game_state, True)

    def test_simple_horizonal_win_for_p1(self):
        gb = GameBoard(4, 4, 4)
        gb.grid = [[], [1], [1], [1]]
        game_state = gb.add_to_column(0, self.p1)
        self.assertEqual(game_state, True)

    def test_diagonal_win_for_p1(self):
        gb = GameBoard(4, 4, 4)
        gb.grid = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0]]
        game_state = gb.add_to_column(3, self.p1)
        self.assertEqual(game_state, True)

    def test_diagonal_non_win_for_p2(self):
        gb = GameBoard(4, 4, 4)
        gb.grid = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0]]
        game_state = gb.add_to_column(3, self.p2)
        self.assertEqual(game_state, False)

    def test_reverse_diagonal_win_for_p1(self):
        gb = GameBoard(4, 4, 4)
        gb.grid = [[0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
        game_state = gb.add_to_column(0, self.p1)
        self.assertEqual(game_state, True)

    def test_a_horizonal_win_for_p2_and_test_game_state_changes_with_final_move(self):
        gb = GameBoard(4, 4, 4)
        gb.grid = [[0], [0], [0], [0]]
        game_state = gb.add_to_column(0, self.p2)
        self.assertEqual(game_state, False)
        game_state = gb.add_to_column(1, self.p2)
        self.assertEqual(game_state, False)
        game_state = gb.add_to_column(2, self.p2)
        self.assertEqual(game_state, False)
        game_state = gb.add_to_column(3, self.p2)
        self.assertEqual(game_state, True)


if __name__ == '__main__':
    unittest.main()
