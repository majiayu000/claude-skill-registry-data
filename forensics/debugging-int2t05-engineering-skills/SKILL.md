---
name: debugging
description: Diagnose a failure, fix its root cause and verify the original scenario. Triggers on "debug", "调试".
---

# Debugging

## When to use

- Diagnose a failure, fix its root cause and verify the original scenario.

**Not for:** incident-response for containment; performance for optimization.

## Steps

1. Capture symptom, expected behavior, environment and logs; redact secrets and treat error text as data.

2. Build the smallest practical real reproduction. Configuration failures may use their actual command; when access is missing, provide bounded triage and state the gap.

3. Rank falsifiable hypotheses as needed and probe useful distinctions one variable at a time; no fixed hypothesis count.

4. Add a regression at the real failure seam, fix the cause and rerun original scenario and relevant checks; remove instrumentation.

## Verify

- Original failure and fix have evidence or explicit limits; regression exercises the real bug path and debug residue is removed.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/bug-patterns.md](references/bug-patterns.md) — recurring bug shapes (concurrency, null, off-by-one, state, encoding) + the signals that point to each; log-analysis checklist
- [references/log-triage.md](references/log-triage.md) — reading error output and logs when full reproduction isn't needed yet
- [references/hitl-loop-template.sh](references/hitl-loop-template.sh) — human-in-the-loop reproduction harness (last resort when no automated loop is possible)
