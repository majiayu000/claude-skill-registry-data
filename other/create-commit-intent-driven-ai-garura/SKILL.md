---
name: create-commit
description: Stage files and create one or more commits in a single pass
user-invocable: false
model: haiku
allowed-tools: Bash
---

# create-commit

Model-invocable skill for creating commits. The grouping and the messages are decided
**before** this skill runs (by `analyze-changes`); this skill only **executes** that
plan. git is the tool and it is already known — so run it directly, in one pass. Do not
reason between commits, do not re-decide grouping, do not invoke a sub-agent per commit.

## Purpose

Stage the decided files and create the decided commits. Pure execution, no
decision-making. When handed several groups, commit **all of them in this one
invocation** — never one call per group.

## Input

Receive from the caller a **commit plan** — one or more groups, each:
- `files`: list of files to stage for this group
- `type`: conventional type (feat, fix, refactor, docs, chore, …)
- `scope`: component/area
- `subject`: imperative, present tense
- `body`: optional description
- `issue`: optional issue number

The plan may arrive inline or as a path to the analysis/groups file (e.g.
`analysis.yaml`); read the file if a path is given. Either way, treat it as the final
plan — execute, don't revise.

## Process

Loop over the groups **in order**, in this single invocation. For each group, run the
two git commands directly — no thinking step in between:

1. **Stage that group's files** (only the files listed — never `git add .` / `-A`)
   ```bash
   git add "file1" "file2" "file3"
   ```

2. **Commit** with the conventional message
   ```bash
   git commit -m "type(scope): subject

   body

   Issue: #123"
   ```

3. **Record the hash**
   ```bash
   git rev-parse --short HEAD
   ```

After the last group, confirm the tree is clean (`git status --porcelain`). Do **not**
push — pushing is the caller's separate step.

## Output

Return using template: `templates/commit-output.md` — one entry per commit (hash +
message), and the final clean-tree confirmation.

## Constraints

- ONLY stage files explicitly listed for each group.
- NEVER use `git add .` or `git add -A`.
- ALWAYS use conventional commit format.
- Commit every group in ONE invocation — never a separate call (or sub-agent) per group.
- NEVER push.

## Version

| Field | Value |
|-------|-------|
| Version | 2.0.0 |
| Category | operations |
