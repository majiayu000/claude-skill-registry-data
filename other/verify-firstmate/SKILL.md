---
name: verify-firstmate
description: >-
  Measure which firstmate behaviors are proven, and say which are not, by running real firstmate sessions and driving the real bin/ scripts against throwaway homes, weighing the result against a tracked inventory of every claim the product makes, and keeping the evidence.
  Use before reporting a change to firstmate's own scripts as done, when checking that an installation or a platform works, and when something feels wrong and you need to know which feature is at fault.
  Firstmate's surface is its command-line scripts and the durable records they keep, so this skill runs sessions, drives scripts and reads records; it does not drive a browser.
user-invocable: true
metadata:
  internal: true
---

# verify-firstmate

The captain talks to an agent, and everything that agent does mechanically is a `bin/fm-*.sh` script acting on one operational home: the `data/`, `state/`, `config/`, and `projects/` directories that `FM_HOME` selects.
That pair, a script and the records it leaves in a home, is the surface this skill drives.
A test in `tests/` pins a contract with fakes and must pass on any machine.
This skill measures the other question, whether the feature works for real on this machine with this code, and it says plainly when the honest answer is "not yet proven" rather than reporting a script's own map as the product.

Two files own the detail, and this skill points at them instead of repeating them.
[`tests/verification/README.md`](../../../tests/verification/README.md) owns the contract every verification script keeps, the coverage table, and the name of any script that is red on purpose.
[`features/README.md`](features/README.md) is the feature map: what each feature is from the captain's side, how to drive it, and what end state proves it.
Read the feature file before you drive its feature.

A drive never starts a model.
A session always does, and only when `VERIFY_REAL_SESSION=1` is set, because it spends tokens and opens tabs in the Herdr session you are looking at; see Sessions below.

## Launch

There is nothing to build and no server to start.
Every verification script builds its own throwaway home under the system temp directory, points `FM_HOME` at it, and removes it when the script exits.
So launching means standing in the worktree that holds the code you want to prove and running the helper from there:

```sh
.agents/skills/verify-firstmate/verify.sh doctor
```

The helper resolves everything from the worktree that holds the helper file, never from your working directory, so the code it drives is the code beside it.
The instance is ready when the doctor prints `# doctor: worth driving`.

Nothing is shared between two worktrees, so parallel runs are the normal case.
The home comes from `mktemp` per script, the evidence directory is derived from the worktree path and the run, and the one feature that needs a Herdr session names its own with a process and random suffix.
The suite also clears every `FM_*_OVERRIDE` variable before it drives anything, because the directory ones win over `FM_HOME` inside the scripts and one left set by the caller would send the run into a live home.

## Doctor

```sh
.agents/skills/verify-firstmate/verify.sh doctor
```

The doctor writes nothing and exits `0` when the checkout is worth driving and `1` when it is not.
Run it first, and run it again whenever a result looks wrong.
It reports whether the suite is present, whether this is a linked worktree or the primary checkout, which commit is under test and how many paths are uncommitted, whether the harness skill link resolves, which tools are missing, and whether the temp directory can hold a throwaway home.
A `warn -` line does not stop a run, but read it: a missing optional tool means a feature will skip, and a skip proves nothing.
`run` calls the doctor itself and refuses to drive a checkout the doctor rejects.

## Behavior inventory

[`behaviors.tsv`](behaviors.tsv) beside this file is the ledger every claim in this skill answers to, one row per behavior, not per script.
Its `source` names where the claim comes from, one of four shapes.

- A bullet under `README.md`'s `## Features`.
- A lifecycle step in `AGENTS.md`.
- A `kind=entry` script in [`tests/verification/coverage.tsv`](../../../tests/verification/coverage.tsv).
- A file under `features/`.

Its `status` is exactly one of four words.

- `proven` - a real session drives this behavior, and `ref` names it: a session script `tests/verification/<ref>.verify.sh`, or a drive trace `tools/fm-drive/traces/<ref>.json` whose `proves` lists the row.
- `unproven` - nothing here drives it yet, and `ref` is the issue that owns closing the gap.
- `broken` - it is known not to work, and `ref` is the issue that tracks the fix.
- `blocked-here` - it needs a harness, backend, Relay, or voice this machine cannot supply, or the operator ruled it out of scope (remote second mates), and `ref` is `#97`.

