---
name: tracing-commit-refs
description: Finds which refs contain a commit, plus copy-paste git commands to inspect its changes. Use for bce or unknown commit hashes.
argument-hint: "<commit-sha> [base-ref, default origin/develop]"
allowed-tools: Bash(git for-each-ref:*), Bash(git log:*), Bash(git show:*), Bash(git diff:*), Bash(git merge-base:*), Bash(git rev-parse:*), Bash(git name-rev:*), Bash(git cat-file:*), Bash(git fetch origin:*)
---

# Tracing Commit Refs

A commit hash arrived from somewhere outside the user's own workflow — a BCE job,
a model-deploy branch, a CI log, a PR comment. The user wants to know: **what ref
is this on, what work does it contain, and what did it change?**

Run steps 1–3, report the findings, then hand the user the copy-paste block.

## Step 1 — Which refs contain it

```bash
git for-each-ref --contains <SHA> --format='%(refname)'
```

**Always pass `--format='%(refname)'`.** The default format's first column is
`%(objectname)` — *the ref's own tip*, not the commit queried. When the queried
commit happens to be a ref's tip, the output looks like git echoing the argument
back, which reads as "this ref points at your commit." It doesn't mean that.

If nothing comes back, first check the object even exists locally with
`git cat-file -t <SHA>` (prints `commit`, or errors if git has never seen it). If it
exists, it is unreachable from every ref — dangling, or on a branch never fetched;
`git fetch origin` and re-run. `git name-rev --name-only <SHA>` gives the nearest
ref name in one line. Do not pass `--all` alongside a SHA — `--all` ignores the
argument and silently prints nothing.

## Step 2 — What is on that ref and not on the base

```bash
git log --format='%h %an | %ad | %s' --date=short <SHA> --not origin/develop
```

This is the load-bearing command. `--not <base>` bounds the walk at a semantic
boundary instead of an arbitrary `-N` window, so the output is exactly the work
that ref carries. Read it top-down: tooling commits first, the user's real commits
below them.

Accuracy depends on a fresh base. If the output shows unrelated commits from other
authors, local `origin/develop` is stale — `git fetch origin develop` and re-run.

## Step 3 — Confirm direction before claiming a base commit

`--contains` is **directional**: it asks which ref tips have the commit in their
history, so moving *down* the graph adds matches and moving *up* removes them.
Re-running `--contains` on a candidate base commit therefore always returns a
superset — it is a different question, not a cross-check. Verify with exit status:

```bash
git merge-base --is-ancestor <BASE> <TIP> && echo "BASE is ancestor of TIP"
git merge-base --is-ancestor <TIP> <BASE> && echo "unexpected: TIP is ancestor of BASE"
```

## Copy-paste block to hand the user

Substitute the real values for `C` and `BASE` before printing it.

```bash
C=<SHA>                  # the commit in question
BASE=origin/develop      # what to diff against

# which refs hold it
git for-each-ref --contains $C --format='%(refname)'

# the commits it carries beyond BASE
git log --format='%h %an | %ad | %s' --date=short $C --not $BASE

# files changed, whole ref vs BASE
git diff --stat $(git merge-base $C $BASE) $C

# full patch, whole ref vs BASE
git diff $(git merge-base $C $BASE) $C

# just this one commit
git show --stat $C
git show $C

# patch between two commits on the ref (e.g. base commit -> ref tip)
git diff --stat <BASE_COMMIT> $C
```

## Nuro: model-deploy and BCE branches

BCE (Behavior Core Eval) is launched with `--commit <SHA>`, and the model-deploy
tooling does **not** evaluate the commit handed to it directly. It cuts a branch
named `<user>_<model>_<timestamp>_<tag>`, stacks one `Build Worker` commit per
model on top ("Commit <model> model changes from gs://..."), and BCE runs the
resulting tip. So the SHA in a BCE job is usually *not* a commit the user wrote.

The original commit is the topmost non-`Build Worker` line from step 2. The
`Build Worker` commits touch only `onboard/models/**/*.version`,
`model_deploy_metadata.json`, and `model_manifest.json` — confirm that with
`git diff --stat <original> <bce-tip>` before concluding nothing else moved.

**Do not identify the base with `git log -20 <ref> | grep -v 'Build Worker' | head -1`.**
It reports the first non-`Build Worker` commit, which on an A/B *baseline* leg is
a random `develop` commit by an unrelated author — the baseline leg often carries
no user commits at all, only a release-model commit. Step 2 shows that correctly:
an empty user-commit list is itself the answer.

For an A/B pair, run step 2 on both legs. If one leg has user commits and the other
does not, the comparison mixes a code change with a model swap — say so, because it
changes how the metrics should be read.

## Reporting

State the ref name, the original commit (SHA + author + subject), how many tooling
commits sit on top, and which files the user's own commits touched. Then print the
copy-paste block with `C` and `BASE` filled in.
