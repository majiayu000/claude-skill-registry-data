---
name: does-work
description: "Use when asked to act on change requests left by a reviewing agent (often invoked with tony:reviews-work) in a spec or plan doc's Changelog. Sleeps in rounds of 5 checks, starting at 3-minute intervals and shrinking to 2, applying each new change request as it appears. When the spec is marked ready it writes the plan and works the plan's review loop until the plan is ready. It implements the plan only when the user also says 'execute plan'. Triggers: 'apply the review changes and wait for more', 'does:work', 'work through the changelog on this doc'."
---

# Does Work (tony:does-work)

## Purpose

Companion to `tony:reviews-work`. That skill leaves change requests inline in
a spec/plan doc's Changelog; this skill is the other side — it waits for
those requests, acts on them directly in the doc, and keeps waiting for more.
It carries the work from spec review through writing and reviewing the plan.
It implements the plan only when the user's request also says "execute plan"
(see **Execute-plan mode**). Run this one when the reviewer's
requests already exist (or are about to), so it sleeps first instead of
writing anything up front.

## Repository path and wakeup fallback

When the user supplies a document path, treat that path as authoritative and resolve it to an
absolute filesystem path before doing any work. Derive the repository/worktree from the target
document's parent directories; do not assume the current workspace or a same-named repository is
the target. Run all reads and writes against that resolved path, and report the resolved path in
the first progress update when it differs from the current working directory.

If `ScheduleWakeup` or an equivalent scheduler is unavailable, use a bounded Python timer as the
fallback rather than ending the worker loop:

1. Create a temporary timer script outside the target repository (for example,
   `/private/tmp/tony_reviews_work_timer.py`) that sleeps for the current round interval and prints
   a completion marker.
2. Run it in a background/interactive command session. Use the current interval from the timing
   rules: 180 seconds for the first round, then 120 seconds once the interval has shrunk to the
   floor.
3. Poll the session at intervals no longer than 30 seconds until the completion marker appears,
   then resume this skill's Changelog check. Send a concise progress update while the timer runs.

The timer is only a wakeup substitute; it does not change the round/check semantics or authorize
edits outside the target document.

## Sleeping between checks — any agent, any harness

This skill is AI-agnostic: it does not depend on any one platform's tool
name. Use whatever built-in wait/sleep/scheduling mechanism your own harness
provides to pause between checks — for example Claude Code's `ScheduleWakeup`
tool, a generic sleep/delay tool, or a supported wait action. Pick whichever
one your environment actually exposes.

Whatever the mechanism, the rule is the same: **you sleep, you wake up, you
resume this skill yourself.** Never end the turn by describing the wait as
something "the reviewer's loop" or "the user" will pick back up — that's the
job of this skill's own loop. Only stop when the skill ends (see **Phases and when the whole skill ends**),
and say so explicitly when you do.

## Changelog format

Same Changelog section, at the bottom of the doc under `## Changelog`, newest
entry on top. Use role `Worker` for every entry you write. When an entry
covers more than one distinct action, list them as a numbered sub-list under
the entry so the count and substance of each item is scannable at a glance —
never collapse several actions into one flat prose sentence:

```markdown
## Changelog

- **2026-09-09T14:40Z — Worker:**
  1. **Topic of change 1:** what you did or are about to do.
  2. **Topic of change 2:** what you did or are about to do.
```

A single-action entry can skip the sub-list and just state the one thing
after the colon. Entries from the other agent will say `Reviewer` (or
whatever role they used) — that's how you tell a genuinely new request apart
from your own last entry. When reading a `Reviewer` entry, its numbered
sub-list is the actual set of requested changes — treat each numbered item
as one discrete change to apply.

## Timing: rounds of 5, shrinking from 3 minutes to 2

The wait between checks is not fixed. It runs in **rounds**:

- Each round is up to **5 checks** at a fixed interval.
- The first round's interval is **3 minutes**.
- Every time a round ends because a *new reviewer entry arrived* (not
  because it ran out of checks), the next round's interval drops by
  **1 minute**, down to a floor of **2 minutes**. Later rounds stay at 2
  minutes once they hit the floor.
- A round that ends because all 5 checks passed with no new entry is a
  the timer loop running out (see below); the interval does not matter at that point.

The rationale: once changes start landing, later ones tend to be smaller
follow-ups, so shorter checks keep up without waiting as long between them.

## Phases and when the whole skill ends

This skill runs these phases in order, without returning to the user in between:

1. **Spec review loop:** apply the reviewer's requests to the spec until the spec is marked ready.
2. **Plan review loop:** write the plan (see **Next phase: spec marked ready**), then run the
   *same* check loop against the plan doc until the plan is ready to execute.
3. **Execution, only in execute-plan mode:** implement the plan (see **Execute-plan mode**).

A spec being marked ready is a **phase transition, not a stop**: move straight on to writing the
plan. A plan being ready is where the skill **stops**, unless execute-plan mode is on.

