---
name: compliance-monitor
description: Real-time compliance watchdog. Track GDPR UK, GwG, FINMA, EU AI Act, SRA rules, nDSG changes. Spot risks before they hit. Auto-generate compliance heatmaps, alert summaries, risk exposure reports. Feeds directly into Compliance Cockpit."
---

# Compliance Monitor — Claude Code wrapper

This is the **Claude Code wrapper** for `compliance-monitor`. The full skill definition lives in `shared/SKILL-CORE.md` in the same skill folder.

## When to use

Use when the user asks for:
- `compliance-monitor`
- "run compliance-monitor"
- Any trigger described in the core skill

## How to invoke

In Claude Code:

```
compliance-monitor
```

## Instructions

1. Read `shared/SKILL-CORE.md` for the platform-agnostic workflow, rules, and examples.
2. Execute the workflow using Claude Code tools.
3. Load any referenced files from `shared/` or subdirectories relative to this skill folder.

## References

- `shared/SKILL-CORE.md` — full skill definition