Only `node tools/fm-drive/drive.mjs record <result.json>` changes a trace row.
It reads a passing `run` result whose home health check held, sets each row the trace's `proves` names to `proven` with the trace as `ref` and the run as evidence, and prints `proven N of M behaviors; K unproven; J broken; B blocked here`.
`record` writes nothing and exits 2 for a rejected trace, a run that failed in its environment, a run that missed a step, a run whose steps differ from the trace at its commit or overran a step budget there, a run whose health check missed, a run on uncommitted changes, a commit that `origin/main` or a given `--head origin/<branch>` does not contain, and a row id the table does not have.
Recording the same result twice leaves the table unchanged.

`verify.sh doctor` runs `inventory.sh check` and refuses a checkout whose table has a hole, whether that is a `bin/` script, a feature file, or a README bullet with no row, a `proven` row whose script does not exist, or a malformed `ref`.
`verify.sh run` ends with the fractional verdict `inventory.sh verdict` computes from that run's log, `proven N of M behaviors; K unproven; J broken; B blocked here`.
That fraction, not the suite's own `<n> passed, <n> failed, <n> skipped` line, is what "verified" means for this repository.
A `proven` row whose script skipped, or did not run at all, counts toward `unproven`, never toward `proven`, so a skip can never read as proof.
A `proven` row whose evidence `record` wrote counts as proven from that run, and `inventory.sh check` holds it to its trace's `proves` even when a session script has the same name.

## Drive

```sh
.agents/skills/verify-firstmate/verify.sh list                 # the features that can be driven
.agents/skills/verify-firstmate/verify.sh run wake-queue       # one feature
.agents/skills/verify-firstmate/verify.sh run                  # all of them
```

Every line a script prints is a claim about its feature in plain language, `ok - <claim>` or `not ok - <what is wrong>`.
The run ends with `verification: <n> passed, <n> failed, <n> skipped`, then the inventory's fractional verdict, and exits with the number of failed scripts.
A skipped script is one this machine could not answer, so report it as skipped and never as verified; the verdict line scores it as unproven for the same reason.

To prove a change, run the feature twice: once on the base your branch started from, in a worktree of that commit, and once on your change.
A script that is red on both sides is not your defect; check the suite README for a script that is red on purpose before you chase it.
A script that is green on both sides did not exercise your change, so it proves nothing about it.
Extend that script, or add one, until it fails without your change and passes with it.

When a feature has no script, add one to the suite the way its README describes instead of driving by hand, so the next agent inherits the proof.
If you must drive by hand, keep the same rules: a home you created with `mktemp`, holding `data/`, `state/`, `config/`, `projects/`, and a copy of `.tasks.toml`; `FM_HOME` exported to it; scripts called by absolute path from this worktree's `bin/`.
Never point a drive at a home you did not create.

## Evidence

Every run keeps its evidence here, and prints the path on its last line:

```
${TMPDIR:-/tmp}/fm-verification-artifacts/<worktree name>-<path checksum>/<UTC time>-<commit>-<pid>/
  doctor.txt                  what the doctor said before the run
  code.txt                    branch, commit, and every uncommitted path and diff under test
  run.log                     everything the run printed
  <feature>/transcript.txt    each claim the script checked, and the commit it ran against
  <feature>/<kept file>       any record the script chose to keep
```

`VERIFY_EVIDENCE_ROOT` moves the root.
The directory sits outside every worktree, so it survives the cleanup of the worktree that produced it.

A proof meets these standards.

- It exercises the path a user takes: the `bin/` script the captain or the agent really runs, with the arguments they really pass, not a library function, a test override, or a record written by hand.
- It captures the action and the resulting state, not only a final exit code.
- It reads the side effect from the durable record, such as a file under `state/` or `data/`, a backlog item, or a git ref, as well as from what the command printed.
- It fakes only a boundary the product already isolates, such as a project repository or a worker endpoint, and says so.
- It reports the evidence path and the summary line, and names every skip as a skip.


