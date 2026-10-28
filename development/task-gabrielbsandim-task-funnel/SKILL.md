---
name: task
description: "Delivery funnel for one repository task: a feature, bug fix, refactor or chore, from description or issue number to a pushed branch and a draft pull request with the board moved. Use whenever the user asks, in any language, to implement, fix, build, change or refactor something in this repository, including requests like \"fix this and leave it ready for a PR\", \"open a pull request for\", or a bare issue number, and on /task <description | issue number>. Not for questions about why something happens: that is investigate. Every path, gate command and board id comes from .claude/funnel.config.json, so this runs on any stack."
---

# task: one task, from description to draft pull request

You run the funnel **and you write the code**. Agents read: a premise check before a
risky change, a test writer that works before the code exists, a reviewer and a
verifier after it. None of them writes production code, and none of them approves
what you wrote.

Input: the task description or issue number after the command. Empty → ask which
task and stop.

Two files sit next to this one and are **not** loaded with it. `review.md` is stage 4
in full, and stage 4 says to read it before dispatching. `evidence.md` is the
measurement behind every rule here that reads as arbitrary; open it when you are about
to disagree with a rule or adapt the funnel to a repository it was not written
against, never to run a task.

## The repo describes itself

Nothing in this skill knows your paths, commands or board. All of that is in
`.claude/funnel.config.json`, read through `kit`:

```
kit doctor                     # is this machine and this repo ready
kit config get .base           # the base branch
kit config gates ship          # which gates a stage runs
kit lane src/billing/fee.ts    # direct or risk, from the repo's risk.paths
kit review                     # the review plan for this branch's lane
```

If `kit` is not on PATH, or cannot run (a sandbox that hides the directory its link
points into), use the copy shipped beside this skill for the whole task:
`${CLAUDE_PLUGIN_ROOT}/scripts/kit`. Write that absolute path wherever this skill, its
reference files or an agent's dispatch says `kit`, because a Bash call does not keep
an alias. `/task-funnel:setup` puts `kit` on PATH for later sessions. If the repo has
no config, `kit config init` writes a starting one and `kit config check` validates it.

## Before stage 0: is this skill the one that shipped

```
kit version 0.18.2
```

The literal is the version this file shipped in, so the command compares the text you
are reading against what is installed (`evidence.md` &middot; *Stale kit*).

- **STALE SKILL**: the caller declares a version newer than anything installed, so
  this skill was loaded from a directory (a plugin under development, or an eval)
  and the `kit` on PATH belongs to an older copy. Use
  `${CLAUDE_PLUGIN_ROOT}/scripts/kit` for the whole task, as above, and carry on.
- **STALE KIT**: run the `kit setup` line it prints, then carry on.
- **`unknown subcommand: version`**: the `kit` on PATH is older than 0.3.0. `kit setup`
  from the newest installed copy fixes it:
  `ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/*/task-funnel/*/ | sort -V | tail -1`.
- Anything else: carry on without mentioning it.

## Rules that hold for the whole funnel

- **The repo's own pipeline document wins.** `kit config get .docs.pipeline` names
  it. Where it and this skill disagree, that document is right.
- **Verification is inside the loop, and it is the repo's gate.** Every change to
  source is followed by `kit gate <stage>` before you report it, never by a bare
  `tsc` or `vitest`: the gate carries the environment the repo needs (a heap size, a
  flag) and leaves a receipt. A Stop hook refuses to end a turn that changed code in
  a funnel checkout without one, and a guard refuses a gate's tool run without its
  environment.
- **Full spec in every dispatch.** A subagent inherits none of your context. Every
  prompt carries objective, file scope, prohibitions and acceptance criteria, the
  prohibitions always including: _you are one stage inside the task funnel; do not
  invoke the task or investigate skills yourself_.
- **Never write a `model` field into a dispatch.** Every agent declares its model in
  its own frontmatter, and a `model` in the Agent input silently overrides it. The
  only exception is a `model:` line `kit review` printed (`evidence.md` &middot; *The
  model of a dispatch*).
- **The writer never approves their own work.** You write; review runs in clean
  agents that did not.
