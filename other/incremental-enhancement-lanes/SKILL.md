---
name: incremental-enhancement-lanes
description: Use when the user requests agents to improve several distinct areas in parallel over a fixed number of rounds, with a stack of PRs per lane left open for human review. For an existing issue dependency graph use workbench:orchestrate-issues; for one autonomous improvement use workbench:enhance.
---

# Incremental enhancement lanes

Requires git, Python 3.10+, authenticated GitHub CLI (`gh`), and background agents with worktree isolation. Read the bundled references relative to this skill directory.

The user has bought **breadth × depth**: several areas of the codebase improved
at once, each one deepened over a fixed number of rounds, delivered as stacks
they can review lane by lane and accept or drop whole.

```
<default branch>
 ├── lane/cli-ergonomics/r1 ──→ r2 ──→ r3     PR #101 ← #104 ← #109
 ├── lane/test-harness/r1 ────→ r2 ──→ r3     PR #102 ← #106 ← #110
 └── lane/error-paths/r1 ─────→ r2            PR #103 ← #107   (lane closed early)
```

**Lanes are breadth. Rounds are depth.** A lane is a standing charter over one
part of the repo; a round is one increment inside it, branched off the round
before it. Each round is a *fresh* subagent given the charter and told to pick
the most valuable thing it can build there — you don't hand it a spec, you hand
it a fence and the record of what's already been done inside it.

You are the loop, not the labour, and not the author of the increments.

## The one rule: you never implement

Not one edit to a source file, in any lane, including the round that "just needs
one line."

- **Your context has to outlast every lane and every round.** N lanes × R rounds
  is N×R implementers plus their reviewers. Each spends its budget reading and
  rewriting and then exits — that's the entire point of it being a subagent. Burn
  that context yourself and you get compacted mid-run, at which point you've
  forgotten which branch is which lane's tip and start stacking round 3 on round 1.
- **You're sitting in the wrong tree.** Implementers work in isolated worktrees
  so parallel lanes can't collide. Your checkout is not one of them; edits you
  make there are invisible to every lane and will fight the stacks.

The pull is strongest right after a reviewer reports a one-line fix. Send it back
to the implementer anyway — it still has the worktree and the reasoning.

**The one carve-out: preserving work is not authoring it.** If an implementer stalls or dies
holding uncommitted changes, committing them verbatim on its lane branch and pushing is loop
maintenance — you write no code, change no line, and decide nothing about the increment. Label the
commit as unreviewed and undescribed, and hand it to a fresh agent to evaluate. Losing hours of an
agent's work to protect the letter of this rule serves nobody.

## Step 1 — Preflight

### Resolve the ground

```bash
git -C . remote get-url origin      # what repo am I actually in?
gh repo view --json defaultBranchRef -q .defaultBranchRef.name  # resolve the default branch
```

Record the resolved default branch and pass it in every round-1 brief and stack-maintenance recipe.

`isolation: "worktree"` branches the repo *you* are running in. If that isn't the
target repo, clone it and run from the clone — otherwise every implementer in
every lane commits to the wrong repository and dies at first push, after doing
all the work.

Check the remote exists and you can push before dispatching anything. A run whose
output is supposed to be N stacks of PRs is worthless if there's nowhere to push;
find that out in one command, not in six simultaneous agent failures.

### Design the lanes

If the user named the lanes, use theirs. If they said "four lanes" and left the
scoping to you, or gave rough themes, you're designing them — and this is the
step that decides whether the run is worth anything.

**Read the trajectory first.** Read the README, the entry point, and the core
module until you could use the thing in your head, then read direction out of the
history:

```bash
git log --oneline -40
```

What keeps landing tells you what the project is trying to become. Lanes should
be places where that trend line has further to run — not an inventory of what
exists.

**Then partition by surface, not by theme.** This is the part that goes wrong.
"Performance", "error handling", and "observability" sound like three separate
lanes, and all three will edit the same hot module on round 1. Nothing merges
during this run, so all N stacks sit open against the default branch at once — two lanes
touching the same file hands the user a conflict pile and makes the second stack
unacceptable as a whole, which is exactly the outcome stacking was meant to
prevent.

So: draw the boundaries on the file tree first, then attach a theme to each
region. A charter names the paths it owns, and those path sets do not intersect.
Shared low-level files — a common types module, a config schema, a lockfile —
belong to at most one lane, and it's usually cleaner to declare them **unowned
and off-limits to everyone** than to give one lane a veto over the others.

A lane charter is four things:

