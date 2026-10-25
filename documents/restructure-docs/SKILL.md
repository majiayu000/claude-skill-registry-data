---
name: restructure-docs
description: Consolidate a project's scattered Markdown docs into one docs/ folder and rename them with a numbered x.y-title.md scheme that encodes reading order, rewriting every cross-reference to match. Use when the user asks to "move all docs to docs folder", "organize/restructure the docs", "number the docs", "order the docs", or when a repo has many top-level .md files that should be consolidated. Does not touch README.md or the agent's own root instructions file (e.g. CLAUDE.md) — those stay at the repo root by convention.
---

# Restructure Docs

Reorganizes a repository's Markdown documentation two ways, either independently or together:

1. **Consolidate** — move every top-level doc (except `README.md` and the root agent-instructions file, e.g. `CLAUDE.md`) into `docs/`.
2. **Number and order** — rename every file in `docs/` to `x.y-title.md`, where `x` is a topic group and `y` is its position within that group, so the folder listing itself shows the intended reading order.

Both steps end with every cross-reference across the repo rewritten to match — markdown links, bare filename mentions in prose/tables, and ASCII directory-tree diagrams in README files.

## When to run which step

- "Move all docs to docs folder" → consolidate only.
- "Order/number the docs" → numbering only, run against whatever is already in `docs/`.
- "Restructure/organize the docs" → do both, consolidate first, then number.

## Workflow

### 0. Isolate

This changes tracked files across the repo. If not already in an isolated worktree, create one before touching anything (this plugin assumes the harness's worktree tooling; if working directly in a checkout, use a feature branch instead).

### 1. Inventory

List every `.md` file under the repo root and under `docs/` (or the user's named docs folder). Read each file's title/opening paragraph if the filename alone doesn't make its topic obvious — don't guess categories from filename keywords alone when the content says otherwise.

### 2. Consolidate (if in scope)

- Move every top-level `.md` file into `docs/` with `git mv`, preserving history. Exceptions: `README.md` stays at root (GitHub renders it there); the root agent-instructions file (`CLAUDE.md` or equivalent, if the project has one) stays at root.
- Check for untracked `.md` files at the root too (`git status --porcelain`) — a doc the user is mid-drafting is still a doc. Copy/move it in as well; it will show as a new untracked file in `docs/` rather than a rename, which is expected.
- Leave README files that are local to a subfolder (e.g. `kernel/README.md`, `src/README.md`) where they are — those document that subfolder, not the project as a whole, and moving them would strip their context.

### 3. Design the numbering scheme (if in scope)

Group the docs by topic and assign `x.y`:

- Read enough of each doc to place it correctly — a crash-analysis runbook and a quick-start guide for the same feature belong in the same group even if their filenames don't share a prefix.
- Typical groups, adapt to what the repo actually has: getting started (quickstart/setup/configuration), architecture/reference, usage, deployment, specialized ops runbooks (e.g. red-team, incident-response), hardening/governance/compliance, planning/roadmap docs.
- Number groups in the order a new reader should hit them (getting started first, planning/roadmap last), and number files within a group in reading order.
- Filenames: lowercase, hyphenated, `x.y-short-title.md` — e.g. `1.1-quickstart.md`, `2.3-base-sensor-capabilities.md`. Keep the title short enough that the filename stays legible in a directory listing.

Rename with `git mv` one at a time (or chained) so each becomes a tracked rename, not a delete+add.

### 4. Rewrite every cross-reference

This is the step most likely to be done incompletely — do it exhaustively, not just for the files you remember linking.

- Grep the **whole repo** (not just `docs/`) for every old filename, both bare (`FOO.md`) and inside markdown link syntax (`[text](path/FOO.md)`), including README files in subfolders that mention top-level docs informally (e.g. a table listing "see ARCHITECTURE.md").
- Update the **link target** to the new path and, separately, consider whether the **link text** should also change — `[QUICKSTART.md](docs/1.1-quickstart.md)` reads oddly once the file is renamed; prefer `[1.1-quickstart.md](docs/1.1-quickstart.md)` or a descriptive label, consistently.
- Update ASCII directory-tree diagrams in `README.md` (and any architecture doc that draws one) to show the new filenames — these are easy to miss because they're not real markdown links.
- Check docs for self-references ("(this file)") and sibling references between docs that moved together — both sides of the link need the new name.
- After editing, re-grep for every old filename across the whole repo (`.md`, `.yml`, `.yaml`, and any doc-generation config) and confirm zero hits before moving on. Treat any remaining hit as a bug in this step, not an acceptable leftover.

### 5. Verify and ship

- `git status --porcelain` should show clean renames (`R`) for moved/renamed files and `M` for files whose links were edited, plus any genuinely new file (e.g. a doc that was untracked before consolidation).
- Stage, commit with a message describing the grouping scheme (not just "moved files"), and push to the working branch.
- Follow the repo's own PR process if one exists (open a PR rather than pushing to main/master).

## Pitfalls seen in practice

- Blanket find-and-replace on a bare filename (no path, no link syntax) can over-match: a phrase like `MITIGATION_CHECKLIST.md Tier 1` in prose needs the same substitution as a real link, but double-check the replacement didn't land inside a sentence awkwardly.
- Files describing a *different* project's structure (e.g. a refactor-plan doc that lists `README.md`/`STRUCTURE.md` as part of a proposed layout for a separate sub-package) can contain filenames that look like repo docs but aren't — read the surrounding context before rewriting.
- Dead links that already existed before the restructure (a doc referencing a file that was never created) are not this skill's problem to fix — just don't let the rewrite pass silently "fix" them into pointing at an unrelated real file of a similar name.
