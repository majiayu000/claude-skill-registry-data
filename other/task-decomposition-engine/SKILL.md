---
name: task-decomposition-engine
description: >
  ROOT ORCHESTRATOR — the main() of CodeHands. Activates on EVERY task.
  Classifies the request, assesses complexity, gates non-trivial work
  through mandatory decomposition, selects the correct skill chain,
  and tracks execution state. This is the single entry point that makes
  the CodeHands lifecycle mandatory, not advisory.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "any new task or request"
  - context: "session start"
  - context: "user gives a new instruction"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies: []
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
    entry_phrasing: "Before we start, let me understand what we're working with."
  gemini:
    enforcement_style: "structured-checklist"
    entry_phrasing: "INTAKE: ☐ Classify ☐ Assess complexity ☐ Reconnoiter ☐ Decompose ☐ Route"
  gpt:
    enforcement_style: "directive-imperative"
    entry_phrasing: "You MUST classify and assess every request before writing any code."
author: codehands-core
signed: true
tier: 0
priority: 0
---

## Overview

This is the base workflow — the spine of CodeHands. Every request passes through this engine FIRST. It classifies the work, assesses risk and complexity, decides whether decomposition is needed, and routes to the correct skill chain. Without this engine, skills are advisory. With it, the lifecycle is mandatory.

## When to Use

- **ALWAYS.** This skill activates on every new task, every session start, every user instruction that requires action. There are no exceptions.
- If you are about to write code and you haven't passed through this engine, STOP.

## Process

### Phase 0: Session State Recovery

Before anything else, check if this is a continuation:

```
1. Does docs/plans/*.md exist with IN PROGRESS tasks?
   → YES: Load the plan, show progress summary, resume from next pending task
   → NO: Continue to Phase 1

2. Does .codehands/session-state.md exist?
   → YES: Read it. It contains decisions and context from the last session.
   → NO: Fresh start. Continue to Phase 1.
```

If resuming, skip directly to the executing-plans skill with loaded state.

### Phase 1: Request Classification

Classify every incoming request into exactly ONE category:

| Category | Examples | Lifecycle Path |
|---|---|---|
| **Question** | "How does X work?", "Where is Y?" | Answer directly. No lifecycle needed. |
| **Trivial Fix** | "Fix this typo", "Add a log line", "Update this string" | FAST PATH → implement directly with TDD |
| **Bug Fix** | "X is broken", "Y returns wrong value" | DEBUG PATH → systematic-debugging → TDD fix |
| **Feature** | "Build X", "Add Y", "Create Z" | FULL PATH → Define → Plan → Build → Verify → Review → Ship |
| **Refactor** | "Clean up X", "Simplify Y", "Split Z" | REFACTOR PATH → source-driven → simplify → TDD → verify |
| **Investigation** | "Why is X slow?", "Audit Y for security" | INVESTIGATE PATH → reconnaissance → targeted analysis |
| **Configuration** | "Set up CI", "Configure linting" | CONFIG PATH → targeted skill (ci-cd, etc.) |

**Classification rules:**
- When in doubt, classify UP (Feature over Trivial, Bug over Trivial)
- If the user says "quick" or "just" → still classify honestly. "Just add auth" is a Feature, not Trivial.
- Multi-part requests → classify each part independently

### Phase 2: Complexity Assessment

For non-trivial work, assess complexity on three dimensions:

```markdown
## Complexity Assessment
- **Scope:** [Isolated | Cross-cutting | System-wide]
  How many files/modules will this change touch?

- **Risk:** [Low | Medium | High | Critical]
  Does it touch: auth? payments? data? infrastructure? production config?

- **Uncertainty:** [Clear | Some unknowns | Mostly unknown]
  Do we understand the requirements and the codebase well enough?
```

| Scope + Risk | Action |
|---|---|
| Isolated + Low | May proceed with minimal planning |
| Cross-cutting OR Medium risk | Mandatory planning phase |
| System-wide OR High/Critical risk | Mandatory spec + plan + security review |
| High uncertainty on any axis | Mandatory reconnaissance (Phase 3) before planning |

### Phase 3: Codebase Reconnaissance

