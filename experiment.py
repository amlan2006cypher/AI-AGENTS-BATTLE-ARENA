import csv
import os
import random
import time
from agents import Agent
from game import TicTacToe
from heuristic import heuristic_h1, heuristic_h2


RESULT_DIR = 'results'
DEPTH_FILE = os.path.join(RESULT_DIR, 'depth_results.csv')
BATTLE_FILE = os.path.join(RESULT_DIR, 'battle_results.csv')


def make_agent(name, depth, heuristic_name):
    heuristic = heuristic_h1 if heuristic_name == 'H1' else heuristic_h2
    return Agent(name, depth, heuristic)


def run_game(agent_x, agent_o, game_number=1):
    game = TicTacToe()
    agents = {'X': agent_x, 'O': agent_o}
    total_nodes = {agent_x.name: 0, agent_o.name: 0}
    total_pruned = {agent_x.name: 0, agent_o.name: 0}
    total_time = {agent_x.name: 0.0, agent_o.name: 0.0}
    moves = 0

    start = time.perf_counter()
    while not game.is_terminal():
        player = 'X' if moves % 2 == 0 else 'O'
        agent = agents[player]
        move, stats, elapsed, _ = agent.choose_move(game, player)
        game.make_move(move, player)
        total_nodes[agent.name] += stats.nodes_evaluated
        total_pruned[agent.name] += stats.nodes_pruned
        total_time[agent.name] += elapsed
        moves += 1

    elapsed_game = time.perf_counter() - start
    winner_symbol = game.check_winner()
    winner = 'DRAW' if winner_symbol is None else agents[winner_symbol].name
    return {
        'game': game_number,
        'first': agent_x.name,
        'winner': winner,
        'moves': moves,
        'nexus_nodes': total_nodes.get('NEXUS', 0),
        'titan_nodes': total_nodes.get('TITAN', 0),
        'nexus_pruned': total_pruned.get('NEXUS', 0),
        'titan_pruned': total_pruned.get('TITAN', 0),
        'test_nodes': total_nodes.get('DEPTH_TEST', 0),
        'test_pruned': total_pruned.get('DEPTH_TEST', 0),
        'execution_time': elapsed_game,
        'nexus_time': total_time.get('NEXUS', 0.0),
        'titan_time': total_time.get('TITAN', 0.0),
    }


def run_depth_experiment():
    rows = []
    reference_depth = 4
    for depth in [1, 2, 3, 4]:
        test_agent = make_agent('DEPTH_TEST', depth, 'H1')
        reference_agent = make_agent('REFERENCE', reference_depth, 'H1')
        total_test_nodes = total_test_pruned = 0
        total_time = 0.0
        wins = draws = losses = 0
        for i in range(10):
            x, o = (test_agent, reference_agent) if i % 2 == 0 else (reference_agent, test_agent)
            result = run_game(x, o, i + 1)
            winner = result['winner']
            if winner == 'DEPTH_TEST':
                wins += 1
            elif winner == 'DRAW':
                draws += 1
            else:
                losses += 1
            total_test_nodes += result['test_nodes']
            total_test_pruned += result['test_pruned']
            total_time += result['execution_time']
        rows.append({
            'depth': depth,
            'result': f'{wins} wins / {draws} draws / {losses} losses',
            'nodes_evaluated': total_test_nodes,
            'nodes_pruned': total_test_pruned,
            'time_seconds': round(total_time, 6),
            'average_time_seconds': round(total_time / 10, 6),
        })

    os.makedirs(RESULT_DIR, exist_ok=True)
    with open(DEPTH_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows


def run_battle():
    nexus = make_agent('NEXUS', 3, 'H1')
    titan = make_agent('TITAN', 3, 'H2')
    rows = []
    for i in range(10):
        x, o = (nexus, titan) if i % 2 == 0 else (titan, nexus)
        rows.append(run_game(x, o, i + 1))

    os.makedirs(RESULT_DIR, exist_ok=True)
    with open(BATTLE_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows


def summarize_battle(rows):
    nexus_wins = sum(r['winner'] == 'NEXUS' for r in rows)
    titan_wins = sum(r['winner'] == 'TITAN' for r in rows)
    draws = sum(r['winner'] == 'DRAW' for r in rows)
    return nexus_wins, titan_wins, draws


def print_summary(depth_rows, battle_rows):
    print('\n=== SEARCH DEPTH EXPERIMENT ===')
    for row in depth_rows:
        print(row)
    n, t, d = summarize_battle(battle_rows)
    print('\n=== 10-GAME AI BATTLE ===')
    for row in battle_rows:
        print(row)
    print(f'\nNEXUS wins: {n} | TITAN wins: {t} | Draws: {d}')


if __name__ == '__main__':
    random.seed(42)
    depth_rows = run_depth_experiment()
    battle_rows = run_battle()
    print_summary(depth_rows, battle_rows)
