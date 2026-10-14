---
name: craft-verdict
description: The committed verdict. Severity, one row per finding, and how the loop ends.
---

# Skill: Craft Verdict

> "What can be said in one word must not take three."

## Severity

| Sev | Means | Blocks |
|-----|-------|--------|
| `C` Critical | Correctness, security, architecture violation | **yes** |
| `W` Warning | Debt, maintainability | no — residual risk |
| `N` Nitpick | Style, preference | no |

A failing oracle blocks regardless. Two oracles disagreeing is a **stop** — escalate, don't pick one.

## A Finding Is A Row

```markdown
| Sev | Where | Issue | Change | Principle |
|-----|-------|-------|--------|-----------|
| C | craft-spec:30 | ":30 forbids self-run gates, :34 shows how | scope it to solo walks | Law 1 |
```

`Where` is `file:line`. Everything else is one clause.

**Risk is not a column.** Severity carries it — a Critical *is* "this breaks." Add one only when
severity fails to convey it: *"passes single-threaded, fails under load."*

**Principle is not optional.** It is the only thing separating a verdict from taste.

## Budget

| Section | Limit |
|---------|-------|
| Findings | one row each |
| What's Good | 3 bullets — only what a refactor would *lose* |
| Promote | one line each |
| Anything else | doesn't exist |

Over ~40 lines is itself a finding. **Candidate oracle:** `wc -l` against a threshold.

## Read The History First

Prior verdicts are input, not archive. Before forming a finding, read `verdicts/`:

- Raised **3 times** → `Promote` candidate, not a fourth finding.
- Approved over **3 times** → no longer residual. Raise the accumulation, not the instance.
- Already settled → don't re-raise unless it worsened.

Slop is invisible in one diff and obvious across forty. A judge that can't see forty can't see slop.

## What The Convener Runs

That read answers recurrence. It cannot say which round you are on, and no judge can ask — the
toolset is `Read`, `Glob`, `Grep`. So everything mechanical runs here, in the parent session, before
a judge is spawned. The gates, and the chain:

```sh
# which round this review is on
sh "${CLAUDE_PLUGIN_ROOT}/bin/verdicts.sh" round <dir> <review>

# the record before it — exit 1 when nothing stamps one
sh "${CLAUDE_PLUGIN_ROOT}/bin/verdicts.sh" prior <dir> <round> <review>

# the commit the judge is reading, and the refusal if the branch leaves it
git -C <worktree> rev-parse HEAD
sh "${CLAUDE_PLUGIN_ROOT}/bin/verdicts.sh" record <dir> <role> <review> \
  --worktree <worktree> --commit <sha>
```

**Take that commit before the judge starts, and hand it the same one.** A judge reads a worktree for
as long as it works, and a commit landing meanwhile changes what it reads. `record` then refuses,
exit 3, and names both commits.

**That `bin/` is Panel's, never the project you are reviewing.** Installed, your working directory
is the user's repository, and a bare `bin/verdicts.sh` finds their script or none. Unset, the
variable leaves `/bin/verdicts.sh` and exit 127 — loud, which is the point.

Hand over the round, and that record in full. On round one, word that this review has stamped none.
**A path is not a handoff:** a judge sent to go and look has been told its history.

Hand over each gate too: its name, its exit code, and what it printed. **A gate nobody ran is not a
gate that passed.** Name the ones you skipped, or the judge records that box unticked — and it
should.

**Read that out of the log the grade kept, never out of your own summary.** A grade condensed to
*the 25 gates at `<head>` — ALL GREEN* is a claim, and a judge can weigh a claim only as one.
`brief.sh --evidence <ledger>` reads the log instead, and refuses a work file that shouts a grade
with no log behind it.

**Hand it the ledger of the commit the judge reads.** With `--worktree` beside it, a log grading
another commit is refused. **And the log proves nothing on its own** — a row is a line of text.
The brief says so, and asks the judge to weigh it as a record rather than as a run.

`bin/brief.sh` does all this for a judge on another host. It refuses to print a brief when the chain
cannot answer. **Nothing refuses you here.** Forget it and the judge refuses instead, which is the
whole of the enforcement. **Refuse when the gap makes a verdict wrong; say so and carry on when it
only makes one smaller.**

## Deeper

| | |
|---|---|
| [artifact](artifact.md) | the files a review leaves, and the verdict template |
| [ending](ending.md) | SPLIT, the bar and the ratchet, and DEADLOCK's two triggers |

## The Anti-Patterns

| Don't | Do |
|-------|----|
| Verdict in chat | Verdict in git |
| Everything Critical | Use the bar |
| New nitpicks in round three | Ratchet |
| Approve without recording risks | Record them |
| "Recording what held…", "That is the point:", "Worth noting" | Delete. Meta-narration. |
| Restate the table in prose below it | The table said it |
