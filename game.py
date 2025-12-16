import random
from utils import *

LETTERS = "АБВГДЕЖЗИК"


class Game:
    """
    Основной класс игры "Морской бой".

    Управляет состоянием игры, ходами игрока и компьютера,
    отображением досок и проверкой победы.

    :ivar player_board: Доска игрока с кораблями.
    :vartype player_board: list[list[str]]
    :ivar computer_board: Доска компьютера с кораблями.
    :vartype computer_board: list[list[str]]
    :ivar player_shots: Список сделанных игроком выстрелов.
    :vartype player_shots: list[tuple[int, int]]
    :ivar computer_shots: Список сделанных компьютером выстрелов.
    :vartype computer_shots: list[tuple[int, int]]
    :ivar hunting: Флаг режима "охоты" компьютера после попадания.
    :vartype hunting: bool
    :ivar last_hit: Координаты последнего попадания компьютера.
    :vartype last_hit: tuple[int, int] | None
    :ivar directions_to_try: Список направлений для стрельбы в режиме охоты.
    :vartype directions_to_try: list[tuple[int, int]]
    :ivar current_direction: Текущее выбранное направление в режиме охоты.
    :vartype current_direction: tuple[int, int] | None
    """

    def __init__(self, board):
        """
        Конструктор класса Game.

        :param board: Готовая доска игрока с расставленными кораблями.
        :type board: list[list[str]]
        """
        self.player_board = board
        self.computer_board = auto_place_computer()
        self.player_shots = []
        self.computer_shots = []

        self.hunting = False
        self.last_hit = None
        self.directions_to_try = []
        self.current_direction = None

    def player_shot(self, r, c):
        """
        Обрабатывает выстрел игрока по компьютеру.

        :param r: Строка выстрела (0-9).
        :type r: int
        :param c: Столбец выстрела (0-9).
        :type c: int
        :returns: True при попадании, False при промахе,
                  None при повторном выстреле в ту же клетку,
                  строка "already_empty" если клетка уже помечена как пустая.
        :rtype: bool | None | str
        """
        if (r, c) in self.player_shots:
            return None

        if self.computer_board[r][c] == "O":
            return "already_empty"

        self.player_shots.append((r, c))
        hit = self.computer_board[r][c] == "S"

        if hit:
            self.computer_board[r][c] = "X"
            cells = find_ship_cells(self.computer_board, r, c)
            if all(self.computer_board[x][y] == "X" for x, y in cells):
                mark_around_sunk(self.computer_board, r, c)
                print("Вы уничтожили корабль!")
        else:
            self.computer_board[r][c] = "O"
        return hit

    def computer_shot(self):
        """
        Обрабатывает выстрел компьютера по игроку.

        Использует стратегию:
        1. Случайная стрельба до первого попадания.
        2. После попадания — режим "охоты" с поиском в соседних клетках.
        3. После потопления корабля — сброс режима охоты.

        :returns: Кортеж (r, c, hit, sunk) — координаты выстрела,
                  флаг попадания, флаг потопления корабля.
        :rtype: tuple[int, int, bool, bool]
        """
        if not self.hunting:
            while True:
                r = random.randint(0, 9)
                c = random.randint(0, 9)
                if (r, c) not in self.computer_shots:
                    break
        else:
            if not self.directions_to_try:
                self.directions_to_try = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(self.directions_to_try)

            found = False
            for dr, dc in self.directions_to_try:
                start_r, start_c = self.last_hit
                nr, nc = start_r + dr, start_c + dc

                if (
                    0 <= nr < 10
                    and 0 <= nc < 10
                    and (nr, nc) not in self.computer_shots
                ):
                    r, c = nr, nc
                    found = True
                    self.current_direction = (dr, dc)
                    break

            if not found:
                self.hunting = False
                self.last_hit = None
                self.directions_to_try = []
                self.current_direction = None
                return self.computer_shot()

        self.computer_shots.append((r, c))
        hit = self.player_board[r][c] == "S"

        if hit:
            self.player_board[r][c] = "X"

            if not self.hunting:
                self.hunting = True
                self.last_hit = (r, c)
                self.directions_to_try = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(self.directions_to_try)
                self.current_direction = None
            else:
                self.last_hit = (r, c)

                if self.current_direction:
                    self.directions_to_try = [self.current_direction]
                    opposite_dir = (
                        -self.current_direction[0],
                        -self.current_direction[1],
                    )
                    if opposite_dir not in self.directions_to_try:
                        self.directions_to_try.append(opposite_dir)

            ship_cells = find_ship_cells(self.player_board, r, c)
            sunk = all(self.player_board[x][y] == "X" for x, y in ship_cells)

            if sunk:
                mark_around_sunk(self.player_board, r, c)
                self.hunting = False
                self.last_hit = None
                self.directions_to_try = []
                self.current_direction = None

            return r, c, hit, sunk

        else:
            self.player_board[r][c] = "O"

            if self.hunting and self.current_direction:
                if self.current_direction in self.directions_to_try:
                    self.directions_to_try.remove(self.current_direction)
                self.current_direction = None

            return r, c, hit, False

    def print_boards(self):
        """
        Выводит в консоль текущее состояние обеих досок: игрока и компьютера.

        Отображает:
        - Доску игрока с кораблями ('S'), попаданиями ('X') и промахами ('O').
        - Доску компьютера с видимыми для игрока попаданиями ('X') и промахами ('O').
        - Счётчик оставшихся кораблей у игрока и компьютера.
        """
        print("\n" + "=" * 60)
        print("ВАШЕ ПОЛЕ".center(28) + " | " + "КОМПЬЮТЕР".center(28))
        print("    1 2 3 4 5 6 7 8 9 10      1 2 3 4 5 6 7 8 9 10")

        for i in range(10):
            left = []
            for cell in self.player_board[i]:
                if cell == "S":
                    left.append("S ")
                elif cell == "X":
                    left.append("X ")
                elif cell == "O":
                    left.append("O ")
                else:
                    left.append("~ ")

            right = []
            for j in range(10):
                if self.computer_board[i][j] == "X":
                    right.append("X ")
                elif self.computer_board[i][j] == "O":
                    right.append("O ")
                elif (i, j) in self.player_shots:
                    right.append("O ")
                else:
                    right.append("~ ")

            print(
                f"{LETTERS[i]} | {''.join(left).rstrip()} | {LETTERS[i]} | {''.join(right).rstrip()}"
            )

        player_ships = count_ships(self.player_board)
        computer_ships = count_ships(self.computer_board)
        print(f"\nВаши корабли: {player_ships}/10 | Корабли противника: {computer_ships}/10")


