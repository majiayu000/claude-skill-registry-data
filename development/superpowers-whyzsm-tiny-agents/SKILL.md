---
name: superpowers
description: >
  Spec-first, TDD, subagent-driven software development workflow. Use when:
  (1) building any new feature or app — triggers brainstorm → plan → subagent execution loop,
  (2) debugging a bug or test failure — triggers systematic root-cause process,
  (3) user says "let's build", "help me plan", "I want to add X", or "this is broken",
  (4) completing a feature branch — triggers test verification + merge/PR options.
  NOT for: one-liner fixes (just edit), reading code, or non-code tasks.
  Requires exec tool and sessions_spawn.
---

# Superpowers — OpenClaw Edition

Adapted from [obra/superpowers](https://github.com/obra/superpowers). Mandatory workflow — not suggestions.

## The Pipeline

```
Idea → Brainstorm → Plan → Subagent-Driven Build (TDD) → Code Review → Finish Branch
```

Every coding task follows this pipeline. "Too simple to need a design" is always wrong.

---

## Phase 1: Brainstorming

**Trigger:** User wants to build something. Activate before touching any code.

**See:** [references/brainstorming.md](references/brainstorming.md)

**Summary:**
1. Explore project context (files, docs, recent commits)
2. Ask clarifying questions — **one at a time**, prefer multiple choice
3. Propose 2–3 approaches with trade-offs + recommendation
4. Present design in sections, get approval after each
5. Write design doc → `docs/plans/YYYY-MM-DD-<topic>-design.md` → commit
6. Hand off to **Phase 2: Writing Plans**

**HARD GATE:** Do NOT write any code until user approves design.

---

## Phase 2: Writing Plans

**Trigger:** Design approved. Activated by brainstorming phase.

**See:** [references/writing-plans.md](references/writing-plans.md)

**Summary:**
- Write a detailed task-by-task implementation plan
- Each task = 2–5 minutes: write test → watch fail → implement → watch pass → commit
- Save to `docs/plans/YYYY-MM-DD-<feature>.md`
- Announce: `"I'm using the writing-plans skill to create the implementation plan."`
- After saving, offer two execution modes:
  - **Subagent-driven (current session):** `sessions_spawn` per task + two-stage review
  - **Manual execution:** User runs tasks themselves

---

## Phase 3: Subagent-Driven Development

**Trigger:** Plan exists, user chooses subagent-driven execution.

**See:** [references/subagent-development.md](references/subagent-development.md)

**Per-task loop (OpenClaw):**
1. `sessions_spawn` an implementer subagent with task + full plan context
2. Wait for completion announcement
3. `sessions_spawn` a spec-reviewer subagent → must confirm code matches spec
4. `sessions_spawn` a code-quality reviewer subagent → must approve quality
5. Fix any issues, re-review if needed
6. Mark task done, move to next
7. Final: dispatch overall code reviewer → hand off to Phase 5

**TDD is mandatory in every task.** See [references/tdd.md](references/tdd.md).

---

## Phase 4: Systematic Debugging

**Trigger:** Bug, test failure, unexpected behaviour — any technical issue.

**See:** [references/systematic-debugging.md](references/systematic-debugging.md)

**HARD GATE:** No fixes without root cause investigation first.

**Four phases:**
1. Root Cause Investigation (read errors, reproduce, check recent changes, trace data flow)
2. Pattern Analysis (find working examples, compare, identify differences)
3. Hypothesis + Testing (one hypothesis at a time, test to prove/disprove)
4. Fix + Verification (fix at root, not symptom; verify fix doesn't break anything)

---

## Phase 5: Finishing a Branch

**Trigger:** All tasks complete, all tests pass.

**See:** [references/finishing-branch.md](references/finishing-branch.md)

**Summary:**
1. Verify all tests pass
2. Determine base branch
3. Present 4 options: merge locally / push + PR / keep / discard
4. Execute choice
5. Clean up

---

## OpenClaw Subagent Dispatch Pattern

When dispatching implementer or reviewer subagents, use `sessions_spawn`:

```
Goal: [one sentence]
Context: [why it matters, which plan file]
Files: [exact paths]
Constraints: [what NOT to do — no scope creep, TDD only]
Verify: [how to confirm success — tests pass, specific command]
Task text: [paste full task from plan]
```

Run `sessions_spawn` with the task as a detailed prompt. The sub-agent announces results automatically.

---

## Key Principles

- **One question at a time** during brainstorm
- **TDD always** — write failing test first, delete code written before tests
- **YAGNI** — remove unnecessary features from all designs
- **DRY** — no duplication
- **Systematic over ad-hoc** — follow the process especially under time pressure
- **Evidence over claims** — verify before declaring success
- **Frequent commits** — after each green test
