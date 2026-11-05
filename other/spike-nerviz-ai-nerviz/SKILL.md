---
name: spike
description: >
  Opens a throwaway spike of this project in its own git worktree, beside the project
  directory, with every hook off there except the audit trail — no format, check, tests,
  compose gate or guard — so exploratory code can be written fast while the main checkout
  stays fully enforced and the spike's token spend still shows in /audit-usage.
  Explicit invocation only.
argument-hint: "<slug> | end <slug>"
disable-model-invocation: true
allowed-tools: AskUserQuestion, Bash(git worktree:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(java:*)
model: sonnet
effort: low
---

# `spike` — a throwaway worktree where only the audit trail stays on

`/spike <slug>` creates `../<project>-spike-<slug>` on branch `spike/<slug>` and reduces that
worktree's `.claude/settings.json` to the hooks `spike.keep_modes` lists. The main checkout
never relaxes, and this session stays enforced; the person opens `claude` in the worktree.

## Why this is a skill (Form 2) and not an agent

Form 2 because the trigger is the person deciding to explore (axis 2) and its effect — a worktree with enforcement off — must never start on the model's own decision. It is not an agent: none of the three reasons applies, the output is two lines and the work is three commands. Not `disableAllHooks` in a `settings.local.json`, which turns the audit trail off with everything else (0198, option 2).

## Contract

- **Class:** ops — `skill_classes.ops` in `@.claude/schemas/extensions.json`: writes no file of this project with a tool; its effect is a sibling worktree, made by `git worktree add` and `ArchHook.jar spike`.
- **Reads** the project root (`git rev-parse --show-toplevel`) and the argument.
- **Writes** nothing inside the project. Outside it: the worktree `../<project>-spike-<slug>` on branch `spike/<slug>`, whose `.claude/settings.json` `ArchHook.jar spike` reduces to the `spike.keep_modes` entries and marks `skip-worktree`.
- **Does not** merge, commit or push the spike, nor delete it — `end` prints the commands. Promoting spike code is a `/new-feature` run in the main checkout.
- Design: `@.claude/decisions/0198-spike-worktree-with-hooks-off.md`.

## Procedure

1. **Preconditions.** Run from the main checkout: `git rev-parse --git-dir` equals `git rev-parse --git-common-dir`; otherwise stop (failure mode 1). The argument is a slug matching `[a-z0-9][a-z0-9-]*`; missing → ask once with `AskUserQuestion`, then stop.
2. **`end <slug>`** — print, do not run: `git worktree remove ../<project>-spike-<slug>` and `git branch -D spike/<slug>`, plus one line: the spike's spend is already in `/audit-usage`. Stop.
3. **Create.** `git worktree add ../<project>-spike-<slug> -b spike/<slug>`, where `<project>` is the basename of the root. Exists already → failure mode 2.
4. **Relax.** `java -jar .claude/hooks/ArchHook.jar spike ../<project>-spike-<slug>` and relay its stdout line verbatim. Non-zero → failure mode 3.
5. **Report**, then stop:
   ```
   ✅ Spike <slug> — ../<project>-spike-<slug> on spike/<slug>
   Hooks ....... audit only (format, check, tests, compose gate, guard off there)
   Next ........ open `claude` in that directory; this session stays enforced
   End ......... /spike end <slug>
   ```

## Failure modes

1. Not the main checkout: `❌ /spike runs from the main checkout; this is a linked worktree. Open the project root and run it there.`
2. Worktree or branch exists: `❌ ../<project>-spike-<slug> or spike/<slug> already exists. Pick another slug, or /spike end <slug> first.`
3. `spike` mode refused: `❌ ArchHook spike refused: <its stderr first line>. The worktree exists with every hook on — remove it with git worktree remove ../<project>-spike-<slug>.`