def main():
    """
    Основная функция игры.

    Запускает игровой цикл, обрабатывает ввод пользователя,
    координирует ходы игрока и компьютера до победы одного из них.
    """
    filename = input("Введите имя файла с расстановкой: ").strip()
    board = load_board(filename)

    if board is None:
        print("Ошибка загрузки файла!")
        return

    game = Game(board)
    player_turn = True

    while True:
        game.print_boards()

        if count_ships(game.player_board) == 0:
            print("\n💀 КОМПЬЮТЕР ПОБЕДИЛ!")
            break
        if count_ships(game.computer_board) == 0:
            print("\n🎉 ВЫ ПОБЕДИЛИ!")
            break

        if player_turn:
            while True:
                try:
                    row = input("\nВаш ход - строка (А-К): ").upper().strip()
                    if not row:
                        print("Ошибка! Введите букву от А до К.")
                        continue

                    if row not in LETTERS:
                        print("Ошибка! Используйте буквы от А до К.")
                        continue

                    col_str = input("Ваш ход - столбец (1-10): ").strip()
                    if not col_str:
                        print("Ошибка! Введите число от 1 до 10.")
                        continue

                    col = int(col_str)

                    pos = coord_to_index(row, col)

                    if pos is None:
                        print("Ошибка координат! Строка: А-К, столбец: 1-10.")
                        continue

                    r, c = pos
                    result = game.player_shot(r, c)

                    if result is None:
                        print("Уже стреляли сюда!")
                        continue
                    elif result == "already_empty":
                        print("Эта клетка уже отмечена как пустая!")
                        continue
                    elif result:
                        print("✅ Попадание! Стреляйте еще!")
                        if count_ships(game.computer_board) == 0:
                            break
                        game.print_boards()
                        continue
                    else:
                        print("💦 Промах!")
                        player_turn = False
                        break

                except ValueError:
                    print("Ошибка! Введите число от 1 до 10.")
                    continue
                except KeyboardInterrupt:
                    print("\nИгра прервана.")
                    return
                except Exception:
                    print("Неожиданная ошибка.")
                    continue
        else:
            computer_turn = True
            while computer_turn:
                print("\nХод компьютера...")
                rr, cc, hit, sunk = game.computer_shot()
                print(f"Компьютер стреляет в ({LETTERS[rr]},{cc + 1})")

                if hit:
                    if sunk:
                        print("💥 Попал! Корабль потоплен!")
                        game.print_boards()
                        if count_ships(game.player_board) == 0:
                            break
                        continue
                    else:
                        print("💥 Попал! Стреляет еще!")
                        if count_ships(game.player_board) == 0:
                            break
                        game.print_boards()
                        continue
                else:
                    print("💦 Промах!")

                computer_turn = False

            player_turn = True


if __name__ == "__main__":
    main()
