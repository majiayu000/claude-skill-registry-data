---
name: subagent-patterns
description: |-
  Use when dispatching development work to one or more subagents and deciding how to shape each dispatch. Triggers: "use subagents", "orchestrate subagents", "delegate to a cheaper/stronger model", "big:little" / "little:big", "verifier / adversary / explorer / oracle subagent", "run this with subagents", "get an independent second opinion". Not for: the parallel code-review path (use `code-review`), or driving a separate agent CLI non-interactively.
---

# Subagent Patterns

## Overview

This skill helps you decide what to dispatch to a subagent and how.
Each dispatch comes down to five choices: whether to dispatch at all, which model, what job the worker does, why to isolate it, and how to wire several together.
Make those choices deliberately instead of reaching for a named pattern.

Resolve the five decisions in order, then apply the rules that hold for every dispatch.

> Harness note: this skill says _dispatch_, _worker_, and _the model on the dispatch_ for whatever your harness calls its subagent tool and per-call model parameter — substitute the equivalents.

## When to Use

- You're about to farm work out to one or more subagents and want the shape right: how many, which model, what job, what to withhold.
- Executing a multi-task plan (e.g. an `sdd-apply` run) with a coordinator that gates each task.
- A cheap primary keeps hitting decisions above its weight and needs an on-demand expert.
- You want a genuinely independent second opinion, from a fresh context or a stronger model.
- Long autonomous runs are drowning in their own history and you need to move state to files.

## When Not to Use

- **Unless the user asked for it.**
  Subagent delegation is opt-in and off by default; never something you start on your own.
  Dispatching multiplies token spend, so whether to use subagents is the user's call, not yours.
  Without an explicit instruction (or an active skill like `sdd-apply` that already prescribes delegation), do the work in your own context.
  If you judge it would help, propose it and wait for a permission grant.
- **Parallel code review.**
  The `code-review` skill already owns that path (`references/parallel-subagent-review.md`); invoke it instead of rebuilding it here.
- **Driving another agent CLI non-interactively** (shelling out to Codex, Gemini, `llm`, Pi, and the like).
  A child harness's permission prompts can't surface back to the user, so its actions escape human oversight.
  Keep every dispatch inside your own harness, where approvals still reach the person running it.

## Invocation Notice

- Tell the user when this skill is running: `subagent-patterns`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## The Five Decisions

| #   | Decision             | Default               | Change it when                                                                         | Sets                                                              |
| --- | -------------------- | --------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| 0   | **Dispatch at all?** | No; do it inline      | output is token-heavy, you need an independent view, or the work is genuinely parallel | whether a subagent exists                                         |
| 1   | **Model tier**       | peer                  | cheaper if the brief holds the code; stronger if the task exceeds your reach           | the model on the dispatch                                         |
| 2   | **Role**             | implement             | you need verify, explore, advise, or buffer                                            | tool scope and return contract                                    |
| 3   | **Isolation**        | keep my context clean | you need unbiased judgment, or clean-room independence                                 | what you withhold from the brief                                  |
| 4   | **Wiring**           | one                   | fan-out, pipeline, panel, or loop                                                      | dispatch cadence, and whether you synthesize the results yourself |

Two of these get rushed most often:

- **Decision 0 is a real gate.**
  A subagent earns its place only by buying you one thing: isolation from token-heavy output, parallelism, a cheaper or stronger model, or an independent view.
  Without one of those, do the work inline.
  A root agent with tokens to spare reviews its own output fine, and a pile of narrow specialists costs more reliability than it adds.
  One thing a dispatch never buys: judgment you yourself cannot specify.
  A dispatch delegates labor, not accountability, and it can only carry what the brief can state.
  When the quality bar is tacit — taste, voice, register, craft — the brief carries constraints but not the standard, so the worker satisfices to the letter of the brief and returns the minimum that technically passes.
  Do that work inline, or dispatch it only with a worked exemplar of the target and the rubric you will judge by.
- **Decision 3 is about what is withheld, not just why you fork.**
  Keep-context: withhold nothing, but make the worker return a digest instead of its raw output.
  Unbiased: withhold your own conclusion and the other workers' findings, so the judgment is genuinely independent.
  Clean-room: withhold the original, so the worker rebuilds or judges from the spec and you compare the two.
  Leak the thing you meant to withhold — your verdict to an "unbiased" verifier — and you have defeated the reason you dispatched.

