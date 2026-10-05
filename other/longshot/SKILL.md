---
name: longshot
description: Run a long autonomous build session from a brief — interview the user with `blind-spots`, prepare the plan, and wait for explicit final approval to start implementation. Only then decide later ambiguities as recorded rulings and execute without check-ins. Per task a fresh implementer subagent, an independent spec+quality reviewer, a fix loop, then a whole-branch review, the plan harvested into the repo's docs and deleted, and a handoff report with rulings, deferred questions and a squash proposal. Use when the user says "longshot", "work on this independently", "run with this", "ask me everything up front then go", "I'll be away", or hands over a multi-hour feature or package to build end to end. Do NOT use for a single small change — use `plan` for that.
argument-hint: '[--plan FILE] [--no-worktree] [--repos a,b] (brief, or blank to take it from the conversation)'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Longshot

Take a brief, settle its consequential decisions with the user, prepare the plan,
then get final approval to start implementation and build without check-ins.

**Preparation needs the user; implementation is autonomous.** Until the Phase 2
start gate is approved, stay read-only and wait for answers to every question you
ask. Silence, an empty tool response, a preselected recommendation, elapsed time,
and the initial longshot invocation are never answers or start approval. The
autonomous contract below applies only after that gate, including its stop rules
and troubleshooting advice.

A fresh longshot run needs its own start approval; a previous run's ledger does
not authorize new scope.

## The contract

Approving the implementation start authorizes staging and implementation commits
for the run's work in its writable repos, including on the primary repo's current
branch. Honor any explicit limits the user gives. Do not ask for a separate commit
confirmation. Final squashing requires its own approval under Phase 6.

State it back to the user at the implementation start gate, verbatim in substance:

1. **Every question up front.** Finish the interrogation and planning, then wait for
   the user's final go-ahead. Announce implementation starting; only then are there
   no more questions except the four stops below.
2. **Rulings, not stalls.** Every conflict, gap, plan defect or judgment call gets
   decided and written to the ledger as
   `Ruling: <decision> — <why> — <cost if wrong>`.
3. **Milestone pings only.** One line per completed task. Never a question, never a
   progress summary, never "should I continue?".
4. **Nothing is pushed.** Nothing outside the repos named in the brief is touched.

**After implementation starts, four things stop the run:** an irreversible or
destructive operation; a security-sensitive action; a side effect outside the work
tree that norms say you ask about first (a merge, a push, a release); or the brief
turning out to be wrong about something load-bearing. Everything else is a ruling.

## Phase 0 — Recon before questions

Uninformed questions waste rounds and spend the user's patience. Before asking
anything, read:

- the project instruction files (`AGENTS.md`, `CLAUDE.md`, `README.md`)
- the workflow file — `workflow.md` / `WORKFLOW.md`, or whatever the brief names.
  **It outranks this skill's defaults.** If none exists, use the default workflow below.
- any plan or spec doc (`docs/plans/*.md`, `docs/specs/*.md`) and note its date
- the reference/neighbour repos the brief names — for the integration surface *and*
  for their tooling: lint, static analysis, git hooks, CI, test layout, release scripts
- git state: branch, whether there are commits at all, what is untracked

Dispatch at most 3 read-only `Explore` agents in parallel for the repo sweeps.

If the brief opens with a technical question of the user's own, **answer it with
analysis and a recommendation** in the first round. Do not hand it back.

## Phase 1 — The interrogation

**Check the brief is one run first.** If it describes several independent subsystems,
say so before interviewing: propose the decomposition and its order, and run longshot
on the first piece. One run that plans three projects at once produces a plan whose
shape nobody approved. The opposite failure is a brief too small to pay for the
overhead — say so and offer `plan` (see Examples).

Then invoke `blind-spots` on the brief and run it to completion. Phase 0 already did
the recon its step 2 calls for — do not repeat it.

**The user is still needed through planning and the final start gate.** The
interrogation ends when every consequential decision is settled by existing
context, a user answer, or the user's explicit delegation of that decision.

`blind-spots` supplies the mechanics: dependency-ordered rounds, a recommendation on
every question so an explicit "use your recommendations" can settle the round, and
pruning to decisions that fork the design. Longshot sharpens its fork test — *would
a wrong guess here cost a rewrite, or just a follow-up commit?* Follow-up commit →
do not ask it, rule on it during the run.

These are mandatory wherever they sit in the tree, because the run cannot proceed
correctly without them. Put any still open into the first round:

- **Repo boundary.** Which checkouts may be written to, which are read-only
  reference, and whether new clones/worktrees may be created.
- **Definition of done.** "A complete package I can integrate" means something
  specific — name it: green suite, CI config, docs, a migration branch per consumer.
