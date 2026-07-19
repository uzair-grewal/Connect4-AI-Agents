#!/usr/bin/env python3
"""Simple CLI tool to simulate Connect Four games between agents."""

import argparse
import sys
from engine import ConnectFour
from agents.random_agent import RandomAgent
from agents.rule_based_agent import RuleBasedAgent
from agents.minimax_agent import MinimaxAgent


def play_game(agent1, agent2, verbose=False):
    """Play a single game and return (winner, move_count)."""
    game = ConnectFour()
    agents = {1: agent1, 2: agent2}
    moves = []

    while not game.is_terminal():
        agent = agents[game.current_player]
        move = agent.choose_move(game)
        moves.append(move)
        game.apply_move(move)

    winner = game.winner()
    if verbose:
        print(game)
        print(f"Moves: {moves}")
        if winner:
            print(f"Player {winner} wins!")
        else:
            print("Draw!")

    return winner, len(moves)


def main():
    parser = argparse.ArgumentParser(
        description="Simulate Connect Four games between agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simulate.py --agent1 random --agent2 rule-based --games 10
  python simulate.py --agent1 minimax --agent2 random --games 50
  python simulate.py --agent1 rule-based --agent2 minimax --games 20 --verbose

Notes:
  - Minimax depth is fixed at 4
  - First player alternates every game (e.g., games 0,2,4... agent1 is first)
  - Results show combined statistics across all alternations
        """
    )

    parser.add_argument(
        "--agent1",
        choices=["random", "rule-based", "minimax"],
        default="random",
        help="First agent (default: random)"
    )
    parser.add_argument(
        "--agent2",
        choices=["random", "rule-based", "minimax"],
        default="rule-based",
        help="Second agent (default: rule-based)"
    )
    parser.add_argument(
        "--games",
        type=int,
        default=5,
        help="Number of games to simulate (default: 5)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed base for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print board state and moves for each game"
    )

    args = parser.parse_args()

    # Minimax depth is fixed at 4
    MINIMAX_DEPTH = 4

    # Create agent factories
    def create_agent(agent_type, seed):
        if agent_type == "random":
            return RandomAgent(seed=seed)
        elif agent_type == "rule-based":
            return RuleBasedAgent(seed=seed)
        elif agent_type == "minimax":
            return MinimaxAgent(depth=MINIMAX_DEPTH, seed=seed)

    # Run simulations
    print(f"\nSimulating {args.games} games: {args.agent1.upper()} vs {args.agent2.upper()}")
    if args.agent1 == "minimax" or args.agent2 == "minimax":
        print(f"Minimax depth: {MINIMAX_DEPTH} (fixed)")
    print(f"Seed base: {args.seed}")
    print(f"First-player alternation: ENABLED (alternates every game)")
    print("-" * 60)

    agent1_wins = 0
    agent2_wins = 0
    draws = 0
    total_moves = 0

    for game_num in range(args.games):
        # Alternate which agent moves first
        if game_num % 2 == 0:
            # Even games: agent1 moves first
            agent1 = create_agent(args.agent1, args.seed + game_num)
            agent2 = create_agent(args.agent2, args.seed + 1000 + game_num)
            winner, move_count = play_game(agent1, agent2, verbose=args.verbose)
        else:
            # Odd games: agent2 moves first
            agent2 = create_agent(args.agent2, args.seed + 1000 + game_num)
            agent1 = create_agent(args.agent1, args.seed + game_num)
            winner, move_count = play_game(agent2, agent1, verbose=args.verbose)
            # Flip winner since we swapped agent positions
            if winner is not None:
                winner = 3 - winner

        total_moves += move_count

        if winner == 1:
            agent1_wins += 1
        elif winner == 2:
            agent2_wins += 1
        else:
            draws += 1

        if args.verbose and game_num < args.games - 1:
            print("\n" + "=" * 60 + "\n")

    # Print results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\n{args.agent1.upper():15} wins: {agent1_wins:3} ({agent1_wins/args.games*100:5.1f}%)")
    print(f"{args.agent2.upper():15} wins: {agent2_wins:3} ({agent2_wins/args.games*100:5.1f}%)")
    print(f"{'Draws':15}      : {draws:3} ({draws/args.games*100:5.1f}%)")
    print(f"\nTotal games: {args.games}")
    print(f"Total moves: {total_moves}")
    print(f"Avg moves/game: {total_moves / args.games:.1f}")
    print()


if __name__ == "__main__":
    main()
