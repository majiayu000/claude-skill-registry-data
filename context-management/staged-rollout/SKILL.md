---
name: staged-rollout
description: Run a large build as many small, resumable sessions by decomposing it into a `.plan/` folder of dependency-ordered stages with an evidence ledger, then executing one stage per fresh session. Use when the user says "this is too big for one session", "plan a staged rollout", or describes a multi-day build that needs cross-session progress tracking.
---

# Staged rollout

Run a large build as **many small sessions, not one huge one.** Decompose the
work once into dependency-ordered stages in a `.plan/` folder, then execute one
stage per fresh session. Context can't accumulate across stages because sessions
don't share it; the plan can't drift because every decision lives in exactly one
place; progress is a glanceable ledger, not a transcript.

The file formats are in `references/templates/` (`PLAN.md`, `LEDGER.md`,
`stage-N.md`, `stage-f-review.md`, `README.md`, `RUNNER.md`) — copy those
verbatim for structure, then fill every `<placeholder>` when scaffolding.
`RUNNER.md` is the stage-runner contract scaffolded into each plan so any
session — cloud included, where this plugin does not load — can run a stage
cold from a one-line instruction pointing at `.plan/RUNNER.md`. This file is the
*method*: when to use it, how to decompose, how to set flags. Don't restate
the templates here.

## When to use it

All of these true: the work spans multiple sessions (hours/days, roughly four+
sessions of work); it decomposes into ordered units with dependencies; you want
to stop and resume freely; you care about keeping per-session token cost flat;
and the design is settle-able (there are decisions worth freezing).

## When NOT to use it

- **Work that fits in one to three sessions.** The scaffold has a floor cost;
  below ~four sessions, just do the work.
- **Exploratory work with no settle-able design.** If every session would
  legitimately rewrite the frozen decisions, there's nothing to freeze yet.
- **Work that can't be decomposed.** One giant inseparable step gains nothing
  from a ledger around it.

