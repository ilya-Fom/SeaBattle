import random
def create_board():
    return [['~']*10 for _ in range(10)]
def can_place(board, row, col, size, horizontal):
    if horizontal:
        if col + size > 10:
            return False
        for i in range(max(0,row-1), min(10,row+2)):
            for j in range(max(0,col-1), min(10,col+size+1)):
                if board[i][j] == 'S':
                    return False
    else:
        if row + size > 10:
            return False
        for i in range(max(0,row-1), min(10,row+size+1)):
            for j in range(max(0,col-1), min(10,col+2)):
                if board[i][j] == 'S':
                    return False
    return True
def place_ship(board, row, col, size, horizontal):
    if horizontal:
        for j in range(col, col+size): board[row][j] = 'S'
    else:
        for i in range(row, row+size): board[i][col] = 'S'
def auto_place():
    board, ships = create_board(), [4,3,3,2,2,2,1,1,1,1]
    for size in ships:
        placed, attempts = False, 0
        while not placed and attempts < 1000:
            h = random.choice([True,False])
            r = random.randint(0,9)
            c = random.randint(0,10-size) if h else random.randint(0,9)
            if can_place(board,r,c,size,h):
                place_ship(board,r,c,size,h)
                placed = True
            attempts += 1
        if not placed:
            return None
    return board
def manual_place():
    board, ships = create_board(), [4,3,3,2,2,2,1,1,1,1]
    letters = 'АБВГДЕЖЗИК'
    print("Расстановка кораблей: 1x4, 2x3, 3x2, 4x1")
    print("💡 Пояснение:")
    print("   - Горизонтально: корабль размещается ВПРАВО от выбранной клетки")
    print("   - Вертикально: корабль размещается ВНИЗ от выбранной клетки")
    for size in ships:
        print(f"\nРазместите {size}-клеточный корабль")
        print("   1 2 3 4 5 6 7 8 9 10")
        for i in range(10):
            row = ['S ' if cell=='S'
                   else '~ ' for cell in board[i]]
            row[-1] = row[-1].strip()
            print(f"{letters[i]}  {''.join(row)}")
        while True:
            try:
                row_input = input("Строка (А-К): ").upper()
                if row_input not in letters:
                    print("Неверная строка! Используйте А-К")
                    continue
                r = letters.index(row_input)
                c = int(input("Столбец (1-10): ")) - 1
                if size > 1: 
                    d = input("Горизонтально (г) или вертикально (в)? ").lower()
                    h = d == 'г'
                else:
                    h = True
                if 0<=c<=9 and can_place(board,r,c,size,h):
                    place_ship(board,r,c,size,h)
                    break
                else:
                    print("Нельзя разместить здесь! Корабли не могут касаться.")
            except:
                print("Ошибка ввода!")
    return board
def save_board(board, filename):
    try:
        with open(filename, 'w') as f:
            for row in board: f.write(''.join(row)+'\n')
        return True
    except:
        return False
def main():
    print("1. Авторасстановка\n2. Ручная расстановка")
    choice = input("Выберите: ")
    board = auto_place() if choice == '1' else manual_place()
    if not board:
        return
    letters = 'АБВГДЕЖЗИК'
    print("\nИтоговое расположение:")
    print("   1 2 3 4 5 6 7 8 9 10")
    for i in range(10):
        row = ['S ' if cell=='S' else '~ ' for cell in board[i]]
        row[-1] = row[-1].strip()
        print(f"{letters[i]}  {''.join(row)}")
    filename = input("\nИмя файла для сохранения: ").strip()
    if filename and save_board(board, filename):
        print("Сохранено!")
if __name__ == "__main__":
    main()
