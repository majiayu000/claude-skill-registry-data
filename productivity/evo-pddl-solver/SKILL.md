---
name: evo-pddl-solver
description: Core PDDL planning solver that parses domain/problem files, invokes pyperplan with optimal search configuration (GBFS + hFF), handles timeouts and fallbacks, and returns a plan as a list of action strings.
---

# evo-pddl-solver

Solves PDDL planning problems using unified_planning with pyperplan backend,
with direct pyperplan fallback.

## Key Functions

- `solve_pddl_task(domain_path, problem_path, timeout=300)` - Main entry point
- `solve_with_unified_planning(domain_path, problem_path, timeout=300)` - UP-based solving
- `solve_with_pyperplan_direct(domain_path, problem_path, timeout=300)` - Direct pyperplan
- `solve_with_fallback_strategies(domain_path, problem_path, timeout=300)` - Try all strategies

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pddl-solver/scripts')
from utils import solve_pddl_task

plan = solve_pddl_task('domain.pddl', 'problem.pddl', timeout=300)
# Returns list of strings like: ["action_name(param1, param2, ...)", ...]
```

## Strategy

1. Uses unified_planning PDDLReader to parse PDDL files
2. Invokes pyperplan via UP with GBFS + hFF (fastest satisficing config)
3. Falls back to default pyperplan config if GBFS+hFF fails
4. Falls back to direct pyperplan invocation if UP integration fails
5. Returns plan as list of "action_name(param1, param2, ...)" strings

## Airport Domain Notes

- Airport domain files must be STRIPS versions (not ADL)
- Uses not_blocked/not_occupied predicates instead of negation
- Large instances may cause memory issues - pyperplan is pure Python
- GBFS + hFF is the recommended strategy for satisficing planning
- unified_planning lowercases all names during parsing
