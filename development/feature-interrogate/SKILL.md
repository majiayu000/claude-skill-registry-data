---
name: feature-interrogate
description: >-
  Adversarially stress-tests a feature's SPEC.md, ARCHITECTURE.md, and PLAN.md before
  feature-build starts: independent review lenses in parallel, each finding refuted by a
  skeptic to kill noise, survivors triaged with the user one by one. Optional and
  heavyweight — reach for it on a large or risky plan, not every one. Use when asked to
  interrogate, pressure-test, stress-test, or find the gaps in a plan, or before committing
  to a risky build.
user-invocable: true
argument-hint: [path to the feature's plan folder, optional]
---

# feature-interrogate

Stress-tests a plan that already exists, before anyone writes code against it. Dispatches a
panel of single-lens subagents to attack `SPEC.md`/`ARCHITECTURE.md`/`PLAN.md` from
independent angles, refutes each finding to kill noise, then triages the survivors with the
user and routes any accepted fix back to the phase that owns the file it would change.

**Core principle:** a plan is cheapest to fix before code exists. Independent lenses catch
more than one re-read; refuting each finding keeps the user's attention on what's real.

**This is the heavyweight, opt-in pass.** `feature-build`'s per-task `reviewer` and its
whole-feature review catch what only a real diff shows. This skill catches the opposite: a
plan that reads fine but rests on a bad assumption, a gap, or a task order that can't work —
before any of that code exists. It never gates `feature-build`; the user reaches for it
deliberately, on a plan that's worth the extra scrutiny.

## Scope

- IN: read `SPEC.md`, `ARCHITECTURE.md`, `PLAN.md`, and `STORIES.md` in one feature's plan
  folder; find and verify gaps; triage them with the user; route an accepted fix to the phase
  that owns the affected file; log every decision.
- OUT: editing `SPEC.md`, `ARCHITECTURE.md`, `PLAN.md`, or `STORIES.md` directly — only
  `feature-design` and `feature-plan` own those files (see the project's `CLAUDE.md`, "one
  owner per file"); writing any code (`feature-build`); reviewing a diff instead of a plan
  (`reviewer`, `pr-review`); surfacing what a finished build assumed (`decision-review` — the
  same job, run the other way round, after the code exists).

## When to use

- The user asks to interrogate, pressure-test, challenge, or find holes in a plan.
- A large or risky feature is about to go into `feature-build` and the user wants confidence
  first, beyond the light confirmation `feature-plan`'s own interview already gives it.

**When not to use:**
- `SPEC.md` is still a stub, or `PLAN.md` has no checkboxes yet — send the user back to
  `feature-design`/`feature-plan` first; there's nothing concrete to interrogate.
- The user wants the *code* reviewed, not the plan — that's `reviewer` (inside
  `feature-build`) or `pr-review`.
- The user just wants a quick sanity check — that's already the light confirmation step
  built into `feature-plan`'s interview.

## Preflight

1. Resolve the plan folder: the path given in the argument; else match the current
   branch/worktree name against a plan folder, same as `feature-build`'s "Finding the current
   feature's plan folder" rule; else, if exactly one plan folder exists, use it; otherwise ask
   which.
2. Read `SPEC.md`, `ARCHITECTURE.md`, `PLAN.md`, and `STORIES.md` (if present) in full. If
   `SPEC.md` is still a stub or `PLAN.md` has no checkboxes, stop and send the user back to
   `feature-design`/`feature-plan`.
3. Check `BUILD-LOG.md`. If it already has entries, some tasks are built: say so, and scope
   the panel to the unbuilt tasks plus anything a finding about a built task would mean
   reopening — reopening built code is a finding for a fresh `builder` via `feature-build`'s
   normal recursion, not a plan edit.

## Set depth

Gauge the plan's size and risk, and scan the request for a cue:
- **Default** (normal plan, no cue): the 5 core lenses.
- **Thorough** (large or risky plan, or "deep/thorough/be comprehensive"): core lenses, plus
  the extended lenses, plus a completeness-critic round.

## Dispatch the panel

Launch one `Agent` call per lens, in parallel — a single message, multiple calls. Give each
agent the full text of `SPEC.md`, `ARCHITECTURE.md`, `PLAN.md`, `STORIES.md`, and this
contract:

> You are interrogating a feature plan through ONE lens: **{LENS}**. Attack only through that
> lens. Return a JSON array of findings; each finding is `{ "claim": "...", "location":
> "file + section/task", "severity": "blocking|significant|minor", "why": "..." }`. Be
> specific — cite the exact task or section. If the plan is clean through your lens, return
> `[]`. Do not propose fixes; only identify problems.
> **Your FINAL message must BE the JSON array and nothing else** — no preamble, no summary.
> Only your final message reaches the orchestrator; JSON in an earlier message is lost.

**Grounding tip:** when the plan makes a concrete claim about Umbraco (an API, a lifecycle
hook, how a notification fires), tell the agent to check it against `umbraco-cms-source` or
`umbraco-docs` at the project's target version instead of trusting the claim. A finding
backed by the real source is worth far more than a guess, and it lets the refute pass correct
the mechanism instead of re-guessing it.

**Core lenses (always):**
1. **Hidden assumptions** — an API, extension point, or data shape the plan takes for
   granted; an assumption about what the CMS already does.
2. **Missing edge cases / failure modes** — unhandled input, error paths, concurrency,
   partial failure, rollback — especially on any task touching sync (`umbraco-env-sync`) or a
   migration (`ef-core-data`).
3. **Sequencing & dependency risk** — a `depends-on:` that's wrong, missing, or circular; a
   `parallel-group:` that actually shares a file or a migration.
4. **Over-engineering / YAGNI** — a task or abstraction the spec doesn't actually require.
5. **Testability & verification** — a task with no real way to prove it works, or whose only
   acceptance criterion is a unit test where `feature-plan`'s "wire tasks are first-class"
   rule requires a real entry point.

**Extended lenses (thorough mode only):** security & data exposure (flag for
`umbraco-security` too), performance/scale, integration & blast-radius (what a change here
couples to elsewhere), rollback/recovery.

## Completeness critic (thorough mode only)

After the panel returns, dispatch one more agent with every finding plus the plan:

> Here is a feature plan and the findings a review panel produced. What did they MISS — a
> section not examined, a claim not challenged, a class of risk not covered? Return any
> additional findings in the same JSON shape, or `[]`.

Fold its findings into the pool.

## Verify (refute) each finding

For each finding, dispatch a skeptic agent:

> A reviewer claims the following about a feature plan: "{CLAIM}" (at {LOCATION}). Try to
> REFUTE it: is it a real problem given the full plan, or is it wrong, already handled, or
> out of scope? Default to `refuted` if unconvinced. Return `{ "verdict": "survived|refuted",
> "reasoning": "..." }` as your sole final message.

Drop refuted findings. **Correct the mechanism even when a finding survives** — a claim can
be real for a different reason than the lens gave it. Capture the corrected reason, not the
original guess, in the log entry and in whatever gets routed onward.

## Triage with the user

Rank survivors blocking → significant → minor. For each, use `AskUserQuestion` (up to 4 per
call) with **accept / reject / defer**, written the way `plain-writing` asks every finding to
be written — plain headline first, jargon pushed into one optional `Detail` line:

```
<id> · <plain-English headline>
Problem:  what goes wrong, in everyday terms
When:     the concrete scenario that triggers it
Impact:   the consequence the feature's user or the package's consumer actually feels
Fix:      what changes if accepted, in plain terms
Detail:   (optional) the task id, file, or API name, for anyone who wants to verify
```

**Scale to the finding count:** a small set (≲10) — walk every one. A large set (a thorough
run on a big plan) — triage the blocking tier interactively, then offer to bulk-fold the
significant/minor findings into `DECISION-LOG.md` as known accepted risks instead of walking
each one.

## Route accepted findings, and log every decision

This skill never edits `SPEC.md`, `ARCHITECTURE.md`, `PLAN.md`, or `STORIES.md` itself —
those stay owned by `feature-design` and `feature-plan`. For every finding, append one dated
entry to `DECISION-LOG.md`: the claim, the verification verdict (and corrected mechanism if
any), and the decision (accepted/rejected/deferred) with why.

For an **accepted** finding:
- A change to `SPEC.md`/`ARCHITECTURE.md` (a requirement, an extension point, a data shape)
  → hand the specific wording to `feature-design` to fold in. It's re-entrant: this refines
  the file, it doesn't restart the phase.
- A change to `PLAN.md`/`STORIES.md` (resequencing, a missing task, a wrong `depends-on:`) →
  hand the specific wording to `feature-plan` the same way.
- Collect every accepted finding first, then hand off once, grouped by which phase needs to
  run — don't invoke those phases mid-triage, one finding at a time.

A **rejected** finding gets its one-line log entry and nothing else. A **deferred** finding is
logged as a known accepted risk; `decision-review` and the eventual PR are where it next gets
a human's attention.

## Hand off

Report: N findings, S survived verification, the blocking tier's decisions, and how the rest
were triaged. Then:
- Findings routed to `feature-design` or `feature-plan` → `Suggested next: re-run
  <feature-design|feature-plan> to fold these in, then feature-interrogate again if the
  change was non-trivial, before feature-build.`
- Nothing routed → `Suggested next: feature-build.`

## Rules

- **Skipping verification is the main way this fails.** Unrefuted findings are noisy and
  waste the user's triage time; always run the refute pass before showing anything to them.
- **One agent, one lens.** An agent asked to find "all problems" flattens perspective; keep
  lenses as independent subagents.
- **Never edit the plan.** Route every accepted finding to its owning phase instead — this is
  what keeps `SPEC.md`/`ARCHITECTURE.md`/`PLAN.md` single-owner, same as the rest of the
  pipeline.
- **Never auto-apply.** Triage gates every routed change; nothing gets folded in without an
  explicit accept.
- **A subagent's final message must be exactly the requested JSON.** If one buries it in
  prose, re-invoke it (`SendMessage` to its agent id) asking for the JSON array alone — a
  summary is not the finding.