```
SLUG:        cli-ergonomics                  # branch-safe, used in branch names
THEME:       what "better" means here, in a sentence or two
OWNS:        src/cli/**, tests/cli/**        # the only paths it may edit
OFF-LIMITS:  src/core/types.ts, package-lock.json, anything outside OWNS
```

Sanity-check each lane against two questions before proposing it:

- *Is there R rounds of real work here?* A lane with one good idea in it should
  be one round deep, not padded to three. Better to run three lanes at depth 3
  and one at depth 1 than to force filler. If that means proposing fewer rounds
  (or lanes) than the user asked for, say so in the contract with the reason —
  the yes they give should be to the run you'll actually do.
- *Would a maintainer recognize this as a coherent area?* Lanes cut across the
  grain of the codebase produce diffs nobody can review as a unit.

### Agree the run contract

Present the charters and these parameters together and get **one** explicit yes.
After that the run is unattended — this is the only gate, so make it count by
stating the volume plainly (N lanes × R rounds is N×R implementers and at least
that many reviewers; say the number).

| Parameter | Default | Notes |
|---|---|---|
| Lanes | 3 | Each with a charter as above. |
| Rounds | 2 | Depth per lane. Lanes may close early; they never run long. |
| Merge authority | **none** | This skill does not merge. Ever. Stacks are handed over open. |
| PR state | draft until reviewed, then ready | Draft first so CI runs before anything looks human-ready. |
| Fix rounds | 1 | **Per round, not per lane** — each round gets this many attempts to answer its review before the lane closes at the last round that passed. A lane that spends a fix round on round 3 starts round 4 with a fresh one. |
| Round barrier | off | Lanes advance independently as each round passes review. |
| Concurrency | all lanes at once | That's the point. Cap at 4-5 before the notifications get unreadable. |

Two things worth saying out loud when you propose it:

- **Nothing merges** is a feature, not a limitation. The user gets to accept a
  lane whole, drop a lane whole, or take the first two rounds of one and leave
  the third — which is only possible because each round is its own PR against the
  round before it.
- **Later rounds build on unreviewed-by-human code.** Round 3 is branched off
  round 2's branch. If round 1 was wrong, rounds 2 and 3 inherit it and the
  human can't cheaply excise the middle of a stack. That's why round 1 of each
  lane should be the most load-bearing, least speculative increment available —
  front-load the foundation and spend the ambition later.

## Step 2 — The round loop

For each lane independently, until it hits the round budget or closes:

1. **Dispatch** a fresh implementer for round *r*, based on the lane's current
   tip branch (the resolved default branch for r=1).
2. **Wait.** Background agents notify you; you don't poll.
3. **Review** the PR it opened (Step 4).
4. **Close the round** — on `PASS`, that branch becomes the lane's tip, the PR
   goes ready-for-review, and the ledger gets an entry (Step 5).
5. If rounds remain and the lane isn't closed, go to 1 with `r+1`.

Lanes do not wait for each other. Lane A's round 3 can be in flight while lane
C is still on round 1 — they're independent stacks and a barrier just wastes
wall-clock. Keep a table of `lane → round → branch → PR → state` and update it
as notifications arrive; that table is the thing you report from.

### The lane ledger

Every round is a fresh agent with no memory of the previous ones. What carries
continuity is the ledger you maintain per lane and paste into each brief:

```
Round 1 — [#101] Added --json to every read command. Verified: make test.
          NOTED: the error paths print to stdout, which breaks --json consumers.
Round 2 — [#104] Moved diagnostics to stderr and added exit codes. Verified: make test.
          NOTED: no shell completion; the flag surface is now big enough to want it.
```

This is doing more work than it looks like. Without it, round 2 re-derives round
1's idea from scratch — the most obvious increment in a lane stays the most
obvious one — and burns a whole agent discovering it's already done. And the
`NOTED` lines are the real payload: an out-of-scope observation from round 1 is
frequently round 2's best candidate, because it was found by someone with their
hands in the code rather than by you reading from outside.

Keep the ledger factual. Ship it verbatim from the implementers' reports rather
than paraphrasing — your summary of what round 1 did is exactly the artifact
round 2 shouldn't be trusting over the code in front of it.

## Step 3 — Dispatch a round

Dispatch with the Agent tool: `run_in_background: true`, `isolation: "worktree"`,
`name: "lane-<slug>-r<n>"` so you can message it during fix rounds.

Build the brief from `references/lane-briefs.md`. Fill every placeholder — a
brief with a hole in it becomes a background agent asking you questions, which
defeats the point. The brief carries:

- the **charter** (theme, OWNS, OFF-LIMITS) verbatim
- the **base branch** and the branch to create: `lane/<slug>/r<n>`
- the **ledger** for this lane so far
- **what the other lanes own**, so it knows which parts of the repo are somebody
  else's and won't wander in
