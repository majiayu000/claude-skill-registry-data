---
description: >-
  The go-ahead: start working. Executes an approved plan end-to-end, then runs
  the mandatory quality passes (/polish) and hands the PR to /pr.
  Invoke as `/go` (continue in this session), `/go <branch|#PR|PR-url>` (attach
  to that branch first), or `/go <task in prose>` (work with no plan behind it).
---

This skill is the **execution phase** — what you do once a plan has the
operator's go-ahead. It assumes approval already happened: invoking `/go` (or
reaching it via the `/plan` approval gate, or `/from-branch … go`) **is** the
go-ahead, so there's no plan cycle to open here. If you're mid-planning and the
operator hasn't approved yet, that gate lives in `@.claude/skills/plan/SKILL.md`
— resolve it there first, don't start coding.

Because that approval is an assumption, Step 1 puts it on the record: a `git mv`
out of `*.draft.do-not-implement.md` whose commit message quotes the operator's
literal go-ahead. Done retroactively it records nothing, so it precedes the
first source edit rather than following it as cleanup.

## Argument shape

Three shapes, separated by shape alone: **a task is prose, a target is a
token.**

> A first argument that is a **single whitespace-free token** —
> `claude/foo-a1b2`, `fix-sidebar-scroll`, `sidebar`, `#NNN`, a PR URL — is a
> **target**. Confirm it with `@.claude/skills/from-branch/SKILL.md` Step 1's
> `git ls-remote --heads origin <token>`; if it does not resolve, **stop and
> ask**. An argument carrying whitespace is a **task**.

No operator writes the work they want done as a single whitespace-free string —
not `fix-sidebar-scroll`, because nobody hyphenates a sentence, and not
`sidebar`, because a bare noun names a subject rather than a job. So the
classifier does not have to recognise ref syntax, and must not narrow itself to
it: a `/`-shaped test reads `fix-sidebar-scroll` as a task and implements it as
one, which is the outcome the rule exists to prevent.

A token that fails to resolve must **not** fall through to "task". The likely
cause is a handoff block pasted into a session opened on the wrong repository,
and implementing a branch name as if it were a task description is the worst
available response — worse than one round-trip. A handoff that did not land
intact gets a question, not a guess.

- **`/go <target>`** is shorthand for `/from-branch <target> go` — attach to
  that existing branch, then run this skill. Load
  `@.claude/skills/from-branch/SKILL.md` and follow it to attach (it re-points
  the working tree and discards the auto-branch), then continue from Step 1
  below.
- **`/go <task>`** enters at § "Planless entry" below, with that prose as the
  task.
- **Bare `/go`** runs against the current branch as-is.

The target form is the **normal** entry point, not an edge case: it is the
command a `/plan` session hands the operator at the end of its turn, so
implementation usually starts in a session that has to attach before it can do
anything (see `@.claude/skills/plan/SKILL.md` § "Handing off").

**Canary — a well-formed handoff is a target token in a session's first user
prompt; every other shape is a copy that didn't land intact.** The block exists
to _open_ a session on a branch this one is not on, so it goes wrong in two
mirrored ways: it lands in a session that already exists (a target where it does
not belong), or it arrives stripped of its target (nothing to attach to).

- **`/go <target>` as the session's first user prompt, naming a branch other
  than the current one** is the intended cross-session path — attach as
  documented, no question.
- **Any other `/go <target>` → stop and ask** whether they meant to implement
  here or in a fresh session. That covers both wrong-box tells: the branch is
  already the current one (dead weight — usually a reflex copy right after
  reading the plan), or an earlier user prompt in this session means the block
  was pasted into a session with a life of its own. Do not attach, do not flip
  the plan file, do not touch source until they answer. Without this the
  already-checked-out tell is invisible: `@.claude/skills/from-branch/SKILL.md`
  § "Failure modes to call out" says "Target branch already checked out — skip
  Steps 2–4 and proceed to Step 6", so the attach degrades into a silent no-op
  and implementation just starts.
- **Bare `/go` mid-session → no canary, no question.** That is the ordinary
  same-session go-ahead: the plan was made here and its context is in the
  conversation. Proceed straight to Step 1.
