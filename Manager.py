import pygame as gm


class SudokuManager:
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

    GuessIndex = [0, 0]
    GuessedIndices = []

    def solve(self):
        print("Attempting to solve..")
        self.find_guessed_indices()
        newindex = self.get_next_blank(self.GuessIndex)
        print("new index is", newindex)
        while self.GuessIndex is not [-1, -1]:
            if self.guess(self.GuessIndex) is True:
                self.GuessIndex = self.get_next_blank(self.GuessIndex)
            else:
                self.GuessIndex = self.get_previous_blank(self.GuessIndex)

    def find_guessed_indices(self):
        guessIndex = [0, 0]
        while guessIndex != [-1, -1]:
            guessIndex = self.get_next_blank(guessIndex)
            self.GuessedIndices.append(guessIndex)
            
    def get_next_blank(self, index):
        if index[1] < 8:
            index[1] += 1
        elif index[0] == 8:
            return [-1, -1]
        else:
            index[0] += 1
            index[1] = 0

        for x in range(index[0], 9):
            for y in range(0, 9):
                if x > index[0] or (x == index[0] and y >= index[1]):
                    if self.board[x][y] is 0:
                        return [x, y]

    def guess(self, index):
        initial_value = self.board[index[0]][index[1]]
        guess = initial_value
        for i in range(guess, 9):
            for x in range(0, 9):
                if self.board[x][index[1]] == i:
                    continue
            for y in range(0, 9):
                if self.board[index[0]][y] == i:
                    continue
            guess = i
            break
        if guess != initial_value:
            self.board[index[0]][index[1]] = guess
            return True
        else:
            self.board[index[0]][index[1]] = 0
            return False

    def get_previous_blank(self, startIndex):
        GuessedIndex = -1
        for i in range(0, len(self.GuessedIndices)):
            if self.GuessedIndices is startIndex:
                GuessedIndex = i

        if GuessedIndex > 0:
            return self.GuessedIndices[GuessedIndex - 1]
        else:
            print("somethin went wrong in getting previous blank")

    def on_board_complete(self):
        print("Complete!", self.board)


class Drawer:
    FontSize = 20
    GuessFontSize = 10
    GuessFontColor = (125, 125, 125)
    IncorrectBorderColor = (230, 20, 20)
    CorrectBorderColor = (20, 230, 20)

    def __init__(self):
        print("Drawing")

    def add_number(self, index, value, guess):
        print("adding number at", index)

    def remove_number(self, index, value, guess):
        print("removing number at", index)

    def on_finished(self):
        print("Game is complete!")

    def on_player_click(self, index):
        print("Player clicked on square ", index)


Manager = SudokuManager()
Manager.solve()
