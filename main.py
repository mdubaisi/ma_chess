import random
from enum import Enum
from copy import deepcopy


class Color(Enum):
    Black = -1
    White = 1


class Board:
    def __init__(self, w: int, h: int, randomized: bool = False):
        self.h = h
        self.w = w
        self.randomized = randomized
        self.have_b_king = False
        self.have_w_king = False
        self.location = [[None for _ in range(self.w)] for _ in range(self.h)]
        self.black_king_pos = (5, 8)
        self.white_king_pos = (5, 1)
        self.pieces = [Piece.King, Piece.King, Piece.Queen, Piece.Bishop, Piece.Bishop,
                       Piece.Bishop, Piece.Knight, Piece.Knight, Piece.Knight,
                       Piece.Rock, Piece.Rock, Piece.Pawn, Piece.Pawn, Piece.Pawn, Piece.Pawn]

    def __repr__(self):
        s = "\n"
        for i in range(self.h):
            s += f"{self.h - i}    "
            for j in range(self.w):
                if self.location[i][j] is None:
                    s += "* "
                else:
                    s += f"{self.location[i][j]} "
            s += '\n'
        s += '\n'

        s += "     "
        for i in range(self.w):
            s += f"{i + 1} "
        s += '\n'

        return s

    def set_up(self) -> None:
        if self.randomized:
            for i in range(self.h):
                for j in range(self.w):
                    p = self.pieces[random.randrange(0, len(self.pieces))]
                    piece = None

                    if i == 0:
                        while p == Piece.King and self.have_b_king:
                            p = self.pieces[random.randrange(0, len(self.pieces))]
                        piece = Piece(p, j + 1, self.h - i, Color.Black)
                        if j == self.w - 1 and not self.have_b_king:
                            piece = Piece(Piece.King, j + 1, self.h - i, Color.Black)
                        if p == Piece.King:
                            self.have_b_king = True

                    elif self.h - i == 1:
                        while p == Piece.King and self.have_w_king:
                            p = self.pieces[random.randrange(0, len(self.pieces))]
                        piece = Piece(p, j + 1, self.h - i, Color.White)
                        if j == self.w - 1 and not self.have_w_king:
                            piece = Piece(Piece.King, j + 1, self.h - i, Color.White)
                        if p == Piece.King:
                            self.have_w_king = True

                    elif i == 1:
                        while p == Piece.King:
                            p = self.pieces[random.randrange(0, len(self.pieces))]

                        piece = Piece(p, j + 1, self.h - i, Color.Black)
                    elif self.h - i == 2:
                        while p == Piece.King:
                            p = self.pieces[random.randrange(0, len(self.pieces))]

                        piece = Piece(p, j + 1, self.h - i, Color.White)

                    self.location[i][j] = piece
        else:
            for i in range(self.h):
                for j in range(self.w):
                    piece = None

                    if i == 0:
                        if j == 0 or self.w - j == 1:
                            piece = Piece(Piece.Rock, j + 1, self.h - i, Color.Black)
                        elif j == 1 or self.w - j == 2:
                            piece = Piece(Piece.Knight, j + 1, self.h - i, Color.Black)
                        elif j == 2 or self.w - j == 3:
                            piece = Piece(Piece.Bishop, j + 1, self.h - i, Color.Black)
                        elif j == 3:
                            piece = Piece(Piece.Queen, j + 1, self.h - i, Color.Black)
                        elif j == 4:
                            piece = Piece(Piece.King, j + 1, self.h - i, Color.Black)
                    elif self.h - i == 1:
                        if j == 0 or self.w - j == 1:
                            piece = Piece(Piece.Rock, j + 1, self.h - i, Color.White)
                        elif j == 1 or self.w - j == 2:
                            piece = Piece(Piece.Knight, j + 1, self.h - i, Color.White)
                        elif j == 2 or self.w - j == 3:
                            piece = Piece(Piece.Bishop, j + 1, self.h - i, Color.White)
                        elif j == 3:
                            piece = Piece(Piece.Queen, j + 1, self.h - i, Color.White)
                        elif j == 4:
                            piece = Piece(Piece.King, j + 1, self.h - i, Color.White)
                    elif i == 1:
                        piece = Piece(Piece.Pawn, j + 1, self.h - i, Color.Black)
                    elif self.h - i == 2:
                        piece = Piece(Piece.Pawn, j + 1, self.h - i, Color.White)

                    self.location[i][j] = piece

    def get_input(self) -> tuple:
        nums = ['1', '2', '3', '4', '5', '6', '7', '8']
        print("from: ")
        old_x = input("x: ")
        old_y = input("y: ")

        print("to: ")
        new_x = input("x: ")
        new_y = input("y: ")

        if old_x in nums and old_y in nums and new_x in nums and new_y in nums:
            old_x = int(old_x)
            old_y = int(old_y)
            new_x = int(new_x)
            new_y = int(new_y)

            return (old_x, old_y), (new_x, new_y)
        else:
            print("Invalid input!")
            print(self)
            return self.get_input()

    def move(self, inp, t):
        if self.location[self.h - inp[0][1]][inp[0][0] - 1] is not None \
                and t == self.location[self.h - inp[0][1]][inp[0][0] - 1].color.value:
            self.location[self.h - inp[0][1]][inp[0][0] - 1].move(inp[1][0], inp[1][1], self, t)
        else:
            print("Invalid move!")
            print(self)
            re_inp = self.get_input()
            self.move(re_inp, t)

    def checked(self, t):
        for i in range(self.h):
            for j in range(self.w):
                char = self.location[i][j]
                if char is not None and char.color.value != t:
                    char.update_valid_moves(self)
                    if (char.color == Color.White and self.black_king_pos in char.valid_loc) or \
                            (char.color == Color.Black and self.white_king_pos in char.valid_loc):
                        return True
        return False

    def checkmated(self, t):
        def can_move() -> bool:
            king_pos = ()
            king: Piece
            if t == Color.White.value:
                king_pos = self.white_king_pos
            elif t == Color.Black.value:
                king_pos = self.black_king_pos

            king = self.location[self.h - king_pos[1]][king_pos[0] - 1]
            king.update_valid_moves(self)

            for pos in self.location[self.h - king_pos[1]][king_pos[0] - 1].valid_loc:
                test_board = deepcopy(self)

                test_board.location[test_board.h - pos[1]][pos[0] - 1] = king
                test_board.location[test_board.h - king.pos_y][king.pos_x - 1] = None

                if t == Color.White.value:
                    test_board.white_king_pos = (pos[0], pos[1])
                elif t == Color.Black.value:
                    test_board.black_king_pos = (pos[0], pos[1])

                if not test_board.checked(t):
                    return True
            return False

        def can_defend() -> bool:
            attackers_pos = []
            king_pos = ()
            if t == Color.White.value:
                king_pos = self.white_king_pos
            elif t == Color.Black.value:
                king_pos = self.black_king_pos

            for i in range(self.h):
                for j in range(self.w):
                    char = self.location[i][j]
                    if char is not None and char.color.value != t:
                        char.update_valid_moves(self)
                        if king_pos in char.valid_loc:
                            attackers_pos.append((self.h - i, j + 1))

            if len(attackers_pos) > 1:
                return False

            for i in range(self.h):
                for j in range(self.w):
                    char = self.location[i][j]
                    if char is not None and char.color.value == t:
                        char.update_valid_moves(self)
                        if attackers_pos[0] in char.valid_loc:
                            return True
            return False

        if self.checked(t) and not can_move() and not can_defend():
            print(self)
            if t == Color.White.value:
                print("Black won!")
            elif t == Color.Black.value:
                print("White won!")
            return True

        return False

    def draw(self, t):
        def have_moves() -> bool:
            def can_move() -> bool:
                king_pos = ()
                king: Piece
                if t == Color.White.value:
                    king_pos = self.white_king_pos
                elif t == Color.Black.value:
                    king_pos = self.black_king_pos

                king = self.location[self.h - king_pos[1]][king_pos[0] - 1]
                king.update_valid_moves(self)

                for pos in self.location[self.h - king_pos[1]][king_pos[0] - 1].valid_loc:
                    test_board = deepcopy(self)

                    test_board.location[test_board.h - pos[1]][pos[0] - 1] = king
                    test_board.location[test_board.h - king.pos_y][king.pos_x - 1] = None

                    if t == Color.White.value:
                        test_board.white_king_pos = (pos[0], pos[1])
                    elif t == Color.Black.value:
                        test_board.black_king_pos = (pos[0], pos[1])

                    if not test_board.checked(t):
                        return True
                return False

            for i in range(self.h):
                for char in self.location[i]:
                    if char is None or char.color.value != t:
                        continue

                    char.update_valid_moves(self)

                    if len(char.valid_loc) > 0 and char.type != Piece.King:
                        return True
                    elif can_move():
                        return True
            return False

        if not self.checked(Color.White.value) and not self.checked(Color.Black.value) and not have_moves():
            print(self)
            print("Draw!")
            return True

        return False


