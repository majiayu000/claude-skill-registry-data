---
name: challenge-diagnosis
description: Protocol for challenging and revising a bug diagnosis — layer vs reject modes, investigation history format, re-diagnosis instructions.
compatibility: opencode
metadata:
  audience: debug-investigator
  purpose: diagnosis-feedback-loop
---

## What I do

Define how an engineer's challenge to a bug diagnosis gets processed:
which mode to use, how to preserve the reasoning chain, and what the
`debug-investigator` should do differently in each mode.

## Investigation History format

Appended to the bug spec after each challenge round. Never delete existing
rounds — the history is append-only.

```markdown
## Investigation History

### Round 1 — Initial diagnosis
- **Date**: 2026-04-22T14:00:00Z
- **Agent**: debug-investigator
- **Root cause**: <one-line summary>
- **Confidence**: High | Medium | Low
- **Key evidence**: <what pointed to this root cause>

### Round 2 — Challenged (layer)
- **Date**: 2026-04-22T15:30:00Z
- **Challenged by**: engineer
- **Feedback**: "<verbatim engineer feedback>"
- **Revised root cause**: <updated root cause incorporating both threads>
- **What changed**: <what's different from the previous round and why>
- **Confidence**: High | Medium | Low
```

### Round fields

| Field | Required | Notes |
|---|---|---|
| Date | yes | UTC ISO-8601 |
| Agent | yes | `debug-investigator` or `engineer` |
| Root cause / Revised root cause | yes | One-line summary |
| Confidence | yes | High / Medium / Low |
| Challenged by | challenge rounds only | Always `engineer` |
| Feedback | challenge rounds only | Verbatim engineer feedback |
| What changed | challenge rounds only | Delta from previous round |
| Key evidence | initial round only | What pointed to the root cause |

## Mode detection

Scan the engineer's feedback for mode signals:

**Reject signals** — if ANY of these appear, use reject mode:
- "wrong", "incorrect", "not correct", "off base"
- "re-diagnose", "start over", "start fresh"
- "this isn't it", "missed the mark"
- Explicit `--reject` flag

**Layer signals** — everything else defaults to layer:
- "also consider", "what about", "I think it might also be"
- "have you looked at", "related to"
- "in addition to", "another possibility"

When ambiguous, default to layer — it's safer because nothing is discarded.

## Layer mode protocol

The `debug-investigator` receives:

1. The full existing spec (including current Root Cause and Fix Plan)
2. The engineer's feedback as additional context
3. These instructions:

> Treat the existing analysis as valid evidence. The engineer has added a
> new hypothesis or thread. Investigate both the original root cause AND
> the new hypothesis. Produce a single merged analysis — not two competing
> explanations. If the new hypothesis supersedes the original, say so
> explicitly. If they're complementary (e.g. a root cause and a
> contributing factor), explain the relationship.

The investigator updates the spec's Root Cause and Fix Plan sections in
place, then appends a new round to Investigation History.

## Reject mode protocol

Before the `debug-investigator` runs:

1. **Archive** the current `## Root Cause`, `## Fix Plan`, and any
   `## Investigation` sections into `## Investigation History` as the
   previous round. Mark them clearly as superseded.
2. **Clear** the Root Cause and Fix Plan sections (replace with
   placeholders for the investigator to fill).

The `debug-investigator` then receives:

1. The spec with cleared Root Cause / Fix Plan sections
2. The full Investigation History (so it can reference — but not assume
   the correctness of — previous findings)
3. The engineer's feedback as the starting hypothesis
4. These instructions:

> The previous analysis has been rejected by the engineer. Their feedback
> is your starting hypothesis. You may reference the archived findings in
> Investigation History as evidence, but do not assume they are correct.
> Start your investigation from the engineer's hypothesis and follow the
> evidence.

## What this skill does NOT do

- Does not auto-accept or auto-reject diagnoses — the engineer decides
- Does not delete previous analysis — layers merge, rejects archive
- Does not require the original session — the spec on disk is the input
- Does not modify the debug-investigator's core investigation logic —
  only the input framing changes
- Does not add Go code — this is instructions in markdown
