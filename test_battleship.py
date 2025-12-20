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

    def test_coord_to_index_invalid(self):
        """Тестирование некорректных координат"""
        from utils import coord_to_index
        # Неверная буква
        self.assertIsNone(coord_to_index('Л', 5))
        # Неверное число (меньше 1)
        self.assertIsNone(coord_to_index('А', 0))
        # Неверное число (больше 10)
        self.assertIsNone(coord_to_index('А', 11))
        # Пустая строка
        self.assertIsNone(coord_to_index('', 5))
        # Не число (передаём строку)
        self.assertIsNone(coord_to_index('А', 'не число'))
        
    def test_save_board_raises_exceptions(self):
        """Тест на выброс исключений в save_board"""
        board = create_board()
        
        # 1. Неверный тип доски (не список)
        with self.assertRaises(ValueError):
            save_board("не доска", "test.txt")
        
        # 2. Доска неправильного размера
        with self.assertRaises(ValueError):
            save_board([['~'] * 10] * 8, "test.txt")  # 8 строк вместо 10
        
        # 3. Строка неправильного размера
        bad_board = [['~'] * 8 for _ in range(10)]  # 8 столбцов вместо 10
        with self.assertRaises(ValueError):
            save_board(bad_board, "test.txt")
        
        # 4. Недопустимый символ в доске
        bad_board = create_board()
        bad_board[0][0] = 'Z'  # Неправильный символ
        with self.assertRaises(ValueError):
            save_board(bad_board, "test.txt")
        
        # 5. Ошибка записи в файл (системная папка)
        with self.assertRaises(IOError):
            if os.name == 'posix':  # Linux/Mac
                save_board(board, "/root/test.txt")
            else:  # Windows
                save_board(board, "C:\\Windows\\System32\\test.txt")


if __name__ == '__main__':
    unittest.main()
