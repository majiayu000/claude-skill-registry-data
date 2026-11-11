---
name: advance
description: "Move a contract forward by exactly one step. Asks the script what the next move is, then takes it: start the sub-tasks that are ready, escalate a failure to the architect, land a finished contract that has a parent branch (a background script, no question asked) or hand one without a parent branch to verification, or report what is blocked and why. Makes one move and stops, because a merge-gated loop suspends until somebody merges and /pr-merged wakes it. Use when: user says /advance, 'what is next on this contract', 'start the next sub-task', 'continue the contract', or after /pr-merged reports newly released sub-tasks. Never iterates on its own."
user_invocable: true
---

# /advance — move the contract one step

A contract decomposes into sub-tasks, and each one ends in a pull request somebody has to
merge. So the work cannot run start to finish on its own. It moves one step, then waits.

This skill takes that step.

```
/advance <contract>
   ask the script for the next move
   ->  dispatch what is ready     (start it, open a pull request, STOP)
   ->  escalate a failure         (architect re-entry)
   ->  land a finished contract   (parent branch: background landing script)
   ->  hand a finished contract   (no parent branch: /verify-before-done)
   ->  report what is blocked     (and exactly what holds it)
```

## The rule that shapes everything here

**One move, then stop.** This skill never loops.

A merge-gated contract spends most of its life waiting for a person. The step that follows a
dispatch is a human merging a pull request, and nothing here can do that or wait for it. So
this skill acts once and hands back.

`/pr-merged` is what wakes it again. Somebody merges, that phase records the completion and
computes what it released, and `/advance` runs again to start the released work.

Between the two, that is the loop. Neither half iterates.

## Step 1: Ask the script, do not re-derive

### Finding the script, under either install mode

The script ships with the plugin **and** with a vendored copy, but it sits at a different
place in each. Resolve it once, then use the result:

```bash
PRM=
S=.claude/scripts/pr_merged.py
if [ -f "$S" ]; then PRM=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then PRM=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  PRM=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$PRM" --contract <slug|path> --locate-parent
```

A vendored project finds its own copy first. A plugin install finds the running version through `$CLAUDE_PLUGIN_ROOT`, then the install `installed_plugins.json` records, then the newest cache folder by version number. **If `PRM` comes
back empty, stop and say so** — the loop's every rule lives in that file, and a skill that
cannot find it can only guess at what it says.



### Locate the parent branch's worktree first

Work happens in a worktree, never in the main checkout. Before the `--status` call below, find where the contract's parent branch lives and stand there. Run this from wherever the session starts:

```bash
py -3 "$PRM" --contract <slug|path> --locate-parent
```

It takes the slug from the argument, needs no local copy of the contract, and writes nothing but a `git fetch`. Act on `status`:

| `status` | Do |
|---|---|
| `already-here` | Continue. This checkout is the parent worktree, or this contract's detached advance worktree. |
| `found` | `EnterWorktree` with the reported `worktree` path, then continue there. |
| `held-by-main-checkout` | If `worktree` is set, enter it. Otherwise run `py -3 .claude/scripts/flat_worktree.py --create --action advance --slug <slug> --detached <plan.ref>` and enter the plan's `path`. Continue there. |
| `ahead-of-origin` | Stop and print the reported `remedy` (`git push origin <parent>`, which the guard allows). Run `/advance` again after it. |
| `not-checked-out` | Run `py -3 .claude/scripts/flat_worktree.py --create --action advance --slug <slug> --existing --branch <parent>`, enter the plan's `path`, continue. |
| `on-default`, `not-found`, `ambiguous` | Stop, say which, and name the remedy: the contract is already on the default branch, or no branch carries it, or two do and the operator must name one. Do not create a worktree to get around it. |

**Parent held by the main checkout.** Work continues in the detached flat worktree, and the main checkout is never touched. Commits made there are published only with `git push origin HEAD:refs/heads/<parent>`: never `--force`, `--force-with-lease` or a `+` refspec, so git itself refuses anything but a fast-forward. If the push is refused, halt with: "the parent moved on origin; `git fetch` and `git merge --ff-only origin/<parent>` here, then retry". No step is left to a person. `/ship` follows the same rule.

**A subagent handoff ending `BLOCKED: main checkout <target>` halts the run.** The guard refused a write because the stage was launched from the main checkout. Do not retry it there: enter the packet's worktree with `EnterWorktree` and relaunch the stage.

```bash
py -3 "$PRM" --contract <slug|path> --status --json
```

The script owns every rule about sub-tasks, dependencies, records and readiness. It is covered
by 760 tests — measured by running `py -3 .claude/scripts/tests/test_pr_merged.py`, whose own
`unittest` summary line reads `Ran 760 tests ... OK` (exit code 0) — and has been mutation-probed. **Read its
answer. Do not recompute it from the contract**, or there are two implementations of the same
rules and they will disagree.

