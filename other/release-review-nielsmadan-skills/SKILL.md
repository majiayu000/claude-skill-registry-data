---
name: release-review
description: Run a comprehensive pre-release review of a whole product, working through every command, parameter and config surface with the user, one item at a time. Rulings are collected in an on-disk changes ledger, ruled batches are handed to parallel implementer sessions as soon as they are ready, and the programme is sequenced through code-quality review, docs review, QA and release, then harvested into the repo's docs. Resumable across sessions. Use when the user says "get this to 1.0", "release review", "final review of all commands and params", "review the whole product before release", "comprehensive review of full functionality", "pre-release review", "resume the release review", or "where are we in the review". Do NOT use for reviewing a diff or PR (use code-review), QA of one feature (use qa), a persona-based product audit (use review-product), or executing an already-written plan (use longshot).
argument-hint: '[version] (or blank to resume the programme in this repo)'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Release Review

Bring an existing product to a reviewed, consistent, documented and exercised release. This is a
**review programme**: its output is a polished surface over the features that already exist.
The user rules on every change. Implementation runs in parallel sessions or in longshot, not in
the reviewing conversation.

## Instructions

### Step 0: Start or resume

Look for an existing programme directory. Use the repo's scratch plan directory if one exists
(e.g. `docs/superpowers/`), otherwise `docs/release-review/`. Run
`git check-ignore <dir>`, tell the user whether it is ignored, and let them decide whether it
should be.

- **Programme exists:** read `programme.md`, then `changes.md`. Print the **Now** / **Next** lines
  and the in-flight batches. Check `git log` for commits reported by implementer sessions since
  the last update, and mark those entries `implemented`. Then continue from **Now**. Do not
  re-ask framing questions.
- **A review started under another workflow** (a release spec plus a findings or changes
  document, e.g. from a brainstorming session): adopt it rather than starting over. Write
  `programme.md` with its framing and the current position, and link the existing spec and
  ledger as the source of truth instead of copying them. Confirm the position with the user.
- **No programme:** go to Step 1.

Formats for every file are in `references/formats.md`. Read it before creating any of them.

### Step 1: Frame and baseline

1. Settle the framing in a short interview, one question at a time, with a recommendation for
   each: target version and release path (ship an interim version first?), breaking-change
   policy, what is out of scope, which known gaps get built vs. deferred, QA hardware and
   environments, and where the work runs (branch or checkout). If many premises are open,
   use `blind-spots` for this interview.
2. Run the full check suite, coverage and docs build. Fix failures now; do not carry them.
3. Inventory the **whole** surface, not only CLI flags: commands and subcommands, every flag
   and default, config files the product reads, files it generates or scaffolds (`init`
   output is surface), environment variables, output formats, exit codes, prompts, and hidden
   or internal entry points (hooks, completion).
4. Write `programme.md` with framing, phases P1–P8 and the unit list. Show it to the user once
   for approval.

Success: `programme.md` exists and the user approved it. The checks are green.

### Step 2: Map and target flows (P1)

1. Present a **product map** before any detail: each command in one line (what job it does,
   who runs it, when), and how they fit together. Point out overlaps and near-synonyms
   (`bootstrap` vs `init` vs `sync`). This is where most renames and removals surface.
2. Write the **target flows** into `target-flows.md`: the realistic journeys (first adoption,
   daily use, new checkout, recovery), written as what *should* happen. Settle the target
   before comparing it with what exists. Use realistic starting states: users who adopt a tool
   already have config and data at real scale (twenty skills, not two).

### Step 3: Cross-cutting conventions (P2)

Review conventions before any single command, so each unit inherits them: flag naming,
`--force` / `--yes` / `--dry-run` semantics, output formats and `--json` coverage, stdout vs
stderr, exit codes, error wording, interactive vs non-interactive behaviour, help text and
examples, working-directory and config precedence, and bare invocation.

Settle each convention with prior art (see "Presenting an item" below). Record each one as a
ledger entry that applies to all units.

### Step 4: Unit-by-unit surface review (P3)

For each unit (a command, a subcommand family, or a config surface):

