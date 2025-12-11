import unittest
from utils import create_board, can_place, place_ship, count_ships


class TestBattleship(unittest.TestCase):
    def test_create_board(self):
        board = create_board()
        self.assertEqual(len(board), 10)
        self.assertEqual(len(board[0]), 10)
        self.assertEqual(board[0][0], '~')

    def test_can_place(self):
        board = create_board()
        self.assertTrue(can_place(board, 0, 0, 3, True))
        place_ship(board, 0, 0, 3, True)
        self.assertFalse(can_place(board, 0, 0, 3, True))

    def test_count_ships(self):
        board = create_board()
        self.assertEqual(count_ships(board), 0)
        place_ship(board, 0, 0, 3, True)
        self.assertEqual(count_ships(board), 1)


if __name__ == '__main__':
    unittest.main()