class Piece:
    def __init__(self, p_type, x, y, p_color):
        self.color = p_color
        self.type = p_type
        self.point = p_type[1]
        self.pos_x: int = x
        self.pos_y: int = y
        self.valid_loc = []
        self.moved = False

    Rock = ('r', 50)
    Knight = ('k', 30)
    Bishop = ('b', 30)
    Queen = ('q', 90)
    King = ('@', 0)
    Pawn = ('p', 10)

    def promote(self) -> None:
        if ((self.pos_y == 8 and self.color == Color.White) or (self.pos_y == 1 and self.color == Color.Black)) \
                and self.type == Piece.Pawn:
            x: str = input("what would you like to promote the pawn to? ")
            if x.capitalize() == 'R':
                self.type = Piece.Rock
            elif x.capitalize() == 'K':
                self.type = Piece.Knight
            elif x.capitalize() == 'B':
                self.type = Piece.Bishop
            elif x.capitalize() == 'Q':
                self.type = Piece.Queen
            else:
                print("Invalid piece!")
                self.promote()

    def can_castle_right(self, b: Board) -> bool:
        if not self.moved and b.location[b.h - self.pos_y][self.pos_x] is None and \
                b.location[b.h - self.pos_y][self.pos_x + 1] is None and \
                b.location[b.h - self.pos_y][self.pos_x + 2].type == Piece.Rock and \
                not b.location[b.h - self.pos_y][self.pos_x + 2].moved:
            return True
        else:
            return False

    def can_castle_left(self, b: Board) -> bool:
        if not self.moved and b.location[b.h - self.pos_y][self.pos_x - 2] is None and \
                b.location[b.h - self.pos_y][self.pos_x - 3] is None and \
                b.location[b.h - self.pos_y][self.pos_x - 4] is None and \
                b.location[b.h - self.pos_y][self.pos_x - 5].type == Piece.Rock and \
                not b.location[b.h - self.pos_y][self.pos_x - 5].moved:
            return True
        else:
            return False

    def update_valid_moves(self, b: Board) -> None:
        new_valid_loc = []

        if self.type == Piece.Rock:
            x = self.pos_x + 1
            y = self.pos_y
            while x <= b.w and (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x += 1

            x = self.pos_x - 1
            y = self.pos_y
            while x >= 1 and (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x -= 1

            x = self.pos_x
            y = self.pos_y + 1
            while y <= b.h and (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                y += 1

            x = self.pos_x
            y = self.pos_y - 1
            while y >= 1 and (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                y -= 1

        elif self.type == Piece.Knight:
            if self.pos_x <= b.w - 1 and self.pos_y <= b.h - 2 and (b.location[b.h - self.pos_y - 2][self.pos_x]
                                                                    is None or b.location[b.h - self.pos_y - 2][
                                                                        self.pos_x].color != self.color):
                new_valid_loc.append((self.pos_x + 1, self.pos_y + 2))
            if self.pos_x >= 2 and self.pos_y <= b.h - 2 and (b.location[b.h - self.pos_y - 2][self.pos_x - 2]
                                                              is None or b.location[b.h - self.pos_y - 2][
                                                                  self.pos_x - 2].color != self.color):
                new_valid_loc.append((self.pos_x - 1, self.pos_y + 2))
            if self.pos_x <= b.w - 2 and self.pos_y <= b.h - 1 and (b.location[b.h - self.pos_y - 1][self.pos_x + 1]
                                                                    is None or b.location[b.h - self.pos_y - 1][
                                                                        self.pos_x + 1].color != self.color):
                new_valid_loc.append((self.pos_x + 2, self.pos_y + 1))
            if self.pos_x >= 3 and self.pos_y <= b.h - 1 and (b.location[b.h - self.pos_y - 1][self.pos_x - 3]
                                                              is None or b.location[b.h - self.pos_y - 1][
                                                                  self.pos_x - 3].color != self.color):
                new_valid_loc.append((self.pos_x - 2, self.pos_y + 1))

            if self.pos_x <= b.w - 1 and self.pos_y >= 3 and (b.location[b.h - self.pos_y + 2][self.pos_x]
                                                              is None or b.location[b.h - self.pos_y + 2][
                                                                  self.pos_x].color != self.color):
                new_valid_loc.append((self.pos_x + 1, self.pos_y - 2))
            if self.pos_x >= 2 and self.pos_y >= 3 and (b.location[b.h - self.pos_y + 2][self.pos_x - 2]
                                                        is None or b.location[b.h - self.pos_y + 2][
                                                            self.pos_x - 2].color != self.color):
                new_valid_loc.append((self.pos_x - 1, self.pos_y - 2))
            if self.pos_x <= b.w - 2 and self.pos_y >= 2 and (b.location[b.h - self.pos_y + 1][self.pos_x + 1]
                                                              is None or b.location[b.h - self.pos_y + 1][
                                                                  self.pos_x + 1].color != self.color):
                new_valid_loc.append((self.pos_x + 2, self.pos_y - 1))
            if self.pos_x >= 3 and self.pos_y >= 2 and (b.location[b.h - self.pos_y + 1][self.pos_x - 3]
                                                        is None or b.location[b.h - self.pos_y + 1][
                                                            self.pos_x - 3].color != self.color):
                new_valid_loc.append((self.pos_x - 2, self.pos_y - 1))

        elif self.type == Piece.Bishop:
            x = self.pos_x + 1
            y = self.pos_y + 1
            while x <= b.w and y <= b.h and \
                    (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x += 1
                y += 1

            x = self.pos_x - 1
            y = self.pos_y - 1
            while x >= 1 and y >= 1 and \
                    (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x -= 1
                y -= 1

            x = self.pos_x - 1
            y = self.pos_y + 1
            while x >= 1 and y <= b.h and \
                    (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x -= 1
                y += 1

            x = self.pos_x + 1
            y = self.pos_y - 1
            while x <= b.w and y >= 1 and \
                    (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x += 1
                y -= 1

        elif self.type == Piece.Queen:
            x = self.pos_x + 1
            y = self.pos_y
            while x <= b.w and (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x += 1
            x = self.pos_x - 1
            y = self.pos_y
            while x >= 1 and (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break
                new_valid_loc.append((x, y))
                x -= 1
            x = self.pos_x
            y = self.pos_y + 1
            while y <= b.h and (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break
                new_valid_loc.append((x, y))
                y += 1
            x = self.pos_x
            y = self.pos_y - 1
            while y >= 1 and (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                y -= 1

            x = self.pos_x + 1
            y = self.pos_y + 1
            while x <= b.w and y <= b.h and \
                    (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x += 1
                y += 1
            x = self.pos_x - 1
            y = self.pos_y - 1
            while x >= 1 and y >= 1 and \
                    (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x -= 1
                y -= 1
            x = self.pos_x - 1
            y = self.pos_y + 1
            while x >= 1 and y <= b.h and \
                    (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x -= 1
                y += 1
            x = self.pos_x + 1
            y = self.pos_y - 1
            while x <= b.w and y >= 1 and \
                    (b.location[b.h - y][x - 1] is None or b.location[b.h - y][x - 1].color != self.color):
                if b.location[b.h - y][x - 1] is not None and b.location[b.h - y][x - 1].color != self.color:
                    new_valid_loc.append((x, y))
                    break

                new_valid_loc.append((x, y))
                x += 1
                y -= 1

        elif self.type == Piece.King:
            if self.pos_x <= b.w - 1 and (b.location[b.h - self.pos_y][self.pos_x] is None or
                                          b.location[b.h - self.pos_y][self.pos_x].color != self.color):
                new_valid_loc.append((self.pos_x + 1, self.pos_y))
            if self.pos_x >= 2 and (b.location[b.h - self.pos_y][self.pos_x - 2] is None or
                                    b.location[b.h - self.pos_y][self.pos_x - 2].color != self.color):
                new_valid_loc.append((self.pos_x - 1, self.pos_y))
            if self.pos_y <= b.h - 1 and (b.location[b.h - self.pos_y - 1][self.pos_x - 1] is None or
                                          b.location[b.h - self.pos_y - 1][self.pos_x - 1].color != self.color):
                new_valid_loc.append((self.pos_x, self.pos_y + 1))
            if self.pos_y >= 2 and (b.location[b.h - self.pos_y + 1][self.pos_x - 1] is None or
                                    b.location[b.h - self.pos_y + 1][self.pos_x - 1].color != self.color):
                new_valid_loc.append((self.pos_x, self.pos_y - 1))

            if self.pos_x <= b.w - 1 and self.pos_y <= b.h - 1 and (b.location[b.h - self.pos_y - 1][self.pos_x]
                                                                    is None or b.location[b.h - self.pos_y - 1][
                                                                        self.pos_x].color != self.color):
                new_valid_loc.append((self.pos_x + 1, self.pos_y + 1))
            if self.pos_x >= 2 and self.pos_y <= b.h - 1 and (b.location[b.h - self.pos_y - 1][self.pos_x - 2]
                                                              is None or b.location[b.h - self.pos_y - 1][
                                                                  self.pos_x - 2].color != self.color):
                new_valid_loc.append((self.pos_x - 1, self.pos_y + 1))
            if self.pos_x <= b.w - 1 and self.pos_y >= 2 and (b.location[b.h - self.pos_y + 1][self.pos_x]
                                                              is None or b.location[b.h - self.pos_y + 1][
                                                                  self.pos_x].color != self.color):
                new_valid_loc.append((self.pos_x + 1, self.pos_y - 1))
            if self.pos_x >= 2 and self.pos_y >= 2 and (b.location[b.h - self.pos_y + 1][self.pos_x - 2]
                                                        is None or b.location[b.h - self.pos_y + 1][
                                                            self.pos_x - 2].color != self.color):
                new_valid_loc.append((self.pos_x - 1, self.pos_y - 1))

            # castling
            if not b.randomized and self.can_castle_left(b):
                new_valid_loc.append((self.pos_x - 2, self.pos_y))
            if not b.randomized and self.can_castle_right(b):
                new_valid_loc.append((self.pos_x + 2, self.pos_y))

        elif self.type == Piece.Pawn:
            if self.color == Color.White:
                if self.pos_y <= b.h - 1 and b.location[b.h - self.pos_y - 1][self.pos_x - 1] is None:
                    new_valid_loc.append((self.pos_x, self.pos_y + 1))

                if not self.moved and b.location[b.h - self.pos_y - 2][self.pos_x - 1] is None:
                    new_valid_loc.append((self.pos_x, self.pos_y + 2))

                if self.pos_x <= b.w - 1 and \
                        self.pos_y <= b.h - 1 and b.location[b.h - self.pos_y - 1][self.pos_x] is not None \
                        and b.location[b.h - self.pos_y - 1][self.pos_x].color != self.color:
                    new_valid_loc.append((self.pos_x + 1, self.pos_y + 1))
                if self.pos_x >= 2 and \
                        self.pos_y <= b.h - 1 and b.location[b.h - self.pos_y - 1][self.pos_x - 2] is not None \
                        and b.location[b.h - self.pos_y - 1][self.pos_x - 2].color != self.color:
                    new_valid_loc.append((self.pos_x - 1, self.pos_y + 1))

            elif self.color == Color.Black:
                if self.pos_y >= 2 and b.location[b.h - self.pos_y + 1][self.pos_x - 1] is None:
                    new_valid_loc.append((self.pos_x, self.pos_y - 1))

                if not self.moved and b.location[b.h - self.pos_y + 2][self.pos_x - 1] is None:
                    new_valid_loc.append((self.pos_x, self.pos_y - 2))

                if self.pos_x <= b.w - 1 and \
                        self.pos_y >= 0 and b.location[b.h - self.pos_y + 1][self.pos_x] is not None \
                        and b.location[b.h - self.pos_y + 1][self.pos_x].color != self.color:
                    new_valid_loc.append((self.pos_x + 1, self.pos_y - 1))
                if self.pos_x >= 2 and \
                        self.pos_y >= 0 and b.location[b.h - self.pos_y + 1][self.pos_x - 2] is not None and \
                        b.location[b.h - self.pos_y + 1][self.pos_x - 2].color != self.color:
                    new_valid_loc.append((self.pos_x - 1, self.pos_y - 1))

        self.valid_loc = new_valid_loc

    def move(self, new_x: int, new_y: int, b: Board, t: int) -> None:
        def valid() -> bool:
            if b.w >= new_x >= 1 and b.h >= new_y >= 1:
                self.update_valid_moves(b)
                if (new_x, new_y) in self.valid_loc:
                    test_board = deepcopy(b)

                    test_board.location[b.h - new_y][new_x - 1] = self
                    test_board.location[b.h - self.pos_y][self.pos_x - 1] = None

                    if self.type == Piece.King:
                        if self.color == Color.Black:
                            test_board.black_king_pos = (new_x, new_y)
                        elif self.color == Color.White:
                            test_board.white_king_pos = (new_x, new_y)

                    if not test_board.checked(self.color.value):
                        return True
            return False

        if valid():
            if self.type == Piece.King:
                if new_x == self.pos_x + 2:
                    b.location[b.h - new_y][self.pos_x + 2].pos_x = new_x - 1
                    b.location[b.h - new_y][self.pos_x + 2].pos_y = new_y
                    b.location[b.h - new_y][self.pos_x] = b.location[b.h - new_y][self.pos_x + 2]
                    b.location[b.h - new_y][self.pos_x + 2] = None
                elif new_x == self.pos_x - 2:
                    b.location[b.h - new_y][self.pos_x - 5].pos_x = new_x + 1
                    b.location[b.h - new_y][self.pos_x - 5].pos_y = new_y
                    b.location[b.h - new_y][self.pos_x - 2] = b.location[b.h - new_y][self.pos_x - 5]
                    b.location[b.h - new_y][self.pos_x - 5] = None

                if self.color == Color.Black:
                    b.black_king_pos = (new_x, new_y)
                elif self.color == Color.White:
                    b.white_king_pos = (new_x, new_y)

            b.location[b.h - new_y][new_x - 1] = self
            b.location[b.h - self.pos_y][self.pos_x - 1] = None
            self.pos_x = new_x
            self.pos_y = new_y
            self.promote()
            self.moved = True
        else:
            print("Invalid move!")
            print(b)
            inp = b.get_input()
            b.move(inp, t)

    def __repr__(self):
        if self.color == Color.Black:
            return self.type[0]
        else:
            return self.type[0].capitalize()


def test(b: Board):
    b.move(((7, 1), (6, 3)), 1)
    b.move(((4, 7), (4, 5)), -1)
    b.move(((4, 2), (4, 4)), 1)
    b.move(((5, 7), (5, 6)), -1)
    b.move(((2, 1), (3, 3)), 1)
    b.move(((2, 7), (2, 6)), -1)
    b.move(((5, 2), (5, 3)), 1)
    b.move(((3, 7), (3, 5)), -1)
    b.move(((4, 4), (3, 5)), 1)
    b.move(((2, 8), (3, 6)), -1)
    b.move(((3, 5), (2, 6)), 1)
    b.move(((5, 8), (5, 7)), -1)
    b.move(((2, 6), (2, 7)), 1)
    b.move(((3, 8), (4, 7)), -1)
    b.move(((2, 7), (1, 8)), 1)
    b.move(((7, 8), (8, 6)), -1)
    b.move(((1, 8), (1, 7)), 1)
    b.move(((3, 6), (2, 8)), -1)
    b.move(((1, 7), (3, 5)), 1)
    b.move(((5, 7), (6, 6)), -1)
    b.move(((4, 1), (4, 4)), 1)
    b.move(((5, 6), (5, 5)), -1)
    b.move(((4, 4), (5, 5)), 1)
    b.move(((6, 6), (7, 6)), -1)
    b.move(((6, 1), (4, 3)), 1)
    b.move(((4, 7), (6, 5)), -1)
    b.move(((4, 3), (6, 5)), 1)
    b.move(((8, 6), (6, 5)), -1)
    b.move(((6, 3), (4, 4)), 1)
    b.move(((6, 8), (3, 5)), -1)
    b.move(((5, 5), (6, 5)), 1)
    b.move(((7, 6), (8, 6)), -1)
    b.move(((5, 3), (5, 4)), 1)
    b.move(((7, 7), (7, 5)), -1)
    b.move(((6, 5), (7, 5)), 1)
    b.move(((4, 8), (7, 5)), -1)
    b.move(((3, 1), (7, 5)), 1)
    b.move(((8, 6), (8, 5)), -1)
    b.move(((5, 1), (3, 1)), 1)
    b.move(((2, 8), (1, 6)), -1)
    b.move(((6, 2), (6, 4)), 1)
    b.move(((1, 6), (2, 8)), -1)
    b.move(((4, 4), (6, 3)), 1)
    b.move(((4, 5), (5, 4)), -1)
    b.move(((3, 3), (5, 4)), 1)
    b.move(((2, 8), (3, 6)), -1)
    b.move(((5, 4), (3, 5)), 1)
    b.move(((3, 6), (2, 4)), -1)
    b.move(((3, 2), (3, 3)), 1)
    b.move(((8, 8), (7, 8)), -1)
    b.move(((3, 3), (2, 4)), 1)
    b.move(((7, 8), (8, 8)), -1)
    b.move(((8, 1), (7, 1)), 1)
    b.move(((8, 8), (7, 8)), -1)
    b.move(((7, 2), (7, 4)), 1)
    b.move(((8, 5), (7, 6)), -1)
    b.move(((6, 4), (6, 5)), 1)
    b.move(((7, 6), (7, 7)), -1)
    b.move(((3, 5), (5, 6)), 1)
    b.move(((6, 7), (5, 6)), -1)
    b.move(((6, 5), (5, 6)), 1)
    b.move(((7, 7), (7, 6)), -1)
    b.move(((5, 6), (5, 7)), 1)
    b.move(((7, 6), (7, 7)), -1)
    b.move(((4, 1), (4, 8)), 1)
    b.move(((7, 8), (5, 8)), -1)
    b.move(((4, 8), (5, 8)), 1)
    b.move(((8, 7), (8, 5)), -1)
    b.move(((5, 8), (7, 8)), 1)
    b.move(((7, 7), (7, 8)), -1)
    b.move(((5, 7), (5, 8)), 1)
    b.move(((7, 8), (8, 7)), -1)
    b.move(((5, 8), (8, 5)), 1)
    b.move(((8, 7), (7, 8)), -1)
    b.move(((7, 5), (5, 7)), 1)
    b.move(((7, 8), (7, 7)), -1)
    b.move(((8, 5), (6, 5)), 1)
    b.move(((7, 7), (8, 6)), -1)
    b.move(((7, 4), (7, 5)), 1)
    b.move(((8, 6), (7, 7)), -1)
    b.move(((6, 5), (6, 6)), 1)
    b.move(((7, 7), (7, 8)), -1)
    b.move(((6, 6), (6, 8)), 1)
    b.move(((7, 8), (8, 7)), -1)
    b.move(((6, 8), (8, 6)), 1)
    b.move(((8, 7), (7, 8)), -1)
    b.move(((8, 6), (6, 6)), 1)
    b.move(((7, 8), (8, 7)), -1)
    b.move(((7, 5), (7, 6)), 1)
    b.move(((8, 7), (8, 6)), -1)
    b.move(((7, 6), (7, 7)), 1)
    b.move(((8, 6), (8, 5)), -1)


def main() -> None:
    board = Board(8, 8, True)
    board.set_up()

    turn = 1
    # test(board)

    while not board.checkmated(Color.White.value) and not board.checkmated(Color.Black.value) and not board.draw(turn):
        print(board)
        inp = board.get_input()
        board.move(inp, turn)
        turn *= -1


main()
