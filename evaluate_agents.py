#!/usr/bin/env python3
"""Comprehensive evaluation of Connect Four agents with timing and statistics."""

import time
import platform
from typing import Tuple, List, Dict
from dataclasses import dataclass

from engine import ConnectFour
from agents.base_agent import Agent
from agents.random_agent import RandomAgent
from agents.rule_based_agent import RuleBasedAgent
from agents.minimax_agent import MinimaxAgent


@dataclass
class GameResult:
    """Result of a single game."""
    winner: int | None  # 1, 2, or None (draw)
    move_count: int
    agent1_times: List[float]
    agent2_times: List[float]


@dataclass
class MatchStats:
    """Statistics for a match between two agents."""
    agent1_name: str
    agent2_name: str
    games: int
    agent1_wins: int
    agent2_wins: int
    draws: int
    agent1_avg_time: float
    agent2_avg_time: float
    total_moves: int


def play_game(
    agent1: Agent,
    agent2: Agent,
    verbose: bool = False
) -> GameResult:
    """Play a single game and record timing information."""
    game = ConnectFour()
    agents = {1: agent1, 2: agent2}
    agent1_times = []
    agent2_times = []
    move_count = 0

    while not game.is_terminal():
        agent = agents[game.current_player]
        start = time.perf_counter()
        move = agent.choose_move(game)
        elapsed = time.perf_counter() - start

        if game.current_player == 1:
            agent1_times.append(elapsed)
        else:
            agent2_times.append(elapsed)

        game.apply_move(move)
        move_count += 1

    winner = game.winner()
    if verbose:
        print(f"Game ended: Winner={winner}, Moves={move_count}")

    return GameResult(
        winner=winner,
        move_count=move_count,
        agent1_times=agent1_times,
        agent2_times=agent2_times
    )


def run_match(
    agent1_factory,
    agent2_factory,
    agent1_name: str,
    agent2_name: str,
    num_games: int = 30,
    seed_base: int = 42
) -> MatchStats:
    """Run a complete match between two agents."""
    agent1_wins = 0
    agent2_wins = 0
    draws = 0
    all_agent1_times = []
    all_agent2_times = []
    total_moves = 0

    print(f"\nRunning {num_games} games: {agent1_name} vs {agent2_name}")
    print("-" * 60)

    for game_num in range(num_games):
        seed = seed_base + game_num
        agent1 = agent1_factory(seed)
        agent2 = agent2_factory(seed + 1000)

        result = play_game(agent1, agent2)

        if result.winner == 1:
            agent1_wins += 1
        elif result.winner == 2:
            agent2_wins += 1
        else:
            draws += 1

        all_agent1_times.extend(result.agent1_times)
        all_agent2_times.extend(result.agent2_times)
        total_moves += result.move_count

        if (game_num + 1) % 10 == 0:
            print(f"  Completed {game_num + 1}/{num_games} games")

    agent1_avg_time = (
        sum(all_agent1_times) / len(all_agent1_times)
        if all_agent1_times
        else 0
    )
    agent2_avg_time = (
        sum(all_agent2_times) / len(all_agent2_times)
        if all_agent2_times
        else 0
    )

    return MatchStats(
        agent1_name=agent1_name,
        agent2_name=agent2_name,
        games=num_games,
        agent1_wins=agent1_wins,
        agent2_wins=agent2_wins,
        draws=draws,
        agent1_avg_time=agent1_avg_time,
        agent2_avg_time=agent2_avg_time,
        total_moves=total_moves
    )


