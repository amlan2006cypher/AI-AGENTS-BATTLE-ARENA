import argparse
import random
from experiment import run_battle, run_depth_experiment, print_summary


def main():
    parser = argparse.ArgumentParser(description='AI Agent Battle - Tic-Tac-Toe')
    parser.add_argument('--mode', choices=['all', 'depth', 'battle'], default='all')
    args = parser.parse_args()
    random.seed(42)

    depth_rows = run_depth_experiment() if args.mode in ('all', 'depth') else []
    battle_rows = run_battle() if args.mode in ('all', 'battle') else []
    print_summary(depth_rows, battle_rows)


if __name__ == '__main__':
    main()