- The user's own opening question, answered.
- Anything where a wrong guess is architectural.

Once a question is asked, keep it pending until the user answers or explicitly
asks you to choose. These are required decisions, not optional preferences with
timeout defaults. An asynchronous question tool returning means the question was
sent; it does not mean the user submitted the selected option. Continue independent
read-only work while waiting; if none remains, yield with the questions pending.
Never turn an unanswered question into a ruling to close the frontier.

"Use your recommendations" settles the questions it refers to. Recompute the
frontier and ask any dependent questions; it does not bypass the final start gate.
When the frontier is empty, proceed to planning while remaining in preparation.

## Phase 2 — Plan

**Settle the approach before drafting tasks.** Where the settled decisions still leave
a genuine fork in how the thing is built — the same requirements reachable two or
three structurally different ways — present those options with their trade-offs, lead
with your recommendation and the reason, and wait. `blind-spots` establishes what the
work must do; this establishes the shape it takes, and a plan drafted before it is
answered bakes in a choice the user never made. Cut each option to what the definition
of done requires before presenting it. If there is no such fork, say so in one line
and move on rather than inventing alternatives.

Then draft or validate the plan itself, in the **plan format** in
`references/prompts.md`. Every task goes to a fresh subagent that has none of this
conversation, so the plan is its whole brief: Global Constraints carrying the settled
decisions, real code for the interfaces tasks share, and per task the files, tests,
acceptance criteria, a model tier and an independence marker. Function bodies stay
prose — writing them here does the implementation twice, on the most expensive model.

- **A plan doc exists** → read it, then validate it against the *current* repo state:
  which steps are already done, which paths moved, what the plan asserts that is no
  longer true. Fold factual drift into the draft and bring it to the plan format;
  ask about consequential choices the drift exposes before seeking start approval.
- **No plan doc** → draft one now. Use only `plan`'s read-only planning step for the
  exploration on a moderate scope, then recast its output into the plan format; for a
  large one run `review-plan` (multi-agent) over the draft and fold the findings in.
  Keep the draft in the conversation or planner output until approval; save it
  afterwards to `docs/plans/<YYYY-MM-DD>-<slug>.md`.

**Review your own draft before the gate**, whether you wrote it or found it on disk:

- **Placeholders** — a `TBD`, an empty section, a task whose verb has no object.
- **Contradictions** — two tasks assuming different shapes of the same thing, or an
  order in which a task needs output from a later one.
- **Scope** — anything the definition of done does not require. Cut it and say what
  you cut; an autonomous run builds whatever is on the list.
- **Ambiguity** — a task an implementer could read two ways. It will be read by a
  fresh subagent with none of this conversation, so pick a reading and write it down.
- **Missing brief** — no Global Constraints, a shared type described in prose, or a
  task without its tier, independence marker, tests or acceptance criteria.

Fix these inline; no second pass. A consequential choice the review exposes goes back
to Phase 1.

Longshot owns the final start gate; nested planning and review workflows must stay
read-only and return here without implementing. Any new consequential decision
returns to Phase 1. Resolving it does not itself approve implementation.

### Final gate — start implementation

Present the settled decisions, the concrete plan, writable repo boundaries,
definition of done, and the contract above. Say that preparation is complete and
ask **"Start implementation with this plan? After you approve, you can leave it
running; I'll handle later decisions and report milestones."** Then wait for an
explicit reply. This is the single final confirmation that the user is done
attending preparation, even when the original brief settled every decision.

A clear "yes", "looks good", "go ahead", or equivalent in response to this gate
starts implementation immediately; do not ask again. If the reply changes scope
or leaves a consequential choice unresolved, settle it and present the revised
gate. Earlier answers to interview questions do not count as approval of this gate.

After approval, announce **"Implementation is starting. Up-front questions are
complete; you can leave this running. I'll decide later details and send milestone
updates."** Only now activate autonomous rulings, save the plan, create worktrees,
dispatch implementers, or make implementation edits and commits.

Open the ledger at `docs/plans/<YYYY-MM-DD>-<slug>-ledger.md` (see
`references/prompts.md` for its shape). Record the approved plan and the user's
actual start-approval message before the first ruling. Append to it for the rest
of the run; it lives on disk so the phase and approval survive compaction.

Create the run directory `RUN=${TMPDIR:-/tmp}/longshot-<slug>` for check logs and
review findings. Those are working artifacts, not the record — anything that
outlives its fix loop goes in the ledger. **Keeping them on disk instead of in this
session's context is what lets a long run finish without compacting**, so route
them there even when a report looks short enough to read inline.

## Phase 3 — Isolation

Follow the workflow file. Default:

