---
name: workflow-retro
description: >
  Records the outcome half of a feature's workflow evaluation at the end of a
  /feature session: which steps ran or were skipped, cycle counts, what each
  critic caught and what was adopted, plus a short judgment section. Writes
  one fixed-schema file per feature branch to .workflow-log/ (gitignored),
  including the session IDs the companion /workflow-inspect skill needs to
  append the cost half later. Run manually, optionally, at the end of a
  feature session.
---

# /workflow-retro — Record the Feature's Workflow Outcome

Run this skill at the end of a feature session — typically after the PR is
opened (Step 9 of `/feature`), or when the feature is abandoned. It records
what the workflow actually did for this feature: which steps ran, what each
one caught, and what that changed. Over several features, these records are
the evidence base for tuning the workflow — which steps earn their cost,
which are candidates for skip rules.

This is the **outcome half** of the record. The **cost half** (tokens per
step, wall-clock, file-read overlap) is computed from the session transcripts
by the companion `/workflow-inspect` skill and appended to the same file
later. If that skill is not installed yet, the Cost section simply stays
pending — nothing here depends on it.

**Ground rules:**

- **Facts come from artifacts.** Fill each field from the PR body, `git log`,
  and the plan/critique/review/QA outputs in this session — not from memory
  alone when an artifact exists. Anything not established is recorded as
  `unknown`, never guessed.
- **The log is local evaluation data.** `.workflow-log/` is gitignored —
  never commit it or its contents, and never move it into the repo history.
- **One file per feature branch.** If a file for the current branch already
  exists (a previous retro, or the feature spans multiple sessions), update
  it — fill gaps, correct facts, append the new session ID — instead of
  creating a duplicate. Exception: if the existing file evidently records a
  *different* feature that reused the branch name (its PR is already merged,
  or its dates are far from this session's), ask the user whether to replace
  it or pick another filename — do not merge two features into one record.
- Writing the log file (and creating its directory) is the **only** mutation
  this skill performs.
- The skill assumes a `/feature` session. In a session that ran only part of
  the workflow (an ad-hoc `/plan-draft`, a review-only pass), record what
  applies and mark the rest `n/a`.

## Step 1 — Locate the log target

The log lives at `.workflow-log/<branch>.md` under the repository's **main
worktree** — which is not necessarily the current directory: feature work
often runs in a per-feature `git worktree` that is deleted once the PR
merges, and the log must outlive it. Resolve the location with a single
`git rev-parse --path-format=absolute --git-common-dir`: that prints the
shared `.git` directory, whose **parent** is the main worktree root, and the
log directory is `.workflow-log/` there (covered by the `.gitignore` entry
`/init-workflow` adds). In a plain single-checkout clone this resolves to the
repository root itself. Sanity-check the result: if the resolved parent path
still contains a `.git` segment (e.g. the project is a git *submodule*, where
the common dir lives under the outer repo's `.git/modules/`), the layout is
unusual — ask the user where the log should live rather than writing there.

`<branch>` is the branch name with `/` replaced by `-` (e.g. branch
`feat/login-form` → `.workflow-log/feat-login-form.md`). Create the
directory if missing. If the file already exists, this run updates it (see
ground rules).

## Step 2 — Capture the session pointers

`/workflow-inspect` runs in a later, different session that has no way to
know which transcript was the feature session — recording the pointer now,
while only this session knows it, is the point of this step. Transcripts are
pruned after a retention window (Claude Code's `cleanupPeriodDays`, ~30 days
by default), so the join must happen within it.

Get the current session ID, in this order:

1. The `CLAUDE_CODE_SESSION_ID` environment variable (check with a single
   `printenv CLAUDE_CODE_SESSION_ID`). Its value is the session ID — the
   transcript is `<session-id>.jsonl` somewhere under `~/.claude/projects/`.
2. If the variable is unset, fall back to a heuristic: the most recently
   modified `.jsonl` anywhere under `~/.claude/projects/` (a single `find`)
   is *probably* the current session — transcripts are filed under the
   session's *launch* directory, which is not necessarily the current
   worktree's, so search globally rather than deriving a directory from a
   path. If more than one transcript was modified in the last few minutes
   (concurrent sessions), ask the user which one is this session rather
   than picking silently.
3. If neither works — the variable is unset and the directory is missing or
   ambiguous — record `Sessions: unknown` rather than guessing. Both the
   variable and the on-disk layout are current, undocumented Claude Code
   behavior, not a stable interface; a wrong-but-plausible session ID
   silently corrupts the later cost-join, while an honest `unknown` merely
   skips it.

If the feature spanned earlier sessions, record their session IDs too — ask
the user if they can identify them (e.g. by date); otherwise record
`earlier sessions: unknown`.

Also record the **current worktree's absolute path** (the schema's
`Project path` field) — context tying the record to the checkout the work
ran in. The session ID is the load-bearing pointer: `/workflow-inspect`
locates transcripts by a global search for `<session-id>.jsonl`, never by
deriving a directory from the recorded path.

## Step 3 — Fill the record

Draft the file with exactly this structure (fixed schema — later tooling
aggregates across files, so keep the headings and field labels verbatim):

```markdown
# Workflow retro — <branch>

- Date: <YYYY-MM-DD of this retro>
- Branch: <branch>
- PR: <url | not opened | abandoned>
- Plugin version: <installed workflow plugin version, if discoverable | unknown>
- Sessions: <session ID(s), oldest first | unknown>
- Project path: <absolute path(s) of the worktree(s) the sessions ran in | unknown>

## Steps

| Step | Ran? | Notes |
|------|------|-------|
| 1a planner | yes / skipped / n/a | <why skipped, if skipped> |
| 1b plan-critic | yes / skipped / n/a | <why skipped, if skipped> |
| 1c approval | yes / n/a | plan revisions before approval: <N> |
| 2 implement | yes / n/a | deviations: <N> minor, <N> material |
| 3 tests | yes / n/a | final full run: <N> tests, <pass/fail> |
| 4–6 code review | yes / n/a | rounds: <N>; FAIL items: <N>; NEEDS_DECISION: <N> |
| 7–8 QA | yes / skipped / n/a | <why skipped>; findings: <N> |
| 9 PR | yes / n/a | |

## Findings

- plan-critic: <N> findings; adopted into plan: <N>; discarded: <N>
- code-critic FAIL items, one line each: <what, and the fix>
- NEEDS_DECISION items, one line each: <what, and the user's decision>
- QA findings, one line each: <what, and its disposition (fixed / deferred
  <task id> / ignored)>

## Judgment

- Did the planner's plan contain anything the implementer would not have
  found alone? <answer>
- Which plan-critic findings changed the plan? <answer | none>
- Did implementation re-read files the planner had already read?
  (best-effort — /workflow-inspect computes this exactly) <answer>
- Did any step produce nothing of value this feature? <answer | none>

## Cost

pending — run /workflow-inspect before the session transcripts are pruned
```

The Steps and Findings sections are factual — fill them from the artifacts.
The Judgment section is the implementer's honest assessment — answer from
what actually happened this session, in a sentence each; `unknown` is an
acceptable answer.

## Step 4 — Confirm and write

Present the drafted record in one block for the user to confirm or correct —
the Judgment answers especially are theirs to override. Then write the file
and report its path. Do not commit anything.
