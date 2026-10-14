---
name: grilling-skill
description: >-
  Relentless interview to stress-test a plan or design — one question at a time
  with a recommended answer. Modes: grill (default), 'grill with docs' (inline
  CONTEXT.md glossary + ADRs), --plan (emit PLANS/PLAN-GIT-<issue>.md in the
  canonical phased contract). Triggers: grill, grill me, grill with docs,
  stress-test my plan.
license: Apache-2.0
compatibility: opencode
category: Planning & Alignment
---

## What I do

I relentlessly interview the user about a plan or design until we reach a shared understanding:

1. **Decision-tree walk**: Walk down each branch of the design tree, resolving dependencies between decisions one-by-one
2. **One question at a time**: Never ask multiple questions at once — that is bewildering
3. **Recommended answer**: For each question, provide my recommended answer so the user can accept or correct
4. **Codebase-first**: If a question can be answered by exploring the codebase, explore it instead of asking
5. **Shared understanding**: Continue until every branch of the decision tree is resolved

## Modes

**This Modes section supersedes any other session-shape framing elsewhere in this document.** Pick the mode from the user's phrasing:

| Invocation | Behavior |
|------------|----------|
| `grill` / `grill me` / `stress-test this plan` (default) | Interview only — no files written |
| `grill with docs` / `grill me and write it up` / `--docs` | Interview **plus** inline capture: `CONTEXT.md` glossary entries and ADRs, written as decisions crystallise (see §Doc capture) |
| `grill --plan` | Interview, then **emit** `PLANS/PLAN-GIT-{issue}.md` in the canonical phased contract (see §PLAN emission) |

## When to use me

Use this skill when:
- A plan, spec, or design needs stress-testing before implementation begins
- The user uses any "grill" trigger phrase
- You want the alignment session to also produce durable docs (`--docs`) or a checkable plan (`--plan`)
- Ambiguity in requirements is causing misalignment between user and agent

## Core Workflow

### Step 1: Frame the session

State what we're grilling about in one sentence, then begin immediately. Do not ask the user "what do you want to be grilled on?" if it's already clear from context.

### Step 2: Walk the decision tree

For each unresolved branch of the design:

1. **Identify the next dependency** — the decision that unblocks the most other decisions. Start with the highest-leverage unknowns.
2. **Formulate a single question** — one question, phrased so a concrete answer resolves the branch.
3. **Provide your recommended answer** — give your best recommendation with one-line rationale, so the user can say "yes" or correct you.
4. **Wait for feedback** — do NOT proceed until the user answers. Asking multiple questions at once is the primary failure mode of this skill.

### Step 3: Resolve via codebase, not questioning

Before asking any question, check: **can I answer this myself by reading the code or project docs?**

| Situation | Action |
|-----------|--------|
| Code clearly answers it | Read it and state the answer, don't ask |
| Code contradicts the user's claim | Surface the contradiction: "Your code does X, but you said Y — which is right?" |
| Genuinely a user-only decision | Ask the question |
| Documented in `CONTEXT.md`, README, or ADRs | Read it, don't ask |

### Step 4: Continue until convergence

