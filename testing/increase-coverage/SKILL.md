---
name: increase-coverage
description: Analyze test coverage, identify highest-impact uncovered files, generate quality tests, and track progress toward a target coverage percentage.
agent: increase-coverage
argument-hint: "[percentage] [project-path]"
pass-full-context: true
pass-conversation-history: true
---

# /increase-coverage

Systematically increase test coverage for a project.

Target: $ARGUMENTS

## Usage

- `/increase-coverage 10` — increase coverage by 10 percentage points
- `/increase-coverage 5 /path/to/project` — target a specific project
- `/increase-coverage` — will prompt for target percentage

Prioritizes data mutation risk, integration points, and business logic over raw coverage numbers.
