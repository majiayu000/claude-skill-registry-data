---
name: blind-spots
description: Surface consequential decisions a plan, design, or research brief left silently assumed, by interviewing the user in dependency order. Use when the user says "blind spots", "grill me", "stress-test this plan", "poke holes in this", "what am I missing", "interrogate this design", "what haven't I decided", or needs a loose idea or research brief clarified before work begins. Do NOT use for a clear factual lookup, to explain a previous reply in more detail (use `huh`), to generate ideas when it is unclear what to build (use `ideation`), or to review an already-written plan with agents (use `review-plan`).
argument-hint: '[plan, design, idea, or research brief to probe; blank = take it from the conversation]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Blind Spots

Find the decisions the user does not know they have left open, then get each one made.

A plan or research brief can feel complete because its gaps were filled in silently.
Make those decisions visible before they steer implementation or research.

## Instructions

### 1. Resolve the target

The argument is what to probe. If blank, take it from the conversation. If no target
is in play, ask for one sentence on what they want to build, understand, or decide.

### 2. Recon before asking anything

An uninformed question wastes a round and spends the user's patience. Before round one,
read the available context: the conversation and relevant supplied documents; for repo
work, the source, `AGENTS.md` / `CLAUDE.md`, and relevant `docs/`. Reuse recon and settled
decisions supplied by a calling workflow. For an unfamiliar topic, a short direct lookup
can establish the terminology or options needed to ask useful questions.

**Finding facts is your job, never the user's.** Anything discoverable from the
filesystem, the git history, or a tool is yours to look up. Ask the user only for
*decisions*. Open empirical questions remain research tasks; the user need not settle
them before research begins. For example, ask whether offline use is required, then
research which candidates support it.

### 3. Build the decision tree, then prune it

**First, check the target is one piece of work.** A brief describing several
independent subsystems needs splitting before it needs questions — refining the
details of something that should be three projects spends a round on the wrong
thing. Say so, propose the split and the order, and probe only the first piece.

Then map the work as decisions, each branching into the decisions that hang off it.
Sweep the categories below rather than working from intuition — a whole category is
easier to miss than a question inside one:

- **Building something** — purpose, constraints, success criteria; then the shape:
  component boundaries and interfaces, where state lives and how data moves, failure
  behaviour, and what counts as tested.
- **Researching something** — purpose, population, region, timeframe, and the outcome
  being compared. A request to learn about a topic need not serve an adoption decision.

Most categories come back already settled, by the context or by a default nobody
would argue with. The sweep exists to catch the ones that do not.

Pruning is what separates a useful round from an interrogation:

- **Keep** a decision that changes the work — different answers lead to different
  structure, interfaces, candidate pools, evidence to gather, or success criteria.
- **Cut** scope the brief carries that its stated purpose does not require, and ask
  whether it is wanted instead of designing around it. Unrequested scope is a fork
  the user cannot see, and the cheapest one to close.
- **Drop** a decision that is cheap to reverse and constrains nothing downstream.
  Naming, log wording, which of two equivalent helpers to use: decide those yourself
  during the work.

An unspecified detail is not automatically a blind spot. A fork the user cannot see is.

### 4. Ask the frontier

The **frontier** is every kept decision whose prerequisites are already settled — the
questions answerable *now* without guessing at answers you have not heard yet.

Ask the whole frontier in one message, ordered by consequence, then **stop and wait**.

```
❓ **Q1 — <short title>**: <the question, with the options if it is a choice>

➡️ <recommended answer, and the reason in a clause>

---

❓ **Q2 — <short title>**: …

➡️ …
```

Rules for a round:

- **Every question carries your recommendation.** "Go with your defaults" must be a
  complete answer — the user may be tired, or may simply trust you on that branch.
