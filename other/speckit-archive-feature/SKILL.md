---
name: speckit-archive-feature
description: Archive the current feature directory under specs/archive/YYYY-MM-DD-{slug}/,
  update CHANGES.md, and close associated GitHub issues.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: archive:commands/speckit.archive.feature.md
---

# Archive Current Feature

Move the completed feature planning folder from `specs/{slug}/` to `specs/archive/YYYY-MM-DD-{slug}/` using `git mv`, update (or create) `CHANGES.md`, and close any GitHub issues recorded as `source_issue` in `.specify/feature.json`.

## Behavior

1. Parse arguments. Detect a leading `--force` / `-f` flag. Treat the next positional as the feature slug.
2. Resolve the feature directory from the current git branch (`specs/<branch>`), or from the argument if provided. Refuse if the path is already under `specs/archive/`.
3. Verify the feature is ready to archive (tasks.md exists and contains no unchecked `[ ]` items). If unchecked tasks remain, the script exits with status `2` and the list on stderr — see **Interactive confirmation** below. When `--force` was passed up front, log the count and proceed without prompting.
4. Derive archive date `YYYY-MM-DD` from today.
5. Append a `CHANGES.md` entry with the feature title (from `spec.md` H1) and a short summary. Create `CHANGES.md` in Keep-a-Changelog style if absent.
6. `git mv specs/{slug} specs/archive/{date}-{slug}` (creating the parent if needed).
7. If `gh` is available and `.specify/feature.json` has `source_issue`, run `gh issue close <N> -c "Archived in specs/archive/{date}-{slug}/"`.

The archive **can run as part of the feature's PR** — the PR does not have to be merged first. Tasks completion is the real readiness signal; PR merge state is enforced by the platform, not by this script.

## Execution

- **Bash**: `.specify/extensions/archive/scripts/bash/archive-feature.sh [--force] [feature_slug]`

When `feature_slug` is omitted, the script derives it from the current git branch. `--force` skips the unchecked-tasks gate; it does not bypass the "destination exists" or "already-archived" guards.

## Interactive confirmation

Archiving with unfinished tasks loses signal — the right default is to finish them first. When the user did **not** pass `--force` and the script exits with status `2` (unchecked tasks):

1. Show the unchecked-task list from the script's stderr to the user.
2. Recommend completing the open tasks before archiving. If any are clearly small or already done in the code, offer to finish them now.
3. Ask the user explicitly: **"Force archive with N unfinished tasks anyway?"** — present at least these options:
   - Finish the tasks first (default — abort the archive and return to the feature).
   - Force archive now (re-run the script with `--force`).
4. Only re-invoke the script with `--force` after an explicit "yes / force" from the user. Any other response (including silence or ambiguity) aborts the archive.

If the user passed `--force` on the original invocation, skip the prompt entirely — they've already consented.

## Changelog Conventions

The changelog update follows Keep a Changelog conventions (do-changelog style):

- Prefer `CHANGELOG.md`, fall back to `CHANGES.md` if it already exists. Create `CHANGELOG.md` in Keep a Changelog format if neither is present.
- Inspect the existing format before writing — match heading depth and date format.
- Group entries by type: **Added / Changed / Fixed / Removed / Security**. Archive entries are written under `### Changed`.
- Lead with user-visible impact; keep bullets short and specific.
- Do not invent version numbers or release dates — use the archive date `YYYY-MM-DD` as the section heading.

## Graceful Degradation

- If `gh` is missing or no `source_issue` is recorded, the archive still proceeds; issue-close is skipped with a notice.
- If `CHANGES.md` already has a section for today's date, the entry is appended under it rather than duplicating the header.
- If the destination path already exists, the script aborts without overwriting (even with `--force`).
- Unchecked tasks: script exits `2` with the list on stderr. The command layer prompts the user to finish them first or confirm a forced archive — see **Interactive confirmation**. Passing `--force` on the original invocation skips the prompt.