The answer carries `next_move.action`, plus `dispatch` packets when there is something to start.

**Read `records_reading` first, before `next_move`.** The report says whether completion records are
on their way to origin. Branch on it:

| What the report says | Do |
|---|---|
| No `records_reading` key | An older vendored script. Halt with: "this `pr_merged.py` predates 0.14.0: sync the vendored copy (`tools/sync-plugin.cmd`)". The same halt applies when any call exits 2 with `unrecognized arguments:` naming `--sweep-records`, `--from`, `--removed`, `--discard-differing` or `--local-evidence-only`. An absent key never reads as "nothing pending". Any other exit 2 without a JSON `error` is printed verbatim and halts |
| `records_reading: unverifiable` | Halt and dispatch nothing. Print the Next Command's reason: for `records_failure: transient`, retry once git and GitHub answer; for `persistent`, fix the named cause (repair the named record through a records pull request, or install or authenticate `gh`). Dispatch stays refused until then |
| `records_unpushed` or `records_stranded` not empty | Run the records step (`/pr-merged --records <slug>`, which is `references/contract-completion.md` "The records pull request" steps 6 to 9), then read `--status --json` again. Never dispatch on top of unpushed records. A `--dispatch` call that exits **12** with `error` `records-unpushed` or `records-unverifiable` means the same: stop and do this row or the row above |
| `records_differing` not empty | Show each `remedy` (`/pr-merged --records <slug> --discard-differing <path>`, run only when the owner names the path) and continue |
| `records_reading: ok` and the lists empty | Continue with `next_move` |

`--local-evidence-only` is passed through to `pr_merged.py` only on the owner's word. It skips deleting and
pushing records for that call and nothing else: it never changes the evidence, never lifts a hold and
never unblocks dispatch.

### Where this runs, and what a surprising answer usually means

**Run it from a checkout of the contract's parent branch.** The contract, its sub-task briefs and every completion record live on that branch. Until the parent pull request merges, no other branch carries them. The work item brief's `branch:` field names it.

**`contract-not-found` is almost always the wrong branch, not a missing contract.** Before anything else, ask which branch holds the file: `git log --all --oneline -- .claude/concepts/<slug>.md`. Then run the locator above and act on its status. Never switch the main checkout to the parent branch and never edit there: the guard refuses it.

**A released sub-task whose branch or pull request already exists on GitHub means a completion record is missing from this checkout.** A record written on a separate records branch is invisible here until that branch reaches the parent. Dispatching on that answer redoes finished work. Stop, name the sub-task, and say which pull request carries the record. Records on the tip of `docs/<contract-slug>-records` and on `origin/<default>` already count as evidence in the script's answer (`records_reading`), so this backstop catches only a record that no read can see. This rule is about dispatch, which sees only the parent branch. The landing in `complete` below differs on purpose: it also reads records from the `docs/<contract-slug>-records` branch and from `master`, because that is where `/pr-merged` Step 3 puts them.

**Check the packet's `base` against the sub-task brief's `base:` before dispatching for real.** A packet that says the default branch while the brief says the parent branch means the sub-task's identity was never recorded in this checkout's state. Record it first with `--record-subtask`, then dispatch. Otherwise the new branch is cut from the wrong place and misses what earlier sub-tasks built.

**If a separate checkout is genuinely needed, create it flat.** Use an absolute path directly under `<repo>/.claude/worktrees/`, never a relative path from inside another worktree. A nested worktree makes paths so long that the host smoke tests fail with a SqlClient `SNI.dll` load error (`The filename or extension is too long`), which reads like a code defect and is not one.

## Step 2: Take the move the script names

The action set is closed. Each one has exactly one response.

**On every move, show the layout warnings first.** When the status answer carries `layout_warnings` and it is not empty, show each entry's `remedy` to the owner before taking the move, whatever the move is (a `contract-defect` or an `escalate` included). A warning blocks nothing. The key is absent for a contract that is not judged, `[]` when there is nothing to report, and otherwise holds `single-branch-delivery`, `held` (a Records pull request is open: merge it first) or `unverifiable` (an input could not be read: give its re-read remedy).

### `contract-defect` — a block cannot be delivered as written

**Checked before every other action, including `dispatch` and `nothing-planned`.** Report each
entry in `defects` with its block and its reason, then stop. Start nothing.

Two reasons exist. `no-files-but-names-an-agent` is a block that names somebody to do work and
declares no files, so it produces neither a diff nor a record and nothing could ever prove it
ran. `files-but-no-recognised-agent` is a block carrying real files whose agent matches no
entry in the project profile's `implementers` or `review-gates` slots — usually a typo, which
is why the block is still tracked rather than quietly dropped.