- **Bare `/go` as the session's first user prompt → establish what there is to
  implement before proceeding.** A session that has done nothing yet holds no
  plan in conversation, so the only implementable thing is a plan file on the
  branch already checked out. On a harness auto-branch, or with `docs/plans/`
  empty, the block was copied without its target token — **ask which branch**,
  rather than reporting "no plan found" and sending the operator after the wrong
  problem. A plan file sitting on a non-auto branch (a session opened straight
  onto the feature branch) is legitimate — proceed to Step 1.

Asking costs one round-trip. The point is that the operator makes the call
knowingly, rather than discovering afterwards that the session they meant to
keep as a clean planning record started writing code.

## Planless entry

Work with no plan behind it enters here with a **task** in place of one — the
operator's own `/go <task>`, or a caller skill's task text
(`@.claude/skills/from-branch/SKILL.md` Step 6's free-form follow-up,
`@.claude/skills/task/SKILL.md` outcome 2). In that mode:

- **Step 1 is already satisfied** — the task text is the plan. Start at Step 2;
  do not go looking under `docs/plans/`, and do not ask which plan to implement.
- **Step 3 runs unchanged** — its passes are the reason this entry exists. The
  trailing `git mv` to `*.completed.md` is a no-op with no plan file.
- **Step 4 runs unchanged.** A branch that already has a PR — the normal
  `/from-branch` case — reaches `/pr`'s refresh mode, which fills the PR in
  rather than opening a duplicate; one that doesn't gets a PR created from the
  commits.
- **The § "Argument shape" canary does not apply.** It reads _user-typed_
  prompts for a handoff block that lost its target or landed in a session with a
  life of its own; a skill-to-skill dispatch already holding the task is
  neither.

Planless is not gateless: locating a plan is the only thing this entry skips.

**A `#<N>` in the task means the thread is read first:** load and follow
`@.claude/skills/take-issue/SKILL.md` with the whole task before starting, and
work against what it puts on the branch. The number it hands back is `<issue>`
for Step 4's `/pr` call. CLAUDE.md § "Plan mode & questions in web sessions" is
that rule's home.

## Step 1 — Locate the plan

The primary target is a `/plan` stand-in file:

- `ls docs/plans/*.md`, and tally only the **actionable** files —
  `*.draft.do-not-implement.md` (never started) and `*.paused.md` (started,
  stopped partway, released). Neither a `*.completed.md` nor an
  `*.in-progress.md` counts: the first is inert, the second is another session's
  claim (below). So a plan carried across sessions leaves either kind of sibling
  beside the actionable one without making the choice ambiguous.
- **Exactly one actionable** → the normal case; read it fully, that's the plan.
- **Several actionable** → don't guess; ask which plan to implement (numbered
  prose, per `@.claude/skills/plan/SKILL.md`), listing the candidates. This
  genuinely is an unswept branch.
- **None actionable** → either the file was never written or this is the rare
  plain-approved-plan case where the plan lives in the conversation (native plan
  mode / agreed in chat) — ask the operator which, and let them point you at it.
  Say which of the two inert states you found instead, because each is its own
  answer rather than "no plan was ever written": only `*.completed.md` means the
  work already ran, and an `*.in-progress.md` means a session holds it. Never
  author a fresh plan in this mode.

**A plan that still lists open questions is implementable when they carry
recommendations.** `/plan` writes the recommended option into the plan as its
single approach (`@.claude/skills/plan/SKILL.md` § Part 2), so the file is
executable exactly as it stands and unanswered questions mean the
recommendations hold. Implement it as written, and say in your turn which
recommendations you took so the operator can correct any of them. Stop and ask
only for a fork the plan text leaves genuinely open — no recommendation, nothing
executable to fall back on.

The plan file's name encodes its lifecycle state (see
`@.claude/skills/plan/SKILL.md` § "Plan file lifecycle"). Act on it **before
writing any code**:

