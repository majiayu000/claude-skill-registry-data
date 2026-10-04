---
name: pi-cost
description: >-
  Calculate and display the token usage, turns, and estimated cost for the active session
  and subagent runs by parsing the harness session logs. Use when the user asks for
  token usage, session cost, or types `/pi-cost`.
version: 1.0.0
---

# pi-cost

A utility skill to parse and estimate costs for the active Pi coding agent session, including any subagents called during the run.

## Setup

The Python helper script is pre-installed in the skill folder:
`scripts/pi_cost.py`

No extra dependencies are required.

## Usage

When triggered, execute the helper script using the `bash` tool:

```bash
python3 .claude/skills/pi-cost/scripts/pi_cost.py
```

This will output:
1. Active session file name and path.
2. Main session stats: total turns, tokens (input/output/cacheRead/cacheWrite), and estimated cost based on standard model pricing.
3. Nested subagent runs: breakdown of subagent name, model, turns, token details, and estimated cost.
4. Total consolidated session summary.
