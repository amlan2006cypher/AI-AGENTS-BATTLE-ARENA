WIN_SCORE = 100


def _lines(board):
    lines = list(board)
    lines += [[board[r][c] for r in range(3)] for c in range(3)]
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])
    return lines


def heuristic_h1(board, player):
    """Threat-focused heuristic: wins, blocks, center, corners, two-in-a-row."""
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    for line in _lines(board):
        p = line.count(player)
        o = line.count(opponent)
        e = line.count('')
        if p == 3:
            score += 100
        elif o == 3:
            score -= 100
        elif p == 2 and e == 1:
            score += 12
        elif o == 2 and e == 1:
            score -= 15
        elif p == 1 and e == 2:
            score += 2
        elif o == 1 and e == 2:
            score -= 2

    if board[1][1] == player:
        score += 4
    elif board[1][1] == opponent:
        score -= 4

    for r, c in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[r][c] == player:
            score += 3
        elif board[r][c] == opponent:
            score -= 3
    return score


def heuristic_h2(board, player):
    """Position-focused heuristic: weighted line potential plus positional control."""
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    weights = {1: 1, 2: 6, 3: 100}
    for line in _lines(board):
        p = line.count(player)
        o = line.count(opponent)
        if p and not o:
            score += weights[p]
        elif o and not p:
            score -= weights[o]

    if board[1][1] == player:
        score += 7
    elif board[1][1] == opponent:
        score -= 7

    for r, c in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[r][c] == player:
            score += 4
        elif board[r][c] == opponent:
            score -= 4

    # Small edge preference; this keeps H2 meaningfully different from H1.
    for r, c in [(0, 1), (1, 0), (1, 2), (2, 1)]:
        if board[r][c] == player:
            score += 1
        elif board[r][c] == opponent:
            score -= 1
    return score
