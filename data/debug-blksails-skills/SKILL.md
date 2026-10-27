---
name: autoresearch:debug
description: |
  Scientific bug hunting using falsifiable hypotheses. Forms hypotheses, designs
  falsifying tests, eliminates candidates systematically, and logs the full
  investigation trail in a structured debug/ folder.
  TRIGGER when: user has a bug to investigate scientifically; user wants systematic
  root-cause analysis; user says "debug", "investigate", "root cause", "why is this
  failing"; user invokes /autoresearch:debug.
  DO NOT TRIGGER when: user wants to optimize a metric (use /autoresearch); user
  wants to fix a known error automatically (use /autoresearch:fix); user just wants
  a quick one-line answer about what a function does.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
---

# autoresearch:debug — Scientific Bug Investigation

Root-cause analysis using the scientific method: form falsifiable hypotheses, design tests that could disprove them, eliminate candidates, and converge on confirmed root causes. Every step is logged — nothing is assumed, nothing is skipped.

## Core Principle

**A hypothesis is only useful if it can be falsified.** "Something is wrong" is not a hypothesis. "The cache is returning stale data because the TTL is not being reset on write" is a hypothesis — it can be tested and disproved.

## Output Structure

Create `debug/` in the working directory (or alongside the failing artifact):

| File | Purpose |
|------|---------|
| `debug/hypotheses.md` | Active candidates under investigation |
| `debug/eliminated.md` | Ruled-out hypotheses with proof of elimination |
| `debug/findings.md` | Confirmed root causes with reproduction case |

Initialize all three files before the first iteration.

---

## Investigation Loop

Repeat until stop condition:

```
[Observe] --> [Hypothesize] --> [Design Test] --> [Run Test] --> [Update] --> [Log]
     ^                                                                          |
     |__________________________________________________________________________|
```

### Stage 1 — Observe

Collect all available evidence before forming any hypothesis:

- Read error messages, stack traces, logs — verbatim, not paraphrased
- Identify: What is the symptom? When does it appear? When does it NOT appear?
- Identify: What changed recently? (git log, config changes, dependency updates)
- Identify: Is the bug deterministic or intermittent?

Write a symptom summary at the top of `debug/findings.md`:
```
## Symptom
[Exact error message or behavior]

## Observed conditions
- Occurs: [when/where]
- Does NOT occur: [contrasting case if known]
- First observed: [commit/date/event]
```

### Stage 2 — Hypothesize

Form at least 2 candidate hypotheses before testing any of them. More candidates = less confirmation bias.

**Hypothesis format:**
```
H-N: [X] causes [Y] because [Z].
  Test: [specific action that would disprove this if false]
  Confidence: low | medium | high
```

Example:
```
H-1: The database connection pool is exhausted because max_connections is set too low.
  Test: Print active connection count during the failure window. If count < max_connections, this hypothesis is false.
  Confidence: medium

H-2: The timeout is triggered by a slow DNS lookup, not the actual request.
  Test: Replace hostname with IP address in the connection string. If bug disappears, H-2 is confirmed.
  Confidence: low
```

Write all active hypotheses to `debug/hypotheses.md`.

**Prioritization rule:** Test high-confidence, low-cost hypotheses first. A cheap test that eliminates a hypothesis is more valuable than an expensive test that confirms one.

### Stage 3 — Design Falsifying Test

For each hypothesis under test, design the minimal experiment that could disprove it.

Ask: "If this hypothesis is FALSE, what would I observe?"

Design the test to produce that observable. If the test does NOT produce the falsifying observation, the hypothesis survives (not confirmed — survives).

**Good test design:**
- Changes exactly one variable
- Has a clear pass/fail criterion defined BEFORE running
- Can be run in under 5 minutes
- Leaves the system in the same state it started (reversible)

### Stage 4 — Run Test

Execute the test. Record:
- Exact command(s) run
- Exact output (stdout, stderr, exit code)
- Whether the falsifying observation was produced

Do not interpret yet. Record what happened, literally.

### Stage 5 — Update Hypothesis Set

**If the test produced the falsifying observation:**
- The hypothesis is eliminated
- Move it from `debug/hypotheses.md` to `debug/eliminated.md`
- Record why: "H-1 eliminated: connection count was 3/100 during failure — pool exhaustion is not the cause"

**If the test did NOT produce the falsifying observation:**
- The hypothesis survives
- Increase its confidence level
- Narrow its scope: "H-2 now more specifically: slow DNS on IPv6 lookups only"

**If the test produced unexpected output:**
- Add a new hypothesis to explain the unexpected result
- Do not discard it — unexpected observations are often the path to the root cause

### Stage 6 — Log

After each iteration, update all three files:

`debug/hypotheses.md` — current active candidates (sorted by confidence, high first)
`debug/eliminated.md` — append the eliminated hypothesis with proof
`debug/findings.md` — append iteration summary

Then immediately begin Stage 1 of the next iteration.

---

## Stop Conditions

**Success:** Root cause confirmed — stop when ALL of these are true:
1. At least one hypothesis has been confirmed (not just survived — confirmed by a positive test)
2. A minimal reproduction case exists: the smallest code/config/command that triggers the bug
3. The fix has been identified (even if not yet implemented)

Write confirmed root cause to `debug/findings.md`:
```
## Root Cause (Confirmed)
[Hypothesis text]

## Evidence
[Test that confirmed it]

## Reproduction case
[Minimal steps/code to reproduce]

## Proposed fix
[What needs to change]

## Next step
Run `/autoresearch:fix` to implement and verify the fix iteratively.
```

**Budget exhausted:** If `max_iterations` is reached without confirmation, write a partial findings report with the strongest surviving hypothesis and the evidence collected so far.

---

## Stuck Protocol

**If more than 3 iterations pass without eliminating any hypothesis:**

Do not continue making minor variations. Switch observation technique entirely.

Available technique changes (see `investigation-techniques.md` for details):

1. Currently using log analysis → switch to **bisect** (binary search over commits)
2. Currently using bisect → switch to **minimal reproduction** (shrink the failing case)
3. Currently using code reading → switch to **instrumentation** (add logging/metrics)
4. Currently using instrumentation → switch to **differential diagnosis** (compare working vs broken)
5. Currently using one environment → switch to **strace/dtrace** (system-call level)

Log the technique switch:
```
## TECHNIQUE SWITCH — Iteration N
- Previous technique: [name]
- Reason: 3 iterations, 0 hypotheses eliminated
- New technique: [name]
- Rationale: [why this technique is more likely to produce new evidence]
```

---

## Autonomy Directive

Once the investigation begins:

1. **Do not stop to ask permission.** Form hypotheses and run tests autonomously.
2. **Do not summarize and wait.** After logging an iteration, begin the next one.
3. **Do not declare "root cause" without positive confirmation.** Surviving a test is not confirmation.
4. **Do not skip the log step.** Every iteration must update all three files.

The only valid stops are: root cause confirmed, or budget exhausted.

---

## Initial Setup

When `/autoresearch:debug` is invoked:

1. Ask: "What is the bug? Paste the error message or describe the failing behavior."
2. Ask: "What is the last known good state? (last commit that worked, last config that worked)"
3. Ask: "How many investigation iterations should I run before stopping? (default: 15)"
4. Create `debug/` directory and initialize the three files.
5. Begin Stage 1 — Observe.

Do not ask more questions after setup. The investigation is autonomous from Stage 1 onward.
