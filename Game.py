import random

class Game:
    """Основной класс, реализующий логику игры "Морской бой" """
    def __init__(self):
        self.player_board = []
        self.computer_board = [['~'] * 10 for _ in range(10)]
        self.computer_shots = []
        self.player_shots = []
        self.last_hit = None
        self.hunting = False
        self.hunt_direction = None
        self.letters = 'АБВГДЕЖЗИК'

    def load_board(self, filename):
        try:
            with open(filename, 'r') as f:
                self.player_board = [list(line.strip()) for line in f]
            return len(self.player_board) == 10
        except:
            return False

    def place_computer_ships(self):
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for size in ships:
            placed = False
            while not placed:
                h = random.choice([True, False])
                r = random.randint(0, 10 - size) if not h else random.randint(0, 9)
                c = random.randint(0, 10 - size) if h else random.randint(0, 9)
                if self.can_place(self.computer_board, r, c, size, h):
                    self.place_ship(self.computer_board, r, c, size, h)
                    placed = True
        return True

    def can_place(self, board, row, col, size, horizontal):
        if horizontal:
            if col + size > 10: return False
            for i in range(max(0, row - 1), min(10, row + 2)):
                for j in range(max(0, col - 1), min(10, col + size + 1)):
                    if board[i][j] == 'S': return False
        else:
            if row + size > 10: return False
            for i in range(max(0, row - 1), min(10, row + size + 1)):
                for j in range(max(0, col - 1), min(10, col + 2)):
                    if board[i][j] == 'S': return False
        return True

    def place_ship(self, board, row, col, size, horizontal):
        if horizontal:
            for j in range(col, col + size): board[row][j] = 'S'
        else:
            for i in range(row, row + size): board[i][col] = 'S'

    def mark_around_sunk(self, board, row, col):
        cells = self.find_ship_cells(board, row, col)
        for r, c in cells:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 10 and 0 <= nc < 10 and board[nr][nc] == '~':
                        board[nr][nc] = 'O'

    def find_ship_cells(self, board, row, col):
        cells, stack = [], [(row, col)]
        visited = set()
        while stack:
            r, c = stack.pop()
            if (r, c) in visited: continue
            visited.add((r, c))
            if board[r][c] in ['S', 'X']:
                cells.append((r, c))
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in visited:
                        stack.append((nr, nc))
        return cells

    def count_ships(self, board):
        visited, count = set(), 0
        for i in range(10):
            for j in range(10):
                if board[i][j] == 'S' and (i, j) not in visited:
                    count += 1
                    stack = [(i, j)]
                    while stack:
                        r, c = stack.pop()
                        if (r, c) in visited: continue
                        visited.add((r, c))
                        if board[r][c] == 'S':
                            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                                nr, nc = r + dr, c + dc
                                if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in visited:
                                    stack.append((nr, nc))
        return count

    def computer_shot(self):
        if not self.hunting:
            # Стратегия "шахматная доска" для поиска кораблей
            targets = []
            for i in range(10):
                for j in range(10):
                    if (i + j) % 2 == 0 and (i, j) not in self.computer_shots:
                        targets.append((i, j))

            if targets:
                r, c = random.choice(targets)
            else:
                # Если все клетки шашматного порядка проверены, стреляем в любую
                while True:
                    r = random.randint(0, 9)
                    c = random.randint(0, 9)
                    if (r, c) not in self.computer_shots: break
        else:
            # Режим охоты - добиваем раненый корабль
            r, c = self.last_hit

            if not self.hunt_direction:
                # Ищем направление корабля
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                found = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in self.computer_shots:
                        # Проверяем, есть ли продолжение корабля в этом направлении
                        if self.player_board[nr][nc] == 'X':
                            # Уже есть попадание в этом направлении - продолжаем его
                            r, c = nr + dr, nc + dc
                            self.hunt_direction = (dr, dc)
                            found = True
                            break

                if not found:
                    # Пробуем все направления вокруг попадания
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in self.computer_shots:
                            r, c = nr, nc
                            self.hunt_direction = (dr, dc)
                            found = True
                            break

                if not found:
                    self.hunting = False
                    self.hunt_direction = None
                    return self.computer_shot()
            else:
                # Продолжаем в найденном направлении
                dr, dc = self.hunt_direction
                nr, nc = r + dr, c + dc

                # Проверяем границы и нестрелянные клетки
                if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in self.computer_shots:
                    r, c = nr, nc
                else:
                    # Меняем направление на противоположное от начальной точки
                    self.hunt_direction = (-self.hunt_direction[0], -self.hunt_direction[1])
                    dr, dc = self.hunt_direction
                    r, c = self.last_hit
                    nr, nc = r + dr, c + dc

                    if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in self.computer_shots:
                        r, c = nr, nc
                    else:
                        # Не можем стрелять в этом направлении - сбрасываем охоту
                        self.hunting = False
                        self.hunt_direction = None
                        return self.computer_shot()

        self.computer_shots.append((r, c))
        hit = self.player_board[r][c] == 'S'

        if hit:
            self.player_board[r][c] = 'X'
            self.last_hit = (r, c)
            self.hunting = True

            # Проверяем потоплен ли корабль
            ship_cells = self.find_ship_cells(self.player_board, r, c)
            if all(self.player_board[x][y] == 'X' for x, y in ship_cells):
                self.mark_around_sunk(self.player_board, r, c)
                self.hunting = False
                self.hunt_direction = None
                self.last_hit = None
                print("Компьютер потопил ваш корабль!")
        else:
            self.player_board[r][c] = 'O'
            # Если промах в режиме охоты - меняем направление
            if self.hunting and self.hunt_direction:
                self.hunt_direction = (-self.hunt_direction[0], -self.hunt_direction[1])

        return r, c, hit

    def player_shot(self, row, col):
        if (row, col) in self.player_shots: return None
        self.player_shots.append((row, col))
        hit = self.computer_board[row][col] == 'S'

        if hit:
            self.computer_board[row][col] = 'X'

            # Проверяем потоплен ли корабль и помечаем клетки вокруг
            ship_cells = self.find_ship_cells(self.computer_board, row, col)
            if all(self.computer_board[x][y] == 'X' for x, y in ship_cells):
                self.mark_around_sunk(self.computer_board, row, col)
                print("Вы потопили корабль!")
        else:
            self.computer_board[row][col] = 'O'

        return hit

    def display_boards(self):
        print("\n" + "=" * 55)
        print("ВАШЕ ПОЛЕ".center(27) + "|" + "ПРОТИВНИК".center(27))
        print("    1 2 3 4 5 6 7 8 9 10        1 2 3 4 5 6 7 8 9 10")
        print("   ─────────────────────       ─────────────────────")

        for i in range(10):
            # Левое поле (игрок) - показываем ВСЕ клетки, включая 'O' вокруг потопленных
            left = []
            for cell in self.player_board[i]:
                if cell == 'S':
                    left.append('S ')
                elif cell == 'X':
                    left.append('X ')
                elif cell == 'O':
                    left.append('O ')
                else:
                    left.append('~ ')
            left[-1] = left[-1].strip()

            # Правое поле (компьютер) - показываем ВСЕ клетки, включая 'O' вокруг потопленных
            right = []
            for j in range(10):
                # Показываем ВСЕ состояния клетки на поле противника
                if self.computer_board[i][j] == 'X':
                    right.append('X ')
                elif self.computer_board[i][j] == 'O':
                    right.append('O ')
                elif (i, j) in self.player_shots:
                    right.append('~ ')  # Промах, но клетка пустая
                else:
                    right.append('~ ')  # Не стреляли
            right[-1] = right[-1].strip()

            print(f"{self.letters[i]} │ {''.join(left)} │   {self.letters[i]} │ {''.join(right)} │")

        player_ships = self.count_ships(self.player_board)
        computer_ships = self.count_ships(self.computer_board)
        print(f"\nТвои корабли: {player_ships}/10 | Корабли противника: {computer_ships}/10")


