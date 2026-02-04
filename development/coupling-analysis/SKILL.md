---
skill_name: coupling-analysis
activation_code: COUPLING_ANALYSIS_V1
version: 1.0.0
phase: 5.2
category: task-management
optional: true
can_skip_via_signal: SKIP_COUPLING_ANALYSIS
description: |
  Optional analysis skill that identifies parallel task opportunities.
  Analyzes task coupling to determine which tasks can be executed
  simultaneously vs. which require sequential execution.
---

# Coupling Analysis Skill
# Copyright (c) 2025 James J Ter Beest III. All Rights Reserved.

## Description

Analyzes task coupling to determine which tasks can be executed in parallel
vs. which require sequential execution. This optional analysis helps optimize
the development workflow by identifying independent work streams.

## When to Use

This skill activates when:

- User says "task-master show", "taskmaster show"
- User mentions "tightly coupled", "loosely coupled"
- User asks about "parallel implementation", "parallel tasks"
- User says "coupling analysis", "analyze coupling", "task coupling"
- User asks about "proposal strategy" or "analyze tasks"
- The signal `TASKS_APPROVED` has been emitted
- Pipeline state is `tasks_approved`

## How to Invoke

```
[ACTIVATE:COUPLING_ANALYSIS_V1]
```

Or user trigger phrases:

- "analyze task coupling"
- "which tasks can run in parallel"
- "show task dependencies"
- "coupling analysis"

## What It Does

1. **Reads tasks.json** - Parses the task hierarchy
2. **Analyzes dependencies** - Maps task dependencies and blockers
3. **Identifies coupling** - Categorizes tasks as tightly or loosely coupled
4. **Parallel opportunities** - Identifies tasks that can execute simultaneously
5. **Generates report** - Creates coupling analysis summary

## Coupling Categories

| Category | Description | Parallelization |
|----------|-------------|-----------------|
| **Tightly Coupled** | Tasks share state, data, or APIs | Must be sequential |
| **Loosely Coupled** | Independent modules | Can be parallel |
| **Interface Coupled** | Share contracts only | Parallel with contract lock |

## Output

The skill produces:

- Coupling analysis report
- Parallel execution recommendations
- Dependency graph visualization

## Signals

| Signal | Description |
|--------|-------------|
| `COUPLING_ANALYZED` | Analysis complete, proceed to task decomposer |
| `SKIP_COUPLING_ANALYSIS` | Skip this phase (in quick mode) |

## Next Activation

After completion, triggers:

```
[ACTIVATE:TASK_DECOMPOSER_V1]
```

## Skipping This Phase

In quick mode or when explicitly requested, emit `SKIP_COUPLING_ANALYSIS` signal
to bypass this optional phase and proceed directly to task decomposition.

## Related Skills

- `task-review-gate` - Precedes this skill
- `task-decomposer` - Follows this skill
- `prd-to-tasks` - Generates the initial tasks