- the instruction to **declare its increment in the PR body** before anyone
  reviews it

That last one is the hinge of this whole design. Nobody wrote a spec for this
round — the agent chose the work. So the agent has to state what it chose, in a
form the reviewer can hold it to:

```
GOAL:         one paragraph, concrete enough to be unambiguous
WHY:          what it noticed that made this the right next increment here
DONE WHEN:    observable outcome + the exact command that verifies it
NOT IN SCOPE: the adjacent things this deliberately doesn't touch
```

Without that, the reviewer has nothing to review *against* and degrades into a
general code-quality opinion, which is not what protects a stack.

**One increment per round.** A round is a diff a reviewer reads in a single pass.
If the agent's best idea needs three, it takes the first slice that stands alone
and puts the rest in `NOTED` for the next round — which is the mechanism by
which rounds compound instead of sprawling.

## Step 4 — Review the round

When an implementer reports back, dispatch a reviewer against its PR:
`run_in_background: true`, `name: "review-<slug>-r<n>"`, no worktree. Brief in
`references/lane-briefs.md`.

The reviewer answers three questions and nothing else — plus, when the round warrants it, one
more placed *above* them.

**Question zero.** When a round stands on a single checkable claim, name it and make the reviewer
answer it first: a premise correction, an invariant, a "nothing about the output changed" claim, a
migration that must not lose data, a recorded sample that must not be falsified. Say what makes it
load-bearing and what a wrong answer would cost, and tell the reviewer to verify it *by
construction with its own harness*, not by reading and not by trusting the author's harness. This
is where the expensive findings come from — a store bricked by a real kill, a race that
misattributes a record, a fixture in a format the code cannot emit. Skip it when the round has no
such claim; a review asking six questions answers all of them worse.

Then the standing three:

1. **Does the diff deliver the increment the PR declared** — all of it? PR
   descriptions routinely claim more than the diff delivers; that gap is the
   main thing this review exists to catch.
2. **Did it stay inside the lane's OWNS paths?** An out-of-lane edit is the
   expensive failure here — it's invisible in a single PR and only detonates when
   the user tries to merge two stacks.
3. **Is this sound enough to build the next round on?** Round r+1 branches off
   this exact commit. That's a narrower question than "is this good code" — it's
   about whether the foundation holds, not whether you'd have written it this way.

It returns `PASS` or `CHANGES_REQUIRED` with located findings.

**On `CHANGES_REQUIRED`:** send the findings to the same implementer with
`SendMessage` (`to: "lane-<slug>-r<n>"`). It still has the worktree, the branch
and the reasoning. Re-run the reviewer after the fix. Past the agreed fix-round
count, **close the lane** — leave the PRs that passed, note the failed round on
the stack's last good PR, and let the other lanes keep running. A stack that
stops at round 2 of 3 is a fine outcome; a round 3 built on a round 2 nobody
could get to pass is not.

If the implementer has already exited and can't be messaged, dispatch a fresh one
with the findings *and* the branch as its starting point.

## Step 5 — Close the round

On `PASS`:

```bash
gh pr ready <pr> --repo OWNER/REPO
gh pr checks <pr> --repo OWNER/REPO --watch     # skip if the repo has no checks
```

Red CI is not a review question — send failures back to the implementer the same
way findings go back. Do **not** merge. The stack stays open; that's the
deliverable.

Then update the lane's tip to this branch and append the ledger entry. The next
round bases on it.

If a lane's next round has nothing worth building — the charter's genuinely
exhausted — **close the lane at its current depth**. An empty round is a better
outcome than a filler round: hygiene work, a config knob nothing consumes, or a
refactor with no user on the other end costs the user a review slot and dilutes
the stack they were going to accept whole. The bar for declaring exhaustion is
high, though; if the implementer reports "nothing left here" on round 2 of 3,
that usually means it stopped generating candidates early, and the honest move is
one more round with the ledger's `NOTED` items named explicitly in the brief.

### Depth is its own stopping criterion

Exhaustion isn't only "no work left." On an open-ended run the constraint moves: past roughly four
rounds, a lane usually still has candidates, but the marginal round is worth less to the user than
the review time it costs — they now have to read four PRs before reaching it. Watch for the tell:
several consecutive rounds declining the *same* small items, each unable to name a user for them.

