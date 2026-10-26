---
name: kanban-setup
description: Create a GitHub Projects kanban board for a repo and fill it with issues from documented work (planned, already done, or both).
argument-hint: "current | retroactive | both (default: current)"
disable-model-invocation: true
---

Creates a real board and real, public GitHub issues. Steps 1-3 are read-only; show the full preview (step 4) and wait for a yes before creating or changing anything.

## 1. Scope

**Target repo** per [BOARD.md](../next/BOARD.md#target-repo): resolve `origin` (this skill needs it on GitHub), `-R <owner>/<repo>` on every `gh` call, and on a fork ask which repo to write to before step 4 creates anything; `<owner>`/`<repo>` below are that repo. `gh auth status` must list `project`. Missing → offer the refresh (`gh auth refresh -s project -s read:project`, user runs it, opens a browser) or label mode (step 2); stop until the user picks one and, for the refresh, has run it.

## 2. Board (read-only)

Look for this repo's board per [BOARD.md](../next/BOARD.md); another board on the account doesn't count. Note whether one exists; create nothing yet.

The Status field needs an **In Review** option (`session-handoff` moves cards there; the default field has only Todo / In Progress / Done). If a board exists, check `gh project field-list <n> --owner <owner>` and note whether the option is missing (fix: [IN-REVIEW-OPTION.md](IN-REVIEW-OPTION.md)).

**Label mode** (four `status:*` labels instead of a board, colors in BOARD.md) when the user asks for it, the `project` scope isn't granted and the user declines to refresh it, or the owner can't create projects.

## 3. Candidates

Scan whatever exists: README roadmap/TODO sections, `TODO`/`FIXME` comments, `CHANGELOG.md`, `docs/`, plan docs, and (retroactive) `git log`. Skip `skilleddocs/`, the handoff folder `AGENTS.md`/`CLAUDE.md` sets, `node_modules`, `.venv` and vendored dirs. In every mode, drop items that already have an issue, open or closed, or a merged PR (`gh issue list -R <owner>/<repo> --state all --limit 1000`, `gh pr list -R <owner>/<repo> --state merged --limit 1000`; the default is 30). **Match**: the item names one of them by `#n` (incl. a squash subject's trailing `(#n)`), or its text minus a `TODO:`/`FIXME:` prefix equals a title, case-insensitive; a doubtful match → keep it, flagged in the preview.

Open issues not yet on the board (label mode: no `status:*` label) are candidates too: added to Todo, not re-created.

- **current**: planned/undone items.
- **retroactive**: finished items, created then immediately closed, for a clean history.
- **both**: both passes, separated in the preview.

## 4. Preview, then create

Preview first the **board actions** that will run: create the board (`gh project create --owner <owner> --title "<repo> Board"`), link it (`gh project link <n> --owner <owner> --repo <owner>/<repo>`), add the In Review option, or in label mode create the four labels. Then every item: title, mode, target column; existing open issues as a separate "add to board" group. This repo already has another board → ask which paths or labels go to which board and preview it as a `## Boards` section (`<path glob or label> → <board title>`, one per line; BOARD.md reads it) for `AGENTS.md`, or `CLAUDE.md` if that is the one the repo has.

On yes, do the board actions first (and write that `## Boards` section, left uncommitted for the user), then per item: `gh issue create -R <owner>/<repo>`, close it if retroactive, `item-add`, then `item-edit` Status to Todo or Done (BOARD.md); an existing issue gets only `item-add` + `item-edit` Todo. Label mode: `gh issue create -R <owner>/<repo> --label status:todo` (retroactive: `status:done`, then close), no `item-*`; an existing issue gets `gh issue edit <n> -R <owner>/<repo> --add-label status:todo`.
