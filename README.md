# Genetic Pong

A **Python + Pygame implementation of Pong** where an AI paddle learns to play using a **Genetic Algorithm** - no neural networks, no backprop. A population of AI paddles evolves over generations by selecting the best-performing individual, crossing over its coefficients, and applying random mutation. Watch it go from useless to genuinely threatening.

---

## How the GA Works

Each AI paddle has a set of **coefficients** that weight input signals (ball position, velocity, distance, etc.) to decide whether to move up, down, or stay. Each generation:

1. **Evaluate** - 30 paddles play simultaneously; fitness is measured by distance to the ball each frame
2. **Select** - the paddle with the lowest mean fitness score (closest to the ball on average) survives
3. **Crossover + Mutate** - the next generation of 30 paddles inherits the winner's coefficients, with 50% chance of random perturbation (`±10` per coefficient)
4. **Repeat** - over up to 300 episodes until a paddle wins 300 rallies

---

## Run Modes

| Script | Description |
|--------|-------------|
| `pong_manual.py` | Standard two-player Pong (keyboard) |
| `pong_basic_ai.py` | Pong with a simple rule-based AI opponent |
| `pong_genetic.py` | GA training - watch the population evolve |
| `pong_genetic_vs_ai.py` | Evolved GA paddle vs the rule-based AI |
| `pong_genetic_vs_player.py` | Play against the evolved GA paddle yourself |

---

## Setup

```bash
git clone https://github.com/Raffiesaurus/Genetic-Pong.git
cd Genetic-Pong
pip install -r requirements.txt
```

Then pick a mode and run it:

```bash
python pong_genetic.py          # train the GA
python pong_genetic_vs_player.py  # play against it
```

---

## GA Parameters

| Parameter | Value |
|-----------|-------|
| Population size | 30 |
| Max episodes | 300 |
| Win threshold | 300 rallies |
| Mutation chance | 50% per offspring |
| Mutation range | `±10` per coefficient |

Tweak these in `genetic_algo.py` (`GeneticPong.__init__`).

---

## Tech

- **Language:** Python
- **Rendering:** Pygame
- **Algorithm:** Genetic Algorithm (selection → crossover → mutation)
- **Stats:** Logged to `stats/`

---

## License

MIT
