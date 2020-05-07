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
    """Return list of mistake indices found in given board"""
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
    """Handles solving the sudoku board"""
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
        """Solve whole board and fire event on finish"""
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
        """Attempt next step of solution and fire result"""
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
        """Find all indices of the board where guesses need to be made"""
        guess_index = [0, 0]
        while guess_index != [-1, -1]:
            guess_index = self.get_next_blank(guess_index)
            if guess_index != [-1, -1]:
                self.GuessedIndices.append(guess_index)

    def get_next_blank(self, index):
        """Find next guess index needed"""
        for y in range(index[1], 9):  # we do y first so the order is from
            for x in range(0, 9):  # left to right rather than up/down
                if x > index[0] or y >= (index[1] + 1):
                    if self.Board[x][y] is 0:
                        return [x, y]

        return [-1, -1]

    def guess(self, index):
        """Guess value for given index"""
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
        """Check if value conflicts with the rest of board"""
        for x in range(0, 9):
            if self.Board[x][index[1]] == guess_value:
                return True

        for y in range(0, 9):
            if self.Board[index[0]][y] == guess_value:
                return True

    def on_board_complete(self):
        """Fire on board complete event"""
        self.OnBoardComplete()

    def print_board(self):
        """Print board to console"""
        print("", self.Board[0], "\n", self.Board[1], "\n", self.Board[2], "\n", self.Board[3], "\n",
              self.Board[4], "\n", self.Board[5], "\n",
              self.Board[6], "\n", self.Board[7], "\n", self.Board[8], "\n")


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


