---
name: embodiment-grounding-loop
description: Execute a safe sensor/actuator loop to ground tasks in local system state. Use when tasks require environment feedback or bounded actions.
---

# Embodiment Grounding Loop

Use this skill to run a safe sensor and action loop with explicit allowlists.

## Workflow

1) Load a loop plan (use assets/loop_template.json).
2) Collect sensor data.
3) Execute safe actions only.
4) Review the loop report for grounding evidence.

## Scripts

- Run: python scripts/sense_act.py --plan assets/loop_template.json
