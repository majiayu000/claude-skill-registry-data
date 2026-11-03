---
name: exit-skill-audit
description: Monthly self-audit of Pablo's exit-time skills (first target, Forethought closeout). Run only when the before-exit chain invokes it with --receipt-file, or on an explicit request to run or resume an exit-skill audit (not the skill-routing audit). Audits only propose changes for Pablo's approval; never edit the target skill during the audit.
---

# Exit-skill audit

Principle: every exit-time skill audits itself monthly through this skill;
audits only propose, Pablo approves. The principle, its instances and its TODO
targets are in `~/My Drive/dotfiles/claude/context/skill-audits.md`.

A **target** is an exit-time skill plus the checks that audit it, in
`targets/<id>/` beside this file: `target.json` (the skill's path, the
directories whose sessions it covers, the interval in days, the checks file
and the tests directory), `checks.md` (what the audit does, step by step) and
optional `tests/`. Adding a target means adding such a directory; this file
stays generic.

`scripts/skill_audit.py` owns everything deterministic: which target covers
the session, whether an audit is due, the per-target lock, pending proposals
and the receipt. State lives in `${XDG_STATE_HOME:-~/.local/state}/exit-skill-audit/<target>/`
(`state.json`, `lock`, `proposals/DATE.md`, `runs/DATE/`). Never edit those
files by hand; use the script. Below, `SA` means
`python3 -B <this skill's folder>/scripts/skill_audit.py`.

## Arguments

Parse from the current invocation only, never from quoted or historical text.

- `--receipt-file PATH`: the before-exit chain's receipt. Write it exactly once,
  with `SA write-receipt`, as the last step. It must not exist yet.
- `--target ID`, `--force`: manual runs only (Pablo asked). `--force` audits
  even when not due. The chain never passes them.

Session ID: `CLAUDE_CODE_SESSION_ID` in Claude Code, `CODEX_THREAD_ID` in
Codex. If neither is set, write a `failure` receipt saying so; do not invent
one.

## 1. Decide

```bash
SA decide --cwd "$PWD" --session "$SESSION"
```

Use the session's working directory (where it was started), not a directory
you changed into. The result's `action` is one of:

- `no-op`: no target covers this session, none is due, or another session is
  handling it. Write `SA write-receipt --status no-op --message "<reason>"` and
  stop. Do nothing else: this is the common case and must stay cheap.
- `resolve`: every pending proposal has a decision. Go to step 4.
- `resume`: earlier proposals still await Pablo. Go to step 3. Never re-audit
  while proposals are pending.
- `audit`: an audit is due. Go to step 2.

With `--target ID --force` from Pablo, skip `decide` and treat the target as
`audit` (unless it has pending proposals: then `resume`).

## 2. Audit in fresh contexts

```bash
SA begin --target ID --session "$SESSION"
```

It takes the target's lock (exit 3 means another session holds it: write a
`no-op` receipt naming it) and returns the `proposals` path and a `run_dir`.
If it reports that it broke a stale lock, mention that to Pablo.

Read the target's `checks.md` and do what it says **in subagents**, never in
this session's context, which may be huge. Give each subagent only the paths
and instructions it needs (the checks file section, the target skill path, the
sample slice, its report path in `run_dir`); it reads, writes only its report,
and returns a short summary. Use the most capable model at this session's
effort. If this runtime has no subagent tool, stop with `SA fail` and a
`failure` receipt: do not audit in this context.

Then one more fresh subagent synthesises the reports into the proposals file,
in this format:

```markdown
# exit-skill-audit proposals: <target>, <date>
Target skill: <path> at <commit>
Sample: <n> closeouts, <date range>; reports in <run_dir>
Summary: <three to six lines of the headline numbers, with the previous audit's for comparison>

## 1. <short title>
Problem: <what goes wrong, how often, in what share of the sample>
Evidence: <commits, log entries and transcript paths with line references>
Proposed change: <the edit to the target skill or its rules, concrete enough to apply>
Recommendation: do | skip
Decision: pending
```

Number proposals from 1 with no gaps; `Recommendation` and `Decision` are
single words. Order them by expected value. Read the file back yourself; it
must not propose editing anything outside the target skill and the rules it
cites.

- No proposals: `SA complete --target ID --session "$SESSION"`, then a
  `success` receipt ("audit found nothing to change; summary in <file>").
- Otherwise: `SA hold --target ID --session "$SESSION" --proposals <file>`, then
  step 3.

On any failure (a subagent that cannot finish, a script error), run
`SA fail --target ID --session "$SESSION" --reason "<what>"` and write a
`failure` receipt. A failed audit is retried the next day, not on every exit.

## 3. Present and hold

For `resume`, first `SA claim --target ID --session "$SESSION"` (exit 3: write
a `no-op` receipt naming the other session).

Show Pablo the summary and every proposal whose `Decision` is `pending`, as one
numbered list with the file's numbers: title, problem in a line, proposed
change, and the do/skip recommendation. Give the proposals file's path. Then
write the `held` receipt, e.g. "exit-skill-audit: 4 closeout proposals await your
decision (<file>)". The chain stops and the session stays open.

Do not edit the target skill before Pablo answers.

## After Pablo answers (same session)

For each proposal, set its `Decision:` line in the proposals file to `do`,
`skip` or `defer`, as Pablo said. Make each approved change as an ordinary
commit under the target repository's own rules (for ph-ps: its `AGENTS.md`,
"Git"), and add an `Applied: <repo> <short SHA>` line under the proposal. When
every proposal has a decision and every `do` has its `Applied` line, run
`SA resolve --target ID --session "$SESSION"`; it refuses otherwise. If Pablo
leaves the session first, the next exit resumes or resolves.

## 4. Resolve

Check each `Applied` commit exists in the named repository
(`git -C <repo> cat-file -e <sha>`). If one does not, write a `failure` receipt
naming it. Otherwise run `SA resolve --target ID --session "$SESSION"` and write
a `success` receipt ("exit-skill-audit: <n> proposals resolved for <target>").

## Seeding

When a target was audited by hand, record it so the next audit is due a
month later: `SA mark-audited --target ID --date YYYY-MM-DD --note "<where the
findings are>"`. `SA status --target ID` shows the state and lock.

## Verification

Tests for the script: `python3 -B -m unittest discover -s <this skill's
folder>/scripts -p 'test_*.py'`.
