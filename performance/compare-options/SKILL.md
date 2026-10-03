---
metadata:
  name: compare-options
  class: toolboxes
  type: skill
  version: '1.0'
  schema_version: '1.0'
  freshness:
    status: active
    sync_count: 0
    last_synced_by: daemon
    last_synced: '2026-06-27T00:00:00'
credentials:
  maturity: "functional"
  description: "Measure, compare, and optimize choices to ensure best path is taken."
  when_to_use: "Use this skill when the task involves compare options"
  triggers: ["benchmark", "compare", "measure", "optimize", "best option", "which is better"]
  inputs: ["options list", "evaluation criteria", "constraints"]
  outputs: ["comparison matrix", "optimal choice", "rationale", "trade-offs"]
---

# Compare Options

This skill allows the agent to systematically measure, compare, and optimize choices to ensure the objectively best available path is selected with documented rationale.

## Steps

1. **Enumerate all options.** List every available option clearly. Do not pre-filter based on assumption.
2. **Define evaluation criteria.** Identify the dimensions that matter (e.g., cost, speed, risk, compatibility, reversibility). Weight each criterion if applicable.
3. **Score each option per criterion.** Use a consistent scale (e.g., 1–5) and apply it neutrally across all options.
4. **Build the comparison matrix.** Organize scores into a table for clear visual comparison.
5. **Identify the winner.** Select the option with the highest weighted score, noting any exceptions (e.g., a hard constraint that disqualifies a leading option).
6. **Document trade-offs.** Explicitly state what is sacrificed with the winning choice.
7. **Output the recommendation** with the matrix, winner, rationale, and trade-offs.

## Output Format

```yaml
benchmark_result:
  criteria: ["criterion_1", "criterion_2"]
  matrix:
    option_a: {criterion_1: 4, criterion_2: 3}
    option_b: {criterion_1: 2, criterion_2: 5}
  winner: "option_b"
  rationale: "<why this wins>"
  trade_offs:
    - "<what is sacrificed by choosing option_b>"
```

## Notes
- Always make criteria explicit before scoring — implicit criteria lead to biased outcomes.
- If options have hard disqualifying constraints, flag them before scoring.