- Work on the primary repo's current branch unless the user requests another branch.
- **Every foreign repo gets a worktree**, branched off its main:
  `git worktree add ../<project>-worktrees/<repo> -b <feature> ../all/<repo>`.
  Never commit to a foreign repo's `main`. Never combine two repos in one commit.
- `--no-worktree` skips this and works in place.

## Phase 4 — The execution loop

Per plan task, in order. **Sequential — one subagent at a time.** This fixed fan-out
is the skill's own and needs no further dispatch approval; do not widen it.

1. **Implement.** One fresh write-capable `general-purpose` subagent. Construct its
   prompt from scratch — it inherits nothing. It must carry the literal line
   *"Do not dispatch sub-agents; do this work yourself."* Template in
   `references/prompts.md`.
2. **Review.** One fresh `general-purpose` subagent that has not seen the
   implementer's reasoning checks the diff against that task's plan section on
   **both** spec compliance and code quality. It modifies nothing but its findings
   file — not `Explore`, which skims excerpts to locate code rather than audit it,
   and cannot write a file. It writes its findings to `$RUN/review-task-<n>.md` and
   returns only the path, a count and the severities. The findings themselves never
   enter this session's context.
3. **Fix loop.** Hand the fixer the findings *path*, not the findings — passing the
   text through here bills it twice. Then re-review, scoped to those fixes only.
   **Two rounds by default**, a third only if round 2 actually closed findings; then
   rule on what is left, record it in the ledger, and move on.
4. **Verify yourself.** Run the project's own check command (`just check`,
   `npm test`, `cargo test` …) in this session. Never delegate this — a subagent
   reporting "all tests pass" is not evidence. Redirect it and read the end:

   ```
   just check > "$RUN/check-task-<n>.log" 2>&1; echo "exit=$?"; tail -30 "$RUN/check-task-<n>.log"
   ```

   The exit code and the summary line are the verdict, and a green suite costs you
   thirty lines instead of thousands. **A non-zero exit, or a summary naming
   failures, means you open the log and read it properly** — that is not optional,
   and it is where the tokens belong. What you must never do is grep the log for the
   outcome you expect. Failures get fixed, never labelled pre-existing.
5. **Commit** the task's work, per the project's commit convention.
6. **Ping.** One line (see below), then straight into the next task.

**Parallel tasks** only when the plan marks them independent *and* they live in
different worktrees — max 3 at once, still one implementer each.

**Whatever you cannot run** (a GUI test host, a credentialed deploy, a sandbox-blocked
suite) is compile-verified as far as possible, recorded, and carried to the handoff's
"only you can do" list. It is not a reason to stop.

### Model per role

Pass `model` on every dispatch. An omitted one inherits the session model — usually
the most expensive — and that silently puts routine implementation on the top tier.
The names are Claude Code's; on another harness use its equivalent tier.

| Role | Model |
|---|---|
| Implementer, `Tier: standard` | `sonnet` |
| Implementer, `Tier: design` | `opus` |
| Reviewer | `sonnet`; `opus` for a `design` task, or a diff touching concurrency, security, a persisted format or a repo boundary |
| Scoped re-review | `sonnet` |
| Fixer | `sonnet`; `opus` in round 3 |
| Phase 5 contract reviewer and fix wave | `opus` — `code-review` picks its own models |

`haiku` is left out on purpose: working from prose over several steps it takes more
turns than it saves in price. The tier comes from the approved plan, not from a
judgment made mid-run.

### Milestone pings

After each task's verify, exactly one line. No question, no invitation to respond:

```
Task 3/6 done — consumer registry + bounded sink fan-out, 41 tests, clippy clean. On to install/hooks.
```

## Phase 5 — Whole-branch review

Per the workflow file. Default: `code-review` over the full diff of every touched
repo (`--quick` only if the whole longshot was small), then a fix wave, then a
re-review scoped to those fixes. Cross-repo runs get one reviewer whose job is
**contract coherence** — wire formats, manifest shapes, command strings, identity
semantics agreeing across repo boundaries.

These are the largest reports in the run, so the same rule binds hardest here:
findings go to `$RUN/review-branch.md` and `$RUN/review-contract.md`, the fix wave
gets the path, and this session reads the count and the severities. Pull a finding
into context only when you need to rule on it.

## Phase 6 — Harvest and handoff

**Harvest the plan into the docs, then delete it.** A dated plan is stale the day
the work lands, and whoever reads the repo next will not find it. Move what is still
true and still useful into the repo's canonical docs — architecture or design docs,
README, `AGENTS.md`, wherever the repo keeps such things (`doc --session` if it has a
doc set): the design decisions and why they were made, the shared interfaces as
built, and any constraint on future work. Leave behind the task list, the
checkboxes and anything the code now says. Then delete the plan the run saved and
commit both. A plan the user supplied was theirs before the run — harvest it the
same way but propose its deletion in the handoff rather than doing it.