**The remedy is editing one line of the contract, not working around it here.** Do not invent
an agent, do not infer a file list, and do not skip the block and carry on with the rest.

This is checked first on purpose. A contract whose blocks are *all* malformed has no sub-tasks
at all, so asking "is anything planned?" first would answer `nothing-planned` about a contract
that declares nine defective blocks — which is the silent discard this action exists to end.

**A layout defect also makes the move `contract-defect`, in place of `dispatch`.** The status report
carries `layout_defects` for a contract with two or more mergeable blocks and a Status of draft or
approved (the Parent Branch Delivery Rule). Each entry has a `reason` (`no-parent-branch`,
`parent-is-default`, `ambiguous`, `no-parent-issue`, `sub-task-raises-version`,
`single-branch-delivery`) and a `remedy`. Report each with its remedy, then stop and start nothing.
A layout defect never changes a move asked before `dispatch`, and it never reaches a stored record.

### `dispatch` — there is work ready to start

**Read the preconditions before choosing what to start.** One read-only call ranks every
released sub-task. It cuts nothing, writes nothing and takes no lock:

```bash
py -3 "$PRM" --contract <slug> --preconditions --json
```

Decide from each sub-task's `rank` and nothing else. This skill probes no port and calls no
`gh` itself; the script already did.

- One sub-task is `ready` → start it.
- Several are `ready` → list them and ask which (the rule below).
- None is `ready` but some are `unknown` → list them, name each `unknown` item, and ask.
- Every sub-task is `held` → dispatch nothing. Report each held sub-task with its unmet items
  and stop. Say plainly why: once `--dispatch` runs, the branch is cut and `awaiting-merge` is
  written, so holding afterwards undoes nothing.

The packet that `--dispatch` returns carries its own `preconditions` too, but that reading is
information only. If it now shows an item unmet, report it and continue on the branch that was
cut, as the `needs_issue` remedy below does. Never dispatch a second time.

**Start it with the script, not by hand.** The branch, the state write and the readiness
re-check all belong to one command:

```bash
py -3 "$PRM" --contract <slug> --dispatch <sub-task-id> --json
```

It cuts the branch from the sub-task's own base. The base comes from the sub-task's recorded
brief when it has one, otherwise from the parent branch the Sub-Task Work Items declare, and
only then from the repository default branch. The packet's `base_source` says which of
`state`, `declared-topology` or `default` decided it. How `create_branch` cuts it depends on
whether a sub-issue is recorded. With one,
`gh issue develop` cuts the branch on GitHub from that base, and the new branch is then fetched.
Without one, it fetches the base first and cuts the branch locally. It then records the sub-task
as `awaiting-merge` with the cut branch in the state store, and returns the packet.

It refuses with `not-released` if the sub-task's dependencies have not landed, so a wrong
identity cannot start work that has nothing to build on. Exit code 7 carries two refusals,
`base-not-declared` and `needs-issue`, told apart by `error`, each with its own `remedy`. `base-not-declared` is for when the Work Item briefs
disagree on the parent branch, or when the dispatched entry carries no declared base while another
entry in the same state already declares a real parent — never a silent fallback to the default
branch beside a sibling that says otherwise; its remedy is recording the sub-task's own identity
first (`--record-subtask <sub-task-id> --issue <n> --base <parent> --brief <path>`, running
`/task` in Parent-aware mode first if it has no brief yet), then dispatching again. `needs-issue` is
for a contract the Parent Branch Delivery Rule judges (two or more mergeable blocks, Status draft or
approved) whose sub-task has no sub-issue recorded; it is computed before the branch is cut, so
it cuts no branch (not even under `--dry-run`, which refuses it too), and its remedy is `/flow`
Step 2.7. Either refusal cuts no branch and writes nothing. Add `--dry-run` to see the packet without cutting anything — both
refusals hold under `--dry-run` too, so a dry run always previews what the real run would do,
while `--status` and `--resume` only report them.

It also refuses with exit code **8**, `gh-repo-set`, when `GH_REPO` is set in the environment —
`--dispatch` can call `gh issue develop` to cut the sub-task's branch against its sub-issue, and
a non-empty `GH_REPO` would retarget that call at another repository entirely. This refusal cuts
no branch and writes nothing either, and it holds under `--dry-run` too. The remedy is unsetting
`GH_REPO` in that shell and dispatching again.

It refuses with exit code **3** and `{"error": "delivery-unrecorded", ...}` when a merged pull request delivered the whole contract on one branch and no delivery is recorded (the `delivery-unrecorded` move below). That refusal cuts no branch and writes nothing. `--dispatch` never exits 10, so this skill needs no handling for that code. It refuses with exit code **12** and `error` `records-unpushed` (records not on their way to origin; the remedy is `/pr-merged --records <slug>`) or `records-unverifiable` (the records could not be read; see the table in Step 1), also under `--dry-run`. `--local-evidence-only` lifts neither.