**Execute-plan mode is on only when the user's request explicitly says "execute plan"** (for
example `/tony:does-work <doc> then execute plan`). Nothing else turns it on: not "start the
plan", "do the plan", "keep going" or "get it done". "Start doing the plan" means *start writing*
the plan. When in doubt, it is off.

The skill ends only in one of these cases:

1. **The plan is ready, and execute-plan mode is off.** Report that the plan is ready for
   implementation, give its path, and stop. Do not write or change any code.
2. **Execute-plan mode is on, and the plan is fully executed and its PR is open** (or a blocker is
   reported; see **Execute-plan mode**). Report the result and the PR link.
3. **The timer loop runs out.** A full round (5 checks) at the current interval passes with no new
   reviewer entry, in either review loop. Stop, tell the user the reviewer appears to have gone
   quiet, and say which phase you were in and what state each doc is in.

### When is a doc "ready"?

- **Spec ready:** the newest `Reviewer` Changelog entry in the spec contains `READY` or clearly
  says it's approved / ready for planning. `tony:reviews-work` also sets the spec's
  `Status: Ready for planning`.
- **Plan ready to execute:** all three of these hold.
  1. The newest `Reviewer` Changelog entry **in the plan doc** contains `READY` or says it's
     approved / ready for implementation. A `READY` in the spec's Changelog does not count for the
     plan.
  2. The plan's `Status:` line reads `Ready for implementation`. If the reviewer wrote the `READY`
     entry but didn't update the line, update it yourself and note that in a `Worker` entry.
  3. The plan has no unfinished content: no `Status: Plan creation in progress`, no `TBD` /
     `TODO`, and no steps that only describe code instead of showing it. If you find any, the plan
     is not ready. Complete them, hand back for review with a `Worker` entry listing what you
     filled in, and keep looping.

  If 1 and 2 hold but 3 fails, the reviewer missed something. Fix it and ask for one more pass;
  don't execute a plan with holes in it.

## Next phase: spec marked ready → write the plan

When the spec is marked ready, don't stop. Move the work into the next phase:

1. **Pick the plan's path.** Decide where the plan will live before writing
   any of it — follow the repo's existing convention (e.g. a `plans/`
   directory next to or mirroring the spec's `specs/` directory), otherwise
   put it beside the spec with a `-plan` suffix. Resolve it to an absolute
   path.
2. **Create a placeholder plan file** at that path containing only the
   plan's heading and an in-progress status, nothing else:

   ```markdown
   # <Feature name> Implementation Plan

   Status: Plan creation in progress
   ```

3. **Log the plan path in the spec's Changelog.** Add a new
   top-of-Changelog entry, role `Worker`, timestamped now, with the literal
   `PLAN:` marker followed by the absolute plan path:

   ```markdown
   - **2026-09-09T15:02Z — Worker:** PLAN: /abs/path/to/plans/feature-plan.md — plan creation in progress.
   ```

   This is the hand-off signal `tony:reviews-work` reads to find the plan
   it should review next. Write it before starting the plan, not after.
4. **Write the plan into that same file**, replacing the placeholder:
   - If the `superpowers:writing-plans` skill is available, invoke it to
     produce the implementation plan from the now-approved spec, and save
     its output to the path from step 1 (not a path of its own choosing).
   - If it isn't available, write the plan yourself directly, following
     standard planning best practices (clear phases, concrete file targets,
     a testing/verification strategy, no ambiguity left for the
     implementer).

   When the plan is complete, change its `Status:` line to
   `Draft for review`. If the plan ends up at a different path after all,
   add another `PLAN:` entry to the spec's Changelog with the new path.

5. **Switch the loop to the plan.** The plan is now the target doc. Add an empty `## Changelog`
   section at the bottom of the plan if it has none. Start a **fresh** round against the plan: a
   3-minute interval, and the check count reset to 0. Then go back to **Process** step 1. The
   reviewer finds the plan through the `PLAN:` entry and reviews it in the plan's own Changelog.

If you were started directly on a plan doc (no spec phase), begin at the plan review loop.

## Execute-plan mode: plan ready → implement, commit per task, push, PR

Runs **only** when execute-plan mode is on (see above) **and** the plan meets all three "plan ready
to execute" conditions. The user's "execute plan" is the explicit authorization for this run's
branch, commits, push and PR. It does not carry over to any other run.

