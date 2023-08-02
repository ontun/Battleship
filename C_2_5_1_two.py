from random import randint, choice


class BoardException(Exception):#класс исключение (родитель)
    pass

class BoardOutException(BoardException):#класс исключение
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):#класс исключение
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):#класс исключение
    pass



class Dot:# класс точка
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class Ship:# класс корабль
    def __init__(self, size, direct, point):
        self.size = size
        self.direct = direct
        self.point = point
        self.hp = size

    def dots(self):# метод получение всех точек корабля
        points_ship = []
        for i in range(self.size):
            cx = self.point.x
            cy = self.point.y
            if self.direct == 'ax':
                cy += i
            elif self.direct == 'or':
                cx += i
            points_ship.append(Dot(cx, cy))
        return points_ship



class Board:# класс доски
    def __init__(self, hide):
        self.field =  [[' ', ' | 1', ' | 2', ' | 3', ' | 4', ' | 5', ' | 6', ' |'],
                ['1', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' |'],
                ['2', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' |'],
                ['3', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' |'],
                ['4', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' |'],
                ['5', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' |'],
                ['6', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' | 0', ' |'],
                ['_', '___', '___', '___', '___', '___', '___', '__']]

        self.list_ship = []
        self.hide = hide
        self.quantity_live_ship = 7
        self.admiss = []


    def add_ship(self, ship):# метод для добавления корабля на доску
        for i in ship.dots():
            if self.out(i) or i in self.admiss:
                raise BoardWrongShipException()

        for i in ship.dots():
            self.field[i.x][i.y] = " | K"
            self.admiss.append(i)

        self.list_ship.append(ship)
        self.contour(ship)


    def contour(self, ship, location = False):# метод обвода корабля (соседних точек)
            near = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)
            ]
            for d in ship.dots():
                for dx, dy in near:
                    p = Dot(d.x + dx, d.y + dy)

                    if not (self.out(p)) and p not in self.admiss:
                        if location:
                            self.field[p.x][p.y] = " | M"
                        self.admiss.append(p)
    def out(self, point):# метод проверки координат точки
        if point.x > 6 or point.x < 1 or point.y > 6 or point.y < 1:
            return True
        else:
            return False


    def display_board(self):# метод для отображения доски
        disp=''
        delete = ['[',']',"'",',']
        for i in range(7):
            disp += str(self.field[i])
            disp += '\n'
        for i in delete:
            disp = disp.replace(i,'')
        if self.hide:
            disp = disp.replace(' | K', ' | 0')
        print(disp)

    def shot(self, p):# метод выстрела в точку
        if self.out(p):
            raise BoardOutException()

        if p in self.admiss:
            raise BoardUsedException()

        self.admiss.append(p)

        for ship in self.list_ship:
            if p in ship.dots():
                ship.hp -= 1
                self.field[p.x][p.y] = " | X"
                if ship.hp == 0:
                    self.quantity_live_ship -= 1
                    self.contour(ship, location=True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True

        self.field[p.x][p.y] = " | M"
        print("Мимо!")
        return False

    def begin(self):# метод для очищения списка
        self.admiss = []

class Player:# класс игрок
    def __init__(self, my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):# метод - ход в игре
        while True:
            try:
                point = self.ask()
                s = self.enemy_board.shot(point)
                return s
            except BoardException as e:
                print(e)


class User(Player):# класс потомок пользователь
    def ask(self):# метод получения координат точки для выстрела в игре
        while True:
            try:
                x = int(input('Введите номер строки:'))
                y = int(input('Введите номер столбца:'))
                return Dot(x,y)
            except:
                print('Вы ввели не числа, попробуйте снова')




class AI(Player):# класс потомок компьютер
    def ask(self):# метод получения координат точки для выстрела в игре
        point = Dot(randint(1, 6), randint(1, 6))
        print(f"Ход компьютера: {point.x} {point.y}")
        return point


class Game:# класс игра
    def __init__(self):

        user_board = self.random_board(False)
        comp_board = self.random_board(True)
        comp_board.hide = True

        self.comp = AI(comp_board, user_board)
        self.user = User(user_board, comp_board)

    def greet(self):# метод для отображения правил игры
        print("Это игра - морской бой")
        print("-" * 80)
        print("В игре 7 кораблей: один длиной в 3 ячейки\nдва длиной в 2 ячейки\nчетыре длиной в 1 ячейку")
        print("-" * 80)
        print("Для начала надо заполнить поле, если нажать 0, оно заполнится автоматически:")
        print("-" * 80)

    def loop(self):# метод игрового цикла
        move = 0
        user_board = self.ask_create_board()
        while True:
            print("Доска пользователя:")
            self.user.my_board.display_board()
            print("-" * 35)
            print("Доска компьютера:")
            self.comp.my_board.display_board()
            print("-" * 35)
            if move % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("Ходит компьютер!")
                repeat = self.comp.move()
            if repeat:
                move -= 1

            if self.comp.my_board.quantity_live_ship == 0:
                self.comp.my_board.display_board()
                print("-" * 35)
                print("Пользователь выиграл!")
                break

            if self.user.my_board.quantity_live_ship == 0:
                self.user.my_board.display_board()
                print("-" * 35)
                print("Компьютер выиграл!")
                break
            move += 1


    def create_board(self, hide):# методо создания и заполнения доски случайным образом
        ch = ['ax','or']
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(hide)
        quantity = 0
        for l in lens:
            while True:
                quantity += 1
                if quantity > 2000:
                    return None
                ship = Ship(l, choice(ch), Dot(randint(1, 6), randint(1, 6)))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self,hide):# метод для создания доски (работает пока не создастся доска)
        board = None
        while board is None:
            board = self.create_board(hide)
        return board


    def ask_create_board(self):# метод для создания доски пользователем вручную
        # (доступен выбор создания доски автоматически)
        list_ships=[3, 2, 2, 1, 1, 1, 1]
        board = Board(False)
        while len(list_ships)!=0:
            try:
                board.display_board()
                print('--Для автоматического заполнения введите 0 вместо длины корабля--')
                size = int(input('Введите длину корабля, только число от 1 до 3:'))
                print("----------------------------------------------------------------------------------------")
                if size == 0:
                    return self.random_board(False)
                if size < 4 and size > 0:
                    if size in list_ships:
                        dir = input('Введите расположение корабля (ax - горизонтальное, or - вертикальное):')
                        print(
                            "----------------------------------------------------------------------------------------")
                        if dir == 'ax':
                            dl = size-1
                            x = int(input('Введите номер строки:'))
                            y = int(input('Введите номер столбца:'))
                            if y + dl<7 and Dot(x,y) not in board.admiss:
                                board.add_ship(Ship(size, dir, Dot(x,y)))
                                list_ships.remove(size)
                            else:
                                print('Корабль не входит в поле или находится рядом с другим кораблем, попробуйте снова')
                                print(
                                    "----------------------------------------------------------------------------------------")
                        elif dir =='or':
                            dl = size - 1
                            x = int(input('Введите номер строки:'))
                            y = int(input('Введите номер столбца:'))
                            if x + dl < 7 and Dot(x, y) not in board.admiss:
                                board.add_ship(Ship(size, dir, Dot(x, y)))
                                list_ships.remove(size)
                            else:
                                print(
                                    'Корабль не входит в поле или находится рядом с другим кораблем, попробуйте снова')
                                print(
                                    "----------------------------------------------------------------------------------------")
                        else:
                            print('Вы ввели неверное направление, попробуйте снова')
                            print(
                                "----------------------------------------------------------------------------------------")
                    else:
                        print('Все корабли такой длины уже расставлены на доске')
                        print(
                            "----------------------------------------------------------------------------------------")
                else:
                    print('Вы ввели недопустимую длину корабля')
                    print("----------------------------------------------------------------------------------------")
            except ValueError:
                print('Вы ввели не числа, попробуйте снова')
                print("----------------------------------------------------------------------------------------")
            except BoardWrongShipException:
                print('Вы ввели числа вне диапазона доски, попробуйте снова')
                print("----------------------------------------------------------------------------------------")
        return board




    def start(self):# метод для запуска игры
        self.greet()
        self.loop()


game = Game()
game.start()

