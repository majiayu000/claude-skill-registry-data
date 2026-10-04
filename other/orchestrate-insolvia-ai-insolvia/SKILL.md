---
name: orchestrate
description: >-
  Run a piece of work as an ORCHESTRATOR of sub-agents instead of doing it all
  inline: decompose the task, dispatch scoped sub-agents — each on the cheapest
  model that can do its piece well — then verify and synthesize their results.
  The work to perform is whatever is passed as the skill's argument
  (`/orchestrate <work>`). Also use whenever the user asks to "orchestrate",
  "coordinate agents", "fan out", "parallelize", or "delegate" a task, or hands
  over a large multi-part job — a repo-wide audit or migration, broad research,
  a review from several angles, anything whose parts can proceed independently.
---

# Orchestrate — run the work through sub-agents

You are the conductor, not the soloist. Your job is to plan the work, brief
sub-agents to do it, judge what comes back, and synthesize the answer. Your
own context window is the scarce resource: every file dump or test log you
read inline is space stolen from planning and judgment. Sub-agents exist to
absorb that volume — the parent should receive conclusions, not the work that
produced them.

If the work passed in is genuinely small — one file, one question, one
already-decided edit — say so and just do it directly. Orchestration has a
per-agent cold-start cost; spending three agents on a one-agent task is not
thoroughness, it's overhead.

## The loop

1. **Decompose.** Think before dispatching: break the work into pieces with
   real boundaries (by directory, by subsystem, by question, by review lens).
   Overlapping pieces make agents duplicate work; vague pieces make them
   wander. If you can't state a piece's *done* condition in a sentence, it
   isn't scoped yet.
2. **Choose a topology.**
   - *Fan-out* — pieces are independent → dispatch them all in a single
     message so they run concurrently.
   - *Pipeline* — piece B needs A's output → run sequentially, feeding each
     result forward.
   - *Panel* — same artifact, different lenses (correctness, security,
     simplicity…) → parallel agents, one lens each, then you reconcile.
   Most real work is a mix: a fan-out discovery phase, then a pipeline that
   acts on what was found.
3. **Brief each agent** (see below) and pick its model (see below).
4. **Dispatch.** Independent agents go out together in one message.
5. **Verify, then synthesize.** An agent's report is a claim, not a fact.
   Spot-check the load-bearing ones — run the test it says passes, open one
   file it says it fixed. Re-dispatch a corrected brief instead of patching a
   bad result by hand. Then write the synthesis yourself: joining the pieces
   is the judgment part, and it's yours.

## Briefing a sub-agent

A sub-agent starts cold: it sees your prompt, the project's CLAUDE.md, and
nothing else of this conversation. It also **cannot ask you or the user
anything mid-task** — an under-specified brief doesn't come back as a
question, it comes back as guesswork. So every brief carries four things:

- **Objective** — what to find out or change, with the file paths, names, and
  context it can't discover cheaply on its own.
- **Boundaries** — what's out of scope, so parallel agents don't collide or
  duplicate each other.
- **Output format** — exactly what to return (e.g. "a list of
  `path:line — one-line finding`", "the diff summary and the test command
  output"). You have to merge these; make them mergeable.
- **Ground rules that matter here** — the one or two repo constraints the task
  will trip over (for this repo: branch rules, free-tier/EAS constraints,
  design-system PR isolation) rather than a re-paste of everything.

Anthropic's research-system team found that a vague brief ("research X") is
the primary failure mode of orchestration — agents duplicate and drift. The
brief is where orchestration is won or lost.

## How much to spend — effort scaling

Match agent count to task complexity, not ambition:

| Work looks like… | Spend |
|---|---|
| One question, one place to look | 1 agent (or none — do it inline) |
| A comparison, a small survey, a two-sided check | 2–4 agents |
| Repo-wide audit, migration, multi-domain research | 5–10 agents, clearly divided, usually in phases |

More agents than distinct boundaries means overlap, and overlap means
contradictory reports you then have to arbitrate.

## Choosing each agent's model

Sub-agents may run on lesser models than you. Omitting `model` inherits the
session's model; otherwise pass an alias (`haiku`, `sonnet`, `opus`). Decide
per agent with two questions:

1. **What does a wrong answer cost?** If a bad result quietly poisons your
   synthesis, pay for the stronger model. If it's obvious or cheap to re-run,
   economize.
2. **Can I verify the output cheaply?** Cheap verification (does it compile,
   does the grep hit, does the test pass) makes a cheap model safe.

| Tier | Give it | Because |
|---|---|---|
| `haiku` | Locating things (search/glob sweeps), extraction into a fixed format, applying an *exactly specified* mechanical transform, crunching logs/test output into a summary | High volume, low judgment, failures are visible. Fast, cheap search does not need a frontier model. |
| `sonnet` | Well-scoped implementation with clear acceptance criteria, writing tests to a spec, straightforward refactors, doc drafts, first-pass code review | Near-frontier on bounded engineering at a fraction of the cost — the workhorse tier for delegated pieces. |
| *inherit* (omit `model`) | Anything you'd redo if it came back wrong: design decisions, debugging subtle behavior, security-sensitive review, cross-cutting changes, final verification passes | Judgment work degrades quietly on smaller models; you won't see the failure until it's expensive. |
| `opus` explicitly | Only when the session itself runs on something smaller and one piece is the crux of the whole task | Escalation is the exception; the default ceiling is "inherit". |

Two hard rules. **Never downgrade the judge**: if an agent's role is to
evaluate, arbitrate, or verify other agents' output, it runs at your tier —
a weak judge silently launders weak work into your synthesis. And
**synthesis is never delegated at all**: the final joining of results is the
orchestrator's own job.

When unsure between two tiers, take the cheaper one *only if* you added a
verification step that would catch its failure; otherwise take the stronger.

## What never goes to a sub-agent

- **Approval-gated or destructive actions.** Sub-agents can't surface
  permission prompts mid-task; a gated call fails or stalls silently. Deploys,
  pushes, deletions, anything needing a human yes stays in the parent.
- **Conversational iteration.** If a piece needs back-and-forth with the user,
  it was never delegable.
- **The final answer.** Reports in, synthesis out — written by you, from
  verified pieces, in your own words.
