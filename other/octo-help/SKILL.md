---
name: octo-help
description: Cheatsheet for reading and replying to PR review comments with octo.nvim on the Nuro monorepo. Use for octo, "Octo pr", or PR-comments-in-nvim questions.
---

# octo.nvim cheatsheet

Config: `~/dotfiles/nvim/lua/custom/plugins/octo.lua`. `<localleader>` is Space. Run from inside the repo; octo finds the PR from the current branch.

## Opening

| Command | Opens |
|---|---|
| `:Octo pr` | PR for the current branch (via `gh pr view`) |
| `:Octo pr edit 291538` | PR by number |
| `:Octo search is:pr is:open author:@me` | your open PRs, one request |
| `:Octo review browse` | read-only side-by-side diff with threads |

Avoid `:Octo pr list`: it pages through every open PR in the monorepo (~9k, ~93 requests) before showing anything. It has no author filter.

## Conversation buffer (`:Octo pr`)

Threads show their code snippet as virtual text above the comments.

| Key | Does |
|---|---|
| `]c` / `[c` | next / prev comment, across all files |
| `gf` | open the real file at the commented line; `<C-o>` back |
| `<localleader>cr` | reply to thread |
| `<localleader>ca` | add a top-level comment |
| `<localleader>rt` | resolve thread |
| `:w` | post edits; nothing is sent before this |
| `<C-r>` | reload from GitHub; discards unposted drafts |
| `<C-b>` | open in browser |

Loop: `]c` → `gf` → fix → `<C-o>` → `<localleader>cr` / `<localleader>rt` → `:w`.

**Canceling a reply:** `Esc`, then `<C-r>`. An empty draft is skipped on `:w`, but one with text is posted by any `:w`. Don't use `<localleader>cd` (deletes *posted* comments) or `u` on a draft.

## Review diff (`:Octo review browse`)

| Key | Does |
|---|---|
| `]q` / `[q` | next / prev changed file |
| `]t` / `[t` | next / prev thread, **current file only, past the cursor** (silent no-op otherwise) |
| `:Octo review thread` | threads on the cursor line |
| `:Octo review close` | exit |

To comment from the diff: `:Octo review start`, `<localleader>ca` on a line or visual selection, then `<localleader>vs` to submit.

## Gotchas

- `gf` uses the line at the PR head commit, so local edits since push can shift it. Outdated threads may have no current line.
- `gf` isn't mapped in the review diff by default.
- clangd attaches to `octo://` cpp buffers and errors on CursorHold. `init.lua`'s detach guard matches any `scheme://` name.
