---
name: evo-tpp-solver
description: Solve TPP (Travelling Purchase Problem) PDDL planning tasks. Use when you need to read a problem.json config file, parse PDDL domain/problem files, generate valid plans using pyperplan via unified_planning, format actions as function-call strings, write plan output files, and serialize plans as pickle. Handles the complete pipeline from JSON config to validated plan output.
---

# TPP PDDL Solver

Solves Travelling Purchase Problem (TPP) planning tasks encoded in PDDL using pyperplan via the unified_planning framework.

## When to use this skill

- You have a `problem.json` file listing TPP planning tasks
- Each task specifies a PDDL domain file, problem file, and output path
- You need to generate valid plans and write them as formatted text files
- You need pickle-serialized plans for validation compatibility

## Quick Start

Run the solver script directly:

```bash
cd /app
python -m environment.skills.evo-tpp-solver.scripts.solve
```

Or use the solver from Python:

```python
from pathlib import Path
import sys
sys.path.insert(0, "/app/environment/skills/evo-tpp-solver")
from scripts.solve import solve_all_tasks

solve_all_tasks(Path("/app/problem.json"), Path("/app"))
```

## Pipeline Overview

1. **Load config** — Read `problem.json` to get the list of tasks (each has domain path, problem path, output filename)
2. **Parse PDDL** — Use `unified_planning.io.PDDLReader` to parse domain + problem files into a Problem object
3. **Solve** — Use `OneshotPlanner(name="pyperplan")` with configurable search/heuristic. Default: `gbf`/`hff` for speed. Falls back to `wastar`/`hadd` if the fast config fails.
4. **Format actions** — Each action is formatted as `action_name(arg1, arg2, ...)` using `str(action_instance)` which already produces this format
5. **Write plan** — One action per line to the output text file
6. **Serialize** — Pickle the plan actions list for validation compatibility

## Key Implementation Details

### Action Format
The `str()` representation of a unified_planning `ActionInstance` already produces the required format:
```
drive(truck1, depot1, market1)
buy(truck1, goods1, market1, level0, level1, level0, level1)
```
All identifiers are lowercase (PDDL is case-insensitive; PDDLReader normalizes to lowercase).

### Solver Configuration
pyperplan supports these search/heuristic combinations via `OneshotPlanner` params:
- **Search**: `gbf`, `astar`, `wastar`, `bfs`, `ehs`, `ids`
- **Heuristic**: `hff`, `hadd`, `hmax`, `hsa`, `blind`, `lmcut`, `landmark`

The default UP-pyperplan config is `wastar`/`hadd`. For faster solving, use `gbf`/`hff`.

### Fallback Strategy
If the primary solver config fails or times out:
1. Try `gbf`/`hff` (fast, satisficing)
2. Try `wastar`/`hadd` (UP default)
3. Try `astar`/`hff` (optimal but slower)
4. Try `bfs`/`blind` (complete but slowest)

### TPP Domain Structure
The TPP domain uses `:strips :typing` requirements with these actions:
- `drive(?t, ?from, ?to)` — move truck between places
- `buy(?t, ?g, ?m, ?l1, ?l2, ?l3, ?l4)` — purchase goods at market
- `load(?g, ?t, ?m, ?l1, ?l2, ?l3, ?l4)` — load goods onto truck
- `unload(?g, ?t, ?d, ?l1, ?l2, ?l3, ?l4)` — unload goods at depot

Levels (`level0`, `level1`, ...) encode quantities propositionally since pyperplan only supports STRIPS.

## Script Reference

- `scripts/solve.py` — Main solver module with all pipeline functions. Run directly or import.

### Key Functions
- `load_task_config(config_path)` — Parse problem.json, return list of task dicts
- `solve_task(domain_path, problem_path, configs)` — Parse PDDL and solve with fallback
- `format_action(action_instance)` — Format a single action as `name(arg1, arg2, ...)`
- `write_plan(actions, output_path)` — Write formatted plan to text file + pickle
- `solve_all_tasks(config_path, base_dir)` — End-to-end: load config, solve all, write all