def main():
    game = Game()

    while True:
        filename = input("Введите имя файла с расстановкой: ").strip()
        if game.load_board(filename): break
        print("Файл не найден!")

    print("Компьютер расставляет корабли...")
    game.place_computer_ships()

    while True:
        game.display_boards()

        if game.count_ships(game.player_board) == 0:
            print("\n💀 КОМПЬЮТЕР ПОБЕДИЛ!");
            break
        if game.count_ships(game.computer_board) == 0:
            print("\n🎉 ВЫ ПОБЕДИЛИ!");
            break

        # Ход игрока
        player_turn = True
        while player_turn:
            try:
                row_input = input("\nТвой ход - строка (А-К): ").upper()
                if row_input not in game.letters:
                    print("Неверная строка! Используйте А-К")
                    continue
                r = game.letters.index(row_input)
                c = int(input("Твой ход - столбец (1-10): ")) - 1
                if 0 <= c <= 9:
                    result = game.player_shot(r, c)
                    if result is None:
                        print("Уже стреляли сюда!")
                        continue
                    if result:
                        print("✅ Попадание! Стреляйте еще!")
                        game.display_boards()
                        if game.count_ships(game.computer_board) == 0:
                            print("\n🎉 ВЫ ПОБЕДИЛИ!")
                            return
                    else:
                        print("💦 Промах!")
                        player_turn = False
                else:
                    print("Столбец от 1 до 10!")
            except:
                print("Ошибка ввода!")

        # Ход компьютера
        computer_turn = True
        while computer_turn:
            print("\nХод компьютера...")
            r, c, hit = game.computer_shot()
            print(f"Компьютер стреляет в ({game.letters[r]},{c + 1})")
            if hit:
                print("💥 Попал! Стреляет еще!")
                game.display_boards()
                if game.count_ships(game.player_board) == 0:
                    print("\n💀 КОМПЬЮТЕР ПОБЕДИЛ!")
                    return
            else:
                print("💦 Промах!")
                computer_turn = False


if __name__ == "__main__":
    main()