- **Never merge.** The funnel ends at the draft pull request.
- **An inherited claim is not a fact.** A triage finding carried into the spec is
  marked **MEASURED**, with the command that proved it, or **INFERRED**, and whoever
  writes an INFERRED claim into code measures it first.
- **Everything the funnel writes is English**, whatever language the conversation is
  in: branch, commits, pull request, code, comments, dispatch labels. Talk to the user
  in their language.
- **A code comment says why, in at most two lines.** No ticket key, pull request
  number, date or count.
- **A new issue is the last resort, and never an orphan.** Before creating one, run
  `kit issues related "<title>" --files a.ts,b.ts --parent <epic>`; two distinctive
  files in common means it is the same work. If you create it, link it to a parent
  (`evidence.md` &middot; *Orphan issues*).
- **One task per session on the risk lane.** You write the code now, so the session
  carries the task's whole context, and the next task should not inherit it. After the
  report, say `/clear` is the next step.
- **Compact at a boundary, by prefix size, and always before a long pause.**
  `kit context` prints **HOLD** below 120k tokens in context, **AT THE NEXT BOUNDARY**
  from 120k to 300k, **NOW** above 300k, and **LATE** below 15% of the window free. The
  end of a unit of work is the trigger, and a large prefix before a pause is the one
  place a single request costs five dollars (`evidence.md` &middot; *Prefix rewrite*,
  *Why the bands are token counts*, *A pause is the expensive moment*).

## Stage 0 · Pre-flight and the lane, read-only

- `kit doctor`. A missing `project` scope or an invalid config is cheaper to find now.
- Issue number known → run the pre-flight the pipeline document prescribes for picking
  up an issue. An existing remote branch may mean the issue is taken, abandoned or done.
- `git status` clean, including your own edits.
- No worktree yet: the environment is paid for after the spec says the task is real.
- **Which lane.** Answered here, before anything is dispatched, because the risk lane's
  first step is already its most expensive question (`evidence.md` &middot; *The
  triage floor*).

### Three lanes, decided by what the change can break

**Not a line count.** One line in an auth guard is the most dangerous change in the
repository and thirty lines of copy are nothing, so size is the wrong axis. The axis is
which surface moves:

| Surface | Examples of it moving | Lane |
| --- | --- | --- |
| Money, permission, tenancy | anything a customer is charged, refused or shown | risk |
| Data | a migration, a write path, a query's scope, a cache key | risk |
| Contract | a signature, route, schema or exported type another module reads | risk |
| Behaviour | a new branch, a new state, an order of operations, a cap or a retry | direct |
| Published prose | a help entry, a policy, the assistant corpus, a public document | direct |
| None of the above | a copy string, a config value, a comment, a typo, a rename in one file | trivial |

Then ask the repo. `kit lane <the files you expect to change>` prints `risk` when any
of them matches the config's `risk.paths`, and a repo's list of risky paths outranks
your reading of the table: it was written by someone who knows which files bite.
After code exists, `kit lane` with no argument reads the branch's own diff.

- **direct** is the default: most tasks. You write a short spec, write the code, the
  gates run, one reviewer reads it, a verifier checks each finding, and that is the
  only review round.
- **risk** buys the premise check, tests written before the code, five review lenses
  and a second round that reads only the fix.
- **trivial** is the direct lane without the review, for a change no reviewer would
  have anything to read in.

**Announce and proceed, without waiting.** Say in one line which lane and which
surface decided it, then run it. The user chose announce-and-proceed on 2026-08-18,
over announce-and-confirm, so a confirmation round here is the cost that decision
rejected. Naming the criterion is what makes it arguable: the user can stop you
before anything is written.

**Uncertainty goes up, never down.** If the table is arguable, take the higher lane.
Escalating late costs the minutes already spent; a risky change on the direct lane
ships a defect with a green report attached. Triage may raise a direct task to risk
(the user says so, or the premise check finds a surface you missed); nothing lowers a
risk task except the triage verdict `DIRECT_LANE`.

### What every lane runs

The lanes differ in who reads the change. They do not differ in the rails:

