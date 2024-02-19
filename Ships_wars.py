import random
import time
class GameWarringExeption(Exception):
    pass
class CoordError(GameWarringExeption):
    pass
class CoordOutError(Exception):
    pass
class MoveError(GameWarringExeption):
    pass

class Dot:
    def __init__(self):
        self.allow_coords = [(x, y + 1) for y in range(6) for x in range(1, 7)]  # список всех возможных координат для поля

    def get_coord(self):  # случайно выбирает координату из списка
        self.random_coord = random.choice(self.allow_coords)
        return self.random_coord[0], self.random_coord[1]

    def reborn_allow_coords(self):  # заново создает список возможных координат
        self.allow_coords = [(x, y + 1) for y in range(6) for x in range(1, 7)]
        return self.allow_coords

class Ship:
    ship_coords = []

    def __init__(self, coord, lenght, rotation):
        self.coord = coord
        self.lenght = lenght
        self.rotation = rotation

    def set_ship_coords(self):  # отррисовка координат корабля
        Ship.ship_coords = []
        __cur_x = self.coord[0]
        __cur_y = self.coord[1]
        Ship.ship_coords.append((__cur_x, __cur_y))

        for l in range(1, self.lenght):
            if self.rotation == 0:
                __cur_x += 1
            elif self.rotation == 1:
                __cur_y += 1
            Ship.ship_coords.append((__cur_x, __cur_y))
        return Ship.ship_coords

class Field:
    def __init__(self, hide=False):  # создание поля
        self.ships = []
        self.ships_copy = []
        self.hide = hide
        self.busy_cells = []

        self.field = [['0' for i in range(7)] for j in range(7)]

        self.field[0].pop(0)
        self.field[0].insert(0, "№")

        count = 1
        for row1 in range(1, len(self.field[0])):
            self.field[0].remove("0")
            self.field[0].append(count)
            count += 1

        count = 1
        for col1 in range(1, len(self.field)):
            self.field[col1].remove("0")
            self.field[col1].insert(0, count)
            count += 1

    def in_range(self, coord: tuple):  # Возвращает True если в диапазоне от 1 до 6
        return 1 <= coord[0] <= 6 and 1 <= coord[1] <= 6

    def around_ship(self, coord: tuple, coord_ship=None, player=None,
                    draw_dead_ship=False):  # занимает клетки вокруг корабля или отрисовывает "промахи" если draw_dead_ship равна True
        around_zone = [(-1, 0),
                       (0, -1), (0, 0), (0, 1),
                       (1, 0)]

        for zx, zy in around_zone:
            cur_around = (coord[0] + zx, coord[1] + zy)
            if not (self.in_range(cur_around)):
                continue
            elif cur_around in Ship.ship_coords:
                continue

            if draw_dead_ship and cur_around != coord and not (cur_around in coord_ship):
                self.field[cur_around[0]][cur_around[1]] = "T"
                player.append((cur_around[0], cur_around[1]))
            else:
                self.busy_cells.append(cur_around)
        return self.busy_cells

    def draw_ship(self, l):  # цикл отрисовки 1 корабля
        try:
            ship = Ship(Game.gen.get_coord(), l, random.randint(0, 1))
            ship.set_ship_coords()

            for coord in Ship.ship_coords:  # Проверка созданного корабля: попадает в предел поля и не залезает на другие корабли и их зоны
                if (self.in_range(coord)) and not (coord in self.busy_cells):
                    continue
                else:
                    raise GameWarringExeption

            for coord in Ship.ship_coords:  # Добавляет корабль в список ships если все хорошо
                self.around_ship(coord)
                self.busy_cells.append(coord)
            self.ships.append(Ship.ship_coords)

            for coord in self.busy_cells:  # Все координаты занятые кораблем, включая зону  вокруг них, удаляются из allow_coords
                if coord in Game.gen.allow_coords:
                    Game.gen.allow_coords.remove(coord)

        except GameWarringExeption:
            self.draw_ship(l)

    def set_ships(self):  # цикл отрисовки всех кораблей

        for l in [3, 2, 2, 1, 1, 1, 1]:
            self.draw_ship(l)

        for i, count_list in zip(self.ships, range(0, len(self.ships))):  # Создание независимой копии списка ships
            self.ships_copy.append([])
            for j, count in zip(i, range(0, len(i))):
                coord1 = j[0]
                coord2 = j[1]
                self.ships_copy[count_list].append((coord1, coord2))

        Game.gen.reborn_allow_coords()  # Перегенерация списка allow_coords

        for ship in self.ships:  # Установка на поле кораблей
            for coord in ship:
                if self.hide == False:
                    self.field[coord[0]][coord[1]] = "*"
        return self.ships


