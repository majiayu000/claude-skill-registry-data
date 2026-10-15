---
name: artifact-management
description: "Structured artifact trail for feature implementations — plans, implementations, reviews, and decisions."
context: fork
globs: []
alwaysApply: false
---

# Artifact Management

Structured artifact trail system for documenting feature implementations. Defines what, where, and how agents produce phase outputs.

---

## Temp Folder

All ephemeral artifacts live in `.pantheon/memory-bank/.tmp/` — gitignored and wiped on sprint close.

```
.pantheon/memory-bank/
├── .tmp/                  ← GITIGNORED — ephemeral artifacts
│   ├── PLAN-<feature>.md
│   ├── IMPL-phase1-hermes.md
│   ├── IMPL-phase1-aphrodite.md
│   └── REVIEW-<feature>.md
├── _notes/                ← COMMITTED — permanent ADRs
│   └── ADR-<topic>.md
├── 01-active-context.md
└── 02-progress-log.md
```

---

## Artifact Types

| Prefix | Location | Ephemeral? | Produced by |
|--------|----------|------------|-------------|
| `PLAN-` | `.tmp/` | ✅ | Athena |
| `IMPL-` | `.tmp/` | ✅ | Hermes/Aphrodite/Demeter |
| `REVIEW-` | `.tmp/` | ✅ | Themis |
| `DISC-` | `.tmp/` | ✅ | Apollo |
| `ADR-` | `_notes/` | ❌ Permanent | Any → Mnemosyne |

---

## Who Generates

| Situation | Agent | Artifact |
|-----------|-------|----------|
| Planning | Athena | `PLAN-<feature>.md` |
| Implementation | Worker | `IMPL-phase<N>-<agent>.md` |
| Review | Themis | `REVIEW-<feature>.md` |
| Discovery | Apollo | `DISC-<topic>.md` |
| Decision | Any → Mnemosyne | `ADR-<topic>.md` |

> **Zeus does NOT generate artifacts.** He orchestrates agents that generate them.

---

## Templates

### PLAN
```markdown
# PLAN-<feature>
**Date:** YYYY-MM-DD  **Status:** Awaiting Approval

## Goal
[One sentence]

## Phases
1. Phase 1 — @hermes
2. Phase 2 — @aphrodite

## Risks
- [Risk]
```

### IMPL
```markdown
# IMPL-<phase>-<agent>
**Date:** YYYY-MM-DD  **Status:** Awaiting Themis Review

## What Was Implemented
- [file] — [what changed]

## Tests
- ✅ X tests / Coverage: Y%
```

### REVIEW
```markdown
# REVIEW-<feature>
**Status:** APPROVED | NEEDS_REVISION | FAILED

## Verdict
[APPROVED | NEEDS_REVISION | FAILED]

## Issues
- CRITICAL: X / HIGH: Y / MEDIUM: Z
```

---

## Human Pause Points

1. **After PLAN** → user reads `.tmp/PLAN-<feature>.md` and approves
2. **After REVIEW** → user reads `.tmp/REVIEW-<feature>.md` and validates focus items
3. **Before git commit** → user executes manually

---

## Cleanup

```
@mnemosyne Close sprint    # Wipes entire .tmp/
@mnemosyne Clean tmp       # Wipes .tmp/ without closing sprint
@mnemosyne List artifacts  # Check what's in .tmp/
```