- **An asked question stays pending until the user answers or explicitly delegates
  the choice.** Silence, elapsed time, an empty tool result, and a preselected
  recommendation settle nothing. An asynchronous prompt returning only confirms
  delivery; wait for the user's reply. Continue independent read-only work while
  waiting, then yield if none remains. These are required decisions, not optional
  preferences that may fall back to defaults on timeout.
- **A question whose answer depends on another open question belongs to a later
  round**, not this one. This is the whole mechanism: question 12 does not exist as a
  question until question 4 is answered.
- **More than about seven questions means the tree is split too fine.** Re-prune per
  step 3 rather than sending a wall.
- Never block on a lookup. A running exploration is an unsettled prerequisite, so only
  the questions downstream of it wait — ask the rest of the frontier now.
- Where the harness offers a structured choice prompt, use it for the discrete
  either/or questions and prose for the rest.

### 5. Recompute and repeat

Each set of answers settles decisions, pushing the frontier outward and unblocking
questions that depended on them. Recompute the frontier and ask the next round only
while consequential decisions remain open.

### 6. Close

Stop when every consequential decision is settled. Unknown facts may remain.

**When called by another workflow:** return a compact brief with the purpose, scope,
settled constraints and priorities, and remaining factual questions. If the context
already settles every decision, return immediately without an interview. The caller
owns any existing confirmation or approval step; do not add a separate closing
confirmation or hand off to another workflow.

**When invoked directly:** state the settled understanding back — the decisions and
their answers, compactly, in the user's own terms — and ask the user to confirm it
matches what they meant.

On confirmation, hand off rather than sprawling into implementation: `plan` for a
medium task, `longshot` if they are handing it over and leaving, a heavier planning
workflow for an architectural change. For a research brief, return it for the requested
research. Write the understanding to a file only if asked.

## Boundaries

- **Do not build during the interrogation.** No edits, no scaffolding, no mutating
  commands, no implementation subagents. Direct invocation awaits confirmation of the
  closing summary; embedded use follows the caller's existing approval requirements.
  Reading and searching are expected.
- Cap parallel lookups at **three read-only subagents**, one question each.
- Do not answer a decision on the user's behalf to shorten the session. Recommend, then
  wait.
- Do not re-ask a decision already settled, in this session or in the docs.

## Examples

### A loose feature idea

`blind-spots add team workspaces` — recon finds single-tenant auth and no authorization
layer. Round 1 asks the four forks that follow: does a user belong to many workspaces,
is existing data migrated or grandfathered, are invites by email or link, does billing
move to the workspace. Round 2 exists only because round 1 answered "many workspaces" —
role model and per-workspace permission checks are now answerable. Round 3 is empty.
The summary lists nine settled decisions, three of which the user had not realized were
open.

### A plan the user already wrote

`blind-spots` after pasting a migration plan — recon reads the current schema, so the
round asks only about forks the plan left implicit (backfill under load, rollback
window, dual-write duration), never about what the plan already states.

### A research brief

`research-general research home batteries` — context leaves the purpose unclear.
Ask whether the user wants an explanation or a purchase comparison, recommending an
overview if they are exploring. Only a purchase comparison opens questions about the
installation region and whether backup power or bill savings matters most. Prices and
available products remain research questions. Return the brief to `research-general`.

### A caller already settled the scope

`evaluate-tech` delegates research on export support for a named candidate with the
job and constraints supplied. Research that capability directly. A worker discovering
a scope blocker returns it to the caller; it does not start another interview.

## Troubleshooting

### The user answers "you decide" to everything

Take it at face value: record your recommendation as the decision and move on. If it
happens across a whole round, step 3's pruning was too loose — those were not forks.
Tighten it and shorten the next round.

### A question turns out to depend on an answer already given

It belonged to an earlier round and was missed. Drop it, apply the known answer, carry
on. Do not make the user repeat themselves.

### The frontier keeps growing and the session will not end

Each round should narrow. If it widens twice running, propose splitting the work
into bounded pieces and probe only the first piece.

### The user says a question is trivia

Believe them and drop it. It failed step 3's fork test.