The ledger stays until the user has read the handoff: it is the record of what was
decided on their behalf. Its rulings that constrain future work are harvested now;
the file itself is deleted once the user confirms the squash, and folds into it.
Remove `$RUN` at the same time.

Then one report. Template in `references/prompts.md`. It must contain:

- **What exists, where** — a repo / path / branch / commit-count table.
- **Where the plan went** — which docs received what, and that the plan was deleted.
- **Only you can do** — each blocked check with the exact command to run.
- **Rulings** — the ledger, grouped scope vs. design, each as
  decision — why — cost if wrong.
- **Deferred questions** — everything collected but not urgent enough to break the
  contract.
- **Squash proposal** — the concrete before/after commit list, awaiting a yes.
  Never rewrite history without one (delegate to `squash-commits` once approved).
- **Nothing was pushed** — and which checkouts were left untouched.

## Default workflow

Used only when the project has no workflow file:

> Pick the next task → parallelizable? send it to a worktree → plan it → big? review
> the plan multi-agent → implement → QA → code-review (multi; quick for small) → fix
> everything → squash → re-integrate the worktree.

## Examples

### Example: a package to be integrated by two other repos

User: *"Work on this fairly independently. Other repos are under `../all/juggler` and
`../all/ringleader`. Ask whatever you need up front so you can work independently
after. Follow `./workflow.md`. In the end I want a complete package I can integrate.
One question to start: what about sessions that get killed?"*

Actions: read `workflow.md`, the plan doc, both neighbour repos' tooling and the
integration surfaces (3 `Explore` agents) → answer the killed-sessions question with
a recommendation, then `blind-spots`: round 1 asks the questions answerable now
(repo boundary, protocol scope, what "integrate" means, …), round 2 the
two that only became questions once protocol scope was settled → validate the plan
against the repo → present the final plan and contract → wait for start approval →
announce implementation starting → worktree per consumer repo → 6 tasks through
the loop with pings → whole-branch review + contract-coherence pass + fix wave → handoff.

Result: three branches ready to integrate, a rulings ledger explaining every decision
made in the user's absence, one XCTest run flagged as theirs to do, and a squash plan
waiting on a yes. Zero required user turns between start approval and the report.

### Example: unanswered choices in an asynchronous prompt

The agent asks whether a file contains a complete prompt or reusable instructions,
and whether redirected stdin should be read automatically. Both have recommended
options, but the user has not replied. The question tool returns immediately.

Actions: keep both questions pending; do only independent read-only work, then
yield. If the user says "use both recommendations", record those answers and
finish any dependent questions and planning. Present the final start gate and
wait. Once the user approves that gate, announce implementation and proceed.

### Example: too small for longshot

User: *"Add a `--json` flag to the export command, run it independently."*

Action: say this is a `plan`-sized task, not a longshot, and offer to run `plan`
instead. Longshot's overhead only pays off across many tasks.

## Troubleshooting

### The agent accepts its own interview recommendations

**Cause:** applying implementation autonomy during preparation, or treating a
question tool's return or preselected option as a user answer.
**Solution:** keep the questions pending. Read the user's actual replies; wait for
answers and final start approval. Waiting during preparation is required.

### Implementation stalls waiting for the user anyway

**Cause:** treating an ambiguity as a stop condition after start approval.
**Solution:** verify that implementation was approved, then re-read the four stops.
If it is not one of them, decide, write the ruling, continue. A plan defect is a
ruling. A conflict between the plan and the spec is a ruling — the spec wins.

### Reviews keep passing but the code is wrong

**Cause:** the reviewer inherited the implementer's framing, or you accepted a
subagent's word for a green suite.
**Solution:** the reviewer must be a fresh agent given the diff and the plan
section, never the implementer's report, running on at least `sonnet` — an
undeclared model or an `Explore` agent can quietly downgrade the gate. And run the
check command yourself in Phase 4 step 4 — that step is not delegable.

### Context runs out mid-run

**Cause:** a multi-hour run outlives its context window.
**Solution:** recover the current phase and the user's replies first. Pending
questions and an unapproved start gate stay pending. During implementation,
re-read the plan and ledger, including the recorded start approval, and resume at
the first unchecked task. A plan or ledger existing is not itself approval. If
approval cannot be recovered, ask before implementing; never invent it.

### The user comes back mid-run and asks something

**Cause:** normal — the contract binds you, not them.
**Solution:** answer, then resume. Do not turn it into a check-in or re-open the
interrogation.