1. **Announce it** in the plan's Changelog with a `Worker` entry: `EXECUTING: starting
   implementation of this plan.`
2. **Get on the right branch, inline, never in a worktree.** In each repo the plan touches:
   - **On the default branch** (`main`/`master`): `git fetch`, then create and switch to a new
     branch from the up-to-date default branch, named per the repo's convention (e.g.
     `<user>/<feature>`).
   - **On another branch:** check that it's new for this work: it has no commits beyond the
     default branch that don't belong to this feature, and no open PR for something else
     (`git log <default>..HEAD`, `gh pr list --head <branch>`). If it's new, use it. If it carries
     unrelated work, stop and ask rather than mixing the two.
   - Never create a worktree for this.
3. **Implement task by task, inline.** Use `superpowers:executing-plans` if it's available, but
   run it inline in this session with no subagents or worktrees, unless the user said to use
   subagents. Follow each task's steps: failing test, watch it fail, implement, watch it pass, then
   the task's verification. Tick each step's checkbox as you finish it.
4. **Stage, then commit, per task.** When a task is done and verified:
   a. Check `git status` / `git diff --cached` first. If anything is already staged that isn't
      this task's work (another session may share the branch), stop and ask.
   b. Stage exactly the files this task changed (`git add <paths>`), never `git add -A` / `.`.
   c. If anything is staged, commit it with a message naming the task (e.g.
      `Task 3: send all-or-none progress identity`), ending with the attribution trailer the
      environment specifies.
   d. Move on to the next task and repeat. One commit per task, in plan order. A task spanning
      two repos gets one commit in each.
   The plan and spec docs are committed with the task that last changed them (checkbox ticks
   included). Docs the skill didn't write are never staged.
5. **Don't stop between tasks.** A finished task is a reason to start the next one.
6. **Stop only for a real blocker:**
   - a test or build that fails for a reason the plan didn't anticipate, after a genuine attempt
     to fix it
   - a step that needs a decision or permission only the user can give (a production database
     write, a deploy, a precondition the plan asks you to confirm)
   - a contradiction between the plan and the code that changes the design
   - unrelated staged files or an unrelated branch (steps 2 and 4a)

   Leave finished tasks committed. Add a `BLOCKED:` `Worker` entry to the plan's Changelog with
   what happened and what you need, report it, and end the skill. Do not push or open a PR for a
   blocked run.
7. **Finish: push and open the PR.** When every task is committed:
   a. Run the plan's final verification. Add a `DONE:` `Worker` entry with the results, set the
      plan's `Status:` to `Implemented`, and commit that doc change.
   b. `git push -u origin <branch>` in each repo touched.
   c. Open a PR per repo with `gh pr create`. The body covers: what and why (link the spec and
      plan paths), a per-task summary matching the commits, how it was verified (test commands and
      results, including anything that failed for reasons outside this change), deviations from
      the plan, anything the user must still do (deploys, migrations, production scripts, manual
      checks), and links to the sibling PR when two repos are involved. End it with the
      attribution line the environment specifies.
   d. Report the PR URLs. That ends the skill.

Never force-push, rebase shared history, or merge the PR.

Everything else (a new change request arriving, applying it, handing back)
keeps the loop going. Do not stop just because you finished applying a
change and handed back — that's exactly when you go back to sleep and keep
checking, per the timing rules above.

## Process

1. **Enter the check loop first — do not edit anything yet.** Sleep for the
   current round's interval (3 minutes on the very first check), then check
   the Changelog. Treat this as check 1 of round 1.
2. **On each wake, read the Changelog.**
   - **No entry from the reviewer since you last checked:** one check used.
     If this was check 5 of the current round with still nothing new, the
     timer loop has run out: stop and tell the user. Otherwise sleep again for
     the same interval and repeat this step, incrementing the check count.
   - **A new entry from the reviewer (role isn't `Worker`) that only
     acknowledges** (e.g. "re-reviewing now") and requests nothing: count it
     as a check used, and keep the same interval.
   - **A new entry from the reviewer with requested changes:** go to step 3.
   - **The new entry says the doc is ready:**
     - Target is the **spec**: go to **Next phase** (write the plan, then loop on it).
     - Target is the **plan**: check the three "plan ready to execute"
       conditions. If not all hold, fix the gaps, hand back, and keep looping.
       If they all hold: with execute-plan mode **off**, report the plan is ready and
       stop; with it **on**, go to **Execute-plan mode**.
3. **Acknowledge, then act.**
   a. Add a new top-of-Changelog entry, role `Worker`, timestamped now,
      saying you've seen their request and are reviewing/making the
      change(s) — this tells the reviewer you're active if they check back
      before you finish.
   b. Read each numbered item in the reviewer's requested-change list and
      apply it directly to the doc (content, structure, whatever the
      request asked for — not just the Changelog). Work through every item,
      not just the first.
4. **Hand back, then keep going.** Add a Changelog entry, role `Worker`,
   with a numbered sub-list mirroring what you changed (one item per
   requested change you addressed), stating it's ready for another review
   pass. Start a new round: drop the interval by 1 minute (floor 2 minutes),
   reset the check count to 0, and go back to step 1. Do not stop here —
   the skill only ends as described in **Phases and when the whole skill ends**.

## Output

- **During the review loops:** Changelog entries plus the doc edits described in step 3b, written
  directly into the spec or plan. In the **Next phase**, also the new plan file and the spec's
  `PLAN:` Changelog entry. No code changes, no commits.
- **In execute-plan mode only:** the plan's code, test and config changes, one commit per task on
  a non-worktree branch, the plan's checkbox updates and `EXECUTING:` / `BLOCKED:` / `DONE:`
  entries, a push, and one PR per repo.
- **A short chat message only when the skill ends:** the plan is ready (execute-plan mode off),
  the PR(s) are open, the run is blocked, or the reviewer went quiet.

Outside execute-plan mode: no commits, no pushes, no PRs.