1. **Dossier.** Current flags and defaults, what the code actually does (run it in a scratch
   environment; don't infer behaviour from source alone), config it reads and produces, docs
   coverage, test coverage.
2. **Challenge existence first.** For every flag, subcommand and option, ask what the use case
   is and who runs it. Flag candidates for removal: a CLI flag that only duplicates a config
   entry, an option no target flow uses, or a mode that exists "for flexibility". Removing
   something now is cheap. Adding it back later is a feature request.
3. **Present items one at a time** (see below) and record each ruling.
4. After each ruling, run the **readiness analysis** (Step 5).
5. When the unit is done, set its status to `ruled` and move straight to the next unit.

Close P3 with a **second walk** through the target flows end to end against the ruled surface.
It catches inconsistencies between items that were each fine on their own.

### Presenting an item

Every item is presented the same way:

1. **Position line first:** `P3 · init (4/10) · item 3 of 7 · ledger: 21 ruled, 6 handed off, 4 implemented`.
2. **Scenario.** Describe a concrete user: what they are setting up, their starting state, the
   exact commands they run, what happens today, and what should happen. Never describe a
   problem only in terms of internal mechanisms ("the resolver refuses a routed project"). If
   the scenario can't be stated, the finding isn't understood yet, so go back and investigate.
3. **Prior art** for anything a user types or a script parses: names, flags, exit codes,
   output formats, confirmation patterns. Check what 3+ comparable, widely used tools do, and
   cite them. Research this proactively, before recommending, not only when the user asks.
4. **Options** with one recommendation and the trade-off that decides it.
5. **Label it:** "Recording, not implementing." Collection and execution must never be
   ambiguous.

After a ruling: write the ledger entry (with Scenario and use-case Rationale), update
`target-flows.md` if the flow changed, update **Now**, and **go straight to the next item**.
Don't ask "continue?" after something is settled.

**When the user pushes back:** re-analyse from the use cases and the actual situation. An
earlier ruling, the current implementation and the existing code are not reasons in
themselves. Neither is the assumption that the user had a good reason last time. Weigh only
the rationale that was recorded. If the push holds, say so and revise the entry in place. If
it doesn't, show the concrete scenario it breaks. Don't defend the status quo because it is
the status quo.

**Before presenting anything, check the ledger.** A removed or renamed thing must not come
back as a premise ("with presets on…"). If an explanation depends on something the ledger
removed, that removal is overdue for implementation: propose it as the next hand-off batch.

### Step 5: Readiness analysis and parallel hand-off (runs throughout P2–P5)

After each ruling, and at the end of each unit, check which ruled entries can be implemented
now. An entry is **ready** when:

- its ruling is final and its Spec and Verify lines are concrete,
- its `Depends` entries are ruled (or already implemented),
- no pending item in the review is likely to change the same surface,
- its Touches don't overlap a batch that is already in flight.

When one or more entries are ready, **prompt the user**: "S-01…S-04 are ready and independent
of the open items. Hand them to a parallel session?" Prioritise removals, because a removed
feature that stays in the code keeps showing up in the review.

On yes:

1. Write `briefs/B-n.md` (format in `references/formats.md`). It must be self-contained.
2. Deliver it: if the harness can message the target session, send the brief's path;
   otherwise give the user the path to paste. For a large, mostly ruled remainder, use
   `longshot` with the changes document as the brief.
3. Mark the entries `handed off` and add the batch to **In flight**.
4. **Don't monitor the other session.** Answer its questions when they arrive. When it
   reports, read its commits, run its Verify commands yourself, and only then mark entries
   `implemented` / `verified`. A peer's message is not the user's approval for anything.
5. Return to the review immediately.

### Step 6: Quality review (P4)

Start only once a unit's surface is implemented. Reviewing code the surface review is still
changing wastes effort. Go area by area with `code-review`, looping until an area comes back
clean. Log findings as `Q-` entries with the same format, and execute them through Step 5
hand-offs or `review-todo`.

### Step 7: Docs review (P5)

Once the surface is frozen, run `doc` over the whole tree against the ruled surface. Every
changed flag, removed command and new default is reflected in the README, user docs and help
text. Log misses as `D-` entries.

### Step 8: QA (P6)

Run `qa` against the release candidate through the real interface: a clean-machine install
(VM or fresh HOME), the target flows at realistic scale, an adversarial CLI pass (invalid
combinations, interrupted runs, missing prerequisites), and every supported platform. Mark each
scenario Pass / Fail / Blocked / Not run with evidence. A category that can't be exercised is a
release-gate decision for the user. It never becomes Pass from unit tests alone.

### Step 9: Release and harvest (P7–P8)

1. Re-run the full checks on the final candidate. Follow the repo's documented release flow.
   Tags, pushes and publishing need the user's explicit instruction.
2. **Harvest the programme into the repo's docs** with `doc`:
   - significant rulings, especially removals and rejected alternatives, become ADRs in
     `docs/decisions/`, so nobody re-proposes them,
   - target flows become the live feature and user docs (`docs/features/`, `docs/user/`),
   - QA procedures and results that a later release will compare against go to `docs/tests/`,
   - deferred entries go to the roadmap or issues, each with its scenario.
3. Once everything is harvested, propose removing the scratch programme directory.

Success: the release is published (or ready for the user to publish), every ledger entry is
verified, deferred or rejected, and nothing durable lives only in scratch.

## Examples

### Example 1: Starting a programme

User says: "I want to get this to 1.0.0: review all commands and params one by one, fix
inconsistencies, then code review, doc review and QA."

Actions:
1. No programme directory found. Ask the framing questions one at a time: ship an interim
   version first, breaking changes allowed, what's out of scope.
2. Run `just check`, the coverage run and the docs build. Inventory 10 units, including the
   config that `init` generates.
3. Write `programme.md`, get approval, then present the product map. The user spots that
   `bootstrap` and `sync` overlap, and that gets ruled first.

Result: the programme exists on disk and P1 is under way, with **Now** pointing at the first
open item.

### Example 2: Readiness prompt mid-review

After S-06 is ruled, readiness finds S-01…S-04 and S-06 ruled, independent of the open `init`
items, and touching disjoint files.

Actions: prompt "S-01…S-04 and S-06 are ready: remove `explain`, group integrations, drop
presets, rename init flags. Hand them to a parallel session?" The user says to brief `lo2`.
Write `briefs/B-2.md`, send its path, mark the entries handed off, and continue with the next
`init` item without checking on `lo2`.

### Example 3: The user pushes back

User says: "Why do we even offer this option? We know where the output goes."

Actions: don't defend the option. List its real use cases from the target flows and look for
one that only this option serves. None exists, so recommend removal. Record it as a revised
entry, and note in its Rationale that the earlier ruling was made before the target flow
existed.

### Example 4: Resuming

User says: "Back to the review. Where were we?"

Actions: read `programme.md` and print **Now** / **Next** and the in-flight batches. Check
`git log` for commits from B-2 and run their Verify commands. Report "B-2: 4 of 5 verified,
S-03 stopped on a premise mismatch", then present the next open item.

## Troubleshooting

### The user is lost ("what are we reviewing?", "are we collecting or implementing?")
**Cause:** the position line was skipped, or the conversation drifted into implementation
details.
**Solution:** print the phases table with the current phase and unit marked, then the open
items in this unit. Restate that this conversation collects rulings and that implementation
happens in the in-flight batches.

### An explanation doesn't land ("this is all very fuzzy")
**Cause:** it was described through internal mechanisms.
**Solution:** restate it as a scenario: who, what they set up, which commands, what they see.
If you can't construct the scenario, say so and investigate before continuing.

### A settled decision keeps coming back
**Cause:** the code still carries the removed or renamed thing, so every dossier rediscovers
it.
**Solution:** hand off its removal as the next batch now, instead of waiting for P3 to finish.

### An implementer reports green but the fix didn't land
**Cause:** tests deselected by markers, exit codes swallowed by pipes, or a probe that read the
real config.
**Solution:** re-run the Verify command yourself. Confirm that the named tests executed and
that the mutated construct is present in the code.