> **Only skip this if you've already reconnoitered this codebase in this session.**

Before planning or implementing, understand what you're working with:

```
1. Language & Framework: What language? What framework? What version?
2. Project Structure:    Where does code live? What's the module pattern?
3. Test Infrastructure:  Does it have tests? What framework? Where are they?
4. Build System:         How to build? How to run? How to test?
5. Existing Patterns:    Error handling style? Naming conventions? Import style?
6. CI/CD:                Is there a pipeline? What does it run?
7. Dependencies:         Package manager? Lock file present? Last audit?
```

Cache results in `.codehands/session-state.md` (template in `templates.md`).
For deep analysis, invoke `codehands:codebase-reconnaissance`.

### Phase 4: Decomposition Gate

Based on classification and complexity:

| Path | Decomposition Required? | Skills Activated |
|---|---|---|
| **Question** | ❌ No | Answer directly |
| **Trivial Fix** | ❌ No | TDD → verify |
| **Bug Fix** | ⚠️ Lightweight | systematic-debugging → TDD (Prove-It) |
| **Feature (isolated, low risk)** | ✅ Yes (lightweight) | brainstorming (optional) → plan → TDD → verify |
| **Feature (cross-cutting or risky)** | ✅ Yes (full) | brainstorming → spec → plan → build → verify → review |
| **Refactor** | ✅ Yes (lightweight) | source-driven → plan → simplification → verify |
| **Investigation** | ❌ No | Targeted analysis → report to user |
| **Configuration** | ⚠️ Lightweight | Targeted skill → verify |

For tasks requiring decomposition, invoke `codehands:planning-and-task-breakdown` before any implementation.

### Phase 5: Skill Chain Assembly

Assemble the skill chain for this task based on classification. Pre-built chains are in `templates.md`. Present the chain to the user:

> "This looks like a **[classification]** with **[risk level]**. I recommend: [skill chain summary]. Want to proceed or adjust?"

### Phase 6: Progress Journaling

Maintain `.codehands/session-state.md` throughout execution (template in `templates.md`). Record: request, classification, decisions, progress, discoveries, and next-session instructions. This provides session continuity, decision audit trail, and user visibility.

## Fast Paths

- **Trivial Fix:** Classify → test → fix → verify → commit (~30s overhead)
- **Bug Fix:** Classify → reproduce with test → root cause → fix → verify → commit
- **Question:** Classify → answer directly (no lifecycle)

Detailed skill chains for each path are in `templates.md`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know what this needs, I don't need to classify it" | Classification takes 10 seconds. Misclassifying a Feature as Trivial costs hours when you discover it's bigger than expected halfway through. |
| "The user wants code NOW, not a classification exercise" | The classification is invisible to the user — it happens in your head in seconds. The user sees better results, not more process. |
| "This is obviously trivial" | "Obviously trivial" is the leading cause of scope explosions. If it touches more than 1 file or has any risk, it's not trivial. |
| "I don't need to journal, I'll remember" | You won't. Context windows reset. Sessions end. Journaling takes 30 seconds and provides infinite recall. |
| "Reconnaissance is overhead for a project I already know" | You don't already know it — you read it earlier in a context window that may have been truncated. Verify, don't assume. |

## Red Flags

- Code written without passing through classification
- Feature-sized work treated as "trivial fix"
- No session state file for multi-task work
- Skipping reconnaissance on an unfamiliar codebase
- No skill chain assembled before starting work
- "Just" or "quickly" used to justify skipping decomposition

## Verification

- [ ] Request classified into exactly one category
- [ ] Complexity assessed (scope, risk, uncertainty) for non-trivial work
- [ ] Codebase reconnoitered if unfamiliar or uncertain
- [ ] Decomposition gate applied (plan required or fast path justified)
- [ ] Skill chain assembled and presented to user (for non-trivial)
- [ ] Session state journaled for multi-task work

## See Also

- `codehands:codebase-reconnaissance` — Deep codebase analysis
- `codehands:planning-and-task-breakdown` — Task decomposition (invoked by this engine)
- `codehands:executing-plans` — Plan execution (invoked by this engine)
- `codehands:using-codehands` — Framework overview
