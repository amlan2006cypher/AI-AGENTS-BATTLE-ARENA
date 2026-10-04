from dataclasses import dataclass


@dataclass
class SearchStats:
    nodes_evaluated: int = 0
    nodes_pruned: int = 0

    def reset(self):
        self.nodes_evaluated = 0
        self.nodes_pruned = 0


def minimax_alpha_beta(game, depth, maximizing_player, ai_player, heuristic, stats, alpha=float('-inf'), beta=float('inf')):
    winner = game.check_winner()
    opponent = 'O' if ai_player == 'X' else 'X'

    if winner == ai_player:
        stats.nodes_evaluated += 1
        return 1000 + depth
    if winner == opponent:
        stats.nodes_evaluated += 1
        return -1000 - depth
    if game.is_draw() or depth == 0:
        stats.nodes_evaluated += 1
        return heuristic(game.board, ai_player)

    if maximizing_player:
        best = float('-inf')
        for move in game.get_valid_moves():
            child = game.copy()
            child.make_move(move, ai_player)
            value = minimax_alpha_beta(child, depth - 1, False, ai_player, heuristic, stats, alpha, beta)
            best = max(best, value)
            alpha = max(alpha, best)
            if alpha >= beta:
                stats.nodes_pruned += 1
                break
        return best

    best = float('inf')
    for move in game.get_valid_moves():
        child = game.copy()
        child.make_move(move, opponent)
        value = minimax_alpha_beta(child, depth - 1, True, ai_player, heuristic, stats, alpha, beta)
        best = min(best, value)
        beta = min(beta, best)
        if alpha >= beta:
            stats.nodes_pruned += 1
            break
    return best


def search(game, ai_player, depth, heuristic, stats):
    best_score = float('-inf')
    best_moves = []
    alpha = float('-inf')
    beta = float('inf')

    for move in game.get_valid_moves():
        child = game.copy()
        child.make_move(move, ai_player)
        score = minimax_alpha_beta(
            child, max(depth - 1, 0), False, ai_player, heuristic, stats, alpha, beta
        )
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)
        alpha = max(alpha, best_score)

    return best_moves, best_score