class Player:
    def __init__(self, yourself_field, enemy_field):
        self.yourself_field = yourself_field
        self.enemy_field = enemy_field

        self.move_list = []
        self.enemy_count_ship = 7

    def create_field(self, hide=False):
        self.yourself_field.set_ships()
        self.enemy_field.set_ships()

    def verify_shot(self, move: tuple):
        for ship, i_ship in zip(self.enemy_field.ships, range(len(self.enemy_field.ships))):  # Проверка на попадание
            if move in ship:
                self.enemy_field.field[move[0]][move[1]] = "X"

                for coord, i_coord in zip(ship, range(len(ship))):
                    if move == coord:
                        del self.enemy_field.ships[i_ship][i_coord]
                        return True
            else:
                continue

    def verify_destroy(self, move):
        for ship, ship_copy in zip(self.enemy_field.ships,
                self.enemy_field.ships_copy):  # Проверка на уничтожение корабля
            if len(ship) == 0:
                for coord_copy in ship_copy:
                    self.enemy_field.around_ship(coord_copy, ship_copy, self.move_list, True)
                print("Корабль уничтожен")
                ship.append("X")
                self.enemy_count_ship -= 1
                Game.turn = True
                return Game.turn
            else:
                continue
        print("Корабль ранен")
        self.move_list.append((move))
        Game.turn = True
        return Game.turn

    def moving(self, move):
        self.move = move

        if self.verify_shot(self.move):
            self.verify_destroy(self.move)
        else:
            print("Промах")
            self.enemy_field.field[self.move[0]].pop(self.move[1])
            self.enemy_field.field[self.move[0]].insert(self.move[1], "T")
            self.move_list.append(self.move)
            Game.turn = False
            return Game.turn

class Human(Player):
    def hand_move(self):
        try:
            self.move = input("Введите координаты через пробел: ").split()
            x, y = int(self.move[0]), int(self.move[1])

            if x < 0 or x > 6 or y < 0 or y > 6:
                raise CoordOutError("координаты должны быть от 1 до 6")
            self.move = tuple((x, y))

            if self.move in self.move_list:
                raise MoveError("в этой клетке уже был произведен выстрел")
            return self.move

        except CoordError as e:
            print(f"CoordError: {e}")
            self.hand_move()

        except CoordOutError as e:
            print(f"CoordOutError: {e}")
            self.hand_move()

        except ValueError:
            print("ValueError: координаты должны быть цифрами")
            self.hand_move()

        except MoveError as e:
            print(f"MoveError: {e}")
            self.hand_move()

        except IndexError:
            print(f"IndexError: вы ввели 1 координату вместо 2")
            self.hand_move()

class AI(Player):
    def auto_move(self):
        self.move = Game.gen.get_coord()
        print(f"Копьютер походил на {self.move[0]} {self.move[1]}")
        Game.gen.allow_coords.remove(self.move)
        print(f"allow {Game.gen.allow_coords}")
        return self.move

class Game:
    gen = Dot()
    turn = True
    
    @staticmethod
    def viev_fields(this, other):
        for i, j in zip(this.field, other.field):
            print(*i, " " * 10, *j, sep=' | ')

    def start(self):
        field = Field()
        field1 = Field(True)

        self.human = Human(field, field1)
        self.bot = AI(field1, field)
        self.human.create_field()

        print(" " * 25, "Морской бой")
        print("Вычислите расположение всех кораблей противника чтобы победить")
        print()
        time.sleep(3)
        prepare = input("Нажмите любую кнопку чтобы начать игру")
        print()

        while self.human.enemy_count_ship > 0 and self.human.enemy_count_ship > 0:
            while Game.turn:
                print(f"Игрок: {self.bot.enemy_count_ship} {" " * 30} Компьютер: {self.human.enemy_count_ship}")
                Game.viev_fields(self.human.yourself_field, self.bot.yourself_field)
                print()
                print("Ваш ход")
                self.human.moving(self.human.hand_move())
                print()
                if self.human.enemy_count_ship == 0:
                    return f"Вы победили"
            Game.turn = True
            while Game.turn:
                print(f"Игрок: {self.bot.enemy_count_ship} {" " * 30} Компьютер: {self.human.enemy_count_ship}")
                Game.viev_fields(self.human.yourself_field, self.bot.yourself_field)
                print()
                print("Ход компьютера")
                time.sleep(2)
                self.bot.moving(self.bot.auto_move())
                print()
                if self.bot.enemy_count_ship == 0:
                    return f"Компьютер победил"
            Game.turn = True

print(Game().start())
