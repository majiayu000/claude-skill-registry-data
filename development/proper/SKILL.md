---
name: proper
description: >
  Solve a request strategically and architecturally rather than tactically.
  Use when the user invokes /proper, asks for "the Proper™ way", wants the
  long-term design rather than the quickest fix, or wants to refactor /
  rearchitect first so the requested feature fits naturally. This skill
  diagnoses why the request feels awkward today, proposes a design change
  that makes the feature easy, and -- if the strategic path is non-trivial
  -- hands off to /mikado to execute it in safe incremental steps.
---

# The Proper™ Way

> "Make the change easy, then make the easy change." -- Kent Beck

When the user invokes `/proper`, they are explicitly opting **out** of the
quickest tactical fix and **in** to a strategic design pass. The goal is to
reshape the code first so the requested feature becomes a small, natural
follow-up.

## When to use this skill

- The user typed `/proper` (with or without arguments describing the ask).
- The user says things like "do this properly", "the Proper™ way",
  "solve this strategically", "architecturally", "do it right, not fast".
- A feature feels awkward to fit into the current code shape, and the user
  wants to step back before implementing it.

## What this skill is NOT

- **Not a license to refactor the world.** The strategic proposal must
  stay tied to the requested feature. Gold-plating is off-limits -- but
  if you spot adjacent smells with real leverage, **surface them and ask**
  whether to widen the scope. The user decides; never expand silently.
- **Not an autonomous implementation step.** The output is a diagnosis +
  proposal. The user decides whether to proceed, and non-trivial execution
  goes through `/mikado`.
- **Not a verdict.** Sometimes the tactical fix really is the right call;
  say so honestly when that's true.

## Process

### Step 1 -- Restate the immediate ask

Repeat the user's request back in one sentence. Confirm the surface-level
ask before stepping back. If `/proper` was invoked without an explicit
prompt, ask what the underlying request is.

### Step 2 -- Find the friction

Investigate the code as it exists today and answer:

- Where would the tactical fix go? (find the file/function)
- **Why isn't this feature already easy?** What design choice makes it
  awkward?

Common friction patterns to look for:

| Smell                 | What it looks like                                           |
| --------------------- | ------------------------------------------------------------ |
| Missing abstraction   | The feature requires touching N similar call sites           |
| Leaky boundary        | A module knows things it shouldn't, to make this work        |
| Conflated concerns    | One function would gain a second responsibility              |
| Hard-coded assumption | A value/behaviour is baked in that the feature needs to vary |
| Missing seam          | There is no clean place to plug new behaviour in             |
| Implicit contract     | Callers rely on side effects the new feature would break     |
| Wrong ownership       | The data or logic lives in the wrong layer for this feature  |

Name the friction explicitly. If there is no friction (the feature really
does fit cleanly with a small tactical change), **say so**. `/proper` is
not an excuse to invent refactorings.

### Step 3 -- Propose the strategic shape

Describe, in concrete terms, what the code would need to look like for the
requested feature to be a small, obvious change. Typical moves:

- **Introduce an abstraction** (interface, strategy, registry, adapter)
- **Extract a seam** (split a function, move a boundary, parameterise a
  hard-coded value)
- **Rename / regroup** so the new concept becomes first-class
- **Invert a dependency** so the new feature doesn't have to reach upward
- **Split a module** so the new concern has a natural home
- **Unify duplicated logic** so the feature only has to land in one place

Be specific: name files, types, functions. Sketch before/after when it
helps. Keep the scope tight -- the refactoring exists to serve _this_
feature, not to fix every smell you spotted along the way.

If you notice **adjacent smells** that would be much cheaper to fix while
you're already in this area (or that would compound the friction if left
alone), list them separately as _"Optional scope expansions"_ with a brief
cost/benefit, and ask whether to fold any in. Default to the minimum
scope; only widen if the user agrees.

### Step 4 -- Compare paths

Present a short, honest comparison so the user can decide with eyes open:

|                              | Tactical      | Strategic      |
| ---------------------------- | ------------- | -------------- |
| What it touches              | ...           | ...            |
| Effort                       | small         | medium / large |
| Next similar request         | painful again | easy           |
| Risk of regression           | ...           | ...            |
| What it teaches the codebase | nothing       | a new concept  |

Recommend a path, but make the trade-off real. A throwaway script, a
soon-to-be-deleted module, or a genuinely one-off request can absolutely
deserve the tactical fix.

### Step 5 -- Decide with the user

Wait for the user to choose. Do **not** start implementing until they
pick. Possible outcomes:

- **Go tactical** -- drop `/proper`, do the small fix.
- **Go strategic, small** -- the refactoring fits in one or two commits.
  Implement it directly, then add the feature.
- **Go strategic, non-trivial** -- hand off to `/mikado` (next step).

### Step 6 -- Hand off to /mikado for non-trivial work

If the strategic path is non-trivial (multiple prerequisite changes, risk
of breakage along the way, wants safe incremental steps), use `/mikado`
to manage execution:

1. Frame the Mikado goal as the **end state of the refactoring**, not the
   feature itself. Good:
   _"Extract a `Transport` interface so the WebSocket implementation can
   be swapped."_
   Bad: _"Add SSE support."_
2. Suggest `/mikado goal "<the strategic goal>"` to seed the graph.
3. Let `/mikado` discover prerequisites by attempting the naive change and
   observing what breaks. Do **not** pre-populate the graph with
   speculative steps.
4. Track the original feature request as a Mikado follow-up
   (`/mikado later "<feature>"`) or simply implement it after the
   refactoring goal is reached. It is **not** part of the refactoring
   graph itself.

## Rules

- **Diagnosis before code.** Steps 1-4 produce a proposal, not edits.
- **Stay tied to the requested feature** by default. Prune anything that
  does not serve it. If widening looks worthwhile, **negotiate** -- list
  the option, the cost, the benefit, and let the user pick. Never expand
  scope silently.
- **The user is in control of scope.** Always.
- **Acknowledge when tactical wins.** `/proper` is a thinking tool, not a
  verdict.
- **Defer execution** of non-trivial strategic work to `/mikado`. Do not
  try to do Mikado-style incremental work inside this skill.
- **Never commit autonomously.** The user reviews and commits.
