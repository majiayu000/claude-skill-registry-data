---
name: aoc-daily-solver
description: Automate Advent of Code daily puzzle solving - fetch puzzle, implement solution, test, and submit answers
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, LS
---

# AoC Daily Solver

Automate the complete workflow for solving Advent of Code puzzles: fetch puzzle description and input, implement the solution, test it, and submit answers.

## When to Use This Skill

- User asks to solve today's AoC puzzle
- User asks to solve a specific day's puzzle (e.g., "solve day 15")
- User wants to work on AoC puzzles following the established workflow

## Prerequisites

- `AOC_SESSION` environment variable must be set (from `.env` file or GitHub secrets)
- Python environment with required packages (`requests`, `beautifulsoup4`, etc.)
- Repository structure follows the pattern: `YYYY/N/dayN.py` and `YYYY/N/input.txt`

## Instructions

Follow this workflow for both automated (GitHub Action) and local solving:

### 1. Read Guidelines
- Read "Problem-Solving Workflow" below for detailed problem-solving approach
- Understand the repository structure and coding patterns

### 2. Load Environment Variables (Local Execution Only)

**IMPORTANT**: When running locally, you MUST load the `.env` file first to set `AOC_SESSION`:

```bash
set -a; source .env; set +a
```

This exports all variables from `.env` to the current shell. Skip this step in GitHub workflows (secrets are already set).

### 3. Fetch Puzzle and Input
```bash
FORCE_DAY=$DAY FORCE_YEAR=$YEAR python3 .claude/skills/aoc-daily-solver/scripts/solve_daily.py
```
- This creates `${YEAR}/${DAY}/puzzle.md` and `${YEAR}/${DAY}/input.txt`
- Script will notify if parts are already solved

### 4. Check Existing Solutions
- Open `puzzle.md` and check for "Your puzzle answer was..."
- If both parts solved: stop immediately
- If only Part 1 solved: skip to Step 8 (Part 2)

### 5. Implement Solution
- Create `${YEAR}/${DAY}/day${DAY}.py` with:
  - `part1()` function
  - `part2()` function
  - `run_example()` for testing with sample input
  - `if __name__ == "__main__"` block to print results
- Load input using: `os.path.join(sys.path[0], 'input.txt')`
- Use any Python libraries needed (`numpy`, `networkx`, `sympy`, `z3`, etc.)

### 6. Test with Timeout
```bash
timeout 30 python3 ${YEAR}/${DAY}/day${DAY}.py
```
- If it times out, rethink the algorithm (see "Performance Tips" below)
- Test with example input first using `run_example()`

### 7. Submit Part 1
```bash
python3 .claude/skills/aoc-daily-solver/scripts/submit_answer.py 1 <answer> $DAY $YEAR
```
- Read the response carefully
- If wrong, analyze feedback and fix

### 8. Re-fetch Puzzle for Part 2 (MANDATORY)

**IMPORTANT**: You MUST re-fetch the puzzle after Part 1 is accepted, BEFORE implementing Part 2:

```bash
FORCE_DAY=$DAY FORCE_YEAR=$YEAR python3 .claude/skills/aoc-daily-solver/scripts/solve_daily.py
```

**Why this is mandatory:**
- Part 2 description is only revealed after Part 1 is solved
- The `puzzle.md` file must be updated to include Part 2 text
- For older AoC years, AI models may have solutions in training data and could "solve" Part 2 without ever reading its description. Always re-fetch to ensure Part 2 is properly documented.

### 9. Implement and Submit Part 2
- **First**: Read the updated `puzzle.md` to understand Part 2 requirements
- Implement `part2()` function
- Test again with timeout
- Submit: `python3 .claude/skills/aoc-daily-solver/scripts/submit_answer.py 2 <answer> $DAY $YEAR`

### 10. Update Dependencies (if needed)
- If you installed new packages, add them to `requirements.txt`

### 11. Commit Results
- Commit the entire day folder with puzzle, input, and solution
- Include which AI model assisted in the commit message

## Examples

**Solve today's puzzle:**
> "Solve today's Advent of Code puzzle"

**Solve specific day:**
> "Solve AoC 2024 day 15"

**Continue from Part 2:**
> "Part 1 is done, help me with Part 2 of day 10"

## Important Notes

- **Never skip the filename pattern**: Must be `day${DAY}.py`
- **Performance target**: Solutions should run in <30 seconds
- **Test incrementally**: Verify parsing with example input first
- **Sequential solving**: When solving multiple days, finish one completely before starting the next
- **Mandatory re-fetch before Part 2**: After Part 1 is accepted, ALWAYS re-fetch the puzzle to get Part 2 description. This ensures `puzzle.md` documents both parts, especially important for older puzzles where AI may have training data.

## Problem-Solving Workflow

1. **Read carefully** - Don't assume input format. Summarize the core mechanics in your own words before coding.
2. **Example first** - Create `run_example()` with hardcoded sample input. Print parsed structures and validate against expected output before running on full input.
3. **Test incrementally** - Verify each part works. On errors, re-check parsing first.
4. **Performance target** - No puzzle should take >30 seconds. If slow, rethink the algorithm.

## Parsing Tips

- Read format carefully: char-by-char vs whitespace-separated, handle empty lines.
- Debug parsing first: print parsed data on example, verify structure (grid dims, value ranges).
- For grids: `grid = [[int(c) for c in line] for line in lines if line.strip()]`

## Performance Tips (When Slow)

**Quick fixes:**
- `set()` for O(1) lookups
- `collections.deque` for BFS queues
- `@functools.cache` for recursive memoization

**Algorithm issues:**
- If >10s, brute force won't work. Look for: known algorithms, mathematical properties, structural patterns.
- Avoid O(n² × cost) - preprocess to make inner checks O(1) via prefix sums, sparse tables, coordinate compression.
- Sort candidates by potential value descending; early-terminate when remaining can't beat best.

## Lessons from Past Days

Add a short note here whenever a day's solution required multiple iterations or ran into a performance issue—summarize the problem and the eventual fix so future runs avoid the same trap.

- **2024 Day 24 Part 2**: When finding defects in structured systems (circuits, graphs), analyze expected patterns rather than testing all combinations. Define structural invariants, find violations directly.
- **2025 Day 9 Part 2**: When checking O(n²) candidate pairs, don't let each validation be O(area). Preprocess data structures for O(1) checks. Use coordinate compression. Sort by potential and early-terminate.
- **2025 Day 10**: For constraint satisfaction problems involving linear toggling (modulo 2) or integer counts with a minimization objective, immediately use an SMT solver like `z3`. It is much faster to implement and less error-prone than manual Gaussian elimination or search/DP.

## Supporting Files

- [CLAUDE.md](../../../CLAUDE.md) - Repository structure and global conventions
- [scripts/aoc_client.py](scripts/aoc_client.py) - HTTP client for AoC API
- [scripts/solve_daily.py](scripts/solve_daily.py) - Puzzle fetcher
- [scripts/submit_answer.py](scripts/submit_answer.py) - Answer submitter