Two things follow. Put the cost in the brief — past ~4 rounds, tell the implementer that *"fine,
but I'd have taken the lane without it"* is the **default verdict** unless it can beat it, and that
declaring exhaustion costs nothing. And tell the user plainly that the binding constraint has moved
from work-remaining to review-capacity, with a recommendation that follows from it: once the tell
is showing, that recommendation is **close the lane at its current depth**. Don't soften it into
"send one more and stop if it comes back empty" — that spends another review slot to confirm what
the declining rounds already showed. If they've asked for open-ended rounds, that instruction
stands until they change it: say the stop recommendation plainly, hold the next dispatch for their
answer, and if they say continue, send it with the raised bar above. Don't unilaterally stop; if
you do stop a lane, say it was your call and offer to resume.

A round that clears the bar this late usually does so by correcting a premise rather than by
finding new work — the last real increment in a lane is often the one that shows an earlier
"can't be done without X" was wrong.

## Step 6 — Report

Between rounds, a status line is enough: which lane advanced, to what, what's in
flight.

At the end, give the user the map they have to review:

- **Per lane**: the charter one-liner, then each round as `PR #n — what it did`,
  in stack order, with the base of each so the review order is obvious
- **Where to start**: bottom of each stack, since the top can't be read without it
- **Lanes that closed early**, and why — exhausted, or failed review
- **Cross-lane notes**: anything two lanes both touched, anything a lane flagged
  as belonging outside its charter
- **What a human now owns**: every merge decision, which is all of them

Report only what you actually did. "Three lanes dispatched and round 1 is up" is
a claim about the state of GitHub, and it's either true or it's something you'll
believe yourself next round and stack on top of. If you're unsure whether a PR
opened, check — `scripts/lanes.py` is cheap and your memory of an unattended run
is not evidence.

## When things go wrong

- **You get compacted mid-run.** The repo is your state, not your memory.
  `python3 "${CLAUDE_PLUGIN_ROOT}/skills/incremental-enhancement-lanes/scripts/lanes.py" --repo OWNER/REPO` reconstructs every lane
  from branch names and open PRs: rounds, bases, tips, and any broken chain.
  Rebuild the table from that and continue.
- **A round's PR targets the wrong base.** The stack is broken and the diffs will
  read as duplicates of each other. Retarget it (`gh pr edit <pr> --base
  lane/<slug>/r<n-1>`) rather than letting a reviewer read a diff containing three
  rounds of work.
- **An implementer dies or returns nothing.** Its `Agent` result is null. Don't
  read its transcript — the `.output` file is a symlink to the full JSONL and will
  flood your context. Check whether a branch or draft PR survived, then
  re-dispatch that round from there.
- **An implementer is alive but stalled**, running far longer than its peers with nothing
  pushed. This is worse than a death, because the work is still hostage. Diagnose without
  disturbing it — its worktree is `.claude/worktrees/agent-<id>`:
  ```bash
  git -C <worktree> status --porcelain          # is there uncommitted work?
  git -C <worktree> diff --stat <lane-tip>      # how much, and in which files?
  stat -f "%Sm %N" -t "%H:%M:%S" <worktree>/<owned-paths>/*   # when did files last change?
  ```
  Stale mtimes plus a running agent means stalled, not working. Message it once with a concrete,
  ordered instruction naming what you found on disk — that alone sometimes lands it. If nothing
  changes: commit its work verbatim (tracked files only; leave scratch directories untracked),
  push the lane branch, `TaskStop` it, and dispatch a fresh agent with the inheritance and
  **explicit permission to discard it**. Tell that agent the previous author's judgement is not
  evidence — a long silent run may mean excellent work or a lost agent, and it is the first to
  actually look. A rejected inheritance is a real answer.
- **A lane edits outside its OWNS paths.** Caught by review; send it back. If it's
  already in a merged-into-tip round, say so explicitly in the final report — the
  user needs to know which two stacks now conflict before they start merging.
- **The user merges a mid-stack PR while the run is going.** GitHub retargets the
  child PR onto the merged PR's base. Confirm the lane's remaining rounds still
  chain correctly and rebase the tip if not; `references/stacking.md` has the
  recipes.
- **Two lanes propose the same idea.** They're both reading the same trend line.
  Give the second one the first's declared increment in its brief and let it pick
  again — that's a charter overlap you drew, not an agent failure.

## Reference files

- `references/lane-briefs.md` — the implementer, fix-round, and reviewer briefs.
  Read before the first dispatch.
- `references/stacking.md` — `gh`/`git` recipes for stacked PRs: opening onto a
  parent branch, rebasing a stack, retargeting after a mid-stack merge, and
  handing the finished stacks over.
- `scripts/lanes.py` — reconstructs lane state from the remote. Use it to resume
  after compaction and to verify claims before reporting them.