## Sessions

A drive runs `bin/` scripts itself against a throwaway home, so it plays firstmate.
A session is firstmate: the code under test is cloned into a fresh home under the temp directory, a real `claude` primary starts there in a Herdr workspace of its own with the toolchain a captain has on its PATH, the script types captain messages into its pane, and every claim is read from `state/`, `data/`, Herdr's tab list and the project's git refs.
What the agent prints is kept as evidence and is never a claim.
Only a session can make an inventory row `proven`.

A session script sources `tests/verification/session-lib.sh` after `lib.sh`.
It skips unless `VERIFY_REAL_SESSION=1` is set, because it spends model tokens and opens tabs in the Herdr session you are looking at, and a skip counts as unproven.
`VERIFY_SESSION_MODEL` picks the primary's model, `opus` by default, so a run does not spend your default model's quota; workers use whatever firstmate resolves for them.
The clone gets the primary checkout's `.tools/` directory, or `VERIFY_TOOLS_DIR`, and `VERIFY_PANE_PATH_EXTRA` adds PATH entries for the pane.

Every session ends with a health check of the home it used, run from `verify_done` so no script can skip it: no lock takeover chain, no lock owner left behind, an empty acknowledged notification queue, no captain note still waiting, no task record left, a watcher beacon that stayed fresh whenever work was in flight and the primary was idle, and no tab labelled for one of its tasks still open.
A script whose claims pass but whose home is damaged fails.
The close then exits the primary, stops only this home's watcher, closes only the tabs and workspaces the session made, removes only the treehouse pools its project created, and archives `state/` and `data/`.

A session keeps more evidence than a drive:

```
<feature>/session.txt          workspace, pane, model and the PATH the pane adopted
<feature>/captain.log          every message typed into the primary, with its time
<feature>/panes/<pane>-<time>.txt   the primary's pane and every worker's pane, kept whenever it changed
<feature>/records/state-<time>.txt  state/ listing, every task record, the queue, the backlog and the registry, kept whenever they changed
<feature>/ticks.tsv            one line per ten seconds: task records, watcher beacon age, what the primary was doing
<feature>/task-ids.txt         every task id the home ever recorded
<feature>/home-records.tar     state/ and data/ as the session left them
```

The home lives under the temp directory on purpose: on this machine that path has two spellings, which is the condition that exposed #82.

## Cleanup

Each script removes its own throwaway home from an exit trap, and `herdr-lab-pane` tears down its own lab session through `bin/fm-herdr-lab.sh teardown`.
Cleanup never touches the evidence directory.

A run that was killed can leave two things behind.
An `fm-verify-<feature>.*` directory under the temp directory is inert scratch; remove it only when you know the run that made it is yours and is over.
A Herdr session named `fm-lab-paneshell*` is removed with `bin/fm-herdr-lab.sh teardown <session>`, which refuses the default session.
`condition-watch` starts a background watch that carries its own three-minute deadline, so an interrupted run of it ends by itself.
Never stop a process by name, and never aim a `herdr` command at a session you did not create.

## Helpers

[`verify.sh`](verify.sh) is the helper you run; the three invocations under Doctor and Drive above are all of it, and it calls [`inventory.sh`](inventory.sh) itself, at both points.
Run `verify.sh` with no arguments to print its own usage.

`inventory.sh` is driven directly only when you are working on the table itself:

```sh
.agents/skills/verify-firstmate/inventory.sh check              # the same hole check verify.sh doctor runs
.agents/skills/verify-firstmate/inventory.sh verdict <run.log>  # the fraction for an already-captured run.log
```

## Keeping the map honest

When a change alters how a feature is reached or which record proves it, update that feature's file under `features/` in the same change.
When a change adds a verification script, add its feature file, its line in the feature index, and flip its `behaviors.tsv` row to `proven` with that script's name as `ref`.
When a trace proves a row, list the row in its `proves` and let `record` flip it from a pushed run.
When a change adds or removes a `bin/` entry point, a README feature bullet, or an `AGENTS.md` lifecycle step, add or remove its row in `behaviors.tsv` in the same change; `inventory.sh check` is what catches the ones left behind.
