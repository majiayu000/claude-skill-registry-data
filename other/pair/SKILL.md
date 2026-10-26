---
name: pair
description: Run one task (issue number or free text) in an isolated git worktree via a manager subagent that owns its implementer and retries; you push and open the PR at the end. Use for "implement issue N", "pair on this", or one task on any repo, forks included.
argument-hint: "<issue # | task text> [--no-worktree] [--push] [--model haiku|sonnet|opus]"
---

You run **one task** through a `manager` subagent. Neither you nor the agents implement in your context; you are the only one who touches the remote.

Flags: `--no-worktree` (new branch in the current checkout), `--push` (push + PR without asking), `--model` (implementer model; default: by size, the `manager` agent's step 3).

## 1. Resolve

- **Target repo** per the `next` skill's `BOARD.md`, Target repo section (path in §2): `-R <o/r>` on every `gh` call. Number → `gh issue view <n> -R <o/r>` (on a fork, the parent's issue is fine to read). Text → write a 3–6 item acceptance checklist.
- Repo facts: default branch, branch prefix (user's `CLAUDE.md`, else `feat`), test command, `CONTRIBUTING.md` / `AGENTS.md`.
- **Fork** (`upstream` remote): reading is fine, so `git fetch upstream`, fast-forward default to `upstream/<default>`, then confirm every file or symbol the issue names still exists. Put anything missing in the brief.

## 2. Isolate

`origin` a relative path (`git remote get-url origin` has no `scheme://`, `host:`, leading `/` or drive letter, e.g. `../origin.git`): git resolves it from each worktree's own root, so fetch and push fail inside a worktree. Make it absolute first, from the main checkout: Git Bash or mac/linux `git -C "<main>" remote set-url origin "$(cd "<main>" && cd "<url>" && pwd)"`; PowerShell `git -C "<main>" remote set-url origin (Resolve-Path (Join-Path "<main>" "<url>")).Path`. Same target, and remotes are shared by every worktree, so this one change covers them all; tell the user the old and new URL.

```
slug = issue-<n>-<kebab-title>   (or ≤6 kebab words of the task)
git worktree add ../_worktrees/<repo>-<slug> -b <prefix>/<slug> <default>
```

This is the one branch rule; a planner brief's Branch follows it, and when a brief names one, use it verbatim (`<slug>` = its part after `<prefix>/`).

`--no-worktree`: `git switch -c <prefix>/<slug> <default>`. Existing worktree or branch → reuse it and say so.

Deps (`node_modules`, `.venv`): link each from the main checkout, paths quoted (shown for `.venv`). Windows: link only when both paths are absolute; an empty one puts the junction at the drive root (`C:\.venv`).
- Windows, Git Bash (`cygpath` builds the paths; without `MSYS_NO_PATHCONV` MSYS rewrites `/J` into a path):
  ```
  w=$(cygpath -wa "<wt>"); m=$(cygpath -wa "<main>")
  if [[ $w == [A-Za-z]:'\'?* && $m == [A-Za-z]:'\'?* ]]; then MSYS_NO_PATHCONV=1 cmd /c mklink /J "$w\.venv" "$m\.venv"; else echo "STOP: path not absolute: '$w' '$m'"; fi
  ```
- Windows, PowerShell: `if ("<wt>" -match '^[A-Za-z]:\\.' -and "<main>" -match '^[A-Za-z]:\\.') { cmd /c mklink /J "<wt>\.venv" "<main>\.venv" } else { "STOP: path not absolute" }`.
- mac/linux: `ln -s "<main>/.venv" "<wt>/.venv"`.

Issue number on a board, worktree/branch not reused → (fork: only after the target-repo answer) move it to In Progress and comment "Started on branch `<branch>`" (the `next` skill's `BOARD.md`: `~/.claude/skills/next/` or, as the plugin, `kanban/next/`). Board errors never block the task.

## 3. Delegate

One blocking call, `subagent_type="manager"` (or `"krish:manager"` when installed as the plugin; never `fork`: it ignores the model and can't nest):

```
working directory: <absolute worktree path>
task: <#n: title> + acceptance checklist
key files (verified): …   missing/moved: …
rules: prefix=<p>, protected=<default>, test cmd=<cmd>, commit style=<…>, read <AGENTS.md>
implementer model: <--model or "by size">
decisions: <ask | assume>; first A-id: A-<k> (next after the highest A-<number> in main's register)
register header: <main's register header row, verbatim; none → the default in TEARDOWN.md, Register rows>; each A-n is one row in that format
max_rounds: 3
never push, merge, or open a PR.
```

Leave the worktree alone while it runs.

## 4. On return

1. **INTERIM** report, or one missing the Branch, Tests or Rounds section (a placeholder, a one-liner) → not a result. INTERIM: wait for the next handback. Otherwise ask the manager once (SendMessage) for its full report; still missing → rerun from §3 with a fresh manager.
2. Show the report verbatim.
3. Thin report or risky change → rerun the tests yourself. One-line fixes: commit them.
4. Unfinished (`skilleddocs/HANDOFF.md`, or the SHA that last held it) → say what's left; offer another round from it.
5. Before any push: `git -C <worktree> diff --name-only <default>...HEAD` lists no `skilleddocs/HANDOFF.md`, nothing in the handoff folder (AGENTS.md/CLAUDE.md's, else `skilleddocs/handoffs/`) in commit mode, and nothing under `skilleddocs/` or that folder when untracked ([TRACKING.md](../handoff-auto/TRACKING.md)). A hit → remove it in a commit.
6. `--push` or the user says go:
   ```
   git -C <worktree> push -u origin <branch>
   gh pr create -R <o/r> --head <origin-owner>:<branch> --title "<title>" --body "<summary>\n\nCloses #<n>"
   ```
   `<o/r>` = the PR's base: on a fork, ask fork or parent first; the parent only on an explicit yes naming it. Never merge.
7. Review comments later → step 3 again, comments as the task, same worktree.

## 5. Print and teardown

Print: branch, worktree, PR URL or "not pushed", test result, rounds, HANDOFF.md path if any.

Teardown only after the PR merges, with the exact commands in [TEARDOWN.md](TEARDOWN.md) (Git Bash and PowerShell). `git worktree remove` deletes git-excluded files silently, and it and any recursive delete (`rm -rf`, `Remove-Item -Recurse`) follow a link and empty the main checkout's copy: never run them while a link exists.

1. **Records**: every untracked or ignored file under the worktree's `skilleddocs/` and the doc folders `AGENTS.md`/`CLAUDE.md` names (dated handoffs, `HANDOFF.md`, the decisions register, anything else) goes to the same subpath in the main checkout: new files moved without overwriting; `HANDOFF.md` renamed to a dated handoff in main's handoff folder (never overwriting) so the next teardown doesn't clash on it; the register merged by appending the rows whose ids main lacks. The worktree's register is deleted only when every line was carried over or is already in main (trailing `\r` ignored); a heading, prose, a wrong cell count or a clashing row keeps it and prints `STOP` with those lines. A same-named file stays put and is reported.
2. **Unlink** each dep (removes the link only).
3. **Hard check**: STOP while a dep link (dangling included) is left or `git -C "<wt>" status --porcelain --ignored --untracked-files=all -- <doc folders>` lists anything; only then `git worktree remove`.

STOP → leave the worktree and report what is left. `git worktree remove` refuses → stop and report `git -C "<wt>" status --short`; never `--force`.
