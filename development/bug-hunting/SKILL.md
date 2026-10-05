---
name: bug-hunting
description: "Use when fixing bugs, debugging failures, or proactively reviewing code for hidden bugs. Reactive mode: fix known bugs. Proactive mode: hunt for bugs in code. Enforces confirmed root cause before any fix."
---

# Bug Hunting

## Overview

Bugs have root causes. Symptoms have patches. Patches create future bugs.

**Core principle:** A claim is not evidence. Evidence is not root cause. Root cause is not a fix.

**Violating the letter of this process is violating the spirit of bug hunting.**

## Two Modes

| Mode | Trigger | First Question |
|------|---------|----------------|
| **Reactive** | "Fix this bug", "test failing", "production error" | What is the confirmed root cause? |
| **Proactive** | "Review this code", "find bugs in...", "audit this" | What could go wrong? Where are the weakest points? |

Both modes follow the same 5 phases. Entry point differs; discipline does not.

## The Three Iron Laws

```
LAW 1: NO FIX WITHOUT CONFIRMED ROOT CAUSE
LAW 2: NO CLAIM WITHOUT EVIDENCE
LAW 3: FIX THE SOURCE, NOT THE SYMPTOM
```

**The Laws are non-negotiable. All three must hold for every bug.**

If you haven't confirmed root cause → you cannot propose a fix.
If you have evidence → state it explicitly. Never say "probably" or "almost certainly."
If the fix is at the crash site → trace back further. The source is upstream.

## The Five Phases

Complete each phase before proceeding. No skipping.

### Phase 0: Reconnaissance

**BEFORE touching any code or error message:**

1. What is the **expected behavior**? (What should it do, not what it does?)
2. What **type of bug** is this?
   - Logic error, race condition, data corruption, integration failure, performance, security
3. What **components** are involved?
4. What are **common bugs** in this domain/language/framework?

→ **If expected behavior is unclear: stop and clarify before proceeding.**

*This phase prevents "fixing" intentional behavior and grounds your investigation.*

### Phase 1: Evidence Hunt

**Collect evidence. Do not interpret yet.**

1. Read ALL error messages and stack traces — every line, every file path
2. Reproduce consistently — if you cannot reproduce it, you cannot fix it
3. Check recent changes — git diff, recent commits, new dependencies
4. Add diagnostic instrumentation at component boundaries

   → **Read `references/evidence-collection.md` for multi-component instrumentation patterns**

**Classify every piece of evidence:**
- ✅ **CONFIRMED** — reproducible, directly observed
- 🔍 **SUSPECTED** — correlates but not proven
- 💭 **THEORETICAL** — logical inference, not yet observed

**No fix attempts in this phase. Evidence collection only.**

### Phase 2: Blast Radius Mapping

**Before tracing the root cause, map the full surface.**

→ **Read `references/blast-radius.md` before this phase**

1. Document the **primary bug** with its evidence classification
2. Identify **minimum 2 additional suspects** in the same area:
   - Other functions with the same pattern
   - Related code paths that could fail the same way
   - Adjacent components that share the broken assumption
3. Classify each suspect by severity:
   - 🔴 **Critical** — data loss, security breach, crash in production
   - 🟠 **High** — wrong output, significant user impact
   - 🟡 **Medium** — intermittent, workaround exists
   - 🟢 **Low** — cosmetic, rare edge case

*Fixing one bug while missing three siblings is not a fix — it's a delay.*

### Phase 3: Root Cause Trace

**Trace backward to the origin. Not where it crashes — where it starts.**

→ **Read `references/root-cause-tracing.md` for complete backward tracing technique**

For each bug in Phase 2:
1. Where does the bad value **originate**?
2. What **called** this code with the bad value?
3. Keep tracing **up** until you find the source — not the crash site
4. Form **one hypothesis**: "Root cause is X because [confirmed evidence Y]"
5. Test minimally — one change, one variable

**Gates:**
- Hypothesis not confirmed? → Form new hypothesis. Return to Phase 1.
- 3+ hypotheses failed? → **Architectural problem. Stop and discuss before fix #4.**

### Phase 4: Resolution

**Fix confirmed root causes. Make bugs structurally impossible.**

→ **Read `references/defense-in-depth.md` for layered validation patterns**

1. **Create failing test first** — before writing the fix (write a minimal failing test that reproduces the bug; use TDD: test must fail for the right reason before any code is written)
2. **Fix one bug at a time** — address the root cause, not the crash site
3. **Apply defense-in-depth** — validate at multiple layers so the bug cannot recur
4. **Verify** — test passes, no regressions, issue resolved

**Priority order:** 🔴 Critical → 🟠 High → 🟡 Medium → 🟢 Low

## Evidence Language Rules

| Forbidden phrase | Why | Required replacement |
|------------------|-----|----------------------|
| "almost certainly" | Claim disguised as evidence | State the actual evidence or say "SUSPECTED" |
| "probably X" | Guess dressed as diagnosis | Reproduce it or mark as 💭 THEORETICAL |
| "appears to be" | Hedged assumption | Run the trace. Confirm or mark SUSPECTED. |
| "root cause is X" | May be proximate, not source | Complete Phase 3 trace first |
| "fix is safe regardless of cause" | Skips Law 1 entirely | No. Root cause first. Always. |
| "investigate later/next sprint" | Deferred symptom patch | Do not ship a fix without its root cause confirmed |

## Red Flags — STOP and Return to Phase 0

- "Quick fix for now, investigate later"
- "The correlation is too strong to be coincidence" → correlation ≠ causation
- "The fix is minimal/one-line, it can't hurt anything"
- "Expert/senior/manager already confirmed the root cause" → verify it yourself
- "I don't fully understand but this should work"
- Each fix reveals a new problem in a different place → architectural problem

## Quick Reference

| Phase | Purpose | Gate to proceed |
|-------|---------|-----------------|
| **0. Reconnaissance** | What should it do? What type of bug? | Expected behavior is clear |
| **1. Evidence Hunt** | Collect, classify, reproduce | Can reproduce consistently |
| **2. Blast Radius** | Primary + 2 suspects + severity | All suspects mapped |
| **3. Root Cause Trace** | Trace backward to origin | Root cause CONFIRMED, not "probably" |
| **4. Resolution** | Test, fix source, add layers | All 🔴 Critical resolved, tests pass |

## Supporting Techniques

- **`references/evidence-collection.md`** — Multi-component diagnostic instrumentation
- **`references/blast-radius.md`** — Surface mapping: finding adjacent bugs before fixing one
- **`references/root-cause-tracing.md`** — Backward tracing through call chains
- **`references/defense-in-depth.md`** — Layered validation to make bugs structurally impossible

**Related skills:**
- **TDD skill** (any environment) — For failing test creation (Phase 4, Step 1)
- **Verification** — Verify fix before claiming success: re-run full test suite, confirm issue resolved, no regressions