Two honest limits even when it fits: decomposition quality gates everything (bad
stage boundaries cause cross-stage churn no protocol fixes — the final review
stage catches what leaks, but it can't un-tangle a bad split); and fresh
sessions only know what was written down (note discipline replaces the tacit
context a long session would carry).

## Core principles

1. **Single source of truth, referenced not copied.** All durable decisions live
   in `PLAN.md` as *frozen decisions*. Stage files and prompts point at it; they
   never restate it. Copies are what drift — a decision that exists in one place
   cannot diverge.
2. **Session-per-stage = free context control.** The primary token-control
   mechanism isn't subagents or clever prompting — it's that each stage is small
   and runs in its own fresh session. Cost per stage is flat
   (`O(PLAN.md + stage file + ledger table)`), no matter how many stages came
   before. No compaction spiral.
3. **The ledger is the resume point *and* the memory.** `LEDGER.md` holds
   per-stage status plus as-built notes, so "where were we?" is a 10-line table,
   and a later stage can catch a regression an earlier one introduced because the
   earlier stage's assumptions were written down.
4. **Verify before done.** A stage is done when its acceptance check *ran* and
   the real output is pasted into the ledger — not when the model claims success.
   Evidence, not assertion.

## Decomposing the work

- **Smallest sensible stage.** If a unit has two genuinely different mechanisms,
  or a design-heavy part plus mechanical parts, split it.
- **Group by effort, not just by feature.** Several near-identical mechanical
  units can be one stage; a single design-heavy unit deserves its own.
- **Keystone as S0.** Identify the piece with no prerequisites that everything
  else needs, make it S0, and gate the rest behind it.
- **`depends` is a graph, not a queue.** An edge means "cannot safely start
  until", not "written after". Serialising by habit — writing
  `S0 → S1 → S2 → S3` where the truth is `S0 → {S1, S2, S3}` — is the most
  expensive decomposition mistake available here, because the index still
  reads as correct while the plan takes three rounds instead of two. For every
  edge, name the artifact the dependent stage consumes; if you can't name one,
  drop the edge.
- **Every stage changes something or feeds a stage that does.** A stage whose
  only output is a finding, a verification or documentation — "confirm X",
  "investigate Y", "record Z" — earns its place only when a later stage lists
  it in `depends` and names what it consumes from it. No consumer: fold the
  investigation into the stage that would act on it, or drop it. A finding
  that nothing downstream uses spends a session and changes nothing. The
  standing review stage is the one exception, because its three outcomes are
  themselves actions.
- **Group by gate.** Alongside "group by effort": put the `gate: human`
  stages — the ones where frozen decisions get settled or amended, or whose
  acceptance needs a person — at the **front** of the dependency graph, and
  the review stage at the **end**; keep the middle mechanical, `gate: auto`
  and (when the plan opts in) `merge: auto`. Never interleave a human gate
  between two auto stages unless a dependency edge genuinely forces it: an
  unattended runner stops at every `human` stage, so a human gate in the
  middle of an auto run cuts the run in two for no reason. Decisions that only
  surface mid-build still go through `blocked` (see *Statuses and human-gated
  stages*) — the rule shapes the graph, it doesn't forbid surprises.
- **Standing final review stage.** Always append `SF: plan review` as the last
  stage (see below), scaffolded from `stage-f-review.md`. Bootstrap adds it;
  it's not optional.

## Flag heuristics

Each stage declares `depends` / `mode` / `exec` / `model` / `effort` / `gate`
in the **PLAN.md stage index** — the single authoritative home for these
flags, read by `/stage-run`'s weight check and the runnable-set logic both
commands share. The plan as
a whole declares two more, `merge` and `plan-dir`, on the **plan flags** line
directly under that index — those two are the plan's *declared defaults*, the
answers an unattended session applies where an interactive one would ask (see
*Unattended mode*). Stage files never restate any of them. The **process**
defaults are deliberately cheap — escalate `mode`, `exec` and `gate` only
where a stage genuinely warrants it. `model`/`effort` are not among them:
those are sized to finish the stage, not to be minimised (see below).

- `mode: direct` by default (state a one-line plan, implement). Use `brainstorm`
  only where the stage has real open design choices. A full brainstorm on a
  mechanical one-liner is pure ceremony.
- `exec: inline` by default. Session-per-stage already isolates context, so
  reserve `subagent(<model>)` for churn-heavy stages (lots of iteration, config,
  debugging) where dispatching keeps the churn out of the orchestrator's context.
- `model`/`effort` are **launch hints**, not switches the agent can flip
  mid-session. Both are verifiable: the model from the session itself, and the
  effort level from `CLAUDE_EFFORT` in the environment — so state what is
  actually set rather than restating the flag as a reminder. When that variable
  is absent, say the effort could not be read instead of assuming it matched.
  Pick the tier that would
  carry the stage to its **exit criteria without the session having to
  escalate** — not the cheapest tier that could plausibly start it. A stage
  that stalls and gets re-run costs more than the tier it saved, and because
  the re-run happens in a fresh session the plan never records that it
  happened. **Where two tiers are arguable, take the higher one.** Reserve the
  top model for the keystone and the one or two design-heavy stages; much
  staged work still lands at `low`/`med` effort, but that is an observation
  about past plans, not a target this one should hit.
- `gate: auto` by default. `gate` says whether a stage may be **launched
  unattended** — by an orchestrator session that fires stages back-to-back
  with nobody watching them run (see `references/remote-driver.md`); this flag
  is the contract it reads. A `gate: human` or `gate: local` stage is
  never launched unattended: the orchestrator stops in front of it and
  reports rather than firing, and a session
  that finds itself running one unattended (see *Statuses and human-gated
  stages*) reports and stops rather than starting it. Mark `human` where a
  person must be present for the stage to get anywhere: every
  `mode: brainstorm` stage (a design pass is a conversation), and any stage
  whose acceptance needs a human's eyes or hands (a visual check, a GUI-only
  action, a credential). Mark `local` where the stage needs a resource only
  the local machine has, known at authoring time — local hardware, a
  LAN-only host, a secret not committed anywhere reachable, or a
  locally-installed toolchain. The two gates are independent: the driver
  refuses either exactly the same way, but for a different reason — `human`
  because nobody is watching, `local` because the driver could be running
  anywhere but the machine the stage needs. A stage that only discovers this
  mid-run, with nothing declared up front, uses the `needs-local` blocked
  reason instead (*Statuses and human-gated stages*, below). **Why `auto` is
  the default and not `human`:** the flag changes nothing until something
  runs stages unattended — today, and for any plan that never adopts a
  driver, `merge: manual` already stops at every merge whatever `gate` says,
  so an `auto` default costs existing plans nothing and keeps a fresh plan
  closest to today's fully-manual experience. The conservative alternative
  (`human` by default, opt stages *into* unattended) would make bootstrap
  upgrade every mechanical stage by hand instead of downgrading the few that
  need a person; it was considered and is the right call only if unattended
  runs turn out to misfire on stages that looked mechanical at decomposition.
  An **absent** `gate` column reads as `auto` — plans written before the flag
  existed need no edit.
