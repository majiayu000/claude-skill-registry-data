---
name: codebase-hygiene
description: Find semantic duplicates (same intent, different implementation) and shallow modules (thin wrappers spreading complexity). Read-only advisory — changes route through BUILD with full gates. Use when auditing code quality, before refactoring, or when a codebase feels bloated.
---

# Codebase Hygiene

Advisory and read-only. Diagnoses and proposes; does not refactor. Any actual change: tell the user to run `/build`.

## Mode 1: Semantic duplicate detection

Copy-paste detectors catch syntactic duplicates. This finds **semantic** duplicates — functions serving the same purpose but implemented independently under different names.

### Method

1. **Extract catalog** — grep/glob for exported functions. Record `name | file:line | signature`.
2. **Categorize by domain** (cheap tier) — validation, formatting, path manipulation, HTTP shaping, date handling. Mechanical bucketing to shrink the comparison space.
3. **Drop categories with <3 functions** — can't hide a meaningful duplication pattern.
4. **Detect duplicates per category** (capable tier) — READ the implementations, decide which share intent. **Never use cheap name-based detection** — it anchors on names and rubber-stamps "these look different."
5. **Emit findings** — group by confidence, highest first. Each finding: what is duplicated, why it matters, the fix, `file:line` evidence. Route through the review finding contract.

### High-risk zones

| Zone | Why it duplicates |
| ---- | ----------------- |
| `utils/`, `helpers/`, `lib/` | Catch-all dumping grounds |
| Validation code | "Is this a valid email/id/url" rewritten per feature |
| Error formatting | Every module invents its own Error → string |
| Path manipulation | Join/normalize/relativize reimplemented |
| String formatting | Truncate, slugify, titlecase, pad re-rolled |
| Date formatting | Parse/format/diff scattered |
| API response shaping | Envelope/pagination/error-body copied per endpoint |

### Consolidation discipline

Never delete a duplicate until ALL THREE hold:

1. **Survivor has tests** — pick the implementation with real coverage. If neither has tests, write the test against the chosen survivor first.
2. **All callers updated** — grep to enumerate callers. Missing one is a silent break.
3. **Re-run after consolidation** — test suite + build/typecheck pass. Green tests on the survivor license the deletion.

## Mode 2: Module deepening

Thin wrappers and pass-through layers spread complexity without adding capability. A module that only forwards calls to another module is a shallow module — it adds a layer to navigate without earning it.

### Signals

- A module whose entire body is forwarding calls to one other module.
- "Manager" / "Service" / "Helper" classes that wrap a single dependency and add no logic.
- Functions that take args, immediately pass them unchanged to another function, and return its result.

### Fix direction

Deepen: collapse the wrapper into its caller, OR add real responsibility (validation, transformation, policy) that justifies the layer. A module should either **hide complexity** (deep module) or **not exist**.

## Don't

- Don't refactor from this skill — it's advisory. Propose, then tell the user to run `/build`.
- Don't delete a duplicate without the 3 consolidation gates (tests + callers + re-run).
- Don't trust name-based duplicate detection — read the implementations.
