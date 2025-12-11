from utils import *


def manual_place():
    """
    Ручная расстановка кораблей на доске через консольный интерфейс.

    :returns: Доска с расставленными кораблями.
    :rtype: list[list[str]]
    """
    board = create_board()
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    print("Расстановка кораблей: 1×4, 2×3, 3×2, 4×1\n")

    for size in ships:
        while True:
            print_board(board)
            print(f"Разместите корабль длиной {size}")

            try:
                row_input = input("Строка (А-К): ").upper().strip()
                if not row_input or row_input not in LETTERS:
                    print("Ошибка! Используйте буквы А-К.")
                    continue

                r = LETTERS.index(row_input)

                col_str = input("Столбец (1-10): ").strip()
                if not col_str:
                    print("Ошибка! Введите число от 1 до 10.")
                    continue

                c = int(col_str) - 1

                if not 0 <= c <= 9:
                    print("Ошибка! Столбец от 1 до 10.")
                    continue

                if size > 1:
                    d = input("Горизонтально (г) или вертикально (в)? ").lower().strip()
                    if not d or d not in ["г", "в"]:
                        print("Ошибка! Введите 'г' или 'в'.")
                        continue
                    h = d == "г"
                else:
                    h = True

                if can_place(board, r, c, size, h):
                    place_ship(board, r, c, size, h)
                    break
                else:
                    print("Нельзя разместить здесь! Корабли не должны касаться.")
            except ValueError:
                print("Ошибка! Введите корректное число.")
                continue
            except Exception:
                print("Ошибка ввода!")
                continue

    return board


def auto_place_player():
    """
    Автоматическая расстановка кораблей для игрока.

    :returns: Доска с автоматически расставленными кораблями или None при ошибке.
    :rtype: list[list[str]] | None
    """
    return auto_place_computer()


def print_board(board):
    """
    Выводит игровую доску в консоль в читаемом формате.

    :param board: Игровая доска для отображения.
    :type board: list[list[str]]
    """
    print("\n   1 2 3 4 5 6 7 8 9 10")
    for i in range(10):
        row_str = " ".join(board[i])
        print(f"{LETTERS[i]}  {row_str}")
    print()


def main():
    """
    Основная функция модуля setup.

    Предлагает пользователю выбрать способ расстановки кораблей
    (автоматический или ручной), сохраняет результат в файл.
    """
    while True:
        print("1. Автоматическая расстановка")
        print("2. Ручная расстановка")
        choice = input("Выберите вариант: ").strip()

        if choice == "1":
            board = auto_place_player()
            if board is None:
                print("Не удалось автоматически расставить корабли. Попробуйте еще раз.")
                return
            break
        elif choice == "2":
            board = manual_place()
            break
        else:
            print("Ошибка! Введите 1 или 2.")
            continue

    print_board(board)

    while True:
        filename = input("Введите имя файла для сохранения: ").strip()
        if not filename:
            print("Ошибка! Введите имя файла.")
            continue

        if save_board(board, filename):
            print(f"Расстановка сохранена в файл {filename}")
            break
        else:
            print("Ошибка сохранения! Попробуйте другое имя файла.")


if __name__ == "__main__":
    main()
