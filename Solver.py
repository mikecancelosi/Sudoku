class SudokuSolver:
    # numbers cant match in same row, or board[x+1][y]
    board = [
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

    GuessIndex = 0
    GuessedIndices = []

    def __init__(self):
        print("IniT!")

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
                    if self.board[x][y] is 0:
                        return [x, y]
        return [-1, -1]

    def guess(self, index):
        initial_value = self.board[index[0]][index[1]]
        guess = initial_value
        for i in range(guess + 1, 10):
            if not self.check_for_conflicts(index, i):
                guess = i
                break

        if guess != initial_value:
            self.board[index[0]][index[1]] = guess
            return True
        else:
            self.board[index[0]][index[1]] = 0
            return False

    def check_for_conflicts(self, index, guess_value):
        for x in range(0, 9):
            if self.board[x][index[1]] == guess_value:
                return True

        for y in range(0, 9):
            if self.board[index[0]][y] == guess_value:
                return True

    def on_board_complete(self):
        print("Complete! \n")
        self.print_board()

    def print_board(self):
        print("", self.board[0], "\n", self.board[1], "\n", self.board[2], "\n", self.board[3], "\n",
              self.board[4], "\n", self.board[5], "\n",
              self.board[6], "\n", self.board[7], "\n", self.board[8], "\n")


Manager = SudokuSolver()
