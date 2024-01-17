field = [["-" for i in range(4)] for j in range(4)]
field[0].pop(0)
field[0].insert(0,"№")

count=1
for row1 in range(1, len(field[0])):
    field[0].remove("-")
    field[0].append(count)
    count+=1

count=1
for col1 in range(1, len(field)):
    field[col1].remove("-")
    field[col1].insert(0, count)
    count+=1

def show_field():
    for row in field:
        print(*row)

x = "X"
o = "0"
game_play = True
def game(player):
    global game_play
    def input_debuger():
        try:
            show_field()
            print(f'\nХод: {player}')
            row = int(input("Введите ряд: "))
            col = int(input("Введите колонку: "))
            if field[row][col] != "-":
                print(f"Поле: {row,col} занято")
                input_debuger()
            else:
                field[row].pop(col)
                field[row].insert(col, player)
        except (ValueError, IndexError):
            print("\nНеверное значение")
            input_debuger()
    input_debuger()

    for row in range(3):
        if field[row][1] == player and field[row][2] == player and field[row][3] == player:
            show_field()
            print(f"Игрок {player} победил")
            game_play = False
            break

    for col in range(3):
        if field[1][col] == player and field[2][col] == player and field[3][col] == player:
            show_field()
            print(f"Игрок {player} победил")
            game_play = False
            break

    if field[1][1] == player and field[2][2] == player and field[3][3] == player:
        show_field()
        print(f"Игрок {player} победил")
        game_play = False
    elif field[3][1] == player and field[2][2] == player and field[1][3] == player:
        show_field()
        print(f"Игрок {player} победил")
        game_play = False

count = 0

while game_play and count < 9:
    game(x)
    count+=1
    if game_play and count < 9:
        game(o)
        count+=1
    elif game_play == True and count == 9:
        show_field()
        print("Ничья")

