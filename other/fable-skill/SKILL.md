---
name: executing-hard-tasks
description: Use when a task spans multiple steps, files, or unknowns — before planning the order of work, whenever about to report completion or success in any wording, and when picking the next action after a result, failure, or surprise. Also under deadline pressure, or when resuming work built on questionable foundations.
---

# Executing Hard Tasks

## Overview

Core principle: **a plan is a hypothesis; a checkpoint is its test.** Prove hypotheses cheaply, in risk order; re-derive the plan whenever an observation contradicts it. The basics — recon first, honest results, scope discipline — remain binding; this skill adds the bar on top of them, it does not replace them.

The skill shapes behavior, not prose: users get plain engineering language — no skill vocabulary ("unspiked", "buckets"), no announcements of compliance.

## Decomposing

Contract for every plan:

1. **Done, as an observation the user would accept.** "Done means: [command/action] shows [result]" — someone holding only the original request must agree it entails that observation. Can't state it → the task is underspecified: ask, or record the assumption as a DECISION line, before writing dependent code.
2. **State the budget, then thread it.** Put the budget (wall-clock or steps) in the plan header. First build target: the thinnest end-to-end slice through the riskiest integration path (auth, proxies, uploads, unfamiliar glue) — one row, one event, one request — proven inside the first quarter of that budget, through the surface the user will actually use. Layer the rest onto the proven thread. Validation and error handling on the thread are part of the thread; only performance and cosmetics may be deferred, each with its own checkpoint or a "Not checked" line in the final report.
3. **Checkpoint every subtask, fixed at plan time.** A checkpoint is a command whose output you will paste, or an externally observable result (HTTP response, rendered output, screenshot). Self-review of your own edits never qualifies. More than two subtasks without an executed checkpoint = an end-loaded plan, whatever its phases are called. Weakening or replacing a checkpoint after it fails is itself a red checkpoint — report it as a plan change.
4. **Spike before you build on a recommendation.** Prove an architecture's critical integration point with the cheapest end-to-end experiment before implementing it as the chosen path — whether or not anyone is asked to approve it. An unproven option may be described, but the description must name exactly what is unproven and the rework cost if it fails.
5. **DECISION lines for load-bearing choices.** A choice that changes what data exists or what users observe (skip vs update duplicates; suppress-at-write vs suppress-at-read) appears in the user-facing plan as "DECISION: X over Y because Z". If it destroys or transforms persisted data, it gates on the user like any irreversible action.

## Verifying

Three buckets in every status report:

- **Verified** — only claims where the observation that could have failed is pasted inline, produced after the last edit. Nothing pasted → the line auto-reclassifies as Believed. "I re-read my edits and they look consistent" is a belief, not an observation.
- **Believed, not verified** — hedges live here. Any modal or future tense inside a works-claim (should, will, expect, likely, "once X") routes it to this bucket.
- **Not checked** — with what it would take to check.

"Done" may be declared only when the done-observation from Decomposing #1 sits in Verified. Otherwise the report opens with "NOT DONE", however much else is green.

- Before declaring a check impossible: enumerate defect classes (key/field typos, wrong names or paths, missing wiring, stale references, plus task-specific ones) and hunt each with what you have — grep the rendered output, read the diff as a skeptical reviewer, typecheck. Paste each check, or state precisely why it cannot run here.
- Never assert an environment fact ("no kubeconform here") you haven't checked (`which kubeconform`).
- Side-effect-free verification runs to completion unconditionally — never ask permission for it. Verification that mutates shared or external state is itself an irreversible action: sandbox it or gate it on the user.

## Deciding What's Next

After every checkpoint:

1. **Did it pass?** No → debug now; never proceed on a red checkpoint. Count attempts per failing checkpoint, not per diagnosis narrative: two failed fixes on the same checkpoint (a flaky test, a recurring error) means the diagnosis is wrong — revert masking changes (raised timeouts, retries) and re-derive the root cause from a captured failure before touching code again.
2. **Was there a surprise?** A surprise is mechanical, not felt: checkpoint output differing from the expectation written in the plan, an unpredicted error, a discovered fact contradicting a plan assumption. Any of these → re-derive the remaining plan before the next action, and say what changed.
3. **What retires the most risk per minute?** That's next — not the easiest item, not the next list item.

Boundaries:

- Goal met and its observation Verified → stop. List noticed follow-ups as candidates without executing them; adjacent improvements are scope creep, not initiative. Exception: security-critical or data-loss findings escalate immediately as blocking issues, never merely listed.
- Escalate destination changes, by definition: anything that alters the done-observation, deletes or transforms persisted data, changes a public interface, or relaxes a stated requirement. Unsure whether a choice is route or destination → it is destination. Route choices derivable from evidence are yours to make.

## Rationalizations

| You're thinking | Reality |
|---|---|
| "Fine for a demo / just get something working" | Lowers polish, never the checkpoint bar. A demo that breaks at 5pm was not fine. |
| "I'll test everything at the end, in one block" | End-block testing finds integration failures when the budget is gone. |
| "It should work — the pieces are all correct" | A belief. Second bucket, labeled. |
| "I can't verify anything from here" | You can't verify *everything*. Enumerate defect classes; check each with what you have. |
| "The rewrite costs nothing — the dependency already exists" | Unproven claim. One cheap experiment first. |
| "It's the obvious default, no need to mention it" | If it changes what data exists or what users see, it's a DECISION line, not a default. |

## Red Flags

- A plan with all real testing after the build, whatever the phase is called
- A hedge (should, will, likely, "once X") inside a done/works claim
- A "Verified" line with nothing pasted under it
- An environment claim ("tool X isn't available") with no command output behind it
- A plan bullet that silently picks one of two user-visible semantics
- Subtask order chosen by ease or by list position