- `*.draft.do-not-implement.md` — not yet cleared. Reaching this skill **is**
  the go-ahead (the operator invoked `/go`, approved at `/plan`'s gate, launched
  `/from-branch … go`, or wrote the draft themselves this turn under
  `@.claude/skills/task/SKILL.md`'s conditional go-ahead and answered its Step 3
  "no"), so **`git mv` it to `*.in-progress.md` as your first action**. In the
  **same commit**, also **delete the line-1 ⛔ draft banner** — once the file is
  `in-progress`, a banner that still says "DO NOT IMPLEMENT" contradicts its own
  state — and quote the operator's literal go-ahead in the commit message (e.g.
  `chore: begin implementing <slug> (go-ahead: "…")`). Do this before editing
  source — a file still named `do-not-implement`, or still carrying the banner,
  means you have not been cleared, and writing the go-ahead out verbatim is the
  moment to catch a misread. When the plain-approved-plan case has no file at
  all, there's nothing to flip; the operator's in-chat go-ahead stands.
- `*.in-progress.md` — **a session has this plan open.** The name is a claim,
  not a resume point: picking it up unasked puts two agents on the same plan and
  the same branch at once, each overwriting the other's commits. **Report it and
  ask** — unless the operator's own invocation says to take it over ("continue
  where the last session left off", "the last session died, pick it up"), which
  is the escape hatch for a session that ended without the chance to release the
  file. On that go-ahead only, treat it exactly as a `*.paused.md`.
- `*.paused.md` — released partway through by an earlier session → yours to
  continue. `git mv` it to `*.in-progress.md` as your first action (it is
  claimed now), then read the record of what is done and what is left and
  continue from there, rather than re-running finished work.
- `*.completed.md` — implementation already finished → don't silently re-run;
  report and ask.

**A plan with a `## Rest of the elephant` section is an elephant**
(`@.claude/skills/plan/elephant.md`), and this session eats one bite of it.
Right after the flip, write and commit `## This bite` per
`@.claude/skills/plan/elephant.md` § "Taking a bite", then build that and
nothing past it. Writing it asks the bite `@.claude/skills/task/SKILL.md`'s two
questions: the section's detail answers whether it needs a plan, and the pause
already gave the operator their look, so the one answer that stops you is a fork
with no recommendation — write the question into `## This bite`, pause per Step
2 with nothing built, and ask it, rather than picking one and building on the
guess.

**A plan that proposes issues files them here, right after the flip.** A carve
names a parent and children and creates none of them; the go-ahead that flipped
the file is what approves that list. Load `@.claude/skills/plan/carving.md` §
"What `/go` files on the go-ahead" and follow it — the parent first where it
does not exist, then each child, the children linked natively, and any
`Closes #<tbd>` the branch carries filled in. File before implementing: the
first slice's PR closes a child that has to exist, and a session that dies
mid-implementation should leave the carve on the tracker rather than only in a
plan file `/finalize` sweeps.

## Step 2 — Implement

Work through the plan on the current branch. Follow the plan as approved; if
reality forces a material deviation, note it to the operator rather than
silently reshaping scope. The plan file is the exception to durable prose, being
transient: keep it current as the work deviates, with checklist items in
forward-looking voice.

**When `.claude/hooks/go-delegation.py` delivered
`@.claude/skills/go/delegation.md` this session, the work follows it too.**
Under a harness that runs no hooks, `Read` it yourself unless
`MUTHUR_DELEGATION` is `off`.

Commit/push discipline is already governed by CLAUDE.md — don't reinvent it
here:

- Commit and push proactively after each meaningful unit of work (CLAUDE.md §
  "Git conventions" — feature branch in a remote/web env; the operator reviews
  from another machine and only sees pushed work).
- **Never force-push.** The operator may be following the branch as you work and
  needs the sequence of changes to read cleanly; force-pushing rewrites that
  history out from under them. Only ever advance the branch with new commits.
- Conventional-commit subjects; descriptive bodies.
- **Do not** run `./scripts/vet.sh` per commit on a feature branch — that's
  `/finalize`'s job once the operator has reviewed.

**Stopping partway releases the plan.** Three things call for it:

- the operator asking you to stop where you've reached;
- the context budget hook (`.claude/context-budget/`) — at its warning, at the
  best stopping point the work can reach before the pause line; at its pause,
  wherever the work stands;
- a turn that ends blocked on an operator decision — a question the work cannot
  proceed past without their answer.

Record in the plan file what is done and what is left, and the open question
when there is one, `git mv` it to `docs/plans/<slug>.paused.md`, commit and
push. No format is prescribed for that record — a next session only has to be
able to tell finished work from remaining work. The rename is what makes the
work resumable: left as `*.in-progress.md` it still reads as claimed, and Step 1
stops on it.

