---
name: a3-eval
description: Evaluates mobile GUI agents on completing multi-step tasks across 20 real-world Android applications. It probes both final task completion capability and the agent's ability to navigate intermediate essential states without getting stuck or making terminal errors. Use when the user wants to benchmark on A3, or asks about evaluating this task. Reports Task Success Rate (SR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2501.01149
  bibtex_key: chai2025a3
  confidence: high
---

# a3-eval

> A3: Android Agent Arena for Mobile GUI Agents with Essential-State Procedural Evaluation — Chai et al. (2025) (arXiv:2501.01149, 2025)

## What this evaluates

Evaluates mobile GUI agents on completing multi-step tasks across 20 real-world Android applications. It probes both final task completion capability and the agent's ability to navigate intermediate essential states without getting stuck or making terminal errors.

## Datasets

- **A3** — total 201; splits: test (201)

## Metrics

- `Task Success Rate (SR)` **(primary)** — range: percent
  - Percentage of tasks where the agent successfully completes the entire user instruction. Calculated as (successful tasks / total tasks) * 100%.
- `Essential State Achieved Rate (ESAR)` — range: percent
  - Percentage of predefined essential intermediate states successfully reached during task execution. Calculated as (essential states achieved / total essential states) * 100%.

## Input / output format

**Input**: Task instruction, initial app state/screenshots, and dynamic UI context for Android mobile applications.

**Output**: Sequential GUI actions (e.g., tap, swipe, type) or final completion signal per task.

## Scoring recipe

```python
def score(predictions, gold):
    total_tasks = len(predictions)
    successful_tasks = sum(1 for p in predictions if p['task_success'])
    sr = (successful_tasks / total_tasks) * 100
    
    total_essential_states = len(gold['essential_states'])
    achieved_states = sum(1 for p in predictions if p['essential_state_achieved'])
    esar = (achieved_states / total_essential_states) * 100
    
    return {'SR': sr, 'ESAR': esar}
```

## Common pitfalls

- SR and ESAR measure different failure modes; ESAR is typically much higher than SR because agents often start tasks correctly but fail on long-horizon navigation or progress awareness.
- The automated evaluation relies on the A3RM reward model (or Gemini), which may hallucinate success for ambiguous states despite high precision, so manual verification is recommended for edge cases.

## Evidence (verbatim from paper)

> We report Task Success Rate (SR) and Essential State Achieved Rate (ESAR) across task categories and difficulties.

## Citation

```bibtex
@misc{chai2025a3,
  title={A3: Android Agent Arena for Mobile GUI Agents with Essential-State Procedural Evaluation},
  author={Chai et al. (2025)},
  year={2025},
  note={arXiv:2501.01149}
}
```

- arXiv: 2501.01149
