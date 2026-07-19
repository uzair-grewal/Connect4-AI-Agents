#!/usr/bin/env python3
"""Evaluation script with detailed timing measurements for all three pairings."""

import time
from engine import ConnectFour
from agents.random_agent import RandomAgent
from agents.rule_based_agent import RuleBasedAgent
from agents.minimax_agent import MinimaxAgent


def play_game_with_timing(agent1, agent2):
    """Play a game and record timing information."""
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
    return {
        "winner": winner,
        "move_count": move_count,
        "agent1_times": agent1_times,
        "agent2_times": agent2_times,
    }


def run_pairing(agent1_factory, agent2_factory, agent1_name, agent2_name, num_games=30, seed_base=100):
    """Run a complete pairing with alternating first player."""
    agent1_wins = 0
    agent2_wins = 0
    draws = 0
    all_agent1_times = []
    all_agent2_times = []
    total_moves = 0

    print(f"\nRunning {num_games} games: {agent1_name} vs {agent2_name}")
    print(f"Seeds: {seed_base}-{seed_base + num_games - 1}")
    print("-" * 70)

    for game_num in range(num_games):
        if game_num % 2 == 0:
            # Agent1 is Player 1 (moves first)
            agent1 = agent1_factory(seed_base + game_num)
            agent2 = agent2_factory(seed_base + 1000 + game_num)
            result = play_game_with_timing(agent1, agent2)
            winner = result["winner"]
        else:
            # Agent2 is Player 1 (moves first)
            agent2 = agent2_factory(seed_base + 1000 + game_num)
            agent1 = agent1_factory(seed_base + game_num)
            result = play_game_with_timing(agent2, agent1)
            # Flip winner since agents are swapped
            winner = 3 - result["winner"] if result["winner"] is not None else None
            # Swap timing arrays since agents are swapped
            result["agent1_times"], result["agent2_times"] = result["agent2_times"], result["agent1_times"]

        if winner == 1:
            agent1_wins += 1
        elif winner == 2:
            agent2_wins += 1
        else:
            draws += 1

        all_agent1_times.extend(result["agent1_times"])
        all_agent2_times.extend(result["agent2_times"])
        total_moves += result["move_count"]

        if (game_num + 1) % 10 == 0:
            print(f"  Completed {game_num + 1}/{num_games} games")

    # Calculate statistics
    agent1_avg_time = sum(all_agent1_times) / len(all_agent1_times) if all_agent1_times else 0
    agent2_avg_time = sum(all_agent2_times) / len(all_agent2_times) if all_agent2_times else 0

    return {
        "agent1_name": agent1_name,
        "agent2_name": agent2_name,
        "games": num_games,
        "agent1_wins": agent1_wins,
        "agent2_wins": agent2_wins,
        "draws": draws,
        "agent1_avg_time": agent1_avg_time,
        "agent2_avg_time": agent2_avg_time,
        "total_moves": total_moves,
        "all_agent1_times": all_agent1_times,
        "all_agent2_times": all_agent2_times,
    }


def print_results(result):
    """Print results for a pairing."""
    print(f"\n{'=' * 70}")
    print(f"RESULTS: {result['agent1_name']} vs {result['agent2_name']}")
    print(f"{'=' * 70}")
    print(f"\nWin Statistics (out of {result['games']} games):")
    print(f"  {result['agent1_name']:25} wins: {result['agent1_wins']:3} ({result['agent1_wins']/result['games']*100:5.1f}%)")
    print(f"  {result['agent2_name']:25} wins: {result['agent2_wins']:3} ({result['agent2_wins']/result['games']*100:5.1f}%)")
    print(f"  {'Draws':25}        : {result['draws']:3} ({result['draws']/result['games']*100:5.1f}%)")

    print(f"\nTiming Statistics (per move):")
    print(f"  {result['agent1_name']:25}: {result['agent1_avg_time']*1000:8.2f} ms")
    print(f"  {result['agent2_name']:25}: {result['agent2_avg_time']*1000:8.2f} ms")

    print(f"\nGame Statistics:")
    print(f"  Total games:       {result['games']}")
    print(f"  Total moves:       {result['total_moves']}")
    print(f"  Avg moves/game:    {result['total_moves'] / result['games']:6.1f}")


def print_system_info():
    """Print system specifications."""
    import platform
    print("\n" + "=" * 70)
    print("SYSTEM SPECIFICATIONS")
    print("=" * 70)
    print(f"Platform:    {platform.platform()}")
    print(f"Processor:   {platform.processor()}")
    print(f"Python:      {platform.python_version()}")
    print(f"Timing:      time.perf_counter() (nanosecond precision)")
    print()


def main():
    """Run all pairings."""
    print_system_info()

    # Define agent factories
    random_factory = lambda seed: RandomAgent(seed=seed)
    rule_based_factory = lambda seed: RuleBasedAgent(seed=seed)
    minimax_factory = lambda seed: MinimaxAgent(depth=4, seed=seed)

    # Run pairings
    results = []

    # Pairing 1: Random vs Rule-Based
    result1 = run_pairing(
        random_factory,
        rule_based_factory,
        "Random",
        "Rule-Based",
        num_games=30,
        seed_base=100
    )
    print_results(result1)
    results.append(result1)

    # Pairing 2: Rule-Based vs Minimax
    result2 = run_pairing(
        rule_based_factory,
        minimax_factory,
        "Rule-Based",
        "Minimax",
        num_games=30,
        seed_base=200
    )
    print_results(result2)
    results.append(result2)

    # Pairing 3: Minimax vs Random
    result3 = run_pairing(
        minimax_factory,
        random_factory,
        "Minimax",
        "Random",
        num_games=30,
        seed_base=300
    )
    print_results(result3)
    results.append(result3)

    # Summary table
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"\n{'Pairing':<40} {'Agent 1 Win %':<20} {'Agent 2 Win %':<20} {'Draw %':>8}")
    print("-" * 90)
    for r in results:
        pairing = f"{r['agent1_name']} vs {r['agent2_name']}"
        a1_pct = r['agent1_wins'] / r['games'] * 100
        a2_pct = r['agent2_wins'] / r['games'] * 100
        draw_pct = r['draws'] / r['games'] * 100
        print(f"{pairing:<40} {a1_pct:>18.1f}% {a2_pct:>18.1f}% {draw_pct:>8.1f}%")

    print("\n" + "=" * 70)
    print("TIMING SUMMARY TABLE (ms per move)")
    print("=" * 70)
    print(f"\n{'Pairing':<40} {'Agent 1 (ms)':<20} {'Agent 2 (ms)':>20}")
    print("-" * 80)
    for r in results:
        pairing = f"{r['agent1_name']} vs {r['agent2_name']}"
        time1 = r['agent1_avg_time'] * 1000
        time2 = r['agent2_avg_time'] * 1000
        print(f"{pairing:<40} {time1:>18.2f}   {time2:>18.2f}")

    print("\n" + "=" * 70)
    print(f"Total games evaluated: {sum(r['games'] for r in results)}")
    print(f"Seeds used: 100-699")
    print("=" * 70 + "\n")

    return results


if __name__ == "__main__":
    main()