| Step | Risk | Direct | Trivial |
| --- | --- | --- | --- |
| Stage 0 pre-flight | yes | yes | yes |
| Board to in progress | yes | yes | yes |
| Branch and worktree from the config | yes | yes | yes |
| `kit gate` for the stage | yes | yes | yes |
| Commit under the repo's convention | yes | yes | yes |
| `kit gate ship`, push, draft pull request | yes | yes | yes |
| Body under the `kit pr-body` budget | yes | yes | yes |
| `kit board in_review`, `kit worktree gc --yes` | yes | yes | yes |
| Premise check (triage) and spec approval | yes | no | no |
| Tests written before the code, by an agent | yes | no | no |
| Review rounds, each finding verified | 2 | 1 | 0 |

An issue already on the board is used and moved; the trivial lane never creates one,
because a typo that opens an issue is backlog growth nobody decided on.

### A repo on the lite lane

`kit config get .lane` printing `lite` means the repo chose one reviewer and one round
for every task. Run the direct lane, and on a risky path `kit review` adds the risk
lenses to that one round instead of buying a second.

## The agents this skill dispatches

Each dispatch names its agent, because a generic "dispatch a reviewer" resolves to a
general-purpose agent and the standing instructions in these files are lost:

| Stage | Agent | Model | Lane | Carries |
| --- | --- | --- | --- | --- |
| 1 | `task-funnel:funnel-triage` | inherit | risk | the premise questions, the return shape, the invariant table |
| 2 | `task-funnel:funnel-test-writer` | sonnet | risk | tests from the spec before the code, and proof each fails for its reason |
| 4 | `task-funnel:funnel-reviewer` | sonnet | direct, risk | the reading discipline, Critical and Important only, NEW against PRE-EXISTING |
| 4 | `task-funnel:funnel-verifier` | sonnet | direct, risk | refute each finding, and REAL only with a trace or a reproduction |
| 4 | `task-funnel:funnel-screen-lens` | inherit | risk, when a screen moved | report only what you observed, and NOT PROVEN is not a pass |

There is no implementer agent. It was removed in 0.18.0: half of what it cost went to
fix rounds re-reading a repository the session already had in context
(`evidence.md` &middot; *The funnel, measured over five weeks*).

## Stage 1 · The spec

### Direct and trivial: inline

Write it yourself in 3 to 5 lines: what, why, the files, and the acceptance in one
sentence a test can check. For a bug, the acceptance is the failing test that
reproduces it. Show it as part of the lane announcement and continue.

### Risk: the premise check

One dispatch to `funnel-triage`, structured return, even when the user hands you a
spec already approved: approval settles what to build, and the premise check measures
whether the code is what the request assumes. The gate reads `VERDICT` first:

- `PROCEED` → show the user the spec in 5 to 10 lines, with the PREMISE block, and
  **wait for approval**, unless the user already approved this spec and the PREMISE
  block contradicts nothing in it. This is the one question the funnel keeps, because a spec that
  is wrong makes every later stage correct against the wrong thing.
- `DIRECT_LANE` → the premise holds and no risky surface moves. Say so in one line with
  what triage checked, and run the direct lane on the spec it returned. Do not
  re-dispatch triage to get a different answer, which is US$ 2.46 spent to disagree
  with the first one.
- `NEEDS_DECISION` or `BLOCKED` → stop and present the evidence. AskUserQuestion when
  the alternatives are objective.
- `ALREADY_DONE` → stop and show the commit or the code.

`NEEDS_DECISION` answered by an investigation → **stage 1 does not run again.** The
child issue the investigation produced arrives with measured scope and criteria, which
is more than triage returns; write the spec from the investigation and go to stage 2.
Run stage 0 against the child's number, because a branch may exist for it
(`evidence.md` &middot; *Paying triage twice*).

`PROCEED` with no issue yet → open one the way the pipeline document says, and re-run
the stage 0 pre-flight against its number.

### Invariants, not only criteria

On the run this funnel was first measured on, three of four review rounds went to one
rule nobody had written down (`evidence.md` &middot; *One invariant, found three
times*). So the spec names them up front, on every lane:

| Scope in the spec     | The invariant it carries                                                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Money**             | every path that spends records the spend, **including the one that throws**; a cap sums an aggregate, never a rounded per-row value    |
| **External call**     | every new call has a timeout and a `catch`; the `catch` logs what was lost, because a silent `return { status: 'failed' }` is no handler |
| **Untrusted inbound** | the response code is chosen for the sender, not for us; a path that always answers 200 must not be the path that swallows a retry      |
| **Prose it touches**  | any comment, document or knowledge entry the change **falsifies** moves in the same commit, not only the ones it adds                  |

