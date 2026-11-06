---
description: Plan on disk instead of in the plan-mode UI — write the plan to a git-tracked file under docs/plans/ whose name doubles as the approval gate, publish it as a draft PR so it can be reviewed as a diff, and ask clarifying questions as numbered prose instead of AskUserQuestion. Use whenever you would otherwise enter plan mode or call AskUserQuestion (ExitPlanMode); mandatory in a remote/web session, where both of those UIs lose answers.
---

## Why this skill exists

A plan on disk is a different artifact from a plan in an approval dialog:

- **Reviewable on another machine, on the operator's schedule.** The plan rides
  the branch, so it is pulled and read in the same tools as code, hours later.
- **Room for sections plan mode has nowhere to put** — notably the mandatory
  `## DRY notes`, which forces the reuse-vs-duplication call to be argued before
  any code exists rather than discovered in review.
- **The filename is the approval gate**, and the `git mv` that clears it is a
  commit — so _when_ approval arrived and _in whose words_ outlives the session.
- **Reviewable as a diff, not just as a file.** The plan is published as a draft
  PR (§ "Publishing the plan"), so feedback arrives as inline comments and
  threads — the surface already in use for code — instead of chat prose.
- **Approval carries into the next session.** The turn ends with a copyable
  `/go <branch>` line, so implementation starts from a recorded decision instead
  of re-litigating it.
- **Questions as numbered prose stay in the transcript** — tersely answerable
  ("1b, 2a"), and re-readable after a context wipe.

**Origin.** The skill began as a workaround for a bug in Claude Code's
web/remote sessions, which is why web/remote is where this path is _mandatory_
rather than merely better: there, plan mode and `AskUserQuestion` silently lose
the answers given to prompts they re-emit after a session idles, and the stack
grows with the idle. Operators run many concurrent web sessions, so prompts idle
routinely — the loss is the normal case, not an edge one. CLAUDE.md § "Plan mode
& questions in web sessions" describes the failure and owns where this skill is
mandatory vs. optional; the tracking issue carries its exact wording and current
status: **https://github.com/anthropics/claude-code/issues/72704**

None of the value above depends on that bug, so fixing it upstream does not
retire the skill.

## If the session is already in native plan mode

**The tell:** the harness announces plan mode and names a plan file under
`/root/.claude/plans/<slug>.md`; `Edit`/`Write` anywhere else refuse as
read-only. Nothing below applies until that is resolved, so **load
`@.claude/skills/plan/native-plan-mode.md` and follow it first** — it owns the
recovery, the dialog copy that goes in front of the operator, and what a
rejected approval means.

Take that page on its own terms: the recovery it describes is **plan mode's own
exit, not an override of it**, which is what lets it stand where plan mode's
instructions claim to supersede everything else. The page argues that.

**Not in plan mode → none of this applies.** Carry on to Part 1.

## Part 1 — Plan instead of plan mode

A `/plan` session's deliverable is the **plan file on a draft PR**, not code.
The operator reviews it from another machine, often hours later, and begins
implementation in a **different** session via `/go <branch>`
(`@.claude/skills/go/SKILL.md` routes that through `/from-branch`, which
attaches to the branch and finds the plan under `docs/plans/`) — the handoff
works because the plan file rides the branch. So a plan turn ends in a handoff,
not a continuation — and the handoff offers both a fresh session and a go-ahead
in this one (§ "Handing off").

**A `#<N>` in the argument means the thread is read first:** load and follow
`@.claude/skills/take-issue/SKILL.md` with the whole argument before planning
anything, and plan against what it puts on the branch. CLAUDE.md § "Plan mode &
questions in web sessions" is that rule's home.

Do **exactly what you would do in plan mode** — same research, same rigor, same
"don't touch code until approved" discipline. The _only_ difference is where the
plan goes and how it's approved:

