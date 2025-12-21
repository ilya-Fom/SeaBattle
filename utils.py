import random

LETTERS = "АБВГДЕЖЗИК"


def create_board():
    """
    Создаёт пустую игровую доску размером 10x10.

    :returns: Двумерный список 10x10, заполненный символом '~'.
    :rtype: list[list[str]]
    """
    return [["~"] * 10 for _ in range(10)]


def can_place(board, row, col, size, horizontal):
    """
    Проверяет, можно ли разместить корабль заданного размера в указанной позиции.

    :param board: Игровая доска.
    :type board: list[list[str]]
    :param row: Начальная строка (0-9).
    :type row: int
    :param col: Начальный столбец (0-9).
    :type col: int
    :param size: Длина корабля.
    :type size: int
    :param horizontal: Ориентация корабля (True — горизонтально, False — вертикально).
    :type horizontal: bool
    :returns: True, если размещение возможно, иначе False.
    :rtype: bool
    :raises: Никаких исключений не выбрасывается.
    """
    if horizontal:
        if col + size > 10:
            return False
        for i in range(max(0, row - 1), min(10, row + 2)):
            for j in range(max(0, col - 1), min(10, col + size + 1)):
                if board[i][j] == "S":
                    return False
    else:
        if row + size > 10:
            return False
        for i in range(max(0, row - 1), min(10, row + size + 1)):
            for j in range(max(0, col - 1), min(10, col + 2)):
                if board[i][j] == "S":
                    return False
    return True


def place_ship(board, row, col, size, horizontal):
    """
    Размещает корабль на доске в указанной позиции.

    :param board: Игровая доска.
    :type board: list[list[str]]
    :param row: Начальная строка (0-9).
    :type row: int
    :param col: Начальный столбец (0-9).
    :type col: int
    :param size: Длина корабля.
    :type size: int
    :param horizontal: Ориентация корабля (True — горизонтально, False — вертикально).
    :type horizontal: bool
    :returns: None (функция изменяет переданную доску).
    :rtype: None
    :raises: Никаких исключений не выбрасывается.
    """
    if horizontal:
        for j in range(col, col + size):
            board[row][j] = "S"
    else:
        for i in range(row, row + size):
            board[i][col] = "S"


def find_ship_cells(board, row, col):
    """
    Находит все клетки корабля, содержащего указанную клетку, с помощью поиска в глубину.

    :param board: Игровая доска.
    :type board: list[list[str]]
    :param row: Строка начальной клетки.
    :type row: int
    :param col: Столбец начальной клетки.
    :type col: int
    :returns: Список координат (row, col) всех клеток корабля.
    :rtype: list[tuple[int, int]]
    :raises: Никаких исключений не выбрасывается.
    """
    cells = []
    stack = [(row, col)]
    visited = set()

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if board[r][c] in ["S", "X"]:
            cells.append((r, c))
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in visited:
                    stack.append((nr, nc))

    return cells


def mark_around_sunk(board, row, col):
    """
    Помечает клетки вокруг потопленного корабля как промахи ('O').

    :param board: Игровая доска.
    :type board: list[list[str]]
    :param row: Строка любой клетки потопленного корабля.
    :type row: int
    :param col: Столбец любой клетки потопленного корабля.
    :type col: int
    :returns: None (функция изменяет переданную доску).
    :rtype: None
    :raises: Никаких исключений не выбрасывается.
    """
    cells = find_ship_cells(board, row, col)

    for r, c in cells:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 10 and 0 <= nc < 10 and board[nr][nc] == "~":
                    board[nr][nc] = "O"


def count_ships(board):
    """
    Подсчитывает количество кораблей на доске.

    :param board: Игровая доска.
    :type board: list[list[str]]
    :returns: Количество кораблей (целое число).
    :rtype: int
    :raises: Никаких исключений не выбрасывается.
    """
    visited = set()
    count = 0

    for i in range(10):
        for j in range(10):
            if board[i][j] == "S" and (i, j) not in visited:
                count += 1
                stack = [(i, j)]
                while stack:
                    r, c = stack.pop()
                    if (r, c) in visited:
                        continue
                    visited.add((r, c))
                    if board[r][c] == "S":
                        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in visited:
                                stack.append((nr, nc))

    return count


def coord_to_index(letter, number):
    """
    Преобразует буквенно-цифровые координаты в индексы строки и столбца.

    :param letter: Буква строки (от 'А' до 'К').
    :type letter: str
    :param number: Номер столбца (от 1 до 10).
    :type number: int | float
    :returns: Кортеж (row, col) или None, если координаты некорректны.
    :rtype: tuple[int, int] | None
    :raises: Никаких исключений не выбрасывается.
    """
    if not letter:
        return None
    if not isinstance(number, int):
        return None

    letter = letter.upper().strip()

    if letter not in LETTERS:
        return None
    if not 1 <= number <= 10:
        return None

    return (LETTERS.index(letter), int(number) - 1)


def auto_place_computer():
    """
    Автоматически расставляет корабли для компьютера.

    :returns: Игровая доска с расставленными кораблями или None, если расстановка не удалась.
    :rtype: list[list[str]] | None
    :raises: Никаких исключений не выбрасывается.
    """
    board = create_board()
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    for size in ships:
        placed = False
        attempts = 0
        while not placed and attempts < 1000:
            h = random.choice([True, False])
            r = random.randint(0, 9)
            c = random.randint(0, 10 - size) if h else random.randint(0, 9)

            if can_place(board, r, c, size, h):
                place_ship(board, r, c, size, h)
                placed = True
            attempts += 1

        if not placed:
            return None

    return board


def load_board(filename):
    """
    Загружает доску из файла.

    :param filename: Имя файла для загрузки.
    :type filename: str
    :returns: Загруженная доска или None, если произошла ошибка.
    :rtype: list[list[str]] | None
    :raises: Исключения перехватываются внутри функции.
    """
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f]

        if len(lines) != 10:
            return None

        board = []
        for line in lines:
            if len(line) != 10:
                return None
            row = list(line)
            for cell in row:
                if cell not in ["~", "S"]:
                    return None
            board.append(row)

        return board
    except:
        return None


def save_board(board, filename):
    """
    Сохраняет доску в файл.

    :param board: Игровая доска.
    :type board: list[list[str]]
    :param filename: Имя файла для сохранения.
    :type filename: str
    :returns: True, если сохранение успешно.
    :rtype: bool
    :raises IOError: При ошибке записи в файл.
    :raises ValueError: Если board не является корректной доской.
    """
    # Проверка корректности доски
    if not isinstance(board, list) or len(board) != 10:
        raise ValueError("Доска должна быть списком из 10 строк")

    for row in board:
        if not isinstance(row, list) or len(row) != 10:
            raise ValueError("Каждая строка доски должна быть списком из 10 символов")
        for cell in row:
            if cell not in ['~', 'S', 'X', 'O']:
                raise ValueError(f"Недопустимый символ в доске: '{cell}'")

    # Попытка записи
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for row in board:
                f.write("".join(row) + "\n")
        return True
    except (IOError, OSError, PermissionError) as e:
        # Преобразуем файловые ошибки в наше исключение
        raise IOError(f"Ошибка записи в файл '{filename}': {str(e)}")
