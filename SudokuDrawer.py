import pygame as gm
import Solver as m

gm.init()
gm.font.init()


class SudokuSolver:
    # numbers cant match in same row, or board[x+1][y]
    Board = []
    GuessIndex = 0
    GuessedIndices = []

    def __init__(self,board):
        self.Board = board

    def solve(self):
        self.find_guessed_indices()
        while self.GuessIndex < len(self.GuessedIndices):
            index = self.GuessedIndices[self.GuessIndex]
            if self.guess(index) is True:
                self.GuessIndex += 1
            else:
                if self.GuessIndex > 0:
                    self.GuessIndex -= 1
                else:
                    self.print_board()
                    break
        self.on_board_complete()

    def find_guessed_indices(self):
        guess_index = [0, -1]
        while guess_index != [-1, -1]:
            guess_index = self.get_next_blank(guess_index)
            self.GuessedIndices.append(guess_index)

    def get_next_blank(self, index):
        for x in range(index[0], 9):
            for y in range(0, 9):
                if x > index[0] or (x == index[0] and y >= (index[1] + 1)):
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
        print("Complete! \n")
        self.print_board()

    def print_board(self):
        print("", self.Board[0], "\n", self.Board[1], "\n", self.Board[2], "\n", self.Board[3], "\n",
              self.Board[4], "\n", self.Board[5], "\n",
              self.Board[6], "\n", self.Board[7], "\n", self.Board[8], "\n")

class Button:
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


    TextSize = 20
    Font = gm.font.SysFont('Arial', TextSize)
    BaseColor = (80, 80, 80)
    GuessTextSize = 10
    GuessTextColor = (125, 125, 125)
    IncorrectBorderColor = (230, 20, 20)
    CorrectBorderColor = (20, 230, 20)
    BackgroundColor = (200, 200, 200)

    BoxSize = 30
    BoxColor = (180, 180, 180)
    MarginSize = 10
    PaddingSize = 5

    ButtonSize_x = 50
    ButtonSize_y = 30

    windowSize_x = (BoxSize + PaddingSize) * 9 + (MarginSize * 2) - PaddingSize
    windowSize_y = windowSize_x + ButtonSize_y + PaddingSize

    win = gm.display.set_mode((windowSize_x, windowSize_y))

    def __init__(self):
        self.draw()

    def draw(self):
        run = True
        while run:
            gm.time.delay(100)
            for event in gm.event.get():
                if event.type == gm.QUIT:
                    run = False

            gm.display.update()
            # draw base board
            self.win.fill(self.BackgroundColor)
            for x in range(0, 9):
                for y in range(0, 9):
                    pos = self.get_number_pos([x, y])
                    gm.draw.rect(self.win, self.BoxColor, (pos[0], pos[1], self.BoxSize, self.BoxSize))
                    if self.Board[x][y] != 0:
                        text = self.Font.render(str(self.Board[x][y]), False, self.BaseColor)
                        pos[0] += self.TextSize / 2
                        pos[1] += self.TextSize / 4
                        self.win.blit(text, (pos[0], pos[1]))

            self.draw_solve_button()

    def get_number_pos(self, coords):
        x_pos = (coords[0] * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        y_pos = (coords[1] * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        return [x_pos, y_pos]

    def draw_solve_button(self):
        mouse = gm.mouse.get_pos()
        click = gm.mouse.get_pressed()
        solve_button_pos_y = (9 * (self.BoxSize + self.PaddingSize)) + self.MarginSize
        solve_button = Button([self.MarginSize, solve_button_pos_y, 100, 30], (30, 220, 30), (110, 250, 30))
        if solve_button.IsHovering(mouse):
            gm.draw.rect(self.win, solve_button.HoverColor, solve_button.Rect)
            if click[0] == 1:
                self.Manager.solve()

        else:
            gm.draw.rect(self.win, solve_button.BaseColor, solve_button.Rect)
        solve_text = self.Font.render("Solve", False, self.BaseColor)
        solve_text_pos_x = solve_button.Rect[0] + 25
        solve_text_pos_y = solve_button.Rect[1] + 3
        self.win.blit(solve_text, (solve_text_pos_x, solve_text_pos_y))

    def add_number(self, index, value):
        self.Board[index[0]][index[1]] = value

    def remove_number(self, index):
        self.Board[index[0]][index[1]] = 0

    def on_finished(self):
        print("Game is complete!")

    def on_player_click(self, index):
        print("Player clicked on square ", index)

    def set_manager(self, manager):
        self.Manager = manager

drawer = Drawer()

