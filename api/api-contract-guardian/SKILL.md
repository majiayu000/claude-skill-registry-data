---
name: api-contract-guardian
description: "API contract guard: extracts the API surface (HTTP routes with params, DTO fields, exported signatures - preferring OpenAPI files when present) from two git states of a repo, diffs them, classifies every change as breaking / non-breaking / additive, and writes a ready-to-ship consumer migration note per breaking change. Read-only. Trigger: /api-diff"
trigger: /api-diff
---

## What this is for

Breaking changes happen on the side: a field renamed, a required parameter added, a status code changed - and weeks later a consumer breaks whose existence nobody knew. Manually comparing the API surface of two code states and classifying each change by contract-break severity is so tedious that nobody does it. An LLM can extract surfaces, diff them, and - the real value - write migration notes per breaking change for consumers.

**Audience:** Senior
- API providers get release notes generated as a side effect.
- Consumer teams get migration instructions before they break.
- Versioning decisions get SemVer honesty.

### Trigger: `/api-diff`


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1 - `-help`/`-h` check
Print usage block and stop.

### Step 2 - Determine project + refs
Ask for `-ProjectDir` + old state (`-OldRef`, e.g., tag/branch/hash; default: last tag, else HEAD~20 suggested) + new state (default: working tree). Confirm.

### Step 3 - Run collector twice
```powershell
& .\scripts\api-surface.ps1 -ProjectDir "<path>" -Ref "<old-ref>"
& .\scripts\api-surface.ps1 -ProjectDir "<path>"
```

### Step 4 - LLM diff + classification
1. **Matching**: routes by (method, normalized path - param names don't matter: `/users/:id` = `/users/{userId}`), DTOs by name (rename suspicion: same field set, different name → `probable`), signatures by name.
2. **Classification per difference**:
   - **breaking**: route removed; method changed; required param/field NEW; field removed; field type incompatible; optional→required; response field removed (openapi source); signature param removed/reordered/new required.
   - **additive**: new route; new optional field/param; new signature.
   - **non-breaking**: doc/description change; required→optional; type widening.
   - Gray zones (type text changed, compatibility unclear) → `probable` + open question.
3. **Migration note per breaking change**: copy-ready paragraph for consumers - what changes, what to do BEFORE the update, before/after example from real names.
4. **SemVer recommendation**: breaking > 0 → major; additive > 0 → minor; else patch.

### Step 5 - Produce report
Write `api-diff-report.md`:

```
# API Diff Report - <project>

## Summary
- <B> breaking, <A> additive, <N> non-breaking
- SemVer recommendation: major/minor/patch

## Breaking Changes
### 1. <change description>
- Before (<ref>): ...
- After (working tree): ...
- Migration note: ...
- ...

## Additive Changes
...

## Non-Breaking Changes
...

## Open Questions / Rename Suspicions
...
```

## Usage

```powershell
# Interactive (with ref suggestion)
/api-diff

# Old ref vs. working tree
/api-diff C:\Projects\my-app v1.4.0

# Two refs
/api-diff C:\Projects\my-app v1.3.0 v1.4.0

# Help
/api-diff --help
```
