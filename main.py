def main() -> None:
    board = []
    castled = False


    class Piece:
        def __init__(self, char: str, points: int):
            self.char = char
            self.points = points
            self.pos_x: int
            self.pos_y: int

    def set_up(w: int, h: int) -> None:
        rook = Piece('r', 50)
        knight = Piece('n', 30)
        bishop = Piece('b', 30)
        queen = Piece('q', 90)
        king = Piece('k', 0)
        pawn = Piece('p', 10)
        empty = Piece('*', 0)

        for i in range(h):
            s = ""
            print(str(h - i) + "    ", end='')
            for j in range(w):
                piece = empty

                if i == 0:
                    if j == 0 or w - j == 1:
                        piece = rook
                    elif j == 1 or w - j == 2:
                        piece = knight
                    elif j == 2 or w - j == 3:
                        piece = bishop
                    elif j == 3:
                        piece = queen
                    elif j == 4:
                        piece = king

                elif h - i == 1:
                    if j == 0 or w - j == 1:
                        piece = rook
                        piece.char = piece.char.capitalize()
                    elif j == 1 or w - j == 2:
                        piece = knight
                        piece.char = piece.char.capitalize()
                    elif j == 2 or w - j == 3:
                        piece = bishop
                        piece.char = piece.char.capitalize()
                    elif j == 3:
                        piece = queen
                        piece.char = piece.char.capitalize()
                    elif j == 4:
                        piece = king
                        piece.char = piece.char.capitalize()

                if i == 1:
                    piece = pawn
                elif h - i == 2:
                    piece = pawn
                    piece.char = piece.char.capitalize()

                print(piece.char + " ", end='')
                s += piece.char
            print('')
            board.append(s)

        print('')
        print("     ", end='')
        for i in range(w):
            print(str(i + 1) + " ", end='')
        print('')

    def print_board(w: int, h: int) -> None:
        for i in range(len(board)):
            print(str(h - i) + "    ", end='')
            for j in range(len(board[i])):
                print(board[i][j] + ' ', end='')
            print('')

        print('')
        print("     ", end='')
        for i in range(1, w + 1):
            print(str(i) + ' ', end='')
        print('')

    def valid(char: str, t: int, x: int, y: int, a: int, b: int, h: int, w: int) -> bool:
        def valid_position() -> bool:
            if a == x and b == y:
                return False

            if char.capitalize() == 'R':
                start_x = x - 1
                start_y = y - 1
                end_x = x - 1
                end_y = y - 1

                if char == 'R':
                    while start_x != 0:
                        if board[h - y][start_x] != '*' and start_x != x - 1:
                            if board[h - y][start_x].capitalize() != board[h - y][start_x]:
                                start_x -= 1
                            break
                        start_x -= 1
                    while end_x != w:
                        if board[h - y][end_x] != '*' and end_x != x - 1:
                            if board[h - y][end_x].capitalize() != board[h - y][end_x]:
                                end_x += 1
                            break
                        end_x += 1
                    while start_y != 0:
                        if board[h - start_y - 1][x - 1] != '*' and start_y != y - 1:
                            if board[h - start_y - 1][x - 1].capitalize() != board[h - start_y - 1][x - 1]:
                                start_y -= 1
                            break
                        start_y -= 1
                    while end_y != h:
                        if board[h - end_y - 1][x - 1] != '*' and end_y != y - 1:
                            if board[h - end_y - 1][x - 1].capitalize() != board[h - end_y - 1][x - 1]:
                                end_y += 1
                            break
                        end_y += 1

                elif char == 'r':
                    while start_x != 0:
                        if board[h - y][start_x] != '*' and start_x != x - 1:
                            if board[h - y][start_x].capitalize() == board[h - y][start_x]:
                                start_x -= 1
                            break
                        start_x -= 1
                    while end_x != w:
                        if board[h - y][end_x] != '*' and end_x != x - 1:
                            if board[h - y][end_x].capitalize() == board[h - y][end_x]:
                                end_x += 1
                            break
                        end_x += 1
                    while start_y != 0:
                        if board[h - start_y - 1][x - 1] != '*' and start_y != y - 1:
                            if board[h - start_y - 1][x - 1].capitalize() == board[h - start_y - 1][x - 1]:
                                start_y -= 1
                            break
                        start_y -= 1
                    while end_y != h:
                        if board[h - end_y - 1][x - 1] != '*' and end_y != y - 1:
                            if board[h - end_y - 1][x - 1].capitalize() == board[h - end_y - 1][x - 1]:
                                end_y += 1
                            break
                        end_y += 1

                start_x += 1
                start_y += 1

                if a == x and end_y >= b > start_y:
                    return True
                elif b == y and end_x >= a > start_x:
                    return True
                else:
                    return False

            elif char.capitalize() == 'N':
                if char == 'N':
                    if a == x + 1 and b == y + 2 and (
                            board[h - b][a - 1] == '*' or board[h - b][a - 1].capitalize() != board[h - b][a - 1]):
                        return True
                    elif a == x - 1 and b == y + 2 and \
                            (board[h - b][a - 1] == '*' or board[h - b][a - 1].capitalize() != board[h - b][a - 1]):
                        return True
                    elif a == x + 2 and b == y + 1 and \
                            (board[h - b][a - 1] == '*' or board[h - b][a - 1].capitalize() != board[h - b][a - 1]):
                        return True
                    elif a == x - 2 and b == y + 1 and \
                            (board[h - b][a - 1] == '*' or board[h - b][a - 1].capitalize() != board[h - b][a - 1]):
                        return True

                    elif a == x + 1 and b == y - 2 and \
                            (board[h - b][a - 1] == '*' or board[h - b][a - 1].capitalize() != board[h - b][a - 1]):
                        return True
                    elif a == x - 1 and b == y - 2 and \
                            (board[h - b][a - 1] == '*' or board[h - b][a - 1].capitalize() != board[h - b][a - 1]):
                        return True
                    elif a == x + 2 and b == y - 1 and \
                            (board[h - b][a - 1] == '*' or board[h - b][a - 1].capitalize() != board[h - b][a - 1]):
                        return True
                    elif a == x - 2 and b == y - 1 and \
                            (board[h - b][a - 1] == '*' or board[h - b][a - 1].capitalize() != board[h - b][a - 1]):
                        return True

                    else:
                        return False

                elif char == 'n':
                    if a == x + 1 and b == y + 2 and (
                            board[h - b][a] == '*' or board[h - b][a].capitalize() == board[h - b][a]):
                        return True
                    elif a == x - 1 and b == y + 2 and \
                            (board[h - b][a] == '*' or board[h - b][a].capitalize() == board[h - b][a]):
                        return True
                    elif a == x + 2 and b == y + 1 and \
                            (board[h - b][a] == '*' or board[h - b][a].capitalize() == board[h - b][a]):
                        return True
                    elif a == x - 2 and b == y + 1 and \
                            (board[h - b][a] == '*' or board[h - b][a].capitalize() == board[h - b][a]):
                        return True

                    elif a == x + 1 and b == y - 2 and \
                            (board[h - b][a] == '*' or board[h - b][a].capitalize() == board[h - b][a]):
                        return True
                    elif a == x - 1 and b == y - 2 and \
                            (board[h - b][a] == '*' or board[h - b][a].capitalize() == board[h - b][a]):
                        return True
                    elif a == x + 2 and b == y - 1 and \
                            (board[h - b][a] == '*' or board[h - b][a].capitalize() == board[h - b][a]):
                        return True
                    elif a == x - 2 and b == y - 1 and \
                            (board[h - b][a] == '*' or board[h - b][a].capitalize() == board[h - b][a]):
                        return True

                    else:
                        return False

            elif char.capitalize() == 'B':
                start_x = x - 1
                start_y = y - 1
                end_x = x - 1
                end_y = y - 1

                if char == 'B':
                    while start_x != 0 and start_y != 0:
                        if board[h - start_y - 1][start_x] != '*' and start_x != x - 1 and start_y != y - 1:
                            if board[h - start_y - 1][start_x].capitalize() != board[h - start_y - 1][start_x]:
                                start_x -= 1
                                start_y -= 1
                            break
                        start_x -= 1
                        start_y -= 1

                    while end_x != w and end_y != h:
                        if board[h - end_y - 1][end_x] != '*' and end_x != x - 1 and end_y != y - 1:
                            if board[h - end_y - 1][end_x].capitalize() != board[h - end_y - 1][end_x]:
                                end_x += 1
                                end_y += 1
                            break
                        end_x += 1
                        end_y += 1

                elif char == 'b':
                    while start_x != 0 and start_y != 0:
                        if board[h - start_y - 1][start_x] != '*' and start_x != x - 1 and start_y != y - 1:
                            if board[h - start_y - 1][start_x].capitalize() == board[h - start_y - 1][start_x]:
                                start_x -= 1
                                start_y -= 1
                            break
                        start_x -= 1
                        start_y -= 1

                    while end_x != w and end_y != h:
                        if board[h - end_y - 1][end_x] != '*' and end_x != x - 1 and end_y != y - 1:
                            if board[h - end_y - 1][end_x].capitalize() == board[h - end_y - 1][end_x]:
                                end_x += 1
                                end_y += 1
                            break
                        end_x += 1
                        end_y += 1

                start_x += 1
                start_y += 1

                if (end_x >= a >= start_x and end_y >= b >= start_y) or \
                        (end_x >= a >= start_x and end_y <= b <= start_y):
                    return True

                else:
                    start_x = x
                    start_y = y
                    end_x = x
                    end_y = y

                    if char == 'B':
                        while start_x != w and start_y != 0:
                            if board[h - start_y][start_x - 1] != '*' and start_x != x and start_y != y:
                                if board[h - start_y - 1][start_x - 1].capitalize() != board[h - start_y][start_x - 1]:
                                    start_x += 1
                                    start_y -= 1
                                else:
                                    start_x -= 1
                                    start_y += 1
                                break
                            start_x += 1
                            start_y -= 1

                        while end_x != 0 and end_y != h:
                            if board[h - end_y][end_x - 1] != '*' and end_x != x and end_y != y:
                                if board[h - end_y][end_x - 1].capitalize() != board[h - end_y][end_x - 1]:
                                    end_x -= 1
                                    end_y += 1
                                else:
                                    end_x += 1
                                    end_y -= 1
                                break
                            end_x -= 1
                            end_y += 1

                    elif char == 'b':
                        while start_x != w and start_y != 0:
                            if board[h - start_y][start_x - 1] != '*' and start_x != x and start_y != y:
                                if board[h - start_y - 1][start_x - 1].capitalize() == board[h - start_y][start_x - 1]:
                                    start_x += 1
                                    start_y -= 1
                                else:
                                    start_x -= 1
                                    start_y += 1
                                break
                            start_x += 1
                            start_y -= 1

                        while end_x != 0 and end_y != h:
                            if board[h - end_y][end_x - 1] != '*' and end_x == x and end_y != y:
                                if board[h - end_y][end_x - 1].capitalize() != board[h - end_y][end_x - 1]:
                                    end_x -= 1
                                    end_y += 1
                                else:
                                    end_x += 1
                                    end_y -= 1
                                break
                            end_x -= 1
                            end_y += 1

                    start_x -= 1
                    start_y += 1

                    if (end_x <= a <= start_x and end_y >= b >= start_y) or \
                            (end_x <= a <= start_x and end_y >= b >= start_y):
                        return True

                    else:
                        return False

            elif char.capitalize() == 'Q':
                start_x = x - 1
                start_y = y - 1
                end_x = x - 1
                end_y = y - 1

                if char == 'Q':
                    while start_x != 0 and start_y != 0:
                        if board[h - start_y - 1][start_x] != '*' and start_x != x - 1 and start_y != y - 1:
                            if board[h - start_y - 1][start_x].capitalize() != board[h - start_y - 1][start_x]:
                                start_x -= 1
                                start_y -= 1
                            break
                        start_x -= 1
                        start_y -= 1

                    while end_x != w and end_y != h:
                        if board[h - end_y - 1][end_x] != '*' and end_x != x - 1 and end_y != y - 1:
                            if board[h - end_y - 1][end_x].capitalize() != board[h - end_y - 1][end_x]:
                                end_x += 1
                                end_y += 1
                            break
                        end_x += 1
                        end_y += 1

                elif char == 'q':
                    while start_x != 0 and start_y != 0:
                        if board[h - start_y - 1][start_x] != '*' and start_x != x - 1 and start_y != y - 1:
                            if board[h - start_y - 1][start_x].capitalize() == board[h - start_y - 1][start_x]:
                                start_x -= 1
                                start_y -= 1
                            break
                        start_x -= 1
                        start_y -= 1

                    while end_x != w and end_y != h:
                        if board[h - end_y - 1][end_x] != '*' and end_x != x - 1 and end_y != y - 1:
                            if board[h - end_y - 1][end_x].capitalize() == board[h - end_y - 1][end_x]:
                                end_x += 1
                                end_y += 1
                            break
                        end_x += 1
                        end_y += 1

                start_x += 1
                start_y += 1

                if (end_x >= a >= start_x and end_y >= b >= start_y) or \
                        (end_x >= a >= start_x and end_y <= b <= start_y):
                    return True

                else:
                    start_x = x
                    start_y = y
                    end_x = x
                    end_y = y

                    if char == 'Q':
                        while start_x != w and start_y != 0:
                            if board[h - start_y][start_x - 1] != '*' and start_x != x and start_y != y:
                                if board[h - start_y - 1][start_x - 1].capitalize() != board[h - start_y][start_x - 1]:
                                    start_x += 1
                                    start_y -= 1
                                else:
                                    start_x -= 1
                                    start_y += 1
                                break
                            start_x += 1
                            start_y -= 1

                        while end_x != 0 and end_y != h:
                            if board[h - end_y][end_x - 1] != '*' and end_x != x and end_y != y:
                                if board[h - end_y][end_x - 1].capitalize() != board[h - end_y][end_x - 1]:
                                    end_x -= 1
                                    end_y += 1
                                else:
                                    end_x += 1
                                    end_y -= 1
                                break
                            end_x -= 1
                            end_y += 1

                    elif char == 'q':
                        while start_x != w and start_y != 0:
                            if board[h - start_y][start_x - 1] != '*' and start_x != x and start_y != y:
                                if board[h - start_y - 1][start_x - 1].capitalize() == board[h - start_y][start_x - 1]:
                                    start_x += 1
                                    start_y -= 1
                                else:
                                    start_x -= 1
                                    start_y += 1
                                break
                            start_x += 1
                            start_y -= 1

                        while end_x != 0 and end_y != h:
                            if board[h - end_y][end_x - 1] != '*' and end_x == x and end_y != y:
                                if board[h - end_y][end_x - 1].capitalize() != board[h - end_y][end_x - 1]:
                                    end_x -= 1
                                    end_y += 1
                                else:
                                    end_x += 1
                                    end_y -= 1
                                break
                            end_x -= 1
                            end_y += 1

                    start_x -= 1
                    start_y += 1

                    if (end_x <= a <= start_x and end_y >= b >= start_y) or \
                            (end_x <= a <= start_x and end_y >= b >= start_y):
                        return True

                    else:
                        start_x = x - 1
                        start_y = y - 1
                        end_x = x - 1
                        end_y = y - 1

                        if char == 'Q':
                            while start_x != 0:
                                if board[h - y][start_x] != '*' and start_x != x - 1:
                                    if board[h - y][start_x].capitalize() != board[h - y][start_x]:
                                        start_x -= 1
                                    break
                                start_x -= 1
                            while end_x != w:
                                if board[h - y][end_x] != '*' and end_x != x - 1:
                                    if board[h - y][end_x].capitalize() != board[h - y][end_x]:
                                        end_x += 1
                                    break
                                end_x += 1
                            while start_y != 0:
                                if board[h - start_y - 1][x - 1] != '*' and start_y != y - 1:
                                    if board[h - start_y - 1][x - 1].capitalize() != board[h - start_y - 1][x - 1]:
                                        start_y -= 1
                                    break
                                start_y -= 1
                            while end_y != h:
                                if board[h - end_y - 1][x - 1] != '*' and end_y != y - 1:
                                    if board[h - end_y - 1][x - 1].capitalize() != board[h - end_y - 1][x - 1]:
                                        end_y += 1
                                    break
                                end_y += 1

                        elif char == 'q':
                            while start_x != 0:
                                if board[h - y][start_x] != '*' and start_x != x - 1:
                                    if board[h - y][start_x].capitalize() == board[h - y][start_x]:
                                        start_x -= 1
                                    break
                                start_x -= 1
                            while end_x != w:
                                if board[h - y][end_x] != '*' and end_x != x - 1:
                                    if board[h - y][end_x].capitalize() == board[h - y][end_x]:
                                        end_x += 1
                                    break
                                end_x += 1
                            while start_y != 0:
                                if board[h - start_y - 1][x - 1] != '*' and start_y != y - 1:
                                    if board[h - start_y - 1][x - 1].capitalize() == board[h - start_y - 1][x - 1]:
                                        start_y -= 1
                                    break
                                start_y -= 1
                            while end_y != h:
                                if board[h - end_y - 1][x - 1] != '*' and end_y != y - 1:
                                    if board[h - end_y - 1][x - 1].capitalize() == board[h - end_y - 1][x - 1]:
                                        end_y += 1
                                    break
                                end_y += 1

                        start_x += 1
                        start_y += 1

                        if a == x and end_y >= b > start_y:
                            return True
                        elif b == y and end_x >= a > start_x:
                            return True
                        else:
                            return False

            elif char.capitalize() == 'K':
                if char == 'K':
                    if ((a == x and b == y + 1) or (a == x and b == y - 1) or (a == x + 1 and b == y) or
                        (a == x - 1 and b == y) or (a == x + 1 and b == y + 1) or (a == x - 1 and b == y - 1) or
                        (a == x + 1 and b == y - 1)) or (a == x - 1 and b == y + 1) or \
                            (a == x + 2 and b == y and x == 5 and y == 1 and board[h - b][x] == '*' and board[h - b][
                                x + 1] == '*') \
                            or (a == x - 3 and b == y and x == 5 and y == 1 and board[h - b][x - 2] == '*'
                                and board[h - b][x - 3] == '*' and board[h - b][x - 4] == '*') \
                            and (board[h - b][a] == '*' or board[h - b][a].capitalize() != board[h - b][a]):
                        return True

                elif char == 'k':
                    if ((a == x and b == y + 1) or (a == x and b == y - 1) or (a == x + 1 and b == y) or
                        (a == x - 1 and b == y) or (a == x + 1 and b == y + 1) or (a == x - 1 and b == y - 1) or
                        (a == x + 1 and b == y - 1)) or (a == x - 1 and b == y + 1) \
                            and (board[h - b][a] == '*' or board[h - b][a].capitalize() == board[h - b][a]):
                        return True
                    elif (a == 5 and b == 1 and board[x + 1][b] == '*' and board[x + 2][b] == '*') or \
                            (a == 5 and b == 1 and board[x - 1][b] == '*'
                             and board[x - 2][b] == '*' and board[x - 3][b] == '*'):
                        return True

                return False

            elif char.capitalize() == 'P':
                if char == 'P':
                    if a == x and b == y + 1 and board[h - b][a - 1] == '*':
                        return True
                    elif h - y + 1 == h - 1 and a == x and b == y + 2 and board[h - b - 1][a - 1] == '*' and \
                            board[h - b][a - 1] == '*':
                        return True
                    elif a == x - 1 and b == y + 1 and board[h - b][a - 1] != '*':
                        if board[h - b][a - 1] != board[h - b][a - 1].capitalize():
                            return True
                        else:
                            return False
                    elif a == x + 1 and b == y + 1 and board[h - b][a - 1] != '*':
                        if board[h - b][a - 1] != board[a][b].capitalize():
                            return True
                        else:
                            return False
                    else:
                        return False

                elif char == 'p':
                    if a == x and b == y - 1 and board[h - b][a - 1] == '*':
                        return True
                    elif y == h - 1 and a == x and b == y - 2 and board[h - b][a - 1] == '*' and board[h - b][a - 1]\
                            == '*':
                        return True
                    elif a == x - 1 and b == y - 1 and board[h - b][a - 1] != '*':
                        if board[h - b][a - 1] != board[h - b][a - 1].capitalize():
                            return True
                        else:
                            return False
                    elif a == x + 1 and b == y - 1 and board[h - b][a - 1] != '*':
                        if board[h - b][a - 1] != board[h - b][a - 1].capitalize():
                            return True
                        else:
                            return False
                    else:
                        return False

        if not (char == '*' or (char.capitalize() == char and t == -1) or (char.capitalize() != char and t == 1) or
                a <= 0 or a > w or b <= 0 or b > h or x <= 0 or x > w or y <= 0 or y > h):
            if valid_position():
                return True
            else:
                return False
        else:
            return False

    def move_piece(x: int, y: int, a: int, b: int, w: int, h: int, t: int) -> None:
        char: str = board[h - y][x - 1]

        if not valid(char, t, x, y, a, b, h, w):
            print("Invalid move!")

            print_board(w, h)
            print("from: ")
            x1 = int(input("x -> "))
            y1 = int(input("y -> "))
            print("to: ")
            x2 = int(input("x -> "))
            y2 = int(input("y -> "))
            print('')
            print('')

            move_piece(x1, y1, x2, y2, 8, 8, t)

        else:
            s1 = ""
            for i in range(x - 1):
                s1 += board[h - y][i]
            s1 += '*'
            for i in range(x, w):
                s1 += board[h - y][i]
            board[h - y] = s1

            s2 = ""
            for i in range(a - 1):
                s2 += board[h - b][i]
            s2 += char
            for i in range(a, w):
                s2 += board[h - b][i]
            board[h - b] = s2

    set_up(8, 8)

    turn = 1
    while True:
        print("from: ")
        x1 = int(input("x -> "))
        y1 = int(input("y -> "))
        print("to: ")
        x2 = int(input("x -> "))
        y2 = int(input("y -> "))
        print('')
        print('')
        print('')
        print('')

        move_piece(x1, y1, x2, y2, 8, 8, turn)

        #             turn *= -1
        print_board(8, 8)


main()
