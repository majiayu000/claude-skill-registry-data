---
name: "Roadmap: Claim"
description: "Claim a roadmap task when work on it starts, or release the claim when work stops: asks who is doing it, runs the CLI, commits the change"
when_to_use: "When the user says they are starting, taking or working on a roadmap task (\"claim 2SE.1\", \"I'm picking up the search task\"), or wants to drop one (\"release 2SE.1\", \"I'm not doing that any more\"), or a roadmap hook nudge asks whether the branch is roadmap work. Never for setting an assignee without a start (roadmap-update-devs) or for marking work done (roadmap-maintain)."
model: sonnet
effort: low
metadata:
  glyph: ᛊ
  family: roadmap
disable-model-invocation: false # the trigger is the user saying they are starting a task, which Claude sees first; the commit and push each await approval below
allowed-tools: ["Read", "Bash(python3:*)", "Bash(git:*)"]
arguments: ["task", "who"]
argument-hint: "[<task id>] [<assignee>|release]"
---

# Roadmap Claim

A claim says a person has started a task: the task gains a `started` date and an `assignee`, and views show it as in progress. This skill is the one place that procedure lives; the branch-start hook nudge and `roadmap-maintain` both hand over to it.

Shared conventions: `~/.claude/library/references/roadmap-conventions.md` (Claims section). The CLI is `python3 "$HOME"/.claude/library/scripts/roadmap.py`.

**Hard rule, inherited from the conventions:** an assignee is never inferred. Never propose or pre-fill a name from the task text, git author or who owns neighbouring tasks. The one name that may be offered is the task's own current `assignee`.

---

## Step 0: Parse the arguments

Both arguments are optional and positional: passing `$who` requires `$task`.

| Call | Meaning |
|---|---|
| (no arguments) | pick a ready task from a list, then claim it |
| `<task id>` | claim that task; ask who is doing it |
| `<task id> <assignee>` | claim it for that assignee; nothing to ask |
| `<task id> release` | drop the claim |

`release` is a reserved word in the `$who` slot, so a dev with that name needs `roadmap.py claim` run by hand. A multi-word assignee arrives quoted (`"Mary Ann"`); take the quoted string whole.

Match `$task` against the phase's task ids exactly, then case-insensitively. No match: hard stop, print the usage line with the three closest ids and run nothing. Never guess a task.

```text
Usage: /roadmap-claim [<task id>] [<assignee>|release]
```

---

## Step 1: Locate the roadmap

Run `python3 "$HOME"/.claude/library/scripts/roadmap.py detect`. Exit **3** = old simple format: stop and tell the user to run `roadmap-migrate` first. Exit **2** = could not locate or parse: ask the user for the path. Proceed only on exit 0.

**Phase selection.** List the phases in `roadmaps.json` without `archived: true`. One active phase: use it. Several: ask with AskUserQuestion which to work on, listing the last active phase in the array first and marking it recommended. Pass the choice as `--phase "{name}"` on every later CLI call. Never pick silently between active phases.

---

## Step 2: Choose the task (no `$task` only)

Run `roadmap.py ready --json`. Show the first 5 `candidates` (already in leverage order) as `{id}  {description}  (unblocks {transitiveUnblocks}, {milestoneName})`, and under them one line naming each task in `claimed` as `Claimed: {id} ({assignee}, since {started})`, so nobody picks one twice. Ask which with AskUserQuestion, one option per candidate. An empty candidate list is a result: say `No unclaimed ready task.` and stop.

---

## Step 3: Claim or release

**Where this runs.** Check this and the file's uncommitted state (Step 4, item 1) before running the CLI. Claims normally live on the branch doing the work (`git branch --show-current`). On the default branch, ask first with AskUserQuestion: **Claim here and leave it uncommitted** / **Cancel**. Whichever is chosen, skip the commit and push in Step 4 on the default branch.

**Claim.**

1. `$who` given: that is the assignee. Otherwise ask in plain text, `Who is doing {id}?`, offering the task's current `assignee` when it has one.
2. Run `python3 "$HOME"/.claude/library/scripts/roadmap.py claim {id} --assignee "{name}"` with the Step 1 phase and path. Without an assignee answer, leave `--assignee` off.
3. Relay a refusal word for word. The cases: the task is not ready to start (it reports its effective status), it is already claimed (by whom, since when), it is assigned to someone else, or `roadmaps.json` is not in canonical form. For the assignee case offer to hand the task over, and rerun with `--reassign` solely when the user agrees. For the format case say that a write would reformat the whole file, and rerun with `--reformat` solely when the user agrees.

**Release.**

1. Run `roadmap.py release {id}` with the Step 1 phase and path. When the task has an `assignee`, first ask once whether to clear it too; add `--unassign` only on yes.
2. A task that is not claimed is reported as it is; nothing is written.

The CLI writes `roadmaps.json` only. A claim has no PHASE file annotation and no overview line, so nothing else is edited here.

---

## Step 4: Commit and offer the push

Skip this step on the default branch and when the CLI refused.

1. Before Step 3 runs the CLI, note whether `roadmaps.json` (the path `detect` reported) already has uncommitted changes: `git status --short -- {path}`. If it did, ask before committing: those changes would ride along.
2. Commit that file only: `git commit -m "chore(roadmap): claim {id}" -- {path}` (or `release {id}`).
3. Ask once whether to push the branch so the team sees the claim. Push (`git push -u origin {branch}`) only on yes.

---

## Step 5: Report

One line: `Claimed 2SE.1 for Jaz (started 2026-10-02) on feat/search, committed, not pushed.` or the release equivalent. A claim needs no follow-up; the next action is the work itself.

---

## Red flags

**Never:** infer an assignee; edit `status` to `in_progress` (a claim is a field, never a status); hand-edit `started` or `assignee` in `roadmaps.json` when the CLI can do it; use `--reassign` without the user agreeing to take the task from its current owner; commit anything but `roadmaps.json`; push without a yes.

<raw-arguments value="$ARGUMENTS" />