def is_hovering(mouse, rect):
    if rect[0] < mouse[0] < rect[0] + rect[2] and rect[1] < mouse[
        1] < rect[1] + rect[3]:
        return True
    else:
        return False


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

    WindowBackgroundColor = (200, 200, 200)
    BaseTextColor = (90, 90, 90)
    BaseTextSize = 20
    BaseFont = gm.font.SysFont('Arial', BaseTextSize)
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
    board_solved_user = False

    keys = gm.key.get_pressed()
    Mouse = gm.mouse.get_pos()
    Click = gm.mouse.get_pressed()
    ActiveBox = [-1, -1]
    event = gm.event.poll()
    LastNumberInput = 0
    start = time.time()
    SolveStart = time.time()
    SolveTime = "Not solved."

    def __init__(self):
        self.Solver.OnGuessMade += self.add_number
        self.Solver.OnGuessRemoved += self.remove_number
        self.Solver.OnBoardComplete += self.on_solver_complete_board
        self.draw()

    def draw(self):
        """Handle drawing"""
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
            if not self.board_solved_user and not self.board_solved:
                self.draw_time()
            self.draw_solve_button()
            self.draw_check_solution_button()
            if self.board_solved:
                self.draw_solver_complete()
            elif self.board_solved_user:
                self.draw_user_complete()

    def draw_base_board(self):
        """Draw the boxes and number values"""
        self.win.fill(self.WindowBackgroundColor)
        self.draw_guides()
        for x in range(0, 9):
            for y in range(0, 9):
                pos = self.get_number_pos([x, y])
                rect = (pos[0], pos[1], self.BoxSize, self.BoxSize)
                base_color = self.BoxColor
                hover_color = self.GuessBoxColor_Hover

                # find out where the value we are going to put is found.
                guess = self.Guesses[x][y] != 0
                user_guess_soft = self.UserSoftGuesses[x][y] != 0
                base_board = self.Board[x][y] != 0
                mistake = self.Mistakes[x][y] == 1

                # Draw box background
                if not self.Solving:
                    if self.ActiveBox == [x, y]:
                        gm.draw.rect(self.win, self.GuessBoxColor_Active, rect)
                    elif is_hovering(self.Mouse, rect) and not base_board:
                        if self.Click[0] == 1:
                            self.ActiveBox = [x, y]
                            if mistake:
                                self.Mistakes[x][y] = 0
                        else:
                            gm.draw.rect(self.win, hover_color, rect)
                    elif mistake:
                        gm.draw.rect(self.win, (150, 20, 20), rect)
                    else:
                        gm.draw.rect(self.win, base_color, rect)
                else:
                    gm.draw.rect(self.win, base_color, rect)

                # Draw box values
                if guess:
                    value = self.Guesses[x][y]
                    text = self.BaseFont.render(str(value), False, self.GuessTextColor)
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
                        text = self.BaseFont.render(value, False, self.BaseTextColor)
                        pos[0] += self.BaseTextSize / 2
                        pos[1] += self.BaseTextSize / 4
                        self.win.blit(text, (pos[0], pos[1]))

    def get_number_pos(self, coords):
        """Get position of coordinate"""
        x_pos = (coords[0] * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        y_pos = (coords[1] * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        return [x_pos, y_pos]

    def draw_guides(self):
        grid_color = (130, 130, 130)
        line_width = 1
        offset = (self.PaddingSize / 2) - (line_width / 2 )
        size = (self.BoxSize * 9) + (self.PaddingSize * 8)
        one = (self.BoxSize * 3) + (self.PaddingSize * 2) + self.MarginSize + offset
        two = (self.BoxSize * 6) + (self.PaddingSize * 5) + self.MarginSize + offset

        vert_one_rect = (one, self.MarginSize, line_width, size)
        vert_two_rect = (two, self.MarginSize, line_width, size)
        hor_one_rect = (self.MarginSize, one, size, line_width)
        hor_two_rect = (self.MarginSize, two, size, line_width)

        gm.draw.rect(self.win, grid_color, vert_one_rect)
        gm.draw.rect(self.win, grid_color, vert_two_rect)
        gm.draw.rect(self.win, grid_color, hor_one_rect)
        gm.draw.rect(self.win, grid_color, hor_two_rect)

    def draw_solve_button(self):
        """Draw solve button in the bottom left"""
        button_color = (50, 150, 25)
        button_color_hover = (80, 200, 25)
        text_color = (200, 200, 200)

        button_pos_y = (9 * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        rect = (self.MarginSize, button_pos_y, 100, 30)
        if is_hovering(self.Mouse, rect):
            gm.draw.rect(self.win, button_color_hover, rect)
            if self.Click[0] == 1:
                self.Solving = True
                self.on_solve_click()

        else:
            gm.draw.rect(self.win, button_color, rect)
        solve_text = self.BaseFont.render("Solve", False, text_color)
        solve_text_pos_x = rect[0] + 25
        solve_text_pos_y = rect[1] + 3
        self.win.blit(solve_text, (solve_text_pos_x, solve_text_pos_y))

    def draw_time(self):
        """Draw time clock on bottom center"""
        text = self.BaseFont.render(self.get_time_elapsed(self.start), False, self.BaseTextColor)
        x = self.MarginSize + self.PaddingSize + 125
        y = (9 * (self.BoxSize + self.PaddingSize)) + self.MarginSize + 5
        self.win.blit(text, (x, y))

    def get_time_elapsed(self, start_time):
        x = time.time() - start_time
        time_elapsed = str(datetime.timedelta(seconds=x))[2:-7]
        return time_elapsed

    def draw_check_solution_button(self):
        """Draw check solution button on the bottom right """
        button_color = (70, 70, 150)
        button_color_hover = (25, 80, 200)
        text_color = (200, 200, 200)

        button_pos_x = self.windowSize_x - self.MarginSize - 100
        button_pos_y = (9 * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        rect = (button_pos_x, button_pos_y, 100, 30)
        if is_hovering(self.Mouse, rect):
            gm.draw.rect(self.win, button_color_hover, rect)
            if self.Click[0] == 1:
                self.on_check_solution_click()

        else:
            gm.draw.rect(self.win, button_color, rect)
        text = self.BaseFont.render("Check", False, text_color)
        text_pos_x = rect[0] + 25
        text_pos_y = rect[1] + 3
        self.win.blit(text, (text_pos_x, text_pos_y))

    def on_solve_click(self):
        """Use solver to solve the board if it isn't solved"""
        self.SolveStart = time.time()
        while self.board_solved is False:
            self.Solver.solve_step()
            self.draw_base_board()

    def on_check_solution_click(self):
        """Check user input for errors. If none, game is solved."""
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
        self.SolveTime = str(self.get_time_elapsed(self.start))
        self.board_solved_user = True

    def on_user_completes_board_inc(self, mistakes):
        """Add mistakes to mistake array"""
        for mistake in mistakes:
            self.Mistakes[mistake[0]][mistake[1]] = 1

    def add_number(self, index, value):
        """Add number to board"""
        self.Board[index[0]][index[1]] = value
        gm.display.update()

    def remove_number(self, index):
        """Remove number from board"""
        self.Board[index[0]][index[1]] = 0

    def on_solver_complete_board(self):
        """Set solved to true. Display message"""
        self.SolveTime = str(self.get_time_elapsed(self.SolveStart))
        self.board_solved = True

    def draw_user_complete(self):
        window_background_color = (80, 80, 80)
        size = (300, 300)
        center = (self.windowSize_x / 2 - (size[0] / 2), (self.windowSize_y / 2) - (size[1] / 2))
        rect = (center[0], center[1], size[0], size[1])
        gm.draw.rect(self.win, window_background_color, rect)

        heading_label = "Complete!"
        heading_color = (40, 200, 100)
        heading_text_size = 30
        heading_font = gm.font.SysFont('Arial', heading_text_size)
        heading_text = heading_font.render(heading_label, False, heading_color)
        heading_text_pos_x = center[0] + 90
        heading_text_pos_y = center[1] + 100

        self.win.blit(heading_text, (heading_text_pos_x, heading_text_pos_y))

        subheading_label = "You solved the board in " + self.SolveTime + "!"
        subheading_color = (80, 160, 100)
        subheading_text_size = 14
        subheading_font = gm.font.SysFont('Arial', subheading_text_size)
        subheading_text = subheading_font.render(subheading_label, False, subheading_color)
        subheading_text_pos_x = center[0] + 20
        subheading_text_pos_y = center[1] + 150
        self.win.blit(subheading_text, (subheading_text_pos_x, subheading_text_pos_y))

    def draw_solver_complete(self):
        window_background_color = (80, 80, 80)
        size = (300, 300)
        center = (self.windowSize_x / 2 - (size[0] / 2), (self.windowSize_y / 2) - (size[1] / 2))
        rect = (center[0], center[1], size[0], size[1])
        gm.draw.rect(self.win, window_background_color, rect)

        heading_label = "Complete!"
        heading_color = (40, 200, 100)
        heading_text_size = 30
        heading_font = gm.font.SysFont('Arial', heading_text_size)
        heading_text = heading_font.render(heading_label, False, heading_color)
        heading_text_pos_x = center[0] + 90
        heading_text_pos_y = center[1] + 100

        self.win.blit(heading_text, (heading_text_pos_x, heading_text_pos_y))

        subheading_label = "The computer solved the board in " + self.SolveTime + "!"
        subheading_color = (80, 160, 100)
        subheading_text_size = 14
        subheading_font = gm.font.SysFont('Arial', subheading_text_size)
        subheading_text = subheading_font.render(subheading_label, False, subheading_color)
        subheading_text_pos_x = center[0] + 20
        subheading_text_pos_y = center[1] + 150
        self.win.blit(subheading_text, (subheading_text_pos_x, subheading_text_pos_y))


drawer = Drawer()
