"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    for i in range (0,len(board)):
        for k in range(0,len(board)):
            if board[i][k] != " ":
                return False
    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    boundary = 2
    if (y_end + d_y) > 7 or (x_end + d_x) > 7 or (y_end + d_y) < 0 or (x_end + d_x) < 0:
        boundary -= 1
        print("Boundary") ###

    elif (board[y_end + d_y][x_end + d_x] != board[y_end][x_end]) and board[y_end + d_y][x_end + d_x] != " ":
        boundary -= 1
        print("Black") ###

    if (y_end - length*d_y) < 0 or (x_end - length*d_x) < 0 or (y_end - length*d_y) > 7 or (x_end - length*d_x) > 7:
        boundary -= 1
        print("Boundary1") ###

    elif board[y_end - length*d_y][x_end-length*d_x] != (board[y_end][x_end]) and board[y_end - length*d_y][x_end-length*d_x] != " " :
        boundary -= 1
        print("Black1") ###



    if boundary == 2:
        return "OPEN"
    if boundary == 1:
        return "SEMIOPEN"
    if boundary == 0:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):

    open_seq_count = 0
    semi_open_seq_count = 0
    count = 0
    for i in range(0,8):

        if y_start + d_y * i > 7 or x_start + d_x * i > 7 or x_start + d_x * i < 0 or y_start + d_y * i < 0:
            break


        if board[y_start + d_y * i][x_start + d_x * i] != col:
            count = 0

        if board[y_start + d_y * i][x_start + d_x * i] == col:
            count += 1



        if count == length:

            if (y_start + d_y * i + d_y) > 7 or x_start + d_x * i + d_x > 7 or (y_start + d_y * i + d_y) < 0 or (x_start + d_x * i + d_x) < 0:
                if is_bounded(board, y_start + d_y * i, x_start + d_x * i, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1

                if is_bounded(board, y_start + d_y * i, x_start + d_x * i, length, d_y, d_x) == "SEMIOPEN":


                    semi_open_seq_count += 1
                break

            if board[y_start + d_y * i + d_y][x_start + d_x * i + d_x] == col:

                continue   ###Check next one

            else:

                print("yend:",y_start + d_y * i)  ###
                print("xend:",x_start + d_x * i) ###
                if is_bounded(board, y_start + d_y * i, x_start + d_x * i, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                if is_bounded(board, y_start + d_y * i, x_start + d_x * i, length, d_y, d_x) == "SEMIOPEN":

                    semi_open_seq_count += 1



    return open_seq_count, semi_open_seq_count

'''def detect_row(board, col, y_start, x_start, length, d_y, d_x):'''

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    for i in range(0,len(board)): # vertical


        semi_open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[1]


        open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[0]

        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, 0)[1]

        open_seq_count += detect_row(board, col, 0, i, length, 1, 0)[0]

        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, -1)[1]
        #Upper right to Lower left

        open_seq_count += detect_row(board, col, 0, i, length, 1, -1)[0]
        #Upper right to Lower left

        if i != 0:
            semi_open_seq_count += detect_row(board, col, i, 7, length, 1, -1)[1]
            open_seq_count += detect_row(board, col, i, 7, length, 1, -1)[0]

        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[1]

        open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[0]

        if i != 0:
            semi_open_seq_count += detect_row(board, col, i, 0, length, 1, 1)[1]
        # if semi_open_seq_count == 2:
        #     print("3")
        #     print("YESLKJ")
            open_seq_count += detect_row(board, col, i, 0, length, 1, 1)[0]

    return open_seq_count, semi_open_seq_count

def search_max(board):
    current_max_score = score(board)
    current_score = 0
    move_y = 0
    move_x = 0

    for i in range (0,len(board)):
        for k in range(0,len(board)):
            if board[i][k] == " ":
                board[i][k] = "b"
                current_score = score(board)

                if current_score > current_max_score:
                    current_max_score = current_score
                    print("Greater score is found. Move:",move_y,move_x)
                    move_y = i
                    move_x = k
                board[i][k] = " "
    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    if score(board) == 100000:
        return "Black won"
    if score(board) == -100000:
        return "White won"
    for i in range (0,len(board)):
        for k in range(0,len(board)):
            if board[i][k] == " ":
                return "Continue playing"
    return "Draw"






def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    print(board)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    # board = [[' ', 'b', ' ', ' ', ' ', ' ', ' ', 'w'],
    #         ['b', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #         ['b', ' ', 'w', ' ', 'w', 'w', ' ', ' '],
    #         ['b', ' ', 'b', 'w', 'b', 'w', ' ', ' '],
    #         [' ', ' ', 'w', 'b', 'w', ' ', ' ', 'w'],
    #         [' ', ' ', 'b', 'w', 'b', ' ', ' ', 'w'],
    #         [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
    #         [' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b']]

    # board = [[' ', 'b', ' ', ' ', 'b', ' ', ' ', 'w'],
    #          ['b', 'w', 'b', 'w', ' ', 'b', 'b', 'w'],
    #          ['w', 'b', ' ', 'w', 'b', 'b', 'w', 'b'],
    #          ['w', ' ', 'b', 'b', 'b', ' ', ' ', 'w'],
    #          [' ', 'b', 'w', 'w', ' ', 'b', 'w', 'b'],
    #          ['b', 'w', 'b', 'w', 'w', ' ', ' ', ' '],
    #          [' ', 'b', 'w', 'b', ' ', 'b', 'w', 'b'],
    #          ['w', 'b', 'b', ' ', 'w', 'w', 'w', ' ']]
    #
    #
    # detect_row(board, 'b', 0, 5, 4, 1, -1)
    # detect_rows(board, "w", 2)

    play_gomoku(8)








