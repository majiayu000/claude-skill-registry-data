---
name: drive-editor
description: >
  Changes an existing drive — its goal, a constraint, a failure condition, a scenario, its
  plays or their order, the questions it asks first, its checker or runner setting, or how it
  ends — by editing the drive's ICE and rebuilding it, so the drive always matches its intent.
  Companion to drive-creator (which builds new drives). Use when the user wants to edit,
  change, update or fix a drive — or says "edit the drive", "add a play to Kickoff", "the
  drive needs a new question", "drive-editor", or "rebuild the drive after I changed its ICE".
user-invocable: true
model: best
---

# drive-editor

Changes a drive that exists by editing its **ICE** (`reference/ice.md`) and rebuilding — never
by patching the compiled `SKILL.md` so that it says something its ICE does not. The compiled
drive records a fingerprint of its ICE, so drift shows.

Companion to `/drive-creator`, which builds new drives and whose reference is the shape every
drive follows (`../drive-creator/SKILL.md`, `../drive-creator/references/compiled-drive-example/`).
Like `/play-editor`, this skill is written by hand.

The one safe direct edit is wording with no change in meaning. Anything else goes through the
ICE.

Approvals are typed replies (never `AskUserQuestion`). With no person reachable, state each
assumption, record that approval was assumed, and proceed.

## What you can change, and where it lives

| The change | Where it lives in the ICE | What else it reaches |
|------------|---------------------------|----------------------|
| The goal, a constraint, a failure condition | Intent | Step evals, recovery, maybe scenarios and the Done means |
| A scenario, a recovery entry, the Done means | Expectation | Scenario evals; `stop-condition.yaml` |
| Add, drop or reorder a play | Plays | `plays=` in the run block, one step per play, the Task DAG, the Done means and evals that read `<play>-done.json`, any "after `<play>`" input, and the drive's Next line in `pipeline-next.md` when the last play changes |
| A question asked first | Questions first | `questions=`, the contract's answers, the plays that used to ask it |
| The checker or the runner | Checker / Runner | `core/config.yaml` (`drives.<drive>.*`) |
| How the drive ends | End | `end=`, the end steps, the Task DAG |
| Wording only | the compiled drive directly | nothing |

## Pipeline

### 1 — Load the drive and its ICE
Read `SKILL.md`, `reference/ice.md` and `stop-condition.yaml`. Map what is there: constraints,
failure conditions, scenarios, Done means, step and scenario evals, the plays and their order,
the questions, the run block's values, the end. You cannot change safely what you have not
read.

### 2 — Name the change and its reach
Say exactly what changes and the smallest set of things it reaches (the table above). A new
play must exist and run inside a drive (it checks a drive contract); if it does not, stop —
fix the play first, through its own ICE and `/play-editor`. Every input the drive hands a play
(`inputs.<play>.<key>`) must be one the play reads: find `<key>` in the play's SKILL.md. A key
the play does not read is not handed — drop it, or change the play first. A step that would do
real work belongs in a play, not in the drive.

### 3 — Change the ICE first
Edit `reference/ice.md`. When the change shifts what success or recovery looks like, generate
the affected expectation pieces again from the intent (one recovery per failure condition);
leave the rest as they are. Get the person's typed approval of the ICE change.

### 4 — Carry the change through
Change only what the change reaches: the run block's values, the steps (one per play, owned by
that play), the Task DAG, the evals (add or remove — no eval may point at a constraint, failure
or scenario that is gone), `stop-condition.yaml`, the config keys. New Done means and
constraint, failure and scenario ids are appended (D5, D6 …); never renumber the ones that
exist — other files and records point at them. Copy the shared scripts
again, unchanged, as `/drive-creator` step 4 says, so a drive never drifts from the shared run.
Recompute the fingerprint with `shasum -a 256 reference/ice.md`.

### 5 — Verify

From the repository root:

```
python3 core/components/plays/drive-editor/scripts/lint_drive.py core/components/drives/<drive>/SKILL.md
```

Fix every GAP and run it again until it passes; then run
`node core/tools/lint-components/index.js --target core/components --output json` and clear
any error whose file is the drive's. That command exits 1 while other components carry old
errors; that is not this drive's gap. Check by hand that each eval still reads a file the shared run writes.

### 6 — Show what changed
A short summary: which ICE parts changed, which steps, evals and values were added, removed or
regenerated, and that the linter passes.

## Hard rules

- Edit the ICE and rebuild. Only wording with no change in meaning is a direct edit.
- Keep the reach small: change only what the change reaches.
- A drive does no work of its own; a new play must run inside a drive.
- Leave no orphans: remove every eval and recovery tied to what you removed.
- Copy the shared scripts unchanged; recompute the fingerprint; run `lint_drive.py` until clean.
