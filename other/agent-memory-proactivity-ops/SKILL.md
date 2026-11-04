---
name: agent-system-memory-proactivity-ops
description: Audit and improve AgentSystem memory retention, proactive behavior, learning quality, and agent consistency. Use when bots forget context, skip memory writes, wait for explicit prompts, or repeat the same errors across runs.
---

# AgentSystem Memory Proactivity Ops

Use this skill to keep memory and proactivity loops healthy after config, prompt, or plugin changes.

## Quick Start

1. Run baseline checks:
```bash
bash scripts/proactivity_check.sh --hours 24
```

2. Apply known remediation pack:
```bash
bash /Users/user/clawd/scripts/agent-system-plan2-remediate.sh
```

3. Re-check and smoke-test memory jobs:
```bash
bash scripts/proactivity_check.sh --hours 6 --smoke
```

## Workflow

1. Verify scheduler contract and agent consistency metrics.
2. Verify learning score, filler count, and output quality in recent memory jobs.
3. Check latest runs of:
- `hachi-self-compound` (`046bb2db-42ad-4b79-96d4-f9aa1392ede8`)
- `memory-fact-extraction` (`079a9ab8-d706-465c-801d-741f4a2d55a3`)
4. Validate learning artifacts were updated recently.
5. If quality is below target, tighten prompt constraints and re-run smoke checks.

## Resources

- `scripts/proactivity_check.sh`: one-command audit + optional memory smoke tests.
- `references/quality-gates.md`: acceptance thresholds and remediation sequence.
