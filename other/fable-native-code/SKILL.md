---
name: fable-native-code
description: Use when writing or editing code in an existing codebase — before adding comments, docstrings, try/catch blocks, validation, logging, or TODOs the surrounding file doesn't have, and before explaining your style choices in the reply.
---

# Native Code

## Overview

Your diff should read like the file's longtime owner wrote it. The file has
a style — naming, error handling, comment density, formatting. Write in it.
Your personal preferences are not improvements; they're an accent.

## Rules

1. **Match the file:** naming, error-handling idiom, comment density,
   formatting, import organization. If the file has one comment per 200
   lines, your addition almost certainly has zero.
2. **Comments state only constraints the code cannot show** — invariants,
   gotchas, why-not-the-obvious-way. Never what the next line does, never
   narration of your change ("now correctly handles X"), never justification
   aimed at a reviewer. Test: after the PR merges, is this comment
   information or noise?
3. **No defensive bloat:** no try/catch around code that works, no
   validating invariants the types or callers already guarantee, no
   logging, config, or flags nobody asked for. If the contract is worth
   enforcing, that's a test or a boundary assertion — its own change.
4. **Don't narrate your restraint.** The urge to explain what you
   *didn't* add ("note: I deliberately left out the doc comment because…")
   is the same urge that adds it — displaced into the reply. The
   justification a senior dev never writes in code, they also never write
   in chat. Deliver the code; mention style only if the user asks.
5. **Clean exit:** no debug prints, no commented-out code, no TODO crumbs
   you created.
6. **Names come from the codebase's existing vocabulary.** Don't coin a
   second name for an existing concept.

## Contrast

Task: add `clampWindow` to a terse Go file whose only comment in 200 lines
marks a sorting invariant; callers guarantee `max >= 0`.

**Foreign (your habits, not the file's):**

```go
// clampWindow clamps start and end into the valid range [0, max] and
// normalizes inverted windows. Returns (start, start) when end < start.
func clampWindow(start, end, max int) (int, int) {
    if max < 0 {
        return 0, 0 // defensive: should never happen
    }
    ...
}
```

**Native (what the file's owner would write):**

```go
func clampWindow(start, end, max int) (int, int) {
    if start < 0 {
        start = 0
    }
    if start > max {
        start = max
    }
    if end < 0 {
        end = 0
    }
    if end > max {
        end = max
    }
    if end < start {
        return start, start
    }
    return start, end
}
```

No header comment (the signature says it), no `max < 0` guard (the callers
guarantee it, like `mergeWindows` trusts its sorted-input invariant) — and
no paragraph in the reply explaining either omission.

## Rationalizations

| Thought | Reality |
|---|---|
| "A doc comment helps the next reader" | The next reader has the signature and twelve obvious lines. The file's owner trusted them; trust them too. |
| "Extra validation can't hurt" | A guard for an impossible state is dead code that suggests the state is possible. Swallowed errors are the most expensive bugs to find. |
| "My last reviewer praised my documentation habits" | In a codebase whose style wants documentation. This file's style is the spec now. |
| "I'll explain in chat what I left out of the code" | Observed verbatim in baseline: a multi-paragraph "note on what I deliberately left out" after "output only the code." Restraint that announces itself isn't restraint. |
| "I'll leave a TODO for the edge case" | Handle it, or surface it in your report. TODOs are where edge cases go to be forgotten. |

Provenance: baseline Opus 4.8 wrote the native version above, then narrated
its restraint anyway (rule 4 exists because of it). fable-skills test logs,
2026-06-10.

## Red Flags — delete before committing

- A comment that describes the line below it
- "deliberately", "note that I", "for safety" — in code or in your reply
- try/catch whose catch block only logs or re-raises
- A guard for a state the caller contract excludes
- Your addition is the only part of the file with comments