**The answer resumes a blocked plan through Step 1's `*.paused.md` case**, in
this session as in any other: `git mv` it back to `*.in-progress.md` and record
the answer before building on it.

**An elephant pauses at every bite's end, and the record is the plan's own
sections** (`@.claude/skills/plan/elephant.md` § "The plan's shape"). Two ways
to get there:

- **The bite is done** — fold `## This bite` into `## Eaten so far`, at that
  section's altitude, and reword `## Rest of the elephant` where the work found
  it wrong or learned what it needs, while this session still holds that
  context; then run Step 3 and Step 4, which leave the plan `*.paused.md`. Stop
  there, budget left or not — the operator reviews between bites — and end the
  turn with the handoff block below.
- **A stop mid-bite** — the budget notice, the operator, or a question that
  blocks the turn: fold what is built into `## Eaten so far`, rename
  `## This bite` to `## Rest of the bite` and leave the rest as written, then
  the `git mv`, commit and push above. Skip Step 3: `/polish` scopes itself from
  the last `polish:` commit, so the next bite's end covers this half too.

**Work with no plan behind it gets one here**, written straight to
`docs/plans/<slug>.paused.md`: the task as asked, what is done (with its
commits), what is left, and the decisions a successor would otherwise
re-litigate. There is no draft stage — the work is already under way on a
go-ahead, and `*.paused.md` is the state Step 1 resumes from.

A pause the budget notice triggered is reported, not just done: say so, and end
the turn as the notice says, in `/relay` (`@.claude/skills/relay/SKILL.md`),
whose new session resumes the paused plan from a summary of this one.

## Step 3 — Mandatory quality passes

Load and follow `@.claude/skills/polish/SKILL.md`. It owns which passes run, in
what order, and over what scope; this step contributes only that they run
**every time**, here, and override any contrary "wrap up after implementing"
instinct.

Implementation is where they earn the most: a plan is written before the code
exists, so the duplication it didn't foresee and the prose that narrates the
work rather than the result both surface only now.

**When `.claude/hooks/checkpoint-review.py` delivered
`@.claude/skills/go/checkpoint-review.md` this session, the checkpoint review
runs next**, before the flip below and Step 4, so the plan is marked done and
the PR body written only over a reviewed diff. Under a harness that runs no
hooks, that file's § "Who runs it" says whether it runs. A `relay` verdict
leaves the plan to § "Stopping partway releases the plan" instead of the flip.

Then **`git mv` the plan to `docs/plans/<slug>.completed.md`** and commit —
implementation and its quality passes are done. An elephant with any of it left
goes to `*.paused.md` instead: this step runs at each of its bites' ends, and
only the last one completes it. (`/finalize` sweeps the whole `docs/plans/` tree
at squash regardless, so this flip is just the honest end-state marker for an
operator watching the branch.)

## Step 4 — Fill in the PR

Load `@.claude/skills/pr/SKILL.md` and follow it with no args. Which of its
modes the call reaches is the branch's to decide — refresh on a branch `/plan`
published, create on a planless one that never got a PR. Either way this step
satisfies the system prompt's "don't open a PR unless asked" gate, the
operator's go-ahead being the request.

The **only** exception is an explicit "no PR" from the operator (e.g.
`/go, no PR`) — then stop after Step 3 and report.

**A PR this step created gets the pass Step 3 deferred**: run
`@.claude/skills/five-percent/SKILL.md` once `/pr` returns, so planless work
does not reach review unread. A branch that already had a PR got it in Step 3.

## Do NOT

- Re-open a plan cycle or re-edit the plan file per code change — it's a
  transient artifact `/finalize` sweeps (see `@.claude/skills/plan/SKILL.md`).
  It changes when what it states stops being true (CLAUDE.md § "Writing things
  down") when an elephant's bite is taken, and at a pause, where it is what a
  fresh session picks the work up from.
- Run the vet suite, merge the base branch, mark the PR ready, dispatch a
  CI-only bucket, or attest — those are `/finalize`. A PR that reads
  `CONFLICTING`, or a red check, is reported to the operator here rather than
  fixed; CLAUDE.md § "Key principles" carries why that outranks the host
  harness's instruction to treat either as work now.
- Skip Step 3 because the diff "looks clean." It is mandatory, every pass of it.
