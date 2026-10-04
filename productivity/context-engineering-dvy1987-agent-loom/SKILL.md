---
name: context-engineering
description: >
  Build the smallest, highest-signal context package for an AI coding task —
  goal, constraints, repo facts, boundaries, and a verification plan. Load when
  prompts are underspecified, the agent is missing key files or decisions, the
  user says "use the right context", "here's the repo", or when work is drifting
  due to missing constraints. Also triggers on "context engineering", "gather
  context", "what do you need from me", "before you start". Not for cross-session
  continuity (use memory-startup/memory-recall).
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  sources: addyosmani/agent-skills context-engineering (11/12, 2026-05-29), safishamsi/graphify (corpus gates, 11/12)
  resources:
    references:
      - examples.md
---

# Context Engineering

You construct a **minimal, task-relevant** context bundle that prevents rework. You do not "load everything"; you load the smallest set of facts that make the next step safe.

## Hard Rules

- Prefer **repo evidence** over guesses (read files, don’t assume).
- Context must be **purpose-driven**: every included item must support the goal, constraints, or verification.
- Separate **facts** from **assumptions**. Assumptions must be confirmable or safely reversible.
- Never mix cross-session memory with task context. Use `memory-startup`/`memory-recall` for that.
- If the task is blocked by missing context, ask **one** targeted question, not a questionnaire.

---

## Workflow

### Step 1 — State the task in one sentence

Write:

```markdown
TASK: [one sentence]
```

### Step 2 — Capture constraints and boundaries (5 bullets max)

Include items like:
- Must not change: [APIs, files, behavior]
- Must preserve: [compat, performance, security, UX]
- Time/size constraints: [small PR, no new deps, etc.]
- Out of scope: [explicitly]

### Step 3 — Choose a context tier

Pick the smallest tier that makes progress safe:

- **Tier A (micro)**: 1–3 files + reproduction steps (tiny fix)
- **Tier B (feature)**: spec/ACs + touched modules + tests (new feature / refactor)
- **Tier C (system)**: architecture + invariants + interfaces + rollout (cross-cutting change)

### Step 4 — Collect the minimum evidence

**Corpus gate (Tier B/C):** If the repo has >500 scannable files or the task touches >20 paths, narrow scope to the smallest subdirectory that contains the change before loading files.

Collect only what the tier requires:

- **Graph facts** (if `docs/knowledge-graph/graph.json` exists): query 1-hop neighbors of touched modules via `query_graph.py`
- **Repo facts**: stack + relevant configs (package manager, build/test commands)
- **Locality**: entry file(s) for the change, plus direct callers
- **Contracts**: API surface, types/schemas, acceptance criteria
- **Verification**: how we’ll prove correctness (tests, manual steps, metrics)

### Step 5 — Produce the context bundle (copy/pasteable)

Use this template:

```markdown
## Context bundle — [task slug]

Goal:
- ...

Constraints:
- ...

Repo facts (evidence):
- [fact] (from [file])

Key files:
- [path] — why relevant

Interfaces/contracts:
- ...

Assumptions (confirm or safe defaults):
- ...

Verification plan:
- [ ] ...
```

### Step 6 — Execute with context discipline

While implementing, keep a short “context ledger”:
- If you discover a new constraint, add it and restate the plan.
- If you need another file, state why (what question it answers), then fetch it.

---

## Gotchas

- “More context” often makes answers worse; irrelevant files dilute signal.
- If you don’t name constraints, you’ll violate them accidentally.
- Missing a verification plan leads to “looks good” shipping.
- Context for AI coding is **task-scoped**, not session-scoped — don’t conflate with memory.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Let’s just start coding and adjust later" | Unstated constraints cause large rewrites. Spend 2 minutes on a context bundle first. |
| "We should load the whole repo to be safe" | Noise increases mistakes; load only what answers the next question. |
| "I already understand the codebase" | The agent doesn’t — state the evidence and key files explicitly. |
| "Verification can wait until the end" | Without an upfront plan you’ll miss the easiest test hooks. |
| "This is just a small change" | Small changes still break contracts; Tier A context is cheap and prevents regressions. |

---

## Output Format

```markdown
## Context engineering — [task]

Tier: [A/B/C]
Context bundle: [included items]
Open questions: [0–2]
Next action: [exact next step]
```

---

## Examples

<examples>
  <example>
    <input>“Fix failing tests in CI.”</input>
    <output>
Tier A. Collect: failing command, CI logs, the test file, and the code under test. Add constraints: no snapshot regen unless approved. Verification: `npm test` locally and CI rerun.
    </output>
  </example>
</examples>

---

## Verification

- [ ] Task statement + constraints written before implementation starts
- [ ] Every included context item supports goal/constraints/verification
- [ ] Assumptions explicitly listed and confirmable or safely reversible
- [ ] Verification plan is stated upfront (tests/manual/metrics)
- [ ] Context stays minimal (no repo-wide dumps without a reason)

---

## Red Flags

- Context gathered by guessing instead of repo evidence
- Irrelevant files included that dilute the task signal
- Constraints unnamed so violations go unnoticed
- Assumptions presented as facts without confirmation path

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Task: [slug] | Tier: [A/B/C]
Key files: N | Assumptions: N | Verification items: N
Open questions: N
```
