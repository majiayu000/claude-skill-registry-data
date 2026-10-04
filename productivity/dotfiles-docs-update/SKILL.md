---
name: dotfiles-docs-update
description: Use when the user asks to "update docs", "sync docs", "aggiorna la doc", or after making changes to dotfiles configs. Updates the Obsidian vault docs in ~/Documents/Taccuino Cerusico/60 - Progetti/dotfiles/ to reflect the current state of the repo.
---

## Purpose

Keep `docs/` in sync with the actual dotfiles state. Docs live in the Obsidian vault; `dotfiles/docs/` contains symlinks to them. Edit the vault files directly.

## File mapping

| Changed path | Doc to update |
|---|---|
| `aerospace/` | `docs/aerospace.md` |
| `ansible/` | `docs/ansible.md` |
| `atuin/` | `docs/atuin.md` |
| `ansible/group_vars/*/main.yml` | `docs/brew.md` (also `docs/ansible.md`) |
| `claude/` | `docs/claude.md` |
| `zsh/fzf.zsh`, `bat/`, `fzf-git.sh/` | `docs/fzf.md` |
| `gitconfig/`, `git/` | `docs/git.md` |
| `herdr/` | `docs/herdr.md` |
| `nvim/` | `docs/nvim.md` |
| `tmux/` | `docs/tmux.md` |
| `yazi/` | `docs/yazi.md` |
| `zsh/` (excluding fzf.zsh) | `docs/zsh.md` |
| `setup.sh`, `.stowrc`, `CLAUDE.md` | `docs/index.md` |

## Workflow

1. Run `git diff HEAD~1 --name-only` (or `git diff --name-only` for uncommitted) to identify changed files
2. Map changed paths to the relevant docs using the table above
3. For each doc to update, resolve the real path: `readlink dotfiles/docs/<tool>.md`
4. Read the current config files for each affected tool
5. Read and edit the **resolved vault path** — never edit through the `docs/` symlink directly (the Edit tool refuses symlinks)
6. Update only the sections that changed — preserve wikilinks, add new ones where relevant
7. Never remove wikilinks unless the referenced tool was actually removed

## Doc file paths

`dotfiles/docs/<tool>.md` are symlinks into the Obsidian vault. Always resolve with `readlink` before editing.

## Style rules

- No frontmatter tags
- Wikilinks: use `[[dotfiles - tool|label]]` for cross-references between dotfiles docs
- Wikilinks: use `[[Tool]]` for external tools (Obsidian, Catppuccin, Neovim, etc.)
- Config blocks: show actual current values, not placeholders
- Keep it agent-readable: paths, gotchas, current state — not generic docs

## Adding a new tool

1. Create `~/Documents/Taccuino Cerusico/60 - Progetti/dotfiles/dotfiles - <tool>.md`
2. Add symlink locally: `ln -sf "$VAULT/dotfiles - <tool>.md" dotfiles/docs/<tool>.md`
3. Add entry to `docs/index.md` wikilink list
4. Add row to the mapping table in this skill
5. Add the `{ src, dest }` pair to the `loop:` in `ansible/roles/macos/tasks/main.yml`
   (`Symlink docs from Obsidian vault` task) — this is what recreates the symlink on a
   fresh machine or re-run; `setup.sh` is legacy and no longer does this
6. Add the path to the case-statement in `.claude/hooks/docs-staleness-check.sh`

## Automation — Stop hook (staleness reminder)

A Stop hook reminds you to run this skill after committing configs whose vault
doc may now be stale. It does NOT auto-edit docs (the vault is hand-written and
gitignored) — it only nudges.

- **Script**: `.claude/hooks/docs-staleness-check.sh` (versioned, runs on both Macs).
- **Registered in**: `.claude/settings.json` → `hooks.Stop` (project-level).
- **Trigger**: last commit only — `git show --name-only --pretty=format: HEAD`,
  mapped via the table above. Chosen over working-tree diff to avoid nagging on
  WIP during long sessions; the trade-off is it won't fire until you commit.
- **Output**: emits `{"systemMessage": "..."}` suggesting `/dotfiles-docs-update`.
  Never blocks (informational), `set -euo pipefail`, exit 0 when no match.
- **Keep the case-statement mapping in sync with the table above** — `zsh/*` must
  come AFTER `zsh/fzf.zsh` so fzf doesn't get shadowed.

**Gotcha — activating a new hook**: Claude Code's settings watcher only loads
hooks present at session start (or when you open `/hooks`). After first adding
the hook to `.claude/settings.json`, open `/hooks` once or restart — otherwise it
silently won't fire even though the JSON is valid. Verify the JSON with:
`jq -e '.hooks.Stop[].hooks[] | select(.type=="command") | .command' .claude/settings.json`
