import random
import time
from minimax import SearchStats, search


class Agent:
    def __init__(self, name, depth, heuristic):
        self.name = name
        self.depth = depth
        self.heuristic = heuristic

    def choose_move(self, game, player):
        stats = SearchStats()
        start = time.perf_counter()
        moves, score = search(game, player, self.depth, self.heuristic, stats)
        elapsed = time.perf_counter() - start
        move = random.choice(moves)
        return move, stats, elapsed, score