**The branch is cut in a new flat worktree.** `--dispatch` creates the sub-task branch inside a new flat worktree under `<main checkout>/.claude/worktrees/` and never switches the checkout it runs from. The packet's `worktree` is that worktree's absolute path, and `worktree_created` is true when this run made it (null on a read-only run). A helper refusal comes back as `branch-failed` carrying the helper's outcome (`nested`, `branch-in-main-checkout`, `path-taken`, `fetch-failed` or `git-failed`); stop and report it.

Each packet names the sub-task, its branch, its agent, its file scope, the pre-written TASK
block the architect wrote into the contract, the Sub-Task Cycle, and the sub-task's own
identity.

**The Sub-Task Cycle** — `cycle` (always exactly one stage, since this repository's
decomposition rule already splits a red stage and a green stage across two separate blocks,
each with its own pull request — decided by what the block DECLARES, never by who is assigned)
and `cycle_basis` (which declaration decided it).

**Render `cycle_basis` before dispatching**, so an operator can tell a stage the contract asked
for from an unphased stage the loop fell back to:

| `cycle_basis` | What decided the stage |
|---|---|
| `verdict-bearing` | the block's `Files to touch` names a path under `.claude/reviews/` |
| `declared-phase` | the block's own TASK block declares `phase: RED` or `phase: GREEN` |
| `no-declared-phase` | the block declared neither — the packet's `unphased` stage is the loop's own fallback, never a stage the contract asked for |

Each `stage["stage"]` is one of exactly four names — `review`, `red`, `green`, `unphased`. **Never
print a stage word the packet did not ship.**