def print_match_results(stats: MatchStats):
    """Print formatted match results."""
    print(f"\n{'=' * 70}")
    print(f"MATCH RESULTS: {stats.agent1_name} vs {stats.agent2_name}")
    print(f"{'=' * 70}")
    print(f"\nWin Statistics (out of {stats.games} games):")
    print(f"  {stats.agent1_name:20} wins: {stats.agent1_wins:3} ({stats.agent1_wins/stats.games*100:5.1f}%)")
    print(f"  {stats.agent2_name:20} wins: {stats.agent2_wins:3} ({stats.agent2_wins/stats.games*100:5.1f}%)")
    print(f"  Draws:                       {stats.draws:3} ({stats.draws/stats.games*100:5.1f}%)")

    print(f"\nTiming (average per move):")
    print(f"  {stats.agent1_name:20}: {stats.agent1_avg_time*1000:8.2f} ms")
    print(f"  {stats.agent2_name:20}: {stats.agent2_avg_time*1000:8.2f} ms")

    print(f"\nGame Statistics:")
    print(f"  Total games:   {stats.games}")
    print(f"  Total moves:   {stats.total_moves}")
    print(f"  Avg moves/game: {stats.total_moves / stats.games:6.1f}")


def print_system_info():
    """Print system information for reproducibility."""
    print("=" * 70)
    print("SYSTEM INFORMATION")
    print("=" * 70)
    print(f"Platform:     {platform.platform()}")
    print(f"Processor:    {platform.processor()}")
    print(f"Python:       {platform.python_version()}")
    print()


def create_agent_factory(agent_class, **kwargs):
    """Create a factory function for an agent."""
    def factory(seed):
        return agent_class(seed=seed, **kwargs)
    return factory


