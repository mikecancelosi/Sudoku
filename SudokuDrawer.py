import pygame as gm
import time
import datetime

gm.init()
gm.font.init()


class Event(object):

    def __init__(self):
        self.__eventhandlers = []

    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)


def check_board_for_conflicts(board):
    mistakes = []
    for x in range(0, 9):
        for y in range(0, 9):
            for x2 in range(0, 9):
                if x != x2:
                    if board[x][y] == board[x2][y]:
                        mistakes.append([x, y])

            for y2 in range(0, 9):
                if y != y2:
                    if board[x][y] == board[x][y2]:
                        mistakes.append([x, y])

    return mistakes


class SudokuSolver:
    # numbers cant match in same row, or board[x+1][y]
    Board = []
    GuessIndex = 0
    GuessedIndices = []

    def __init__(self, board):
        self.Board = board
        self.find_guessed_indices()
        self.OnGuessMade = Event()
        self.OnGuessRemoved = Event()
        self.OnBoardComplete = Event()

    def solve(self):
        print("whole solve")
        while self.GuessIndex < len(self.GuessedIndices):
            index = self.GuessedIndices[self.GuessIndex]
            if self.guess(index) is True:
                self.OnGuessMade(index, self.Board[index[0]][index[1]])
                self.GuessIndex += 1
            else:
                if self.GuessIndex > 0:
                    self.OnGuessRemoved(index)
                    self.GuessIndex -= 1
                else:
                    self.print_board()
                    break
        self.on_board_complete()

    def solve_step(self):
        if self.GuessIndex < len(self.GuessedIndices):
            index = self.GuessedIndices[self.GuessIndex]
            if self.guess(index) is True:
                self.OnGuessMade(index, self.Board[index[0]][index[1]])
                self.GuessIndex += 1
            else:
                if self.GuessIndex > 0:
                    self.OnGuessRemoved(index)
                    self.GuessIndex -= 1
                else:
                    self.print_board()
        else:
            self.on_board_complete()

    def find_guessed_indices(self):
        guess_index = [0, 0]
        while guess_index != [-1, -1]:
            guess_index = self.get_next_blank(guess_index)
            if guess_index != [-1, -1]:
                self.GuessedIndices.append(guess_index)

    def get_next_blank(self, index):
        for y in range(index[1], 9):  # we do y first so the order is from
            for x in range(0, 9):  # left to right rather than up/down
                if x > index[0] or y >= (index[1] + 1):
                    if self.Board[x][y] is 0:
                        return [x, y]

        return [-1, -1]

    def guess(self, index):
        initial_value = self.Board[index[0]][index[1]]
        guess = initial_value
        for i in range(guess + 1, 10):
            if not self.check_for_conflicts(index, i):
                guess = i
                break

        if guess != initial_value:
            self.Board[index[0]][index[1]] = guess
            return True
        else:
            self.Board[index[0]][index[1]] = 0
            return False

    def check_for_conflicts(self, index, guess_value):
        for x in range(0, 9):
            if self.Board[x][index[1]] == guess_value:
                return True

        for y in range(0, 9):
            if self.Board[index[0]][y] == guess_value:
                return True

    def on_board_complete(self):
        self.OnBoardComplete()

    def print_board(self):
        print("", self.Board[0], "\n", self.Board[1], "\n", self.Board[2], "\n", self.Board[3], "\n",
              self.Board[4], "\n", self.Board[5], "\n",
              self.Board[6], "\n", self.Board[7], "\n", self.Board[8], "\n")


class Square:
    Rect = []
    BaseColor = (130, 130, 130)
    HoverColor = (170, 170, 170)

    def __init__(self, rect, base_color, hover_color):
        self.Rect = rect
        self.BaseColor = base_color
        self.HoverColor = hover_color

    def IsHovering(self, mouse):
        if self.Rect[0] < mouse[0] < self.Rect[0] + self.Rect[2] and self.Rect[1] < mouse[
            1] < self.Rect[1] + self.Rect[3]:
            return True
        else:
            return False


def parse_number_input(input):
    if input.isdigit():
        if 0 < int(input) < 10:
            return int(input)
        else:
            return -1
    elif len(input) == 3 and input[1].isdigit():
        if 0 < int(input[1]) < 10:
            return int(input[1])
        else:
            return -1
    else:
        return -1


