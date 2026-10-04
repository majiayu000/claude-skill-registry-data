---
name: override-confidence
description: >
  Bypass the confidence gate for the next PR/MR creation. Logs the reason
  for accountability. Auto-clears after the next gate fire.
  Triggers on: override confidence, bypass confidence, force PR.
---

## Override Confidence Gate

Creates a one-shot bypass marker so the confidence-gate hook allows the
next `gh pr create` or `glab mr create` even on RED.

### Usage
`/override-confidence "<reason>"`

Reason must be at least 12 characters and not boilerplate. Example:
> /override-confidence "Reviewer flagged perf regression tracked in PERF-42; not blocking this delivery"

### Execute
Run:
```bash
source skills/override-confidence/skill.bash
override_confidence "$ARGUMENTS"
```

The marker file `.git/aw/override-<spec-id>` is consumed by the next hook
fire (success or failure). Reason is logged to the spec's confidence.jsonl
as an `override` event with `trigger: "manual"`.
