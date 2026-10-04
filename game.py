from copy import deepcopy


class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]

    def reset(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]

    def display(self):
        for r in range(3):
            print(' | '.join(cell if cell else ' ' for cell in self.board[r]))
            if r < 2:
                print('---------')

    def get_valid_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '']

    def make_move(self, move, player):
        r, c = move
        if self.board[r][c] != '':
            return False
        self.board[r][c] = player
        return True

    def check_winner(self):
        lines = []
        lines.extend(self.board)
        lines.extend([[self.board[r][c] for r in range(3)] for c in range(3)])
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])
        for line in lines:
            if line[0] and line[0] == line[1] == line[2]:
                return line[0]
        return None

    def is_draw(self):
        return self.check_winner() is None and not self.get_valid_moves()

    def is_terminal(self):
        return self.check_winner() is not None or self.is_draw()

    def copy(self):
        new_game = TicTacToe()
        new_game.board = deepcopy(self.board)
        return new_game