Too big for one reviewable pull request → present the slices and stop.

### Self-review, inline, before you show the spec

Not a subagent. Ask yourself, in writing:

1. Which acceptance criterion cannot be checked by a command or a test?
2. Which file in scope has no criterion attached, and which criterion has no file?
3. Which invariant above applies and is not stated?
4. What would make this "the spec was wrong" rather than "the code was wrong"?

## Stage 2 · The worktree, and on the risk lane the tests

**Risk lane: no worktree without a `funnel-triage` VERDICT from this task.** Measuring
the bug yourself is not it: the premise check is a reader that did not write the
spec, and a spec the user approved in the request does not skip it.

```
kit worktree add <issue> <slug> --kind <feature|bug|refactor|chore>
kit board in_progress --issue <issue>
```

The board move belongs here, right after the worktree exists: the first instant at
which there is work another cycle must not pick up.

**A refused git step is reported, never inferred.** Run `kit worktree add` even when a
probe says git is read-only, because its own error is the evidence the report needs. If
it, or a plain `git switch -c`, is refused, the change is still written in the checkout
with the Edit tool (a sandbox can refuse a shell write and allow Edit, so a failed
`touch` proves nothing about Edit), the stage's gates still run, nothing is committed
to trunk, and the report names each refused step with its error.

**Risk lane: the tests come first.** Dispatch the spec, including its INTERFACE line,
to `funnel-test-writer`, working in the worktree. It writes the tests from the
acceptance criteria and the invariants, runs them, and commits them failing.

**GATE**: every new test fails, and for the reason its criterion names (an assertion on
the value, or the missing export the INTERFACE declares). A test that passes before the
code exists asserts nothing about the change; send it back once, with the test named.

A test written after the code tests the code that was written. One written from the
spec tests what was asked for, and the independence is measured: tests from an agent
that never saw the code were correct 88% of the time, against 61% for the agent
testing its own (`evidence.md` &middot; *Tests before the code*).

**Direct lane**: you write the tests, and for a bug the reproduction comes first:
write it, watch it fail, then fix.

## Stage 3 · Implement, in this session

Write the change in the worktree, against the spec. On the risk lane, the goal is the
test writer's tests passing **without editing them**: a test that looks wrong is a
spec question, raised with the user, not an edit. The `protect-tests` hook refuses the
usual ways a suite gets faked.

**GATE**: `kit gate implement_first_pass`, then the work **committed** per the repo's
commit convention. The review diffs commits, so uncommitted work is invisible to it.

**A red gate is not automatically your defect.** `kit gate` prints a `flake` line when
a failing file is on the config's quarantine list, and says whether this branch's diff
can reach it. A red gate in a file the diff never touched is a re-run of that file, not
a fix. A gate that stays red after two honest attempts is a report, with the output.

On a doc-only scope the worktree has no dependencies installed, so no gate command can
run. The gate is then the commit alone.

## Stage 4 · Review, counted by `kit`

```
kit review                       # this branch's lane, first round
kit review --since <sha>         # risk lane only: the fix round
```

`kit review` decides the lane from `risk.paths` and prints `lane, round N of M`;
`kit review risk` or `kit review direct` passes on a lane triage or the user decided.
**The cap is counted, not remembered**: a branch gets one round on the direct lane and
two on the risk lane, and a further `kit review` on a new head is refused. Two pull
requests once ran 21 and 25 rounds under a written cap of 2 and cost 14% of everything
the funnel spent in five weeks (`evidence.md` &middot; *Rounds without a counter*).
Only the user buys another round, with `--reset-rounds`.

### Before the dispatches go out

Read `review.md` in this skill's directory now. What a skipped read must not lose:

- **Give each printed block verbatim to its own `funnel-reviewer`**, plus only this
  task's half: what the change is for, the acceptance criteria, what was deliberately
  left out, and from round 2 the `ALREADY DECIDED` list. The agent already carries the
  reading discipline, the rubric and the return shape.