class Drawer:
    Board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    Guesses = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    SolverGuesses = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    UserSoftGuesses = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    Mistakes = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    TextSize = 20
    Font = gm.font.SysFont('Arial', TextSize)

    WindowBackgroundColor = (200, 200, 200)
    BaseTextColor = (90, 90, 90)
    GuessTextSize = 20
    GuessTextColor = (125, 125, 125)
    SoftGuessTextSize = 14
    SoftGuessTextColor = (100, 100, 100)
    SoftGuessFont = gm.font.SysFont('Arial', SoftGuessTextSize)
    GuessBoxColor_Base = (80, 80, 80)
    GuessBoxColor_Hover = (90, 90, 90)
    GuessBoxColor_Active = (180, 180, 80)

    BoxSize = 30
    BoxColor = (180, 180, 180)
    MarginSize = 10
    PaddingSize = 5
    ButtonSize_x = 50
    ButtonSize_y = 30
    windowSize_x = (BoxSize + PaddingSize) * 9 + (MarginSize * 2) - PaddingSize
    windowSize_y = windowSize_x + ButtonSize_y + PaddingSize

    win = gm.display.set_mode((windowSize_x, windowSize_y))
    Solver = SudokuSolver(Board)
    board_solved = False
    Solving = False

    keys = gm.key.get_pressed()
    Mouse = gm.mouse.get_pos()
    Click = gm.mouse.get_pressed()
    ActiveBox = [-1, -1]
    event = gm.event.poll()
    LastNumberInput = 0
    start = time.time()

    def __init__(self):
        self.Solver.OnGuessMade += self.add_number
        self.Solver.OnGuessRemoved += self.remove_number
        self.Solver.OnBoardComplete += self.on_finished
        self.draw()

    def draw(self):
        run = True
        while run:
            gm.time.delay(100)
            for event in gm.event.get():
                if event.type == gm.QUIT:
                    run = False
                if event.type == gm.KEYDOWN:
                    key = gm.key.name(event.key)  # Returns string id of pressed key.
                    if key == "tab":
                        next_pos = self.Solver.get_next_blank(self.ActiveBox)
                        if next_pos != [-1, -1]:
                            self.ActiveBox = next_pos
                    elif key == "enter" or key == "return":
                        x = self.ActiveBox[0]
                        y = self.ActiveBox[1]
                        if self.UserSoftGuesses[x][y]:
                            value = self.UserSoftGuesses[x][y]
                            self.UserSoftGuesses[x][y] = 0
                            self.Guesses[x][y] = value
                    else:
                        result = parse_number_input(key)
                        if result != -1:
                            if self.ActiveBox != [-1, -1]:
                                self.UserSoftGuesses[self.ActiveBox[0]][self.ActiveBox[1]] = result

            self.Mouse = gm.mouse.get_pos()
            self.Click = gm.mouse.get_pressed()

            gm.display.update()
            self.draw_base_board()
            self.draw_time()
            self.draw_solve_button()
            self.draw_check_solution_button()

    def draw_base_board(self):
        # draw base board
        self.win.fill(self.WindowBackgroundColor)
        for x in range(0, 9):
            for y in range(0, 9):
                pos = self.get_number_pos([x, y])
                box = Square((pos[0], pos[1], self.BoxSize, self.BoxSize), self.BoxColor, self.GuessBoxColor_Hover)

                # find out where the value we are going to put is found.
                guess = self.Guesses[x][y] != 0
                user_guess_soft = self.UserSoftGuesses[x][y] != 0
                base_board = self.Board[x][y] != 0
                mistake = self.Mistakes[x][y] == 1

                # Draw box background

                if self.ActiveBox == [x, y]:
                    gm.draw.rect(self.win, self.GuessBoxColor_Active, box.Rect)
                elif box.IsHovering(self.Mouse) and not base_board:
                    if self.Click[0] == 1:
                        self.ActiveBox = [x, y]
                    else:
                        gm.draw.rect(self.win, box.HoverColor, box.Rect)
                elif mistake:
                    gm.draw.rect(self.win, (150, 20, 20), box.Rect)
                else:
                    gm.draw.rect(self.win, box.BaseColor, box.Rect)

                # Draw box values
                if guess:
                    value = self.Guesses[x][y]
                    text = self.Font.render(str(value), False, self.GuessTextColor)
                    pos[0] += self.GuessTextSize / 2
                    pos[1] += self.GuessTextSize / 4
                    self.win.blit(text, (pos[0], pos[1]))
                elif user_guess_soft:
                    value = self.UserSoftGuesses[x][y]
                    text = self.SoftGuessFont.render(str(value), False, self.SoftGuessTextColor)
                    pos[0] += self.SoftGuessTextSize / 3
                    pos[1] += self.SoftGuessTextSize / 5
                    self.win.blit(text, (pos[0], pos[1]))
                else:
                    value = str(self.Board[x][y])
                    if value != "0":
                        text = self.Font.render(value, False, self.BaseTextColor)
                        pos[0] += self.TextSize / 2
                        pos[1] += self.TextSize / 4
                        self.win.blit(text, (pos[0], pos[1]))

    def get_number_pos(self, coords):
        x_pos = (coords[0] * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        y_pos = (coords[1] * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        return [x_pos, y_pos]

    def draw_solve_button(self):
        button_color = (50, 150, 25)
        button_color_hover = (80, 200, 25)
        text_color = (200, 200, 200)

        button_pos_y = (9 * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        button = Square([self.MarginSize, button_pos_y, 100, 30], button_color, button_color_hover)
        if button.IsHovering(self.Mouse):
            gm.draw.rect(self.win, button.HoverColor, button.Rect)
            if self.Click[0] == 1:
                self.Solving = True
                self.on_solve_click()

        else:
            gm.draw.rect(self.win, button.BaseColor, button.Rect)
        solve_text = self.Font.render("Solve", False, text_color)
        solve_text_pos_x = button.Rect[0] + 25
        solve_text_pos_y = button.Rect[1] + 3
        self.win.blit(solve_text, (solve_text_pos_x, solve_text_pos_y))

    def draw_time(self):
        x = time.time() - self.start
        time_elapsed = str(datetime.timedelta(seconds=x))[2:-7]
        text = self.Font.render(time_elapsed, False, self.BaseTextColor)
        x = self.MarginSize + self.PaddingSize + 125
        y = (9 * (self.BoxSize + self.PaddingSize)) + self.MarginSize + 5
        self.win.blit(text, (x, y))

    def draw_check_solution_button(self):
        button_color = (70, 70, 150)
        button_color_hover = (25, 80, 200)
        text_color = (200, 200, 200)

        button_pos_x = self.windowSize_x - self.MarginSize - 100
        button_pos_y = (9 * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        button = Square([button_pos_x, button_pos_y, 100, 30], button_color, button_color_hover)
        if button.IsHovering(self.Mouse):
            gm.draw.rect(self.win, button.HoverColor, button.Rect)
            if self.Click[0] == 1:
                self.on_check_solution_click()

        else:
            gm.draw.rect(self.win, button.BaseColor, button.Rect)
        text = self.Font.render("Check", False, text_color)
        text_pos_x = button.Rect[0] + 25
        text_pos_y = button.Rect[1] + 3
        self.win.blit(text, (text_pos_x, text_pos_y))

    def on_solve_click(self):
        while self.board_solved is False:
            self.Solver.solve_step()
            self.draw_base_board()

    def on_check_solution_click(self):
        board_cpy = self.Board
        mistakes = []

        for x in range(0, 9):
            for y in range(0, 9):
                if board_cpy[x][y] == 0:
                    guess = self.Guesses[x][y]
                    if guess == 0:
                        mistakes.append([x, y])
                    else:
                        board_cpy[x][y] = guess

        if len(mistakes) == 0:
            # we now have a filled combined boards
            mistakes = check_board_for_conflicts(board_cpy)
            if len(mistakes) > 0:
                self.on_user_completes_board_inc(mistakes)
            else:
                self.on_user_complete_board()
        else:
            self.on_user_completes_board_inc(mistakes)

    def on_user_complete_board(self):
        print("user did it!")

    def on_user_completes_board_inc(self, mistakes):
        for mistake in mistakes:
            self.Mistakes[mistake[0]][mistake[1]] = 1

    def add_number(self, index, value):
        self.Board[index[0]][index[1]] = value
        gm.display.update()

    def remove_number(self, index):
        self.Board[index[0]][index[1]] = 0

    def on_finished(self):
        print("Game is complete!")
        self.board_solved = True

    def set_manager(self, manager):
        self.Manager = manager


drawer = Drawer()
