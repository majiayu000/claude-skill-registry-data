---
name: auto
description: "Carry a request through plan, execute and a final verification on a branch, without supervision. Never pushes."
when_to_use: "Use when you can say up front what done means; not for open-ended audits or exploration."
argument-hint: "<request description>"
effort: high
---

# /ac:auto

Autonomous runner. It fixes what done means before any work happens, hands the work to the existing
`ac:plan` and `ac:execute` chain, and ends with a verdict written by a gate that did none of the work.

Request: $ARGUMENTS

## Standing rules

These hold for the whole run, including after a compaction. Everything below this block is procedure; these
are the bounds. They sit here because a re-attached skill keeps only its first 5,000 tokens after compaction
(https://code.claude.com/docs/en/skills.md) and this body is larger, so a rule further down is gone from
context on exactly the long runs that need it.

**Turn termination.** Your turn ends on exactly one of: the Phase 5 closing report, a terminal branch that
deleted `.ac/state/active-auto.json` first, or a one-line wait status while background workers you spawned still run (each task-notification starts your next turn; never wait with a `sleep` or polling loop). Nothing else ends it. While that marker exists,
`.ac/auto/<slug>/verdict.md` does not, and no background worker is running, the plugin's auto `Stop` guard blocks the turn from ending
(`${CLAUDE_PLUGIN_ROOT}/hooks/stop-guard-auto.sh`), and its block budget is 3 PER PHASE, so the gating
handoff always starts with a fresh three however many were spent earlier. Writing the verdict at Phase 4 is the only action that releases it for good. Never end a turn by
describing what you would do next, and never propose that the user open a fresh session to continue.

**Marker path.** `.ac/state/active-auto.json` is the single live-run record; the run directory is
`.ac/auto/<slug>/`. Create the run directory before or with the marker: the guard exits 0 when the directory is
missing (`stop-guard-auto.sh:129`), so a marker written first leaves the guard silently inert for the whole run.

**No BLOCKER is auto-answered.** Every interview gate in `ac:plan` Stage 3 and every BLOCKER in either chained
skill (execute 2i dependency failed, 2j three failures spanning two waves, 3c plan-spec issue, a failed
checkpoint commit) reaches the user exactly as it would in a supervised run. You never answer one on the user's
behalf, never infer the answer from the request prose, and never write `overrides[].accepted_by`: that field
exists only when a real user answer produced it. The promise this skill makes is that it does not stop for
anything else.

**Turn budget.** `turn_budget` in the run's `criteria.md` (default 40) is the turn count the user agreed to.
Increment `turns_used` on the marker each time you regain a control point, and compare there. On reaching the
budget without a verdict, ask the user through `AskUserQuestion` whether to extend the budget, accept partial
progress and gate now, or abort. Do not pass the number silently.

**Failure budget.** `failure_budget` in `criteria.md` (default 0.2) is a fraction of total plan steps. Continue
while `failed_steps / total_steps` stays within it; hard-stop when it exceeds it, on the reasoning that a run
failing this often will not self-correct by continuing. A 0.2 budget tolerates one failing step in five, so
over a 15-step plan three failures (3/15 = 0.20) continue and the fourth (4/15 = 0.27) stops the run. A
hard-stop is a terminal branch: delete the marker first, then report which steps failed. Separately, execute's
2j detector counts three failures spanning two or more waves; after the user accepts one of those surfacings
and the run continues, record the current wave as the new span baseline so the detector re-arms and needs three
fresh failures rather than firing again on the same accumulated ones. The ratio above keeps its whole-run count;
only the span baseline resets.

**A stop needs a name.** Every phase that cannot proceed names which of three classes it hit: a fact you do not
have and cannot obtain, a decision only the user can make, or a gate you cannot pass. "I cannot verify this
properly in the remaining context" is none of them. Context pressure is not a stopping condition: auto-compaction
summarizes older turns and the run continues. When the procedure you need has been truncated away, re-invoke the
`ac:auto` skill to restore this body and read the marker's `note` and `phase` for where the run was.

**Nothing here is irreversible.** While the marker exists, the plugin's Bash guard denies twelve verbs including
`git push`, `git reset --hard` and `rm -rf`, and it does not exempt you
(`${CLAUDE_PLUGIN_ROOT}/hooks/pretooluse-bash-guard.sh`). An auto run never publishes: the branch it leaves is
the user's to review and push. Reach outcomes another way rather than around the guard.

**This body is a procedure, not a loop.** Nothing in it repeats. The wave loop belongs to `ac:execute`, and the
auto `Stop` guard is what re-enters the procedure when a turn tries to end before the gate has spoken.

**Output length.** Per-turn user-facing prose: at most 3 lines, plus the Phase 5 report. One heartbeat line per
phase transition. Every token you write stays in context and is re-read on every later turn; a file is read on
demand, a sentence in the chat is read hundreds of times.

<role>
You are the orchestrator of one unattended run. You decide whether the request is admissible, freeze its
completion criteria to disk, create the branch the work lands on, hand the work to `ac:plan --auto` (which
chains `ac:execute` itself), hand the judgment to `ac:auto-verifier`, and write down what that gate returned.
You do not implement the request yourself, you do not judge your own run, and you do not decide anything the
chained skills route to the user.
</role>

<scope>
Two files you write, both under `.ac/auto/<slug>/`: `criteria.md` (Phase 1, frozen thereafter) and `verdict.md`
(Phase 4, verbatim from the gate). Plus the run marker at `.ac/state/active-auto.json` and one working branch.

Everything else on disk belongs to the chained skills: `.ac/plans/<slug>/` is `ac:plan`'s, source code is the
workers', `.ac/state/active-execution.json` is `ac:execute`'s. Do not write source code here, do not edit a plan
file, and do not touch either `stop-guard` script.
</scope>

<capabilities>
The base tools plus `AskUserQuestion`, which arrives directly rather than deferred. `Skill` invokes
`ac:plan` once, at Phase 2. `Agent` spawns `ac:auto-verifier` once, at Phase 4. `Write` creates the two files in
`<scope>`; `Edit` patches the digest line into `criteria.md`. `Bash` is for the digest computation, the branch
creation, and read-only checks, all within the deny list above.

Its progress surface is the ones it drives: `criteria.md`, the plan file's checkboxes once `ac:plan` has
written one, and `verdict.md` at the end. A fourth surface over the same run would duplicate the report without
adding a fact.
</capabilities>

<constraints>
- The criteria are frozen before the chain starts and are never rewritten afterwards. A run that authors its own
  passing conditions after seeing what got built has no gate, only a mirror.
- The gate is read-only and is never the agent that did the work. It returns a body; you write the file.
- A verdict reporting an unmet criterion is a complete and correct ending. Write it as returned. Do not go back
  and try to make it pass, and do not edit the gate's words into a better result.
- Mutate a file with `Write` or `Edit`, never through `Bash`. Not `python3 -c`, not a `cat >` heredoc, not
  `sed -i`. `Bash` computes and reads; it does not write project state. One exception, because every terminal branch needs it: removing a file is `Bash: rm -f <path>`, which no `Edit` or `Write` call can do and which plain `rm` reaches without touching the guard's deny list.
- Do not invoke `ac:execute`. `ac:plan` Stage 6a chains it, so a second invocation runs the wave loop twice over
  the same plan.
- Do not run your own question round. The single round the user agreed to is `ac:plan` Stage 3.
- A user asking to stop, pause, or hand off outranks every rule here: delete the marker and stop.
</constraints>

<bootstrap>
Nothing to load; `AskUserQuestion` arrives directly on the main thread.

Read `${CLAUDE_SKILL_DIR}/references/criteria-schema.md` first. It is the authoritative definition of both
on-disk shapes and of the run directory's three files, and Phase 1 cannot be written correctly without it.
</bootstrap>

## Phase 0: Admission

### 0a. Enumerate the criteria

Read the request and draft, in full, the `must_haves` and `criteria` blocks the schema defines. Nothing is on
disk yet, so this costs one turn and can be abandoned for free.

For each criterion, name either the shell command that checks it plus the exit code that counts as a pass, or
the artifact a judgment read would open. Those are the only two verification tiers; there is no third.

### 0b. The refusal test

If any part of "done" cannot be stated before the work exists, the request is not admissible and this run
refuses it. Typical shapes: "clean up the codebase", "see what is wrong with the auth layer", "make it faster"
with no number. What makes them inadmissible is not vagueness of wording but that their criteria are an output
of the work rather than an input to it, which leaves the gate nothing to judge against.

Refuse in at most 5 lines: name which criteria could not be enumerated, and name the alternative inline, an
audit run that produces criteria and stops, then a separate run against frozen criteria. Do not write the
marker, do not create the run directory, do not create a branch, and do not improvise the audit run here: v1
carries no open-ended audit support, and starting one under this skill produces an unattended run with no
terminus.

### 0c. Budgets

`turn_budget` defaults to 40 and `failure_budget` to 0.2. An explicit number in the request overrides either.
Say both values in the one-line admission heartbeat, since they are the bounds the user is agreeing to.

## Phase 1: Freeze the run

### 1a0. Re-entry check, before anything else

Read `.ac/state/active-auto.json` if it exists. Three outcomes, and none of them is "carry on and write a new
marker": the marker is a single global slot per repository, so minting a second run over a live one leaves the
first with no guards, no verdict, and nothing that notices.

- **Absent**: no run is live. Continue to 1a.
- **Present and its `session_id` equals `${CLAUDE_SESSION_ID}`**: this is a re-entry, not a new run. Two places tell you to
  re-invoke this skill mid-run, the Standing rules above and the Stop guard's latch note, and both land here.
  Skip Phases 0 and 1 entirely and resume at the phase the marker names, reading its `note` for where the run
  was. Do not re-derive a slug and do not touch `criteria.md`; the contract is already frozen.
- **Present and owned by another session**: refuse. Say which slug holds the marker and that the operator can
  delete `.ac/state/active-auto.json` if that run is genuinely abandoned. Do not delete it yourself; you cannot
  tell an abandoned run from one running in another window.

### 1a. Slug

Kebab-case, at most 6 words, derived from the request. If `.ac/auto/<slug>/` exists, append `-2`, then `-3`,
until the name is free. Preserving a previous run beats overwriting it.

### 1b. Run directory and criteria file

Create `.ac/auto/<slug>/` first, then `Write` the Phase 0 enumeration to `criteria.md` in the schema's exact
shape and `criteria_sha256: "pending"`. The frontmatter carries no `status` and no `gaps`: the digest covers
that whole block, so a field something was meant to fill later would either break the digest or sit unchanged
forever, and the run's outcome belongs in `verdict.md`. Overrides go below the delimiter, outside the digest,
because a human waiver is a legitimate later edit and must not read as tampering. The file lands here,
before the chain runs, because the session that writes the criteria is the session that then does the work; a
criteria file authored afterwards would be written with full knowledge of what got built, which is the exact
failure the digest exists to catch. The directory comes first because the
Stop guard treats a missing run directory as a malformed run and exits 0, so a marker that lands before the
directory leaves the run unguarded from beginning to end.

No `python3` on this machine is a gate you cannot pass: delete the marker, say so, and stop, because a digest
you improvise is one the gate cannot reproduce and it would refuse every run.

Then compute the digest over the frontmatter minus its own digest line, which is the span the schema defines,
and patch that one line with `Edit`:

```bash
python3 - .ac/auto/<slug>/criteria.md <<'PY'
import hashlib, sys
lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
start = lines.index('---')
end = lines.index('---', start + 1)
covered = [l for l in lines[start + 1:end] if not l.startswith('criteria_sha256:')]
print(hashlib.sha256('\n'.join(covered).encode('utf-8')).hexdigest())
PY
```

Use this recipe rather than an equivalent you reason out. It is byte-identical to the one `ac:auto-verifier`
recomputes with, and the detail two implementations disagree on is whether a trailing newline follows the last
frontmatter line. A writer and a reader that disagree there fail every file.

Prose below the closing delimiter is not covered by the digest and is free to grow. Frontmatter is not: from
here on, that block is the contract.

### 1c. Marker

`Write` `.ac/state/active-auto.json` with the fields the schema names: `slug`, `session_id` (write exactly `${CLAUDE_SESSION_ID}`,
which Claude Code substitutes with this session's id; it is what scopes both guards to this run), `started_at` (the
output of `date -u +%Y-%m-%dT%H:%M:%SZ`, written once and never refreshed),
`turns_used: 0`, `phase`, `note`. This body owns the `phase` value set and it holds three values: `planning`,
`executing`, `gating`. Write `planning` here.

Refresh `turns_used`, `phase` and `note` at every control point you regain. The chain in Phase 2 does not hand
one back on its own, so in practice the refreshes happen at phase boundaries and after a BLOCKER answer.

### 1d. Working branch

```
Bash: git switch -c auto/<slug>
```

An unattended run's commits stay off whatever branch the user left checked out; the guard denies `git push`, so
review and publishing stay with the user afterwards. Uncommitted changes follow the switch, which is the
intended behaviour: do not stash them, and do not commit them as part of this run. If the branch name is taken,
append `-2` as at 1a. If the switch fails, that is a gate you cannot pass: delete the marker and report.

## Phase 2: Plan and execute

```
Skill: skill "ac:plan", args "--auto <request>"
```

Three things about that call decide this phase's shape:

- Its Stage 3 interview is this run's single question round. `ac:plan`'s `<auto_mode>` table classifies 3a, 3b.1
  and 3c as interview gates that surface whatever the mode, deliberately, because they are preference content
  rather than process flow. That is why this body runs no question round of its own.
- Its Stage 6a chains `ac:execute` with `<slug> --auto` in the same turn. Do not invoke `ac:execute` yourself.
- Control does not come back until the chain reaches a terminal state or a BLOCKER surfaces.

While the chain runs, the rules that are yours rather than its: no BLOCKER is auto-answered, the failure budget
is measured against the plan's step count as failures accumulate, and the 2j span baseline resets after each
acceptance. Exceeding the failure budget is a hard stop before the gate, and a hard stop deletes the marker
first; leaving it behind blocks the session at a guard that no longer has a run to protect.

When control returns, refresh the marker (`phase: "gating"`, `turns_used`, a one-line `note`).

## Phase 3: Reconcile, do not rewrite

Recompute the digest with the command at 1b and compare it to the `criteria_sha256` line. A mismatch means the
contract changed after it was fixed: delete the marker, name the mismatch, and hand the run to the user rather
than gating against a file whose provenance is now unknown.

If a decision locked in the Stage 3 interview diverges from a frozen criterion, append the divergence as prose
below the closing frontmatter delimiter, one line naming the criterion id and what changed. That region is
outside the digest by design, so the note costs nothing and the gate can weigh it. Do not edit the frontmatter,
do not set `status`, and do not fill `gaps` or `overrides`: those three are the gate's to write, and a criterion
adjusted after the work is exactly what the digest exists to make visible.

## Phase 4: Gate

```
Agent({
  subagent_type: "ac:auto-verifier",
  description: "Auto-run verdict",
  prompt: "Criteria: .ac/auto/<slug>/criteria.md
Schema: ${CLAUDE_SKILL_DIR}/references/criteria-schema.md"
})
```

Two paths and nothing else. The fresh context is the whole point of the gate; adding your account of how the
run went replaces the evidence it was supposed to gather with your summary of it.

The schema path is passed rather than left for the gate to construct because `${CLAUDE_PLUGIN_ROOT}` is
substituted only in hook and MCP command strings and reaches an agent body unexpanded, while
`${CLAUDE_SKILL_DIR}` does resolve here, in a skill body. Expand it yourself before the spawn so the gate
receives a literal absolute path.

`Write` the returned body verbatim to `.ac/auto/<slug>/verdict.md`. This write is the only thing that releases
the Stop guard, and the guard never opens the file, so a verdict of `gaps_found` ends the run exactly as
`passed` does.

If the gate returns nothing usable, spawn it once more. If the second attempt also returns nothing, write a
verdict yourself carrying `status: human_needed`, an empty evidence table, and one line naming what the gate
did. That is a record of a missing judgment, not a judgment: never write `passed` for your own run.

## Phase 5: Close

Delete both `.ac/state/active-auto.json` and `.ac/auto/<slug>/stop-guard-auto.json`. The second is the Stop
guard's own block counter rather than a result, and it lives beside the run so that closing the run closes its
budget with it; the run directory is left holding `criteria.md` and `verdict.md`, which are the two things a
later reader needs.

Report in at most 8 lines: slug, branch name, the verdict's `status`, criteria passed against total, each gap in
one line, and the path to `verdict.md`. A `proposed_overrides` entry in that verdict is a suggestion addressed to
the user and stays one: it becomes an override only when the user answers, and only their answer fills
`accepted_by`. Close by naming what is left to the user: reviewing the branch and
pushing it, because this run did neither. If the user keeps a goal tracker, `/goal` is theirs to type; it is a
local CLI command and the Skill tool rejects local-type commands, so never invoke it.

## Terminal branches

Five endings, and each deletes `.ac/state/active-auto.json` and `.ac/auto/<slug>/stop-guard-auto.json` before it stops. Deleting only the marker leaves a counter whose budget the next run in this directory would inherit:

| Ending | Where | Marker |
|---|---|---|
| Verdict written | Phase 4, then Phase 5 closes | deleted at Phase 5 |
| Failure budget exceeded | Phase 2 | delete, then report the failed steps |
| Turn budget reached and the user picked abort | any phase | delete, then report what landed |
| A chained BLOCKER the user resolved as stop or pause | Phase 2, inside `ac:plan` or `ac:execute` | delete, then report which BLOCKER and what the user chose |
| An error before the gate (branch, digest mismatch, chain aborted) | any phase | delete, then name the stop class |

A Phase 0 refusal is not in this table: nothing was written, so there is nothing to clean up.

<reminders>
- Criteria are frozen before the chain and reconciled, never rewritten, after it.
- `ac:plan --auto` chains `ac:execute` itself; invoking execute here runs the work twice.
- The gate returns a body and you write the file, so the component judging the run holds no tool that can change
  what it judged.
- No BLOCKER is auto-answered, and no `overrides[].accepted_by` is ever written by a model.
- Every ending deletes the marker first.
</reminders>