For **model tier** (decision 1), assign it after the steps are written.
A task whose brief already contains the code to write is the cheap tier regardless of file count.
But turn count beats token price: the cheapest models often take 2–3× the turns, so keep a mid tier as the floor for anything that needs prose reasoning.

## Roles and Their Rules

The role fixes what the other decisions don't: the worker's tool scope, the shape of its report, and the rules it works under.
Set all three in the brief when you dispatch.

| Role                | Tool scope | Returns                                                                                                        | Rules                                                                                                                                                            |
| ------------------- | ---------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **implement**       | write      | the change, its commits, a one-line broad-scope test result, and a report-file path                            | build only what the brief asks: no extra features, refactors, or scope; raise (`BLOCKED`) rather than guess past missing context or make an unrequested decision |
| **verify**          | read-only  | findings, each with a severity, a location, the problem, why it matters, and a suggested direction (not a fix) | treat the report as unverified; judge the delta, not the whole deliverable; never pre-judge ("don't flag X")                                                     |
| **explore**         | read-only  | the paths, line numbers, and a short map of what lives where                                                   | return locations, not walls of prose; change nothing                                                                                                             |
| **advise** (oracle) | read-only  | the decision, its rationale, the tradeoffs, and the risks                                                      | advise only, never edit; reason from the brief alone; surface the decision for the primary, don't make it                                                        |
| **buffer**          | read-only  | a digest: the signal (pass/fail, counts) and only the exceptions (failures, warnings)                          | absorb the raw output; run the broad scope; report pristine-or-not, never the full log                                                                           |

Set only what the role and task need.
A one-line spec-complete task needs no essay on scope; a design-heavy one does.
Beyond the contract above, leave _how_ the worker does the job to its judgment and to the skills that own that work (`code-review` for review lenses, `tdd` for the red-green loop).

## Named Archetypes Are Presets

An archetype is a preset: a fixed point in the space above.
Given a name, read off its coordinates and dispatch from them instead of looking for a catalog entry.

| Archetype                         | Coordinates                                                                    |
| --------------------------------- | ------------------------------------------------------------------------------ |
| **implementer:verifier**          | `pipeline[ implement·cheaper → verify·peer+·unbiased ]`                        |
| **oracle / consult** (little:big) | `advise · stronger · read-only · one`                                          |
| **adversary / red-team**          | `verify · peer+ · unbiased`, briefed to **refute**, not review                 |
| **explorer / scout**              | `explore · peer · read-only · keep-context`                                    |
| **test-runner / buffer**          | `buffer · cheaper · read-only · keep-context`                                  |
| **clean-room**                    | `implement-or-verify · peer+ · clean-room` (withhold the original)             |
| **steelman**                      | `advise · peer+ · unbiased` — argue _for_ the set-aside option                 |
| **referee / judge**               | `verify` as the last node of a `panel`; ranks and gives the deciding criterion |

Given a name that isn't listed, resolve it to the five decisions and dispatch from the coordinates.
When a name could mean more than one thing ("cleanroom" as a context buffer, or as an independent rebuild), ask which is meant instead of guessing.

## Two Worked Presets

The two most common points, start to finish.

### big:little — orchestrator

A capable coordinator owns the plan, the gates, the ledger, and the dialogue with the user; cheap `implement` workers do one task each; a stronger `verify` worker checks every task; you arbitrate.
Per unit of work: brief, dispatch one worker, capture the delta it produced, verify that delta against the source of truth, gate and fix, then log it.
Verify the whole deliverable once at the end.
The full loop, gating, and escalation live in `references/review-loop.md`.
Worked example: run `sdd-apply` as the coordinator, with cheap `implement` workers per task, a stronger `verify` worker checking each change through the `code-review` skill, and you as final arbiter.

### little:big — implementer plus oracle

