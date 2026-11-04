---
name: agent-system-learning-loop
description: Evaluate and improve AgentSystem learning quality for memory/self-compound jobs. Use when bots forget, write filler summaries, fail to update learnings, or memory quality regresses over time.
---

# AgentSystem Learning Loop

Use this skill to audit whether learning jobs are producing actionable memory, not filler.

## Quick Start

1. Run learning quality audit:
```bash
python3 scripts/learning_quality_audit.py --hours 72
```

2. Inspect latest learning job runs:
```bash
agent-system cron runs --job 046bb2db-42ad-4b79-96d4-f9aa1392ede8 --limit 5
agent-system cron runs --job 079a9ab8-d706-465c-801d-741f4a2d55a3 --limit 5
```

3. Verify file outputs:
```bash
ls -lt ~/.agent-evolution/docs/learnings.md ~/.agent-evolution/memory | head
```

## Workflow

1. Detect filler output.
Flag summaries containing phrases like "let me check", raw tool logs, or error dumps.

2. Verify artifact updates.
Learning jobs should update `docs/learnings.md` and/or relevant memory files when they report success.

3. Score quality.
Use the script score to decide whether prompts/timeouts/rules need adjustment.

4. Apply remediation.
Tighten prompts for concrete outputs, increase timeout where needed, and re-run the same jobs for verification.

## Resources

- `scripts/learning_quality_audit.py`: Scores recent learning runs and flags regressions.
- `references/quality-criteria.md`: Quality gates for learning/memory cron jobs.
