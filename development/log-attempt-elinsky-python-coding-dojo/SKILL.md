---
name: log-attempt
description: Log a coding problem attempt when user says "log <problem_id>" with time, tries, solved status, hints, or solution usage. Parses natural language like "log count_bits - 15 min, 3 tries, solved" and calls the log-attempt script.
---

# Log Problem Attempt

Parse the user's natural language input and call the log-attempt script.

## Workflow

1. Run the log-attempt script
2. Run update_readme.py to regenerate README.md

```bash
~/.pyenv/versions/python-coding-dojo/bin/python scripts/log_attempt.py <problem_id> [OPTIONS]
~/.pyenv/versions/python-coding-dojo/bin/python scripts/update_readme.py
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--time MINUTES` | Time taken | - |
| `--submissions N` | Number of attempts | 1 if solved |
| `--solved` / `--no-solved` | Whether solved | --solved |
| `--used-hints` / `--no-used-hints` | Whether used hints | --no-used-hints |
| `--used-solution` / `--no-used-solution` | Whether looked at solution | --no-used-solution |
| `--optimal` / `--no-optimal` | Whether solution is optimal (correct complexity) | --no-optimal |
| `--notes "text"` | Optional notes | - |

## Parsing Rules

| User says | Maps to |
|-----------|---------|
| "tries", "attempts", "submissions" | `--submissions` |
| "hint", "hints" | `--used-hints` |
| "solution", "looked at solution" | `--used-solution` |
| "didn't solve", "not solved", "gave up" | `--no-solved` |
| "min", "minutes" | `--time` |
| "optimal" | `--optimal` |

## Examples

| Input | Command |
|-------|---------|
| "log count_bits - 15 min, 3 tries, used hints" | `... log_attempt.py count_bits --time 15 --submissions 3 --used-hints` |
| "log parity, didn't solve, looked at solution" | `... log_attempt.py parity --no-solved --used-solution` |
| "log swap_bits - first try, 8 minutes" | `... log_attempt.py swap_bits --time 8 --submissions 1` |