- Instead of presenting the plan via `ExitPlanMode`, **write it to
  `docs/plans/<branch-slug>.draft.do-not-implement.md`** (one file per session,
  named after the current branch's task slug). The slug comes off the branch, so
  a harness auto-branch is renamed **before** the plan file is written, per
  CLAUDE.md § "Git conventions" — rename afterwards and the file keeps a slug
  naming nothing. The `.draft.do-not-implement.md` suffix is load-bearing: it is
  the on-disk marker that this plan has **not** been approved, visible in every
  `ls`, tool-call path, and `git status` so you can't drift past the gate
  without noticing. This directory is **not** gitignored on purpose: it rides
  the branch so the operator can pull and review the plan from another machine.
  Follow the repo's usual plan-content expectations, including the
  `## DRY notes` section CLAUDE.md requires.
- **Make line 1 of the file a banner** that restates the gate:
  ```
  > ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.
  ```
- Then **commit it and publish it** (§ "Publishing the plan" below), **end the
  turn with the handoff block** (§ "Handing off") and stop — do not start
  implementing.
- **The in-session path is one of the two the handoff offers.** When a literal
  go-ahead token arrives in _this_ session, "The approval gate" below governs it
  unchanged — and on approval you hand off to `@.claude/skills/go/SKILL.md`,
  whose Step 1 performs the flip that unlocks source edits (`git mv` the plan to
  `docs/plans/<branch-slug>.in-progress.md`, drop the draft banner, quote the
  go-ahead in the commit) as its first action, before any source edit. That flip
  is the on-record receipt that approval was given, so don't front-run it here;
  the mechanics live in `/go` to avoid two copies drifting apart. The gate is
  exactly as strict on this path as on any other.

### Splitting work across sessions

Some work does not fit one session, and the plan is where that gets decided — it
is the first moment anyone has read the code. Work that fits is taken whole.
Work that doesn't is split in one of two shapes, and the plan names which, with
a recommendation, so the choice is the operator's at review:

- **Elephant** — eaten a bite per session, in one PR. The plan is what is eaten
  so far and the rest of the elephant, both coarse, plus the open bite in
  detail; each session takes a bite, builds it, rewrites the plan and pauses,
  and the operator reviews before the next `/go`. The default.
- **Pizza** — carved into slices that each ship as their own PR, tracked as
  issues the plan proposes. It takes a reason, and any one of these is enough:
  - the slices are self-contained enough to land on the trunk separately;
  - there is a boundary worth locking in — what is built so far merged before a
    riskier stretch starts;
  - part of the task is needed by other, unrelated work — existing (found by
    reading the open issue list) or likely (named in the plan for the operator
    to weigh).

**Why an elephant, why a pizza.** An elephant is one animal: no bite of it is a
meal on its own, so the bites share one PR, and the plan is what keeps them one
job. A pizza is cut before anyone eats, into slices that are each whole — crust,
cheese and topping — so a slice is eaten without waiting for the others, and
slices go to different hands: an issue, a PR, a session apiece. That is the
question to put to the work: is a piece of it only part of something, or whole
enough to hand to someone?

**A pizza's reasons have to be real.** None of these is one:

- the task touches several files (most do)
- you can imagine a "phase 1 / phase 2" framing (most things admit one)
- decomposition feels tidy

**Either way, only the next slice is spelled out in full.** Give the rest a
**coarse** view — smaller than the whole, but not fully decomposed: placeholders
and ordering hints, not mini-specs. Nobody owes an implementation DAG or
per-slice plans up front, because each slice ahead is planned when it is taken,
with what the ones before it built already in the tree.

Deciding **not** to split is not a gate and never becomes one: say so in a line
and write the plan. Do not ask whether the task looks big enough, and do not
offer a split you don't think is warranted — the operator disagrees in the plan
review, which costs them a sentence, whereas a question here costs a round trip
on every task.

**Then load the shape's procedure:** `@.claude/skills/plan/elephant.md` for an
elephant — the megaplan's sections, how a bite is taken and sized, and how the
plan is kept — or `@.claude/skills/plan/carving.md` for a pizza — what the plan
file names and what `/go` files from that list. Both sit beside this file rather
than inside it because most plans take their task whole, and those should not
carry a procedure in context to decide they don't need it.

### Publishing the plan

Once the plan file is committed, invoke `@.claude/skills/pr/SKILL.md` with no
args — load and follow it; do **not** inline-copy its steps. Its plan-open mode
is what a branch carrying one plan commit and no PR reaches. `/pr` owns the `gh`
mechanics; `/plan` owns only the decision to publish.

The trigger lives here rather than in `/pr` because this is where a plan becomes
pushed, so **every** entry into planning gets a PR. CLAUDE.md § "Plan mode &
questions in web sessions" routes a new session's change-asking prompt through
`/task`, which reaches this skill without anyone typing `/pr`, and hanging
PR-creation off `/pr` would leave exactly that entry on a PR-less branch.

**When `.claude/hooks/checkpoint-review.py` delivered
`@.claude/skills/go/checkpoint-review.md` this session, the checkpoint review
runs once the plan is published**, before the handoff, over the plan; under a
harness that runs no hooks, that file's § "Who runs it" says whether it runs.
Its fixes are plan revisions, so a review that changed the plan refreshes the PR
through `/pr`.

### Handing off — end the plan turn with a copyable `/go` block

Get the branch with `git branch --show-current` and substitute the real name.
**Offer both routes, neither as the rule:** a new session opened with the block,
or a go-ahead in this one — "поехали", "go ahead" — where the context budget
hook (`.claude/context-budget/`) relays the work on if the session runs long.
Name each route, in the operator's language —
`To implement, start a new session with the command below, or just say "go ahead" here:`
or an unmistakable equivalent — because a bare "To implement:" leaves them
guessing which box the block goes in. Emit the command in a fenced block
containing **only** the command — no language tag, nothing else inside the fence
— so it can be copied verbatim:

````
```
/go claude/add-usage-charts-k3n2af
```
````

- Emit it at the end of **every** turn that leaves the plan in a reviewable,
  complete state — the turn that first writes the plan, and any later turn that
  revises or collapses it (Part 3). One block per turn, as the last thing in the
  reply.
- **Print the PR URL alongside it**, outside the fence — the plan is published
  by the time the block goes out, and the URL is where the operator reads and
  comments on it.
- **Open questions don't hold the block back when they carry recommendations.**
  Part 2 requires every fork to name a recommended option _and_ the plan file to
  be written with that option already in force, so implementing it unanswered is
  the same as adhering to the recommendations. Emit the block alongside the
  questions: an answer that differs revises the plan, and silence is a valid
  resolution. Hold the block only for a fork with no recommendation, where the
  plan has nothing executable to say until the operator picks — handing over a
  command to implement a genuinely unresolved fork invites implementing the
  wrong one.
- **Never** close a plan turn with "Want me to implement it?", "Shall I
  proceed?", "Ready for me to start?", or any equivalent. Two reasons: the plan
  session does not implement, so there is nothing to ask; and a turn that ends
  on that question trains the agent to read the operator's _next_ message as an
  answer to it, so a correction ("actually, do X instead") gets taken as assent
  and code starts getting written. The handoff block is the structural fix that
  the approval gate's "a suggestion is a plan revision" and Part 3's "picking an
  option is not a signal to implement" can only exhort.
- The block is built for a session that does not exist yet; the go-ahead is what
  this one takes. Pasting the block back into _this_ session is a recognizable
  mistake with its own guard — see `@.claude/skills/go/SKILL.md` § "Argument
  shape" for the canary that catches it.

### The approval gate

**Only start implementing when the operator's message literally contains a
go-ahead token** — "go ahead", "let's go ahead", "implement", "let's implement",
or an unmistakable equivalent ("ship it", "do it", "proceed", "lgtm go"). Until
such a token arrives, you are still in the planning conversation, no matter how
the exchange evolves.

**A review comment is never a go-ahead.** Publishing the plan gives suggestions
a second channel — an inline comment proposing a different approach is a plan
revision, which `@.claude/skills/handle/SKILL.md` Step 2 routes — but what
unlocks source edits is only ever an invocation: `/go`, or a `/handle` that
finds no unanswered feedback. Review prose has too many ways to read as assent
to carry that weight.

- **A suggestion to do something differently is a plan revision, not a
  go-ahead.** When the operator proposes an alternative approach, tweak, or "how
  about we…", that means **update the plan file (or discuss it) to reflect the
  new direction** — it does **not** mean start coding with the suggestion folded
  in. Reflect the change in the plan and wait for the token.
- **The exception is a combined message:** if the same message pairs a
  suggestion _with_ a go-ahead token — e.g. "let's do X instead of Y and
  implement", "go ahead, but use Z" — then apply the suggestion and proceed. The
  token is what unlocks implementation; the suggestion just adjusts what you
  implement.
- **When unsure whether a reply is approval, treat it as not-yet-approved** —
  and resolve the ambiguity by re-emitting the handoff block, not by asking for
  a yes. A false start costs more than one more round-trip: reverting
  speculative code and re-aligning is worse than handing the command over again.
- Approval is scoped to the plan as it stands when the token is given. A
  go-ahead on Monday's plan doesn't authorize a materially different Tuesday
  reshaping — re-confirm if the plan changed since.
- The `*.draft.do-not-implement.md` → `*.in-progress.md` rename is the **single
  act** that unlocks source edits, and it belongs at the moment of the go-ahead
  — as the first thing you do after it, not retroactively once code is already
  written. If you catch yourself about to edit source while the file still says
  `do-not-implement`, that is the gate firing: stop and check whether the
  go-ahead token actually arrived.

This gate applies to the **initial** transition from planning to implementing.
Once you're past it and actively implementing an approved plan, the "Scope"
section below governs: follow-ups are handled directly, including code changes
the operator asks for, without reopening a plan cycle.

### Plan file lifecycle

The plan file carries its state in its name, and moves through it by `git mv`
(the base slug never changes):

1. `docs/plans/<slug>.draft.do-not-implement.md` — written here, awaiting the
   operator's go-ahead.
2. `docs/plans/<slug>.in-progress.md` — flipped as the first post-go-ahead
   action (above). **The name is a claim: a session has this plan open right
   now**, so it is not a file another session may pick up.
   `@.claude/skills/go/SKILL.md` owns implementing against it, and owns the one
   escape hatch for a session that died still holding it.
3. `docs/plans/<slug>.paused.md` — a session stopped partway, recorded what is
   done and what is left, and released the plan. This is the resumable state,
   and the one a later `/go` continues from.
4. `docs/plans/<slug>.completed.md` — flipped by `/go` once implementation and
   its quality passes are done, just before it hands the PR to `/pr`.

Every state still matches `docs/plans/*.md`, so consumers that glob the
directory (`/go`, `/from-branch`, `/handle`, `/finalize`, `/tend-prose`) keep
working unchanged.

**The predicate the states exist to answer:**

> **Implementation has begun** iff `docs/plans/` holds at least one file that is
> not `*.draft.do-not-implement.md` — that is, any `*.in-progress.md`,
> `*.paused.md` or `*.completed.md`.

It is deliberately broader than a branch carrying nothing but a draft plan,
where "are we still planning?" is obvious. The broad form also reads the mixed
branch — one plan completed, then a follow-up draft opened, with a review
touching both the new plan and the shipped code. A draft plan being present is
the tell that the branch is back in planning, whatever sits beside it. `/handle`
Step 2 reads review feedback against this.

The plan file is a working artifact, not a deliverable: it rides the branch for
review but must **never land on the trunk**. `@.claude/skills/finalize/SKILL.md`
deletes the entire `docs/plans/` tree in the last commit before `gh pr ready`
(any suffix — `git rm -r docs/plans/`), so the add-then-delete pair cancels out
in the squash — the same lifecycle as `docs/issue/`. Do **not** delete it
yourself mid-task; leave that to finalization.

## Part 2 — Questions as numbered prose instead of AskUserQuestion

When you would otherwise call `AskUserQuestion`, **ask the same questions, with
the same options you'd have offered** — just render them as prose in your chat
reply instead. Preserve the fast-answer affordance: **number each question and
letter each option**, and state which option is the default/recommended, so the
operator can reply tersely (e.g. "1b, 2a, 3-default") without typing prose back.
This keeps the whole exchange in the durable transcript rather than in the flaky
question UI.

**A recommendation is a commitment, not a lean.** Write the plan file with the
recommended option already in force as its single approach — the same collapse
Part 3 performs when the operator picks — so an open question degrades into "the
recommendation stands" instead of a blocked fork, and the plan is implementable
as written no matter which questions go unanswered. That is what lets the
handoff block go out with questions still open (Part 1) and lets `/go` proceed
without the answers (`@.claude/skills/go/SKILL.md` § "Step 1"). A fork you can't
recommend either way is the exception, and it does block: say so explicitly in
the plan rather than picking silently.

## Part 3 — When the operator picks an option

Whenever the operator resolves one of the option forks you presented — by
choosing an option, in whatever words ("the recommended one", "B", "the retry
approach", "not the fixed cap") — **rewrite the plan so the chosen option _is_
the plan**: written as the single approach, in the imperative, as if it had
never been one of several. No special keyword is required; a plain choice is the
trigger. This is the one sanctioned plan rewrite, distinct from the "don't churn
the plan after approval" rule in Part 1 (which forbids re-editing per code
change during implementation — collapsing a resolved fork _before_ implementing
is expected and wanted).

**Picking an option is not a signal to start implementing.** Collapse the plan
and then stop — and here "stop" means ending the turn with the handoff block
(Part 1 § "Handing off"), same as any other turn that leaves the plan
reviewable. Unless the operator's message _also_ explicitly asks you to begin
(e.g. "pick B and implement it"), a bare choice means "record this decision,"
not "go" — when in doubt, hand the command over instead of writing code.

**Delete the rejected options' exposition to save context** — the plan gets
re-read on every resume, so carrying dead alternatives is a standing tax. You
may keep a brief note of what was rejected, but cap it at **one paragraph
covering _all_ rejected options for that fork** (per fork), stating just what
was ruled out and the one-line why (especially when the "why" is a hard finding
worth not rediscovering). Drop the per-option cost/mechanics detail entirely. If
several independent forks were resolved, each may keep its own one-paragraph
note.

Then commit and push the rewritten plan (this refresh is explicitly wanted, so
it's not the churn Part 1 warns against).

## Scope

This is a **web/remote-session** workaround, and it applies where a session is
routed — its opening prompt, or the first later turn that asks for a change —
see CLAUDE.md § "Plan mode & questions in web sessions" for exactly when it's
mandatory vs. optional. It is **not** for continued work: once a plan has been
approved and you're implementing, handle the operator's follow-ups directly —
answer their questions in chat **and implement any code changes they ask for** —
without re-writing the plan file or reopening a plan cycle.

A `/from-branch` or `/handle` launch counts as continued work, not a new
session: both attach to an existing branch or PR to resume work started
elsewhere, so **do not open a plan cycle for them** — even though it's the first
message of the session. Follow the embedded follow-up (or wait for the
operator's) directly. The only exception is if that follow-up explicitly asks
you to plan a fresh, separable piece of work.