def main():
    """Run all agent evaluations."""
    print_system_info()

    # Define agent factories
    random_factory = create_agent_factory(RandomAgent)
    rule_based_factory = create_agent_factory(RuleBasedAgent)
    minimax_depth3_factory = create_agent_factory(MinimaxAgent, depth=3)
    minimax_depth4_factory = create_agent_factory(MinimaxAgent, depth=4)

    results = []

    # Pairing 1: Random vs Rule-Based
    print("\n" + "=" * 70)
    print("PAIRING 1: Random Agent (Baseline) vs Rule-Based Agent")
    print("=" * 70)

    # Random first
    stats1a = run_match(
        random_factory,
        rule_based_factory,
        "Random (1st)",
        "Rule-Based",
        num_games=15,
        seed_base=100
    )
    print_match_results(stats1a)

    # Rule-Based first
    stats1b = run_match(
        rule_based_factory,
        random_factory,
        "Rule-Based (1st)",
        "Random",
        num_games=15,
        seed_base=200
    )
    print_match_results(stats1b)

    # Combine results
    stats1 = MatchStats(
        agent1_name="Random",
        agent2_name="Rule-Based",
        games=30,
        agent1_wins=stats1a.agent1_wins + stats1b.agent2_wins,
        agent2_wins=stats1a.agent2_wins + stats1b.agent1_wins,
        draws=stats1a.draws + stats1b.draws,
        agent1_avg_time=(stats1a.agent1_avg_time + stats1b.agent2_avg_time) / 2,
        agent2_avg_time=(stats1a.agent2_avg_time + stats1b.agent1_avg_time) / 2,
        total_moves=stats1a.total_moves + stats1b.total_moves
    )

    print("\n" + "=" * 70)
    print("PAIRING 1 COMBINED RESULTS (30 games, both first/second)")
    print("=" * 70)
    print_match_results(stats1)
    results.append(stats1)

    # Pairing 2: Rule-Based vs Minimax (depth 4)
    print("\n" + "=" * 70)
    print("PAIRING 2: Rule-Based Agent vs Minimax Agent (depth=4)")
    print("=" * 70)

    # Rule-Based first
    stats2a = run_match(
        rule_based_factory,
        minimax_depth4_factory,
        "Rule-Based (1st)",
        "Minimax (depth=4)",
        num_games=15,
        seed_base=300
    )
    print_match_results(stats2a)

    # Minimax first
    stats2b = run_match(
        minimax_depth4_factory,
        rule_based_factory,
        "Minimax (depth=4) (1st)",
        "Rule-Based",
        num_games=15,
        seed_base=400
    )
    print_match_results(stats2b)

    # Combine results
    stats2 = MatchStats(
        agent1_name="Rule-Based",
        agent2_name="Minimax (depth=4)",
        games=30,
        agent1_wins=stats2a.agent1_wins + stats2b.agent2_wins,
        agent2_wins=stats2a.agent2_wins + stats2b.agent1_wins,
        draws=stats2a.draws + stats2b.draws,
        agent1_avg_time=(stats2a.agent1_avg_time + stats2b.agent2_avg_time) / 2,
        agent2_avg_time=(stats2a.agent2_avg_time + stats2b.agent1_avg_time) / 2,
        total_moves=stats2a.total_moves + stats2b.total_moves
    )

    print("\n" + "=" * 70)
    print("PAIRING 2 COMBINED RESULTS (30 games, both first/second)")
    print("=" * 70)
    print_match_results(stats2)
    results.append(stats2)

    # Pairing 3: Minimax vs Random
    print("\n" + "=" * 70)
    print("PAIRING 3: Minimax Agent (depth=4) vs Random Agent")
    print("=" * 70)

    # Minimax first
    stats3a = run_match(
        minimax_depth4_factory,
        random_factory,
        "Minimax (depth=4) (1st)",
        "Random",
        num_games=15,
        seed_base=500
    )
    print_match_results(stats3a)

    # Random first
    stats3b = run_match(
        random_factory,
        minimax_depth4_factory,
        "Random (1st)",
        "Minimax (depth=4)",
        num_games=15,
        seed_base=600
    )
    print_match_results(stats3b)

    # Combine results
    stats3 = MatchStats(
        agent1_name="Minimax (depth=4)",
        agent2_name="Random",
        games=30,
        agent1_wins=stats3a.agent1_wins + stats3b.agent2_wins,
        agent2_wins=stats3a.agent2_wins + stats3b.agent1_wins,
        draws=stats3a.draws + stats3b.draws,
        agent1_avg_time=(stats3a.agent1_avg_time + stats3b.agent2_avg_time) / 2,
        agent2_avg_time=(stats3a.agent2_avg_time + stats3b.agent1_avg_time) / 2,
        total_moves=stats3a.total_moves + stats3b.total_moves
    )

    print("\n" + "=" * 70)
    print("PAIRING 3 COMBINED RESULTS (30 games, both first/second)")
    print("=" * 70)
    print_match_results(stats3)
    results.append(stats3)

    # Summary table
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"\n{'Pairing':<40} {'Agent 1':<12} {'Agent 2':<12} {'Draws':>6}")
    print(f"{'':40} {'Win %':<12} {'Win %':<12} {'%':>6}")
    print("-" * 70)
    for stat in results:
        agent1_pct = stat.agent1_wins / stat.games * 100
        agent2_pct = stat.agent2_wins / stat.games * 100
        draws_pct = stat.draws / stat.games * 100
        pairing = f"{stat.agent1_name} vs {stat.agent2_name}"
        print(f"{pairing:<40} {agent1_pct:>10.1f}% {agent2_pct:>10.1f}% {draws_pct:>6.1f}%")

    print("\n" + "=" * 70)
    print("TIMING SUMMARY TABLE (ms per move)")
    print("=" * 70)
    print(f"\n{'Pairing':<40} {'Agent 1':<15} {'Agent 2':<15}")
    print("-" * 70)
    for stat in results:
        pairing = f"{stat.agent1_name} vs {stat.agent2_name}"
        time1 = stat.agent1_avg_time * 1000
        time2 = stat.agent2_avg_time * 1000
        print(f"{pairing:<40} {time1:>12.2f} ms {time2:>12.2f} ms")

    print("\n" + "=" * 70)
    print("Seeds used: 100-699 (700 games total, 15 per pairing configuration)")
    print("=" * 70)


if __name__ == "__main__":
    main()
