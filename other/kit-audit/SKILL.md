---
name: kit-audit
description: Audit guardrails-kit compliance of the current session — run the transcript marker scorecard. Use when asked to audit compliance, check which guardrail rules fired or were missed, or score the session.
---

1. Run `python3 scripts/audit-transcript.py --latest` (or pass an explicit transcript path).
2. Summarize the scorecard: which trigger checks FIRED/MISSED, and notable zero-count marker families.
3. For each MISSED check, name the kit rule that should have fired and quote the event evidence.
4. Record heuristic false positives as `NOTED (not done):` lines — they feed the F16 rule-lifecycle tuning.