- `merge: manual` by default — **plan-level, not per-stage.** `merge` says
  what happens to a stage PR once it is open: under `manual` the session
  offers the merge and waits for your OK (today's behaviour, unchanged);
  under `auto` it merges the stage PR into the plan branch itself — still a
  squash, still only after the sibling re-sync check, and only once every
  required check is green — then carries straight on to the `done` write and
  teardown. `auto` is opt-in because any other default would silently change
  the merge behaviour of every plan that predates the flag, and it governs
  **stage PRs only**: the plan→main PR is manual in every mode, with no
  override (see *Git model*). An **absent** plan-flags line reads as
  `merge: manual`.
- `plan-dir: delete` by default — **plan-level, and read only at closeout.**
  `plan-dir` says what happens to `.plan/` when the plan is closed: under
  `delete` it goes as the last commit on the plan branch (nothing is lost —
  the full plan history stays in git, and the final PR shows the removal);
  under `keep` it stays, for a project where the plan doubles as its
  documentation. This is the answer `/plan-close` already calls its default,
  written down in advance so an unattended closeout has it — an interactive
  closeout still asks, with this value as the recommendation. An **absent**
  `plan-dir` entry reads as `delete`, so nothing changes for a plan that
  predates the flag.

## Model weight tiers

Every weight check (bootstrap's gate, a stage's `model` comparison) needs a
mechanical rule for "is this session heavy enough" — not the model's own guess
about itself. Maintain this tier list as model families evolve, and place a new
family by its capability and price, not by where its name sorts:

- **Top tier ("Opus-class"):** the Opus generation (e.g. `claude-opus-*`), plus
  any frontier family positioned at or above it (e.g. `claude-fable-*`).
- **Mid tier ("Sonnet-class"):** the Sonnet generation (e.g. `claude-sonnet-*`).
- **Light tier ("Haiku-class"):** the Haiku generation (e.g. `claude-haiku-*`).

**Fail-safe:** if the session's disclosed model ID or name doesn't recognizably
match a tier above — an unfamiliar family, a third-party model, a future rename —
do not guess which tier it belongs to. State the exact model ID/name from the
system prompt and ask the user which tier applies, rather than silently passing
or failing the gate.

## Parallel stages

`depends` is a real dependency graph, so more than one stage is often runnable
at once. Three rules keep that an advantage rather than a source of confusion:

- **Derive, never store.** The runnable set, the waves, and the critical path
  are *views* of the `depends` column, computed on demand — by bootstrap's
  post-decomposition summary and by every stage's end announcement. Do **not**
  add a `wave` or `parallel-group` column to the stage index: that would be a
  second copy of the graph, and principle 1 exists precisely because copies
  drift.
- **Report the set; don't launch it.** The deliverable is telling the operator
  what *can* overlap — every `todo` stage whose `depends` are all `done` or
  `skipped`, each
  with its command, recommended model/effort and `gate`. Starting them is the
  operator's action, one session per stage — or an orchestrator's, firing
  cloud stages and honouring `gate`. In the desktop app a stage can *offer*
  each one as a suggestion chip, but the click is still the operator's: the
  chip cannot pick its launch mode, model or effort, and it exists nowhere
  else (not on a phone, not in a terminal), so the printed command stays the
  handoff every surface can use.
- **Separate working trees are what make it physical.** The semantics below
  make concurrent sessions *safe*; worktree-per-stage (see *Git model*) makes
  them *possible*. Two sessions sharing one working tree fight over `HEAD`
  whatever the merge rules say.

Four semantics are what make concurrent sessions safe rather than merely
possible. They are specified in full in the template `PLAN.md`, which owns the
operating protocol; the reasoning behind them is the method:

- **The plan branch is the serialization point.** Parallel stage PRs merge one
  at a time, first come first served. The second merger syncs the plan branch
  *into* its stage branch and re-runs the acceptance check — "mergeable" means
  no textual conflict, not that the stage still passes. Squash merge makes
  that free (the merge commit is discarded), which is why a stage branch is
  never rebased or force-pushed.
- **A sibling's stage branch is not drift.** Preflight classifies by *whose*
  stage a mismatch belongs to instead of halting on any `todo` row with a
  committed branch — otherwise every parallel session stops the moment a
  second one starts. Real drift on the stage you are running still stops you,
  and a genuinely crashed stage stays visible in every later preflight report
  and in closeout's gate.
- **Shared write territory is a `depends` edge, not a new field.** Two stages
  that write the same files are not independent, whatever the feature graph
  says, and `depends` is the only place that can say so. A dedicated
  "territory" field would be a second record of one constraint — a second
  thing to drift.
- **The `done` ledger write races.** It is a direct commit on the plan branch,
  so two sessions finishing together collide there: replay the commit on
  rejection, keep both rows on conflict, never force-push the plan branch.

**Is `exec: subagent(<model>)` fan-out an alternative to parallel sessions?**
Only *inside* a stage — never as a substitute for them. Dispatching a whole
wave from one orchestrator does sidestep git concurrency, but it collapses N
stages into one: a single branch, PR, ledger row, and acceptance check
covering work the decomposition deliberately kept separate (git semantics 1
and 3) — and the orchestrator accumulates every subagent's return, so
per-session cost stops being flat and principle 2, the mechanism the whole
method rests on, goes with it. For a wave of cheap mechanical stages the
honest options are therefore: run them as N sessions (the supported answer),
or decide at **decomposition** time that they were really one stage, merge
them, and let `exec: subagent(<model>)` absorb the churn within it. That is a
decomposition decision, not an execution one — "group by effort, not just by
feature" already points at it.

## Statuses and human-gated stages

Statuses are `todo → doing → done`, plus `blocked` and `skipped` (full lifecycle
and the checkbox resume mechanism are in the templates). Two are worth calling
out as method, not just vocabulary:

- **`blocked`** is a first-class state, not a failure. A stage that hits a gate
  only a human or an external system can clear (a GUI-only action, a credential,
  an approval) is best written as a **runbook**: produce exact step-by-step
  instructions plus the verification check, mark the stage `blocked`/`doing`, and
  let the human complete it. Never fake progress past a gate. **Where that
  record is committed** is settled once, in the template `PLAN.md`'s operating
  protocol under *Recording a block* — on the plan branch directly when the
  block predates the stage branch, and on the stage branch plus a
  `.plan/BLOCKED.md` section on the plan branch once it exists. That is the
  single source of truth for the rule. Neither this skill nor `/stage-run`
  restates it — they only name which side of it a given decision point falls
  on. **`needs-local`** is the reason value for one specific case: a stage
  that discovers *mid-run* — nothing declared as `gate: local` up front —
  that it needs a resource only the local machine has. Same `blocked` state,
  same commit rule, but the one-line reason is the literal token
  `needs-local` rather than free text, so an orchestrator's report can
  say "re-run this stage locally" instead of a generic failure (`PLAN.md`,
  *Recording a block*, "The discovered case").
- **Unattended, a stage question that has no declared default becomes
  `blocked`.** Mark the stage `blocked` with a runbook stating the question
  and what would unblock it, commit that where *Recording a block* says, and
  stop. This is the existing
  state and the existing mechanism, not new machinery; the only rule
  unattended mode adds is that waiting on an answer is not an option, because
  there is nobody to give one. The human answers later by amending the frozen
  decisions or the ledger and relaunching the stage. Which questions have a
  declared default and which are hard stops is the table in *Unattended
  mode*, below.
- **`skipped`** records a one-line reason for work decided against, so the gap is
  a decision, not a silent hole. It satisfies a dependent's `depends` exactly
  like `done` — the runnable set never deadlocks on a stage that was
  deliberately dropped. If the skipped stage owned acceptance or verification
  work (a check nothing else covers), say so in the same note: that coverage
  is now unowned, and the final review stage (`SF`) is where it gets
  reassigned or explicitly accepted as a gap — never silently lost.

Track known gaps and latent hazards explicitly in the ledger notes (things not
under version control, footguns, "this script would delete X if run") — writing
them down is what stops them becoming surprises, and it's what lets the final
review stage catch them.

## Unattended mode

**One mode, one rule, honoured at every decision point.** A session is
unattended when nobody can answer it: a command was told so explicitly with its
`--unattended` argument, or its opening prompt says so in plain words. That
last path is how a **cloud** session enters this mode: plugins do not load in
cloud containers, so there is no command and no argument to carry the flag —
the orchestrator that fired the stage (see `references/remote-driver.md`)
states it in the prompt instead. However a session
learns it, the contract below is identical. That argument is a single switch selecting **declared
default over ask** — never "proceed anyway". Interactive sessions keep asking
exactly as they always have, and one body of skill text serves both modes. A
fork into interactive and unattended copies is the anti-pattern this contract
exists to prevent: two bodies means every protocol change made twice, and the
seams between the modes are subtle enough that the second copy would be the
one that rots.

Every question the protocol can put to a person is classified once, as one of
two kinds:

- **Declared default.** The answer is fixed ahead of the run — written on
  `PLAN.md`'s **plan flags** line (`merge`, `plan-dir`), or a mechanical rule
  that needs no answer at all. An unattended session applies it and carries
  on; an interactive one still asks, with the declared value as the
  recommendation.
- **Hard stop.** There is no defensible default, so an unattended session
  does not invent one. It records the question where the next session will
  find it — the stage row marked `blocked` with a runbook, committed where
  *Recording a block* says so it is readable without waiting for a merge, or,
  where no stage row owns the question, a report naming the exact state and the
  command that clears it — and ends. Nothing is faked past a gate and nothing
  is retried.

| Decision point | Interactive | Unattended |
|---|---|---|
| A `gate: human` stage | announced — the person at the keyboard *is* the gate | **hard stop**, never started |
| A `gate: local` stage | announced — running it here means this session already has what it needs | **hard stop**, never started |
| Weight check: lighter model than recommended, or a readable effort that differs from the flag | **hard stop** — relaunch named, nothing written | **hard stop** — `blocked` + runbook |
| Weight check: an unrecognised tier | asked which tier applies | **hard stop** — `blocked` + runbook |
| A mid-stage question the frozen decisions don't settle | asked | **hard stop** — `blocked` + runbook |
| Redo of a `done` stage | confirmed first | **hard stop** — `blocked` + runbook |
| A stage PR's merge | offered | `merge` flag — `auto` merges it, `manual` is a **hard stop** |
| Checking out the plan branch to reach `.plan/` | offered | default: check it out when exactly one plan branch matches; two or more is a **hard stop** |
| A stage worktree still present at closeout | offered for removal when its branch is merged and nothing is unpushed | removed on that same condition; anything else is a **hard stop** |
| Deleting `.plan/` at closeout | asked | `plan-dir` flag |
| Merging the plan→main PR | the PR is proposed; you merge it | the PR is opened; you merge it — **no session merges it in any mode**, no flag, no override |

Every **`blocked` + runbook** cell above means the record *Recording a block*
defines. The weight-check and redo hard stops fire before the stage branch
exists, so they commit straight onto the plan branch; a mid-stage question
fires after it does, so it lands on the stage branch and is announced on the
plan branch through `.plan/BLOCKED.md`. The distinction matters more unattended
than anywhere else: a runbook left on an unmerged branch with nothing on the
plan branch pointing at it is one the next pass never reads.

**What no mode loosens.** The plan→main PR is opened by closeout and merged
by a person, always. A `gate: human` stage is never launched unattended, and
neither is a `gate: local` one — same refusal, different reason. A
worktree holding real uncommitted or unpushed work is never removed, and never
with `--force`. A merge the platform refuses is never forced or retried.

**Bootstrap has no unattended mode, deliberately.** `/plan-stages` is design
work — decomposition, frozen decisions, the `merge` question — and those have
no defensible defaults to declare. A plan decomposed badly costs far more than
the session it would have saved. Where a plan genuinely needs to be bootstrapped
headless, a fully-specified brief that says to make every decision and ask
nothing does the job as an ordinary prompt; that route needs no contract behind
it.

## Git model

**Branch-per-stage in a worktree-per-stage is the only supported model** —
it's the model this plugin was built with, and there is no alternative to
choose at bootstrap:

```
main
 └── plan-<slug>                      ← plan branch; .plan/ lives here
      ├── plan-<slug>-s0 → PR → plan-<slug>   (squash merge)
      ├── plan-<slug>-s1 → PR → plan-<slug>   (squash merge)
      └── ...
plan-<slug> → final PR → main         ← at closeout (normal merge)
```

**`.plan/` must be tracked, and the plan branch must have an upstream.** Both
are load-bearing invariants, not tidiness. An untracked (or `.gitignore`d)
`.plan/` breaks the model in two ways at once: a stage whose only artifacts are
decisions or documentation produces nothing to commit, so it can never open the
PR that semantics 3–4 below require, and every stage depending on it deadlocks
on an unsatisfiable gate; and the whole decision record lives only in a working
directory that a `git clean` or a deleted worktree takes with it. A local-only
plan branch is the quieter version of the same failure — the preflight's fetch
and fast-forward both succeed and do nothing, forever. Bootstrap refuses to
scaffold into an ignored path and pushes the plan branch with an upstream;
every stage preflight re-checks both.

Seven frozen semantics:

1. **One branch per stage**, cut from the plan branch (`plan-<slug>`) — no
   exceptions. Uniformity keeps each unit reviewable in isolation and contains
   the classic failure where "one small commit" quietly becomes twenty commits
   of fixes bleeding into shared history.
2. **Commits are compulsory and incremental** — commit at logical units as the
   stage progresses, not a single commit at stage end. Every stage has
   something to commit: the ledger evidence and any frozen-decision amendment
   are tracked files, so even a decision-only stage lands a real commit and a
   real PR.
3. **A stage PR into the plan branch is compulsory** — the finish protocol
   creates it; it is never "offered" as optional.
4. **A stage cannot be closed (marked `done`) until its PR is merged** into
   the plan branch.
5. **After the merge, return to the clone and fast-forward** the plan branch
   before the session ends — the clone is already on it, so there is no
   checkout — and record the stage `done` in the ledger there: the `done`
   edit is committed on the plan branch after the merge, never on the stage
   branch, so a `done` row is always visible from a synced plan branch.
6. **Merge type is fixed by position:** each stage PR is **squash-merged** into
   the plan branch (one clean commit per stage, no intra-stage churn on the plan
   branch); the final PR from the plan branch into `main` is a **normal
   (non-squash) merge**, so every stage lands on `main` as its own distinct
   commit and the as-built history survives. **This is the one rule the plan
   cannot enforce**, because it is the one merge no session performs: the
   person merging gets the repo's default merge button, and a default of
   "Squash and merge" collapses every stage into one commit on `main` while
   still looking like a clean, successful merge. Set the repo's default to
   "Create a merge commit" when the plan is set up — that is the only real
   control; closeout naming the merge type in the PR body is a reminder.
7. **One worktree per stage, and the clone never leaves the plan branch.** A
   stage branch is checked out only in its own sibling worktree
   (`../<repo>-s<N>`); the main clone stays parked on `plan-<slug>` for the
   life of the plan. See *Worktree-per-stage* below.

Also: **flat branch names** (`plan-<slug>-s3`, not `plan/<slug>/s3`) — git
refs can't nest a branch under an existing branch name. And **push freely,
offer merges**: stage and plan branches are feature branches — the agent
creates and **pushes** them without asking, and **opens** the stage PR into
the plan branch as part of the compulsory finish protocol, but **offers** the
merge for your OK — it never merges without your OK, never pushes to `main`,
and the final PR to `main` is always yours to merge.

**The one carve-out: `merge: auto`.** A plan that sets `merge: auto` on its
plan-flags line (see *Flag heuristics*) has given that OK **in advance, for
stage PRs only** — so under `auto` the session squash-merges its own stage PR
into the plan branch once the sibling re-sync check has run and every required
check is green, and continues to the `done` write and teardown without
stopping. Nothing else loosens: the merge is still a squash, the re-sync rule
still applies, and a merge that GitHub refuses (a red or missing check, a
branch-protection rule the plan branch carries) is **not** retried or forced —
the session leaves the row `doing`, reports the refusal and why, and ends; the
next preflight completes the bookkeeping once a person merges it, exactly as
when a merge is declined today. **The plan→main PR is manual in every mode.**
`merge` is never read at closeout, and no value of it — nor any future flag —
creates a path that merges into `main` without a person's explicit OK. That is
the one human gate that survives even a fully unattended plan.

### Worktree-per-stage

**The clone holds the plan; worktrees hold the work.** The main clone is
permanently parked on `plan-<slug>` — that is the only branch ever checked out
there. Every stage branch lives in its own sibling worktree, created from the
plan branch tip:

```
~/src/
  hive/        ← main clone, always on plan-<slug>, holds .plan/
  hive-s1/     ← worktree, branch plan-<slug>-s1
  hive-s3/     ← worktree, branch plan-<slug>-s3   (concurrent)
```

This is fixed, not a choice — the same register as branch-per-stage. Three
things follow from it, and they are why it is worth a frozen semantic rather
than a suggestion:

- **The ledger is always readable and always writable.** Because the clone
  never moves off the plan branch, `.plan/` there is the synced plan-branch
  copy at every moment. The `done` write (finish step 5) is a commit in the
  clone that needs no checkout and cannot disturb an in-flight stage.
- **Concurrency stops contending for `HEAD`.** *Parallel stages* above makes
  concurrent sessions semantically safe; separate working trees are what make
  them physically possible. Two sessions in one directory fight over the
  checkout no matter how correct the merge rules are.
- **Provisioning prefers the harness, falls back to git.** Use the harness's
  native worktree mechanism when there is one (Claude Code's `EnterWorktree`,
  or `superpowers:using-git-worktrees` when installed) — but only when it
  honors the exact branch and path names above (the template `PLAN.md` owns
  the full rule); otherwise `git worktree add`. What it must **never** do is
  degrade to checking the
  stage branch out in the clone — if the harness refuses to work outside its
  original directory, the honest move is to stop and hand the operator the
  path to relaunch in.

Two honest costs, named where they bite rather than discovered later. A fresh
worktree contains only tracked files, so untracked local setup a stage needs
(`.env`, local config, build caches, `node_modules`) is not there — copy what
the stage needs and note it in the ledger. And a worktree is a real directory
that outlives a crashed session, so teardown is part of the protocol: after
the merge, a clean and fully-pushed worktree is removed along with its merged
branch, while anything uncommitted, unpushed, or stashed is left alone and
reported. Preflight reports orphans; closeout gates on any that survive —
removing the ones that are merged and fully pushed, and refusing to close
while one holds work git cannot recover (see *Closeout*).

**Preflight & sync — verify git state before trusting the ledger.** The
ledger is canonical, but only after it's proven fresh: every stage session
and the closeout start with a preflight block, defined once in the template
`PLAN.md`'s operating protocol — confirm `.plan/` is tracked and the plan
branch has an upstream, fetch, fast-forward the plan branch (holds
under both squash-merge and merge-commit remotes), require a clean tree in
both the clone and this worktree, apply the **two-tree rule** to HEAD (the
clone on the plan branch, the stage on its own worktree), and reconcile the
ledger rows against actual branch, PR, and worktree state. One state is
self-healing (a `doing` row whose PR merged remotely gets its `done`
recorded); one is expected under concurrency (another
stage's in-flight branch — reported, not fatal, see *Parallel stages*);
everything else is drift, and the preflight **reports and stops** — it never
auto-stashes, resets, or deletes branches.

## The final review stage

`SF` is the one stage exempt from the read-scope rule: it reads the *entire*
ledger — every note, gotcha, shortcut, and known gap — and sweeps for stragglers.
Crucially, **it catalogs; it never implements.** Each finding becomes exactly one
of three outcomes:

- **A new stage in this plan** — follow-up work belonging to this project. It
  gets a **PLAN.md stage index row** (with its flags — required, since the weight
  check and next-runnable logic only see stages listed in the index), a ledger
  row, and a stage file, and runs later as a normal stage in its own fresh
  session and branch.
- **A spin-off candidate** — work that has outgrown this plan (a genuinely new
  project). Recorded in the ledger and surfaced in the final PR body as follow-up;
  it does *not* block closeout. Start it later with its own bootstrap.
- **An explicit "accepted, won't fix"** — with a one-line reason, so the gap is a
  decision instead of a surprise.

Its acceptance check: every loose end in the notes is either a new stage (a
stage index row, a ledger row, and a stage file) or explicitly closed.

## Closeout

Closeout refuses to run until every ledger row is `done` or `skipped` (including
stages the review spawned) **and** no stage PR into the plan branch remains
open or unmerged — a `done` row alone is not enough; the preflight's
reconcile runs first and treats that mismatch as a gate failure. Then it: distills `PLAN.md` + the ledger into the
final PR body so the *why* and the as-built story survive on `main`; deletes
`.plan/` as the last commit on the plan branch (nothing is lost — the full plan
history remains in git; keeping `.plan/` is the `plan-dir: keep` option, for a
plan that doubles as documentation); and proposes the PR from `plan-<slug>` to
`main` for the human to review and merge.

**Stage worktrees are part of closeout's gate, under one rule in both modes.**
A surviving worktree whose branch matches `plan-<slug>-s*` means some stage
never finished its teardown. If that worktree's branch is merged into the plan
branch and it holds nothing unpushed, it is finished work and removal is safe:
interactive closeout offers to remove it, unattended closeout removes it.
Anything else — unpushed commits, an unmerged branch, work that is not
recoverable from git — stops closeout in both modes, with the path and what it
holds reported. An operator's unrelated worktree (any other branch) is none of
the plan's business and never blocks.

**Closeout runs unattended too** (`/plan-close --unattended`), and an
orchestrator can fire it once every stage is `done` or `skipped`, so a plan can go from
bootstrap to an open plan→main PR with exactly two human gates: a `gate: human`
stage, and the final merge. See *Unattended mode*.

## Anti-patterns this exists to prevent

- Restating decisions in prompts or stage files — copies drift; point at
  `PLAN.md`.
- One giant stage — blows context, can't resume; split it.
- Brainstorming everything — design ceremony on mechanical work; `direct` is the
  default.
- Subagents everywhere — session-per-stage already isolates context; reserve them
  for churn.
- Claiming done without evidence — the acceptance output must actually land in
  the ledger.
- Silent scope creep — "while I'm here…"; note it, spin a stage, move on.
- Editing decisions in two places — frozen decisions change in `PLAN.md` only.
- Skipping the dependency gate — building on an unbuilt prerequisite.
- Checking a stage branch out in the main clone — the clone is the plan's
  window; moving it hides the ledger and breaks every concurrent session.
