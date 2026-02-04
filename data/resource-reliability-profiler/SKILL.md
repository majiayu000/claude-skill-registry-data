---
name: resource-reliability-profiler
description: Run commands under resource budgets and stop runs that exceed CPU, RAM, VRAM, disk write, or time thresholds. Use when reliability and resource constraints must be enforced.
---

# Resource Reliability Profiler

Use this skill to enforce resource budgets on long-running commands.

## Workflow

1) Define a budget file (use references/budget.example.json).
2) Run the command under the budget.
3) Review the report for violations.

## Scripts

- Run: python scripts/profile_run.py --budget references/budget.example.json -- <command>