**The sub-task's own identity** is read by the caller out of its state entry rather than
re-derived: `issue` (its own sub-issue number, or `null` when none is recorded yet — never the
parent's issue), `base` (the branch its branch and its pull request are cut from — the parent
branch for a Sub-Task Work Item, the default branch for an ordinary one), `brief` (the path to
its Work Item Brief), and `needs_issue` (true only once the contract declares two or more
mergeable sub-tasks and this one's `issue` is still `null`).

**One released sub-task** → start it. **Several** → start the first one in the script's
`released` order, say in one line which one and that the rest stay released, and proceed. Do not
ask which (operator decision 2026-10-09). Start only that one: each is a full implementation run,
and starting three at once spends a lot of work on the operator's behalf. An operator who names a
different sub-task overrides the order.

For the one being started:

1. **The branch already exists** — the dispatch command cut it and recorded it in state.
2. **Dispatch every stage of `cycle`, in order, as its own fresh subagent.** This project's own
   decomposition already splits red and green across two separate sub-tasks (Non-Goals), so
   `cycle` in practice carries exactly one stage — but the loop reads however many the contract
   declares, never a fixed count this prose assumes. For each stage, launch a **fresh subagent**
   of `stage["agent"]` — never this session — addressed by the name in `packet["dispatch_as"]`
   (the namespaced `agentic-auto-improve:<agent>` when only the plugin ships that agent, the bare
   name when the project carries its own), and give it exactly four things: the contract path
   (`packet["contract"]`), the packet's own pre-written TASK block (`packet["task_block"]`), the
   packet's file list (`packet["files"]`), and the branch (`packet["branch"]`).
   `stage["isolation"]` is always the constant `fresh-subagent`: that constant IS the isolation
   an operator used to have to produce by remembering to `/clear` between sub-tasks, and the loop
   now produces it by launching a new subagent per stage instead.
3. **Run `/ship`** to open a draft pull request for that sub-task, and only that sub-task. This
   stays in the main session and is unchanged — Non-Goals rules out the dispatched subagent
   opening its own pull request.
4. **Stop.** Report the pull request and say plainly that the contract now waits for a merge,
   and that `/pr-merged` is what continues it.

**Where each part runs.** Every `pr_merged.py` call (`--status`, `--dispatch`, `--record-subtask`, and `/pr-merged`) runs from the parent worktree, because its state store holds `awaiting-merge`. The cycle stages and `/ship` run in the packet's `worktree`: enter it with `EnterWorktree` by path before launching the stage subagents (a subagent launched afterwards runs there), and keep it for `/ship`. When `/ship` returns, enter the parent worktree by path again before the Step 3 status call. Never `ExitWorktree`, which lands in the main checkout. When the parent is held by the main checkout, the parent worktree is the detached flat worktree, and its commits are published with the no-force push above.

**A packet flagged `needs_agent` names no recognised agent.** Refuse it the same way. Say which
sub-task is missing one, and that its heading must name an agent from the project profile's
`implementers` or `review-gates` slots. Do not pick an agent that looks right — the packet is
JSON another model reads, and a guessed name sends real work to the wrong specialist.

**This refusal cannot arise from the loop's own dispatch, and that is deliberate.** A block whose
agent is unrecognised is already a defect, and defects are asked about before anything is
dispatched, so the earlier question always catches it first. The refusal is kept as a guard for a
packet built by hand — `build_dispatch` is public and a caller may construct one directly. Kept
rather than deleted on the operator's decision of 2026-09-16, recorded so nobody removes it as
dead code or re-derives the contradiction.

**A packet flagged `needs_issue` has no sub-issue recorded for it.** For a contract the Parent
Branch Delivery Rule judges, `--dispatch` and `--dry-run` refuse it with `needs-issue` before any
branch is cut (exit code 7, above), so this flag reaches you only under `--status` or `--resume`,
as information: say which sub-task is missing its sub-issue and send the operator to `/flow`
Step 2.7, then dispatch again. Nothing was cut, so there is nothing to undo.

**For a contract the rule does not judge** (its Status is not draft or approved) the old order
stays, so say plainly that, unlike `needs_agent` above, this refusal *does* arise from the loop's
own dispatch. By the time the script computes `needs_issue`, `--dispatch` cut the branch and
wrote `awaiting-merge` into the sub-task's state entry — both happen before the flag is even
checked. So "stop" here does not undo either one: the branch exists, and the next `--status` call
reports this sub-task as out for merge, waiting on a pull request that was never opened. Say which
sub-task is missing its sub-issue, and say this plainly rather than reporting a clean halt.

**The remedy closes the gap forward; it does not abandon the branch.** Create the sub-issue now
(the same `gh issue create --parent` form Parent-aware mode uses), then stamp it into the
already-dispatched sub-task's state entry:

```bash
py -3 "$PRM" --contract <slug> --record-subtask <sub-task-id> --issue <n> --base <base> --brief <brief>
```

(Run `/task` in Parent-aware mode first if this sub-task has no brief yet — `--record-subtask`
requires one.) Then continue on the branch `--dispatch` already cut: dispatch the packet's
`cycle` stages as fresh subagents (Step 2, item 2), then run `/ship`. Do not re-dispatch; the
branch and its `awaiting-merge` state already exist, and
dispatching again would cut a second branch for the same sub-task. Never link the pull request at
the parent issue, and never retarget it at the default branch — both are forbidden by name in the
work item: the sub-issue is this task's own, and the base is the parent branch, not a substitute
for either.

**A packet flagged `needs_authoring` has no TASK block in the contract.** Do not write one and
carry on. Say which sub-task is missing it, and that the contract needs amending. Inventing the
instruction defeats the point of the architect having written it.

**One pull request per sub-task, always.** Bundling two is what makes a merge unable to say
which sub-task it closed.

### `escalate` — a sub-task could not be delivered

Report the failed sub-task, its severity and its reason, then name every sub-task now blocked
behind it.

Route to architect re-entry. Concretely that means `/design-first` amending the contract. Do
not start anything, and do not retry the sub-task from here — whether to retry is one of the
decisions the architect makes.

A sub-task pull request merged into the default branch on the web is not a failure: it is recorded as an ordinary completion, so it never reaches `escalate`.

### `delivery-unrecorded` — a pull request delivered the whole contract and nothing records it

A merged pull request that is the brief's own, but whose branch maps to no sub-task, delivered the contract on one branch. Until that delivery is recorded the script reports every sub-task as pending, and dispatching one would redo finished work. The script asks this after `escalate` and before `awaiting-merge`.

**Start nothing.** Name each candidate from the script's answer and print the Next Command verbatim. It is `/pr-merged <ref> --record-delivery` for the most recent candidate GitHub confirmed, `/pr-merged <url>` when the records are waiting in an open records pull request (merge it first, then run again in a fresh worktree cut from the default branch), or a plain `/pr-merged <ref>` when GitHub could not be asked. This move never offers `/advance`: recording the delivery is `/pr-merged`'s work, not this skill's.

**A delivery on one branch is recorded like any other.** For a contract with two or more mergeable blocks nothing refuses the plain `--record-delivery`: once it is recorded the delivery exists and the move is `complete`. The layout is reported, not enforced here: read `layout_warnings` in the status report, and when it lists `single-branch-delivery`, show its `remedy` to the owner (the work is already on the default branch and is recorded as done; nothing needs undoing; deliver the remaining sub-tasks through the parent branch, `/flow` Step 2.7, then `/advance`). A warning blocks nothing: not recording, not completion, not dispatch. An `unverifiable` entry means `origin/<default>` could not be read; give its re-read remedy (`git fetch origin <default>`, then run again).

### `complete` — every sub-task has a record

Say so, then branch on `next_move.parent_branches`. The script fills it from the Sub-Task Work
Items, never from the state store.

**Empty: the contract has no parent branch.** Hand off using the closing call's `next_command`,
printed verbatim (Step 3 below). That is `/verify-before-done`, followed by `/ship` for the
contract as a whole.

**Non-empty: the contract was built on a parent branch, and the loop lands it.** No question is
asked (operator decision 2026-10-05). The landing is a script, `land_contract.py`. It fetches,
builds its own checkout of the parent branch, merges `master` into it, verifies it, checks that
every child issue is closed and no review verdict is blocked, opens the parent pull request and
merges it. It takes about 25 minutes, and a foreground shell call is capped at ten minutes, so it
runs in the shell tool's **background mode and never in the foreground**. This was measured on
2026-10-06: a background command ran 11 minutes, was not killed, and its completion notice
arrived.

1. **Find the script**, the same way Step 1 finds `pr_merged.py`:

   ```bash
   LANDER=
   S=.claude/scripts/land_contract.py
   if [ -f "$S" ]; then LANDER=$S
   elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then LANDER=$CLAUDE_PLUGIN_ROOT/$S
   else
     # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
     CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
     ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
     REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
     MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
       P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
       [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
     done)
     NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
     LANDER=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
       [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
     done)
   fi
      py -3 "$LANDER" --contract <slug> --status --json
   ```

   **If `LANDER` comes back empty, stop and say so.**
2. **Ask `--status` first.** It takes seconds and changes nothing:

   ```bash
   py -3 "$LANDER" --contract <slug> --status --json
   ```

   Read `state`:
   - `live` — a landing is already running. Report its phase and start time from `lock` and
     `phase`, launch nothing, and stop.
   - `report` — a run has ended. Render its Landing Report (step 5). On `landed` or
     `already-landed` the contract is landed: skip to the parent brief in step 5 and launch
     nothing. On any halt, this is the previous run's report. Render it in one line and go on to
     step 3: rerunning `/advance <slug>` is how a halt resumes (operator decision 2026-10-05),
     and the script re-derives every phase from git and GitHub facts, so a relaunch on an
     unfixed cause ends in the same halt. One report is not a halt: `not-applicable` with
     `manual_landing: true` means the parent brief declares `landing: manual`. Stop, tell the
     operator to merge the parent pull request themselves, and never relaunch the landing.
   - `interrupted` — a lock whose process is gone, with no report for its run. The session
     ended or the machine slept mid-run. Go on to step 3.
   - `none` — no run yet. Go on to step 3.
3. **Launch in background mode.** The command is the operator checkout's copy of the script:

   ```bash
   py -3 "$LANDER" --contract <slug> --json
   ```

   That copy is only the launcher. It builds the landing checkout from the parent branch and hands
   over to that checkout's own copy, so the code that lands is the code that runs (L-16). Never
   run the landing worktree's copy yourself.

   Say plainly that the landing is running in the background and that this skill is now waiting
   for its notice. Once the launcher has taken its lock, `--status` names the live run's
   `run_id`. Keep it.
4. **Wait for the background task's completion notice,** then read `report.json` for that
   `run_id`. It is at `<main root>/.claude/state/landing/<slug>/report.json`, where `<main root>`
   is the parent folder of `git rev-parse --path-format=absolute --git-common-dir`. Read the file,
   never the task's stdout through a pipe: a run that never started exits quietly through a pipe.
   A report whose `run_id` differs, or none at all, means the run was cut short. Treat it as
   `interrupted` and return to step 2. If the session ended or the notice was lost,
   `/advance <slug>` does exactly this on its next call, through `--status`.
5. **Render the Landing Report** field by field: `outcome`, `gate`, `detail`, `remedy`,
   `pull_request`, `merged_commit`, `parent_issue_state_after`, `hand_resolved_in_merge`,
   `bookkeeping_files` and `notes`. Its `next_command` is the closing line, printed verbatim:
   the landing has its own table, so do not substitute Step 3's call to `pr_merged.py`. On
   `not-applicable` with `manual_landing: true`, stop there and relaunch nothing. After
   `landed` or `already-landed`, the script has edited the parent brief in this checkout. Commit
   it to the records draft exactly as `/pr-merged` Step 3 does: the one stable branch
   `docs/<contract-slug>-records`, fetched and committed on top when it exists on origin, cut from
   freshly fetched `origin/master` only when it is absent, pushed without force, never re-cut.
   That push is an ordinary records push, so Step 3's "confirm once" applies to it.

**Do not declare the contract finished beyond what the report says.** `landed` means the parent
pull request merged, and the script's gates decided that. A halt names its gate and merged nothing
into `master`.

### `awaiting-merge` — a sub-task is out for merge

Say which sub-task, and which pull request it waits on. Do not start anything else and do
not treat it as stuck. It is suspended, and `/pr-merged` is what resumes it.

This state is the one the previous orchestrator never had. Without it, a sub-task waiting
on an open pull request is indistinguishable from one that is genuinely blocked.

### `blocked` — sub-tasks remain and none is ready

Report each blocked sub-task with what holds it, straight from the script. Common causes are a
dependency with no completion record yet, a dependency that failed, and a contract with no
`Depends on:` line.

That last one is a contract defect, not a wait. Say so, because nothing will ever unblock it on
its own.

### `nothing-planned` — the contract declares no sub-tasks

Say that plainly. **Never read it as complete.** An empty plan reported as a finished contract
is the exact defect that had the previous orchestrator announcing success having written no
code.

The fix is to give the contract an `## Implementation Handoff` section with numbered sub-task
blocks. `/design-first` is where that happens.

## Step 2.5: Clean up, on every call

**Run the cleanup at the end of EVERY `/advance` call, whatever the move was, and ask nothing.**
`cleanup_delivered.py` (Delivery cleanup) decides for itself whether anything may go. It reads
the contract and the records at `origin/<default>`; until the records pull request has merged it
answers "not delivered yet" and removes nothing, and the first call after that merge removes the
worktrees and merged branches of the work item. It never makes this skill's move any different:
exit 5 (not delivered yet) is normal, exit 3 means some items were kept with a reason each, and
exit 10 means nothing could be verified and nothing was touched.

The lookup order is the plugin root, then the installed-plugin records and the newest cache
folder, then the current worktree's own copy, made absolute before the `cd`. It never tries the
main checkout's copy.

```bash
START="$PWD"
CLN=
S=.claude/scripts/cleanup_delivered.py
if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then CLN=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  CLN=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
  if [ -z "$CLN" ] && [ -f "$PWD/.git" ] && [ -f "$PWD/$S" ]; then CLN=$PWD/$S; fi
fi
( cd "$(py -3 "$CLN" --print-main-root)" && py -3 "$CLN" --contract <slug> --from "$START" [--remove-remote] --json )
```

The `cd` runs in a subshell on purpose: the session's own shell stays in the folder it started in, so Step 3's `--status` call still sees the start tree, and a failed `cd` cannot be followed by a script call from the wrong folder. The current folder's own copy is taken only in a linked worktree (its `.git` is a file), never in the main checkout, whose copy may be stale. If `CLN` comes back empty, stop this step, do not run the line above, and say so in the report: nothing was removed.

**`remove-remote` is a parameter of this skill**, for example `/advance <contract> remove-remote`.
It is off by default. When given, pass `--remove-remote` to the script and nothing else; without
it the script never changes a remote branch.

Print the script's `line` as the report's `- Cleanup:` entry, verbatim and never composed. When
the line ends with `finish: <command>`, a session stood in a tree it had to remove: that tree
was left untouched, and the next call from a shell outside it clears it. Print that one command
and nothing more.

**Then sweep the records leftovers, in every tree this call touched.** Run
`py -3 "$PRM" --contract <slug> --sweep-records --from "$START" [--from <the --dispatch worktree>] [--removed <a tree this call removed>] --json`
and print its `tree_lines` verbatim as the report's `- Trees:` entry. The sweep deletes a records copy
only when its twin is on origin, keeps and names every other, and exits 10 without deleting anything
when the records cannot be read; it is idempotent, so a call that dispatched nothing still runs it.

## Step 3: Report, in the same shape every time

**First, make one more call to the script — read-only, and AFTER the move this skill just
took:**

```bash
py -3 "$PRM" --contract <slug> --status --json
```

**The closing line comes from THIS call's `next_command`, never from Step 1's.** Step 1's
answer described the state *before* this skill acted; printing it as the closing line says
"clear, then advance" at the exact moment this skill is about to dispatch — the stale-answer
defect this ordering exists to remove. The script computes the Next Command; this skill only
prints it verbatim, exactly as `pr_merged.py`'s own human-readable output does.

```
### ADVANCE REPORT
- Contract: <slug>  (<n> sub-tasks)
- Next move: <action>
- Contract defects: <block — reason, one line each | none>
- Started: <sub-task -> branch -> cycle stage(s) dispatched -> pull request url, or none>
- Failed: <sub-task — severity, reason | none>
- Blocked: <sub-task <- what holds it, one line each | none>
- Landing: <outcome, pull request and merged commit | halted at <gate> — remedy | running in the background (run_id) | not applicable>
- Waiting on: <the merge this now needs, or nothing>
- Completion: <the FINAL call's completion line, verbatim>
- Next command: <the FINAL call's next_command.commands, joined by ", then ", or "none — <reason>". After a landing, the Landing Report's own next_command>
- Cleanup: <Step 2.5's cleanup script `line`, verbatim>
- Trees: <Step 2.5's sweep `tree_lines`, verbatim, one per tree touched: the starting tree, the --dispatch worktree and any removed tree>
```

The `completion:` line comes from the same final read-only call: `completion.verdict` and the first entry of `completion.reasons`. Because that call is read-only it shows `not-evaluated` and the dry-run command, never a flip. The flip belongs to `/pr-merged`.

The last two lines matter most. An operator who cannot see what the contract is waiting for,
and what to type next, will either sit watching it or walk away at the wrong moment. **The next
command is the script's own field, read after the move — never a line this skill composes.**

## Where this sits

| Layer | Owner | Owns |
|---|---|---|
| Outer chain | `/flow` | One work item, from intake through to shipped |
| **Inner loop** | **this skill, with `/pr-merged`** | One contract's sub-tasks, a step at a time |
| Sub-task closing | `/pr-merged` | Recording a merge and computing what it released |

`/flow` hands the inner loop here once a contract is approved and carries sub-tasks. For a
contract with a single implementation block there is nothing to iterate, and `/flow` runs it
directly.

## What is pre-authorized, and what is not

**Pre-authorized when `/flow` or the operator invoked this:** reading the script's answer,
creating the branch the packet names, dispatching the packet's cycle stage(s) as fresh
subagents, reporting, starting the first released sub-task when several are released, and on
`complete` with a parent branch, launching the landing in the background (no question is asked).

**Always the operator's call:** the commit
confirmation, opening the pull request, amending a contract after an escalation, and anything
that would start work the script did not release.

## Anti-patterns (halt immediately)

- **Looping.** Take one move and stop. The next move needs a human merge that cannot happen
  while this is running.
- **Recomputing readiness from the contract** instead of reading the script's answer. Two
  implementations of one rule will disagree.
- **Starting a sub-task the script did not release.** Its dependencies have not landed.
- **Writing a TASK block for a packet flagged as needing authoring.** Report the gap.
- **Bundling two sub-tasks into one pull request.** The merge then cannot say what it closed.
- **Reading `nothing-planned` as complete.** That is the defect this whole design exists to
  avoid.
- **Declaring the contract finished** because the last sub-task closed. For a contract without a parent branch, verification decides. With one, the Landing Report decides.
- **Skipping Step 2.5** because the move was not `complete`, or hand-running `git branch -d`, a worktree removal or git's worktree `prune`. The cleanup runs on every call and the script owns the rules.
- **Launching the landing in the foreground,** or running the landing worktree's copy of the script. A foreground call is capped at ten minutes, and only the operator checkout's copy is the launcher.
- **Launching before `--status`,** or launching a second landing beside a live one.
- **Reading the landing's result from stdout through a pipe** instead of `report.json` for the launch's `run_id`.
- **Retrying a failed sub-task** without the architect. Whether to retry is their decision.
- **Running a cycle stage inline, in this session,** instead of dispatching it as a fresh
  subagent. `stage["isolation"]` is the constant `fresh-subagent` for a reason.
- **Naming a cycle stage the packet did not ship,** or inferring one from `agent_role`. The
  closed set is `review`, `red`, `green`, `unphased`, read off `stage["stage"]` for each entry
  of `cycle`, in order — never `cycle[0]` alone.
- **Printing Step 1's `next_command` as the closing line.** It describes the state before this
  skill acted. Only a call made *after* the move reflects what changed.

## When NOT to use this skill

- A work item with no contract, or a contract with one implementation block. Use `/flow`.
- A pull request that just merged. Use `/pr-merged`, which then tells you to come back here.
- Checking state without acting. Run the script with `--status` and read it.

## Skill integrations

- **Reads** `.claude/scripts/pr_merged.py`, which owns the rules and the tests.
- **Runs** `.claude/scripts/cleanup_delivered.py` at the end of every call (Step 2.5), which removes the worktrees and merged branches of a delivered work item.
- **Launches** `.claude/scripts/land_contract.py` in the background on a completed contract with a parent branch. That script owns the landing's gates and its own tests.
- **Dispatches** each stage of the packet's `cycle` as a fresh subagent, then runs `/ship` for its pull request.
- **Paired with** `/pr-merged`, which closes a sub-task and wakes this skill.
- **Called by** `/flow`, which owns the work item around the contract.
- **Escalates to** `/design-first` on a failure, and to `/verify-before-done` on completion of a contract with no parent branch.