- **The browser half runs only on the risk lane, when `kit screens` returns a route
  and `kit screens --preflight` prints `ready`.** Exactly one screen lens at a time, and
  you bring the app up, because the lens has no `Bash`. A preflight blocker is named in
  the report, never worked around inside the lens.
- **Every finding goes to `funnel-verifier` before it costs anything.** One dispatch
  per round, all of that round's findings in it, the worktree path and the diff files.
  Only REAL findings are fixed. REFUTED is dropped. PRE-EXISTING goes to the body as
  one line, after `kit issues related`.
- **REAL findings are fixed in this session, all of them, in one pass**, then
  `kit gate implement_fix_round` and one commit. They are not deferred: a verified
  defect in this change is this change's work.
- **The direct lane stops there.** The fix ships on its gates. **The risk lane** runs
  `kit review --since <the sha round 1 reviewed>` once: the reviewer gets the fix diff
  and the round 1 findings, answers ADDRESSED or NOT ADDRESSED, and reports only new
  Critical or Important breakage inside the fix. Its findings go through the verifier
  the same way.
- **At the cap every open finding gets a written decision** in the pull request body.
  Silent discard is prohibited, and a round whose fix is larger than the original
  commit is the spec having been wrong: say so and stop.

## Stage 5 · Ship

1. `kit gate ship`. Gates whose receipt already covers this exact tree are skipped and
   say so. The tree SHA includes untracked files, so any edit invalidates the receipt.
2. Push. The fix for a red pre-push hook is the failing check, never `--no-verify`.
3. Open the pull request exactly as the pipeline document says: base, draft state and
   issue reference are its decisions. Fill the repo's template honestly.

   **The body has a budget, and it is checked.** Write it to a file and run
   `kit pr-body <file>` before `gh pr create`: at most **2000 characters of prose** and
   **600 per section**, not counting the template, tables, checkboxes or fenced blocks.
   Cut, do not relocate (`evidence.md` &middot; *A body that competes with the diff*).

   The body carries, and nothing else: what changed and why, in the template's own
   sections; what to check; the findings table, one row per finding that reached the
   verifier, which costs no prose; what is knowingly left out and who owns it; and on
   its last line the lane marker, `<!-- funnel: direct -->` or `<!-- funnel: risk -->`,
   which is how `kit escapes` later tells the lanes apart.

   There is no separate findings comment. The table is in the body, and a comment
   answering a person's question in review goes through `kit ledger`, which measures
   it on a comment's budget.
4. `kit board in_review --issue <issue>`, after the pull request URL exists.
5. Never `done`. The tracker's own automation owns that column.
6. `kit worktree gc --yes`, not `rm`. The pull request is open at exactly this head and
   everything is pushed, which is the definition of finished (`evidence.md` &middot;
   *The worktree leak*).

## Stage 6 · Report

**Six items, hard cap, at most 600 characters of prose in total.** Anything that does
not fit goes in the pull request body's budget or nowhere (`evidence.md` &middot; *Why
the budget is in characters*).

1. The pull request link, its draft state and base, the issue it closes, and the lane.
2. What changed, in one sentence naming the class of defect, not each instance.
3. Gates: the count that ran, failed and was skipped by receipt, and the tree SHA.
4. Review: rounds used of the lane's cap, findings by severity, how many the verifier
   refuted.
5. What was left out, and the issue that owns it. If this run created issues, the count
   and the parent each one hangs under.
6. What needs the user, or "nothing". On the risk lane, `/clear` before the next task.

Then `kit context`, and say the verdict in item 6 when it is anything but HOLD.

A gate that stopped the funnel replaces line 1 and is named without varnish. A number
with no command behind it is not a number. Never declare done without lines 3 and 4.

## How to know the funnel is paying

```
kit escapes                     # merged pull requests a later fix corrected, by lane and month
kit usage --all --by-stage      # what each stage cost, per run
kit eval-delta evals/results/*.json   # what the plugin changes against the bare model
```

The funnel's claim is fewer escapes on the risk lane than off the funnel, at a cost
per task the direct lane keeps close to working without it. Each escape `kit escapes`
finds becomes an eval case with `kit escapes --case <n> --out evals`, so the suite
grows from the defects that actually shipped (`evidence.md` &middot; *Measuring
escapes*).