Keep walking the tree until either:
- Every branch is resolved (success)
- The user signals they want to start building (respect this — don't grill past their appetite)
- Remaining unknowns are genuinely unresolvable until implementation begins (note them explicitly and move on)

## Doc capture (`--docs` mode)

Self-contained capture convention — runs interleaved with the interview, not after it:

- **Capture inline, not in a batch.** Write `CONTEXT.md` entries and ADRs the moment a term or decision crystallises.
- **CONTEXT.md is a glossary and nothing else.** Totally devoid of implementation details.

Format — one entry per resolved term:

```md
**Term**: One or two sentences defining what it IS, not what it does.
_Avoid_: alias, other-alias
```

Rules: be opinionated (pick the best word, list the rest under `_Avoid_`); only project-specific terms (general programming concepts don't belong); group under subheadings when natural clusters emerge.

**ADRs — the three-criteria gate.** Offer an ADR only when **all three** are true:
1. **Hard to reverse** — changing your mind later costs meaningfully
2. **Surprising without context** — a future reader will wonder "why this way?"
3. **The result of a real trade-off** — genuine alternatives existed and one was picked for specific reasons

If any of the three is missing, skip the ADR. Most sessions create zero ADRs, and that's correct.

ADR format: `docs/adr/NNNN-slug.md`, sequential numbering (scan for the highest existing number, increment; create the directory lazily). One to three sentences: context, decision, why. Optional Status/Considered/Consequences sections only when they add genuine value.

Conclude `--docs` sessions with a summary: terms added/changed, ADRs created (if any), remaining open questions.

## PLAN emission (`--plan` mode)

After convergence, emit `PLANS/PLAN-GIT-{issue}.md` (or `PLANS/PLAN-{KEY}.md` for non-GitHub keys) in the canonical contract `plan-execution-skill` parses (`--soft`/`--gate`):

```markdown
# PLAN: <title>

**Branch**: feat/<KEY>
**Issue**: <ticket URL>
**Base**: <base>

## Acceptance Criteria
- [ ] <checkable criteria>

## Dependency & Consumer Map

| Node (file/module) | Depends on (must precede) | Consumers (who depends on this) | Change risk |
|---------------------|---------------------------|---------------------------------|-------------|

## Trace

_Append-only run-level events, newest last, never rewritten — `GATE <short-sha> tier=… lint=… …` (format per `verification-loop-skill` §Gate memo) · `LOG <phase> <reason>` · `SKIP <N.M> <reason>`._

## Implementation Phases

### Phase 1: <name>
- [ ] **N.M** <single atomic action — verb + target + outcome>
    — **Why:** <what this unblocks / why it must precede others>
    — **Done when:** <objective, checkable completion signal>
    — **Consumers affected:** <who depends on this; none if N/A>
```

Contract rules: phases parse on `^### Phase`; steps parse on `- [ ] **N.M**` with completion `- [x]`; every step carries the full rationale triple (`Why` / `Done when` / `Consumers affected`) — a step missing any field is malformed; executors read `## Dependency & Consumer Map` before executing, so author it honestly. `## Trace` is the append-only run-level audit trail — executors append GATE memos, LOG lines (full-gate escalation reasons, fix-on-fail attempts), and SKIP/deviation lines there, newest last, and never rewrite it; per-step `— Done:` lines stay with their steps.

## Rules

- **One question at a time.** This is the non-negotiable rule. A wall of questions overwhelms the user and breaks the feedback loop.
- **Always recommend.** A bare question forces the user to do all the thinking. Lead with your recommendation.
- **Never invent answers for user-only decisions.** If it's a product, scope, or preference call, ask — don't assume.
- **Respect the stop signal.** When the user says "that's enough" or "let's build," stop grilling immediately.
- **Don't repeat resolved questions.** Track what's been answered; re-asking signals you weren't listening.

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `ticketing-skill` / `worktree-pipeline-skill` | A grilled, resolved outcome feeds into ticket creation, then the branch+PLAN+execute pipeline |
| `wayfinder-skill` | An oversized grilled plan maps onto decision tickets |
| `civiltekk-context-optimization-skill` | A resolved grilling session can be compacted into a decision summary |

## Example Usage

### Plain grilling session

```
"Grill me about how we should structure the notifications module"
```

The skill will:
1. Frame the session: "We're designing the notifications module structure."
2. Ask one question with a recommendation: "First — should notifications be push, pull, or hybrid? I recommend hybrid (push for real-time, a polling fallback for missed events) — agree?"
3. Wait for the answer, then proceed to the next branch.
4. Continue until the decision tree is resolved.

### With docs and plan output

```
"Grill with docs, then --plan — we're adding a notifications module"
```

Interview as above; as terms resolve ("notification" vs "alert" vs "digest"), update `CONTEXT.md` inline; if a hard-to-reverse decision emerges (message bus, not polling), offer an ADR; on convergence, emit `PLANS/PLAN-GIT-<issue>.md` with the resolved decisions as phased atomic steps.
