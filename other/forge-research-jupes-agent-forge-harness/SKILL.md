---
name: forge-research
description: Phase 1 of the Forge pipeline. Gather real context from the codebase, answer everything the code can answer through exploration, then grill the user one question at a time (with a recommended answer) for only what code cannot answer, and write a research document. Use when starting /forge-research or the research step of /forgemaster, or when the user wants a research-first investigation before planning a feature.
---

# forge-research

Phase 1 of 4 in the Forge pipeline (**research → plan → implement → ship**). The goal is a
`plans/research/<slug>.md` document grounded in real code, with every open question that the
codebase **cannot** answer resolved by the user.

**Hard rule:** never ask the user something the code, knowledge files, or git history can answer.
Explore first, ask last. See [[grill-me]] for the interview discipline this phase reuses.

## When to Use

- The user runs `/forge-research <feature>` or `/forgemaster` enters its research phase.
- A feature is described but the implementation surface, constraints, or decisions are unclear.
- The next useful step is reducing ambiguity, not coding or planning yet.

## Inputs

- Free-text feature description, a `bd show <id>` task, or a spec file path.
- Optional `<slug>` (kebab-case). If absent, derive one from the feature title and reuse it for
  every downstream phase artifact.

## Process

### 1. Establish the target

State the feature in one or two sentences. If it is already clear from context, do not ask the
user to restate it. Pick the `<slug>` now and announce it — all later phases key off it.

### 2. Explore what code can answer (mandatory, before any question)

Load knowledge first, then read real code. Be exhaustive enough to write accurate file paths.

```bash
cat knowledge/_shared.yaml
cat knowledge/repos/<repo>.yaml        # for each affected repo
bd show <id> 2>/dev/null               # if a task id was given
```

Then use Glob/Grep/Read (read-only) to map:

- Entry points and the data flow into the affected area.
- Existing code to **reuse** (hooks, types, components, utilities) — search before assuming new.
- Integration points: what this feature depends on, and what depends on it.
- Existing tests and how this area is currently verified.

Record each discovered fact. If exploration answers a question you were about to ask, **write the
answer down instead of asking it.**

### 3. Separate the unknowns

Sort every open item into two buckets:

- **Answerable by code/docs** → resolve it yourself now; cite the file/line.
- **Not answerable by code** → product intent, scope boundaries, UX choices, external systems,
  priorities, acceptance thresholds. These become user questions.

### 4. Grill the user — one question at a time

For each unanswerable item, ask **exactly one** question per turn, hardest-blocking branch first.
Every question carries a recommended answer and a one-line reason (the [[grill-me]] format):

```md
Shared understanding so far:
- Confirmed (from code): <fact + file:line>
- Open: <the gap this question closes>

Question:
<one question>

Recommended answer:
<your recommendation>

Why:
<brief rationale + consequence>
```

**Explain before you ask.** If the decision rests on a mechanism the user may not have in their
head — a tradeoff, how a tool behaves, or *why the code forces the choice* — open with one or two
plain-language sentences that explain what's going on and why it matters, **then** give the options.
A question the user can't parse wastes the turn (and the tokens). Lead with the "why", not the menu.
If the user says they don't understand, stop and explain the mechanism in plain terms before
re-asking.

Prefer `AskUserQuestion` when the choice is a small closed set. Stop asking when the remaining
uncertainty is explicitly accepted or the user says to proceed.

### 5. Write the research document

Write to `plans/research/<slug>.md` (create the folder if needed):

```markdown
# Research: <slug> — <feature title>
Generated: <date>
Repo: <repo>
Phase: research (1/4)

## Goal
<what the user wants and why, 2–3 sentences>

## What the Code Says (answered by exploration)
- <fact> — `path/to/file.ts:NN`
- Existing code to reuse: `...` — <how it helps>
- Integration points: <upstream / downstream>
- Current test coverage of this area: <summary>

## Decisions Resolved with the User
| Question | Decision | Rationale |
|----------|----------|-----------|
| <q> | <answer> | <why> |

## Constraints & Non-Goals
- Constraint: <...>
- Non-goal: <explicitly out of scope>

## Open Risks / Assumptions Carried Forward
- <risk or accepted assumption>

## Recommended Scope for Planning
<one paragraph: the shape of the feature the plan phase should design>
```

### 6. Hand off

Update the forge state and report:

```bash
bun run forge:phase-gate research --slug <slug> --write
```

Then tell the user: research is complete at `plans/research/<slug>.md`, and the next phase is
`/forge-plan <slug>` (or `/forgemaster` will offer to continue). Do **not** start planning in this
phase — planning is [[forge-plan]].

## Exit Criteria

- [ ] `plans/research/<slug>.md` exists with all sections filled.
- [ ] Every "Decisions Resolved" row came from the user, not guessed.
- [ ] No question was asked that the code already answered.
- [ ] Forge state advanced to `research` complete.