A cheap primary does the bulk of the work in-context and stays there.
On a decision above its weight — a design fork, a subtle bug, a spec gap — it consults a frontier `advise` worker, then proceeds.
The oracle is read-only and advisory; the primary stays the actor and keeps ownership.
Brief the oracle with the question stated as a decision to make (not "look at my code"), the minimal code and constraints it needs (it can't see your session), and the options you've already weighed.
Require back the decision, its rationale, and the tradeoffs, never a patch.
Consult sparingly: an oracle on every step is just an expensive coordinator.

## Rules for Every Dispatch

These hold whatever you dispatched.

1. **Hand work over as files, not pasted text.**
   Everything you paste in, and everything a worker prints back, stays in your context and is re-read every turn.
   Brief-file path in; report-file path out.
2. **Give each worker a self-contained brief.**
   It inherits none of your context, so a good brief carries: one line of placement (where this fits in the effort); the requirements as a file it reads first, with exact values (numbers, signatures, test cases) verbatim; the interfaces and decisions from earlier work it can't know; your resolution of any ambiguity you spotted; and the report-file path.
   Never paste session history or "state after Tasks 1–3."
   Carry the standard, not just the constraints: state what "done" looks like and how you will judge it.
   Where there are no exact values — writing, design, naming, anything with a quality bar — a list of things to avoid is not a spec; add a worked exemplar of the target and the rubric, or the worker will make the smallest change that technically clears the bans.
3. **Match the return contract to the role** (see Roles and Their Rules).
   The detail lives in the file, not the reply.
4. **Name the model explicitly.**
   An omitted model inherits the session's most expensive one.
5. **Run parallel work as multiple dispatch calls in one message.**
   One call per message runs sequentially.
   Parallelize only independent work (disjoint files and subsystems); never fan out writers on the same files, and go sequential when one task needs another's output.
6. **Keep a durable ledger, and never re-dispatch finished work.**
   Append one line per finished task (commits `<base>..<head>`, review clean) to a file agents can write (not under `.git/`) and outside the tracked tree.
   After compaction, trust the ledger and `git log` over recollection.
7. **Defer to a purpose-built skill's own dispatch rules.**
   When a skill governs dispatch for its task, follow it rather than these defaults.
   A skill that prescribes its own procedure (`code-review`, `sdd-verify`) owns its model resolution, subagent caps, severity, and gating; a skill that forbids subagents (`security-triage-finding`) means no dispatch at all, even on request.
   These defaults apply only when no such skill governs the work.

## You Are the Final Arbiter

Across every dispatch, you (the coordinator) are the last reviewer and the escalation point.
A subagent can't reach the user, so it raises blocks and decisions to you; you decide what to carry up and what to resolve yourself.

- Raise genuine ambiguity, an important design decision, or a scenario the specs don't cover early, before spending a dispatch on a guess.
- When you escalate, assume the human has only a cursory understanding: no familiarity with the current task, the underlying context, or the option space.
  Give that context and lay out the options; don't just name the problem.
- Do the final verification pass yourself after the workers finish.
  A worker's report is a claim, not proof (see `references/review-loop.md`).

## Common Mistakes

- Reaching for a named pattern instead of deciding the five; or dispatching when an inline action would do (decision 0).
- Pasting session history into a brief, which bloats your context; hand over a brief file instead.
- Feeding an "unbiased" verifier your own conclusion, or giving an adversary the prior findings so it anchors on them instead of attacking the work fresh; either leaks what you meant to withhold.
- Omitting the model, so a mechanical task inherits the session's most expensive one.
- Handing a verifier the deliverable with no source of truth, so it invents the standard and grades against it.
- Briefing a worker with constraints and prohibitions but no positive standard, so it satisfices — the smallest change that technically clears the bans — and returns shallow work you then accept without re-reading against what "good" should have been.
- Pre-judging the verifier ("don't flag X", "at most Minor"), the bias a fresh context exists to remove.
- Fanning out writers on the same files, or parallelizing tightly dependent steps.
- Re-dispatching a task the ledger already marks finished, especially after compaction.
- Letting the `advise` worker edit code, or briefing it with a question it can't answer from what you pasted.
- Escalating to the human as a bare problem statement, without the context and options they need to decide.

## References

- `references/review-loop.md` — the general verify/gate/fix loop for any deliverable: scoping the check to the delta against its source of truth, treating reports as unverified, no pre-judging, severity gating, the fix loop, and human arbitration (code review defers to `code-review`).
- `code-review` skill (`references/parallel-subagent-review.md`) — the parallel-reviewer dispatch templates and `build_review_packet.py`, reused by the big:little verify step.
