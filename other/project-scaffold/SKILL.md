---
name: project-scaffold
description: Lay down a standard set of empty project docs (CLAUDE, PURPOSE, RULES, GUARDRAILS, CONVENTIONS, DECISIONS, DOCS, CHANGELOG, MAP). Use when the operator says "scaffold this project" or "add the standard docs".
---

# project-scaffold

Runs `cut-project.sh --generic` to lay down empty, well-formed project docs.
It only copies templates. It never fills them and never overwrites a file that
already exists and differs. To also fill them from a project description, use `project-bootstrap`.

## Files

- Core, always: `CLAUDE.md`, `PURPOSE.md`, `RULES.md`, `GUARDRAILS.md`, `CONVENTIONS.md`, `DECISIONS.md`, `DOCS.md`, `CHANGELOG.md`, `MAP.md` (generated), `scripts/map.py`.
- Optional, only when asked: `design`, `agents`, `logs`, `humans`, `context`, `calculations`, `assumptions`, `learnings`, `memory` (each becomes `<NAME>.md`).

## Steps

1. Confirm the target directory with the operator. Default is the current directory; it may be new or hold an existing project.
2. Ask which optional files they want, if any. Do not assume. Name the nine and say that none is the default.
3. Find the script: `project-factory/scripts/cut-project.sh`, which sits beside the `skills/` directory this skill lives in (resolve symlinks first, e.g. `cd -P <this skill dir>/../..`). If it is not there, ask the operator for the path.
4. Run it, adding `--with design,humans` (comma list) or `--all-optional` only as chosen:

   ```bash
   bash <project-factory>/scripts/cut-project.sh --generic [--with a,b | --all-optional] <target-dir>
   ```

5. Report from its output:
   - Created: each `wrote:` line.
   - Skipped: each `SKIPPED` line, meaning the file exists and differs; say it was left untouched.
   - Unchanged: the `unchanged:` count (a re-run is a clean no-op).
   - Any `warning:` or `note:` line (for example `MAP.md` not generated), verbatim.
6. Tell the operator the files hold `<fill: ...>` markers and are not usable until filled. Do not fill them here. Do not edit a skipped file.

## Rules

- Never overwrite, merge into or delete an existing file. A differing file is the operator's to reconcile.
- Never run in a directory the operator has not named.
- To regenerate the map later: `python3 scripts/map.py` in the target.
