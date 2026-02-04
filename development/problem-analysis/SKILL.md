---
name: problem-analysis
description: Invoke IMMEDIATELY for structured problem analysis and solution discovery.
---

# Problem Analysis

When this skill activates, IMMEDIATELY invoke the script. The script IS the
workflow.

## Invocation

```bash
python3 scripts/analyze.py --step 1 --total-steps 4
```

| Argument        | Required | Description                 |
| --------------- | -------- | --------------------------- |
| `--step`        | Yes      | Current step (starts at 1)  |
| `--total-steps` | Yes      | Minimum 4; adjust if needed |

Do NOT analyze or explore first. Run the script and follow its output.
