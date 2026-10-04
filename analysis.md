# AI Agent Battle — Short Analysis Report

## 1. Objective

This experiment studies the effect of search depth and heuristic design in two Minimax + Alpha-Beta Tic-Tac-Toe agents. The implementation follows the assignment requirements: configurable depth, heuristic evaluation, two named agents, automated AI-vs-AI games, statistics, CSV storage and analysis.

## 2. Agent Configuration

| Agent | Algorithm | Depth | Heuristic |
|---|---|---:|---|
| NEXUS | Minimax + Alpha-Beta | 3 | H1 — Threat-Focused |
| TITAN | Minimax + Alpha-Beta | 3 | H2 — Position-Focused |

H1 emphasizes immediate threats, blocking, center control and corners. H2 emphasizes weighted potential winning lines plus center, corners and a small edge preference.

## 3. Experiment 1 — Search Depth

The test agent uses H1 while its depth is varied from 1 through 4. A fixed depth-4 H1 reference agent is used as the opponent, so the experimental variable is the test agent’s search depth. Ten games are played at each depth, with the starting player alternated.

| Depth | Result | Nodes Evaluated | Nodes Pruned | Total Time (s) | Avg Time/Game (s) |
|---:|---|---:|---:|---:|---:|
| 1 | 3 wins / 3 draws / 4 losses | 207 | 0 | 0.073454 | 0.007345 |
| 2 | 2 wins / 8 draws / 0 losses | 637 | 146 | 0.082797 | 0.00828 |
| 3 | 2 wins / 5 draws / 3 losses | 2174 | 439 | 0.110079 | 0.011008 |
| 4 | 1 wins / 8 draws / 1 losses | 5879 | 2017 | 0.15729 | 0.015729 |

### Observations

- Evaluated nodes increased from **207 at depth 1** to **5,879 at depth 4**.
- Total execution time increased from **0.073454 s** to **0.157290 s** across the ten-game depth experiment.
- Alpha-Beta pruning becomes increasingly visible at greater depths: the recorded pruned-node count rises from 0 at depth 1 to 2,017 at depth 4.
- The win/draw/loss outcome did not improve monotonically with depth. This is important: deeper search increases computational effort, but a deeper agent is not automatically guaranteed to obtain a better empirical score in every finite experiment.

## 4. Experiment 2 — NEXUS vs TITAN

Both agents use depth 3 and Minimax + Alpha-Beta. The starting player alternates across the 10 games.

| Game | First | Winner | Moves | NEXUS Nodes | TITAN Nodes | NEXUS Pruned | TITAN Pruned | Time (s) |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | NEXUS | DRAW | 9 | 279 | 187 | 56 | 38 | 0.007038 |
| 2 | TITAN | DRAW | 9 | 206 | 277 | 41 | 56 | 0.005710 |
| 3 | NEXUS | DRAW | 9 | 292 | 185 | 61 | 35 | 0.005735 |
| 4 | TITAN | DRAW | 9 | 228 | 295 | 42 | 58 | 0.006196 |
| 5 | NEXUS | DRAW | 9 | 297 | 207 | 58 | 40 | 0.005918 |
| 6 | TITAN | DRAW | 9 | 182 | 275 | 36 | 56 | 0.006090 |
| 7 | NEXUS | DRAW | 9 | 292 | 185 | 61 | 35 | 0.006489 |
| 8 | TITAN | DRAW | 9 | 209 | 288 | 39 | 55 | 0.005920 |
| 9 | NEXUS | DRAW | 9 | 297 | 207 | 58 | 40 | 0.006299 |
| 10 | TITAN | DRAW | 9 | 203 | 257 | 42 | 50 | 0.005928 |

**Battle result:** NEXUS 0 wins, TITAN 0 wins, **10 draws**. Total game execution time was **0.061322 s**.

### Agent Behaviour and Heuristic Influence

The two agents made the same number of game outcomes in this run—every game ended in a draw—so the evidence does not support claiming that either heuristic is superior in win rate. Their computational statistics nevertheless differ from game to game because H1 and H2 evaluate positions differently, which can change the selected equal-score move sequence and the amount of search encountered.

- NEXUS evaluated **2485** nodes across the 10 games and recorded **494** pruning events.

- TITAN evaluated **2363** nodes across the 10 games and recorded **463** pruning events.

### First-Player Advantage

The first player alternated between NEXUS and TITAN. The observed result was 10 draws, so this particular run did not show a first-player win advantage. This should be treated as an observation of this experiment, not a universal claim about Tic-Tac-Toe.

## 5. Conclusion

The experiment demonstrates the trade-off between deeper search and computational cost. Increasing search depth caused a clear increase in evaluated nodes and execution time. Alpha-Beta pruning removed branches that could not affect the Minimax decision, with more pruning observed at deeper searches. In the agent battle, both agents were sufficiently strong that all ten games ended in draws. Therefore, the experiment supports the conclusion that heuristic design can influence search behaviour and computational statistics even when the final game outcome is identical. The results do not justify declaring one agent universally better.
