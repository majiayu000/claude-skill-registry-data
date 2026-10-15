---
name: checking-dotfiles-status
description: Surveys ~/dotfiles and its submodules and proposes commit groups in commit order. Use for dotfiles status or accumulated changes.
argument-hint: "[--no-fetch]"
allowed-tools: Bash(~/.claude/skills/checking-dotfiles-status/scripts/survey.sh *), Bash(git status *), Bash(git diff *), Bash(git log *), Bash(git show *), Bash(git -C * status *), Bash(git -C * diff *), Bash(git -C * log *), Bash(git -C * show *)
---

# Checking dotfiles status

Turn a pile of accumulated edits into a short list of commits the user can approve. This skill only reads and proposes. Committing, pushing and bumping pins follow the `meta-repo-submodules` skill, after the user picks groups.

## Snapshot

!`~/.claude/skills/checking-dotfiles-status/scripts/survey.sh`

To refresh: `~/.claude/skills/checking-dotfiles-status/scripts/survey.sh [--no-fetch]`. It fetches remote-tracking refs and touches nothing else. Columns: porcelain `XY`, `+added/-deleted` lines, days since the file was written, path. Commit tags: `[unpinned]` is past the meta's recorded pin, `[unpushed]` isn't on the child's remote.

## 1. Read every diff before grouping

Filenames don't tell you intent. Read the content:

```bash
git -C ~/dotfiles diff HEAD -- <path>          # tracked file
git -C ~/dotfiles/<sub> diff HEAD -- <path>    # file inside a submodule
```

Read untracked files whole.

## 2. Group by intent

- **One reason per commit, whole files only.** If one feature touches a `bin/` script, a skill and CLAUDE.md, that's one commit. Never split a file across commits: a file holding two unrelated changes goes whole into one commit, which pulls in any other file tied to it, and the message names both changes. Imperfect grouping beats patch staging.
- **Docs ship with the change they describe.** A CLAUDE.md line, plan doc or `.docs_claude/PLANS_TOC.md` entry goes in the same commit as its change, never in a "docs" catch-all. A changed feature whose CLAUDE.md description is now stale needs that fixed in its group. Flag it.
- **Age is a hint.** Files written on the same day often belong together. Files written a week apart rarely do. Content decides.
- **Machine-local content goes in `machines/<host>.sh`**, not a shared dotfile. Flag hostnames, one machine's project paths, work emails and tokens showing up in `.gitconfig`, `.snippet_aliases`, `.bash_*`. Never propose committing a secret.
- **Submodules:**
  - Only commit inside `owner=jeffrey-ke` children. Group their dirty files the same way, as commits in the child.
  - Third-party children (`fzf-git.sh`) never get commits. Bump them only if the user asks.
  - A clean child detached at its pin needs nothing.
  - A child that is dirty and detached has to switch to a branch first (see `meta-repo-submodules`).
- **The pin bump gets its own meta commit.** It goes after the child commits and names what the child gained, summarized from its `[unpinned]` commit subjects.
- **Untracked:** a new `claude-skills/<name>/` is `claude-skills: add <name>`. Ask about anything that looks like scratch, and suggest `.gitignore` if it keeps coming back.

## 3. Name commits the way this repo does

`<area>: <what changed, lowercase, no period>`. Run `git -C ~/dotfiles log --format=%s -30` to check the current habits.

| Change | Area prefix |
|---|---|
| One dotfile | its name without the dot: `bash_tools:`, `gitconfig:`, `tmux:` |
| `bin/` script | `bin:` or the script name |
| New skill | `claude-skills: add <name>` |
| Edit to one skill | `<skill-name>:` |
| A feature across files | the files joined: `mdmath, tview, typeset-math:` |
| Pin bump | `nvim: bump for <what the child gained>` |

## 4. Present, then ask

Put the proposal in the order the commits would land: child commits, then the bump, then the other meta commits.

```
nvim (child, branch master)
  1. notebook: <msg>                lua/custom/notebook_cells.lua, tests/notebook_cells_test.lua
  2. keymaps: <msg>; <second msg>   lua/keymaps.lua (two unrelated changes, kept whole)
meta
  3. nvim: bump for <summary>       nvim
  4. bash_tools: <msg>              .bash_tools, CLAUDE.md (the .bash_tools row)
  ?  .snippet_aliases               holds a work-only path → machines/jke-desktop.sh?
Push state: meta is 6 ahead; nvim's committed pin isn't on its remote → push nvim before meta.
```

After the list, flag:
- anything ambiguous, marked `?`
- stale CLAUDE.md descriptions
- commits that already exist but aren't pushed. Those need a push, not a new commit.
- an `!!` line from the snapshot. "Pin not on the remote" blocks a meta push, because `push.recurseSubmodules check` refuses it. "Behind" means another machine pushed: use Recipe B in `meta-repo-submodules`.

Then use `AskUserQuestion` with `multiSelect` over the numbered groups so the user can pick which to commit, rename or drop. Commit nothing before they answer.

## 5. Carry out the chosen groups

Follow Recipe A in `meta-repo-submodules`: child commits, child push, bump, meta push. Push only if the user said to. Stage one group at a time with `git add <path>...`, never `git add -p` or `git apply --cached`. Confirm with `git diff --cached --stat` before committing.

Finish by re-running the survey. Show what's still dirty and the meta's ahead/behind count.
