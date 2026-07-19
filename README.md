# Connect Four AI Agents

This repository contains an implementation of Connect Four with various AI agents, including Random, Rule-Based, and Minimax agents, along with a simulation environment and a graphical user interface (GUI).

### Prerequisites

You will need Python 3 installed on your system.

### Running the GUI

To play Connect Four against another human player using the graphical interface:

```bash
python gui.py
```

### Running Simulations

To simulate games between different AI agents from the command line:

```bash
python simulate.py --agent1 <agent_type> --agent2 <agent_type> --games <number_of_games> [--verbose]
```

**Available `agent_type` values:** `random`, `rule-based`, `minimax`

**Examples:**

*   **Simulate 10 games between a Random Agent and a Rule-Based Agent:**
    ```bash
    python simulate.py --agent1 random --agent2 rule-based --games 10
    ```

*   **Simulate 50 games between a Minimax Agent and a Random Agent, showing verbose output:**
    ```bash
    python simulate.py --agent1 minimax --agent2 random --games 50 --verbose
    ```

*   **Simulate 20 games with Minimax vs Rule-Based, with a specific seed:**
    ```bash
    python simulate.py --agent1 minimax --agent2 rule-based --games 20 --seed 123
    ```

## Project Structure

*   `engine.py`: Contains the core Connect Four game logic.
*   `gui.py`: Provides a simple graphical user interface to play the game.
*   `simulate.py`: Command-line tool for simulating games between AI agents.
*   `agents/`: Directory containing different AI agent implementations.
    *   `base_agent.py`: Base class for AI agents.
    *   `random_agent.py`: Implements a simple random move agent.
    *   `rule_based_agent.py`: Implements a rule-based AI agent.
    *   `minimax_agent.py`: Implements a Minimax AI agent.
*   `test_engine.py`: Unit tests for the Connect Four game engine.
*   `evaluate_agents.py`: Script for evaluating agent performance.
*   `evaluate_with_timing.py`: Script for evaluating agent performance with timing.

## Demo Video [LINK](https://youtu.be/Vrl1LCSfFho)
