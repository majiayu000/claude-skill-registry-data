---
name: master
description: Master engineering principles and command index for Phantom Guard. Use at session start to understand project context, commands, and quality gates.
---

# PHANTOM GUARD — FORTRESS 2.0 MASTER PROTOCOL

> **Classification**: MILITARY-GRADE DEVELOPMENT PROTOCOL
> **Project**: Phantom Guard - Slopsquatting Detection
> **Framework**: FORTRESS 2.0
> **Violation Response**: STOP. FIX. CONTINUE.

---

## MISSION STATEMENT

**Build a slopsquatting detection library that protects developers from AI-hallucinated malicious packages.**

- Target: <5% false positive rate
- Speed: <200ms per package
- Scope: PyPI, npm, crates.io

---

## GATE SYSTEM — MANDATORY PROGRESSION

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FORTRESS 2.0 GATE SYSTEM                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   GATE 0: PROBLEM DEFINITION                                        │
│   Status: ✅ COMPLETE (Research Fortress v7)                        │
│   Output: PROJECT_FOUNDATION.md                                     │
│                                                                     │
│   GATE 1: ARCHITECTURE                                              │
│   Command: /architect                                               │
│   Status: 🟡 PENDING                                                │
│   Output: docs/architecture/ARCHITECTURE.md                         │
│   ⛔ STOP: Every decision needs SPEC_ID, HOSTILE_ARCHITECT review   │
│                                                                     │
│   GATE 2: SPECIFICATION                                             │
│   Command: /spec                                                    │
│   Status: ⬜ BLOCKED (needs Gate 1)                                 │
│   Output: docs/specification/SPECIFICATION.md                       │
│   ⛔ STOP: Every invariant numbered, every edge case documented     │
│                                                                     │
│   GATE 3: TEST DESIGN                                               │
│   Command: /test                                                    │
│   Status: ⬜ BLOCKED (needs Gate 2)                                 │
│   Output: tests/ stubs, TEST_MATRIX.md                              │
│   ⛔ STOP: Tests exist BEFORE code, coverage targets defined        │
│                                                                     │
│   GATE 4: PLANNING                                                  │
│   Command: /roadmap                                                 │
│   Status: ⬜ BLOCKED (needs Gate 3)                                 │
│   Output: docs/planning/ROADMAP.md with traced tasks                │
│   ⛔ STOP: Every task < 8 hours, every task traces to SPEC_ID       │
│                                                                     │
│   GATE 5: VALIDATION                                                │
│   Command: /hostile-review                                          │
│   Status: ⬜ BLOCKED (needs implementation)                         │
│   Output: VALIDATION_REPORT.md                                      │
│   ⛔ STOP: HOSTILE_VALIDATOR has VETO power                         │
│                                                                     │
│   GATE 6: RELEASE                                                   │
│   Command: /release                                                 │
│   Status: ⬜ BLOCKED (needs Gate 5)                                 │
│   Output: Release artifacts, CHANGELOG.md                           │
│   ⛔ STOP: RELEASE_GUARDIAN final sign-off                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## COMMAND INDEX

### Gate Commands (Sequential - Cannot Skip)

| Command | Gate | Purpose | Can Skip? |
|---------|------|---------|-----------|
| `/architect` | 1 | System architecture design | **NO** |
| `/spec` | 2 | Specification, invariants | **NO** |
| `/test` | 3 | Test design before code | **NO** |
| `/roadmap` | 4 | Task breakdown | **NO** |
| `/hostile-review` | 5 | Validation (VETO POWER) | **NO** |
| `/release` | 6 | Release preparation | **NO** |

### Implementation Commands

| Command | Purpose |
|---------|---------|
| `/implement` | Guided TDD implementation |
| `/competitive-watch` | Scan for competition (weekly) |
| `/validate-technical` | Validate APIs still work (monthly) |

---

## ABSOLUTE RULES — NO EXCEPTIONS

### Rule 1: Gates Cannot Be Skipped

```
❌ FORBIDDEN: "Let's skip architecture and start coding"
❌ FORBIDDEN: "We'll add tests later"
❌ FORBIDDEN: "This is simple, no spec needed"

✅ REQUIRED: Complete Gate N before starting Gate N+1
✅ REQUIRED: Gate outputs must exist before proceeding
✅ REQUIRED: If blocked, fix the blocker first
```

### Rule 2: HOSTILE_VALIDATOR Has Veto Power

```
If HOSTILE_VALIDATOR says NO_GO:
  1. STOP all work
  2. Address every issue raised
  3. Re-run validation
  4. Only proceed after GO verdict

NO EXCEPTIONS. NO SHORTCUTS. NO "WE'LL FIX IT LATER."
```

### Rule 3: TDD Is Mandatory

```
Before writing ANY production code:
  1. Test stub MUST exist
  2. Test MUST fail when run
  3. Write ONLY enough code to pass test
  4. Refactor if needed
  5. THEN commit
```

### Rule 4: Trace Everything

```
Every function: # IMPLEMENTS: S001
Every test: # SPEC: S001, T001.1
Every task: TRACES: S001, INV001

Orphan code (no trace) = BUILD FAILURE
```

### Rule 5: Performance Budget Is Sacred

```
| Operation | Budget | Violation = |
|-----------|--------|-------------|
| Single package (cached) | <10ms | BLOCK MERGE |
| Single package (uncached) | <200ms | BLOCK MERGE |
| 50 packages | <5s | BLOCK MERGE |

No exceptions. No "we'll optimize later."
```

---

## SESSION START PROTOCOL

Every development session MUST begin with:

```
1. /master                    # Load this context
2. Check .fortress/FORTRESS.md # Know gate status
3. Proceed with current gate   # Continue work
```

---

## FILE STRUCTURE

```
phantom-guard/
├── .fortress/                    # FORTRESS 2.0 config
│   ├── FORTRESS.md               # Framework status
│   └── gates/                    # Gate completion records
├── .claude/skills/               # Command definitions
│   ├── master/                   # This command
│   ├── architect/                # Gate 1
│   ├── spec/                     # Gate 2
│   ├── test/                     # Gate 3
│   ├── roadmap/                  # Gate 4
│   ├── hostile-review/           # Gate 5
│   ├── release/                  # Gate 6
│   ├── implement/                # TDD workflow
│   ├── competitive-watch/        # Competition scan
│   └── validate-technical/       # API validation
├── docs/
│   ├── frameworks/               # FORTRESS 2.0 docs
│   └── research/                 # Technical research
└── PROJECT_FOUNDATION.md         # SOURCE OF TRUTH
```

---

## CURRENT STATUS

**Active Gate**: Gate 1 (Architecture)

**Next Action**: Run `/architect` to begin architecture design

**Blockers**: None

---

## SOURCE OF TRUTH

1. **PROJECT_FOUNDATION.md** - Original research
2. **.fortress/FORTRESS.md** - Framework configuration
3. **docs/frameworks/FORTRESS_2.0_FRAMEWORK.md** - Full framework docs

---

*FORTRESS 2.0 — Because bugs escape reviews, but they don't escape gates.*
