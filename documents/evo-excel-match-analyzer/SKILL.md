---
name: evo-excel-match-analyzer
description: Scores dice games and compares paired matches between players. Loads Excel dice roll data, computes scores using 6 scoring categories (high_and_often, summation, highs_and_lows, only_two_numbers, all_the_numbers, ordered_subset_of_four), finds optimal game scores by pairing different categories across 2 turns, then pairs odd/even games for head-to-head match comparison.
---

# Excel Match Analyzer

Analyzes dice game data from Excel files. Computes game scores using 6 scoring
categories, then pairs odd-numbered games (Player 1) vs even-numbered games
(Player 2) for match comparison.

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-excel-match-analyzer/scripts')
from utils import (
    load_excel_data, compute_all_game_scores, split_by_parity,
    compare_paired_matches, compute_win_difference, write_answer
)

# Load data
data = load_excel_data('/root/data.xlsx', sheet_name='Data')

# Compute all game scores
game_scores = compute_all_game_scores(data)

# Split by parity (odd=P1, even=P2)
p1_scores, p2_scores = split_by_parity(game_scores)

# Compare paired matches (game 1 vs 2, game 3 vs 4, etc.)
p1_wins, p2_wins, ties = compare_paired_matches(p1_scores, p2_scores)

# Compute and write answer
diff = compute_win_difference(p1_wins, p2_wins)
write_answer(diff, '/root/answer.txt')
```

## Scoring Rules (6 Categories)

1. **high_and_often**: Highest number × count of that number
2. **summation**: Sum of all 6 dice
3. **highs_and_lows**: Highest × Lowest × (Highest - Lowest)
4. **only_two_numbers**: If exactly 2 distinct numbers → 30 (else N/A)
5. **all_the_numbers**: If rolls are {1,2,3,4,5,6} → 40 (else N/A)
6. **ordered_subset_of_four**: If rolls contain run of 4 consecutive inc/dec → 50 (else N/A)

## Game Scoring

Each game has 2 turns. Find highest combined score using 2 DIFFERENT categories
(one per turn). Try all valid category pairs and pick the maximum.

## Match Pairing

- Player 1 plays odd-numbered games (1, 3, 5, ...)
- Player 2 plays even-numbered games (2, 4, 6, ...)
- Matches: game 1 vs game 2, game 3 vs game 4, etc.
- Higher game score wins the match

## Key Functions

- `score_high_and_often(rolls)` - Category 1 scorer
- `score_summation(rolls)` - Category 2 scorer
- `score_highs_and_lows(rolls)` - Category 3 scorer
- `score_only_two_numbers(rolls)` - Category 4 scorer (returns None if N/A)
- `score_all_the_numbers(rolls)` - Category 5 scorer (returns None if N/A)
- `score_ordered_subset_of_four(rolls)` - Category 6 scorer (returns None if N/A)
- `compute_turn_scores(rolls)` - All applicable scores for a turn
- `compute_game_score(t1_rolls, t2_rolls)` - Best combined score for a game
- `load_excel_data(filepath, sheet_name)` - Load dice data from Excel
- `compute_all_game_scores(data)` - Score all games
- `split_by_parity(game_scores)` - Split into P1 (odd) and P2 (even)
- `compare_paired_matches(p1, p2)` - Count wins for each player
- `compute_win_difference(p1_wins, p2_wins)` - P1 wins minus P2 wins
- `write_answer(result, filepath)` - Write numeric result to file
