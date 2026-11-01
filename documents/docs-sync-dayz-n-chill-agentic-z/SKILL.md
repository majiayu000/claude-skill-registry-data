---
name: docs-sync
description: "Checks the React wiki (its own repo, cloned next to this one) against the source: agent and skill lists, the count claims listed in its claims table, and the grade tables, and fixes wrong counts in place with --apply. Use after adding, renaming or removing an agent or skill, after a grading round, after editing the DayZ rules files, or when the Stop hook reports wiki problems."
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\<other>\`.

# /docs-sync

Keep the wiki in line with the repository. The wiki lives in its own private repository, `DayZ-n-Chill/Agentic-Z-Wiki`. docs-sync reads it from `$AGENTIC_Z_WIKI` when that is set (empty means no wiki), else from a clone named `Agentic-Z-Wiki` next to this repo. With no wiki it prints `no wiki to check` and exits 0, and the Stop hook stays silent. Problems still name wiki files as `wiki/src/...`, meaning `src/...` in the wiki repo. The wiki is hand-written Markdown under `wiki/src/content/` (`guide.md`, `team.md`, `skills-table.md`) plus the home-page `STATS` in `wiki/src/App.jsx`. One pure-Python script checks it; no model is called. It works only from inside a clone of this repository: the script finds the wiki and the source folders relative to its own location, so a copy of the skill installed elsewhere (for example through a plugin) has nothing to check.

## When to run it

- After adding, renaming or removing a file in `agents/` (or changing an agent's `memory:` line or its `mcp__dayz-rag__` tools), a skill folder in `skills/` or `.claude/skills/` or a hook script in `hooks/`.
- After adding or removing a question file in `evals/questions/`.
- After a grading round changes `docs/grades/final_grades.json` or `docs/grades/final_grades_shared.json`.
- After editing `skills/_shared/dayz-conventions.md` or a topic file in `skills/_shared/conventions/`.
- After rewording or adding a wiki sentence that states a count (then update the claims table in `sync.py`).
- When the Stop hook reports wiki problems at the end of a session.

## How to run

**Check** (the default, writes nothing):

```cmd
python "<skill-dir>\sync.py" --check
```

Each problem prints as `wiki-file:line: what is wrong, expected value (where the value comes from)`. Problems marked `[fixable]` are counts that `--apply` can rewrite.

**Fix the counts in place**:

```cmd
python "<skill-dir>\sync.py" --apply
```

`--apply` rewrites only the numbers marked `[fixable]`, which are always numbers inside a matched claim from the claims table, and writes nothing else. It writes all the fixed files or none: every file is built before any is written, each write goes through a temporary file, and if a write fails or the run is stopped, the files already replaced are put back, so the wiki is never left half-fixed. Names, duplicate rows, wrong grades, claims not found and false "all A+" sentences stay reported for a hand edit.

A sentence whose claim says every graded item is A+ ("All {N} are at A+") is reported as `says every graded item is A+, but X of Y are; reword this sentence` once any item drops below A+, because no number makes it true. While that is reported, `--apply` leaves every other number in that sentence alone; wrong ones are still listed, without `[fixable]`. Reword the sentence in the wiki, then update its entry in the `CLAIMS` table in `sync.py` to the new wording (for example drop "All {N} are at A+", the `graded_total` fact for its `{N}` and the `all_aplus=True` flag), or the next run reports the claim as not found. Then run `--check` again.

`--apply` also exits 1 with one line in each of these cases:

- `stopped; nothing was written`: Ctrl+C before the first write, including during the check.
- `stopped; the wiki files were put back`: Ctrl+C between writes.
- `stopped after writing the fixes`: Ctrl+C once every write finished; the fixes stay.
- `could not read <file>` or `<file> changed since the check; run again`: nothing is written.
- `could not write the wiki: <reason>`: the replaced files are put back; if that also fails, a `could not put back <file>: <reason>` line follows for each such file.

**Preview what `--apply` would change** (writes nothing). Each change line gives the file, line and column, so two fixes on one line can be told apart:

```cmd
python "<skill-dir>\sync.py" --apply --dry-run
```

From a terminal, `scripts\dev\docs-sync.bat` runs the same script with the same arguments and exit codes (for example `scripts\dev\docs-sync.bat --check`), through `python` when it runs and the `py` launcher otherwise, so the Microsoft Store `python` alias, which is on PATH but is not Python, falls through to `py`.

**Show what each check compares**, with the current repository values:

```cmd
python "<skill-dir>\sync.py" --map
```

## What it checks

| Check | Wiki | Compared with |
|---|---|---|
| Names | The tables under `## Agents` in `guide.md`, and `skills-table.md` | `agents/*.md` and every `skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md` (folders whose name starts with an underscore, such as `_shared`, are skipped). Every one must be listed once, and nothing else. |
| Claims | Each entry in the `CLAIMS` table in `sync.py` | The repository fact named for each number in the claim (see below). |
| Grades | The "Quality by version" tables in `guide.md` and `team.md` | `docs/grades/final_grades.json` and `final_grades_shared.json`: every graded item has exactly one row, and the last column holds its latest grade. Row labels match after dropping backticks, a `Pack:` prefix and a trailing `(...)`; two grade items that match the same label are reported, so neither drops out of the check. |

### The claims table

The counts the wiki states are listed one by one in the `CLAIMS` table at the top of `sync.py`. Each entry gives the wiki file, the exact text of the claim with `{N}` where each number sits, and the fact each number must equal. Only the numbers inside these claims are read or rewritten; a number anywhere else in the wiki is never checked, so a sentence such as "the lead dispatches 3 agents in parallel" is left alone. A `{N}` matches digits or a number word from "zero" to "twenty" ("three hooks", "five topic files"); `--apply` writes a word back as a word.

To see every claim, run `--map`: it prints the full table from `CLAIMS`, with each claim's file, text and the current value of every fact. This file does not copy the list, so it cannot go out of date. The counts come from these sources: agent files are `agents/*.md`; skill folders are those in `skills/` and `.claude/skills/` with a `SKILL.md` (not starting with `_`); hook scripts are `hooks/*.py` other than `test_*.py`; the rules core is `skills/_shared/dayz-conventions.md` and the topic files are `skills/_shared/conventions/*.md`, counted as `wc -l` does.

A claim must be found in a section that `wiki/src/content.js` does not hide (its `HIDDEN` set); `App.jsx` has no sections and is read whole. If a claim's text is no longer found, for example because the sentence was reworded or deleted, the check reports `<file>: claim not found: "<text>"; update the CLAIMS table in sync.py`. That problem needs a hand edit: change the claim's text in `CLAIMS` to the new wording, or remove the entry if the wiki no longer makes the claim. When you add a count to the wiki, add its claim to `CLAIMS` as well, or it is not checked. A test in `test_docs_sync.py` scans the visible parts of `guide.md` and `team.md` for a number next to "agents", "skills", "hooks" or "items" and fails when one is outside every claim, unless its `NOT_FACTS` list names it as a count no fact computes (such as "five gate agents"). A count in a hidden section, such as the "Status and next steps" table in `team.md`, is not on the site and is not checked. If `content.js` has no `const HIDDEN = new Set([...])`, the run stops with an error instead of checking hidden sections. The names and grades checks read their tables wherever they sit, hidden or not.

The grade files' folder is the `GRADES_DIR` constant in `sync.py` (`docs/grades/`). Both grade files are committed and required: if either is missing, the run stops with a source error.

## Exit codes

| Code | Means |
|---|---|
| 0 | The wiki matches the source, `--apply` fixed every problem (or `--apply --dry-run` would), `--map` ran, or `--quiet` was set (the Stop hook never fails a session). |
| 1 | Something needs attention. The causes are listed below the table. |
| 2 | Usage error: `--dry-run` without `--apply`, more than one of `--check`, `--apply` and `--map`, or `--quiet` with `--apply` or `--map`. |

Exit code 1 means one of these:

- `--check` found problems.
- `--apply` left problems that need a hand edit.
- `--apply` could not read or write a wiki file, or found a wiki file changed since the check.
- The run was stopped with Ctrl+C (except under `--quiet`).
- The check failed in an unexpected way (one `check failed: <reason>` line).
- A wiki page is missing, not UTF-8 or not parsable.
- A grade file is missing, not UTF-8 or not parsable, or has a grade entry whose batch name does not start with `agents`, `skills` or `shared` (the counts would leave it out).
- A `content.js` has no `HIDDEN` set.
- A rules core or topic file is missing or cannot be read.
- An `agents/`, `evals/questions/`, `hooks/` or `conventions/` folder is missing, or has none of the files it is counted from: `*.md` agents, `*.json` question files, `*.py` hook scripts other than `test_*.py`, `*.md` topic files.

A missing or empty source is never counted as 0, so `--apply` writes nothing.

## Stop hook integration

The check is wired to Claude Code's Stop hook in `.claude/settings.json` as `scripts/dev/docs-sync.bat --check --quiet`. Going through the wrapper means the hook runs `sync.py` with `python` when it runs and the `py` launcher otherwise, so a machine where `python` is only the Microsoft Store alias still gets the check instead of a hook error. Claude Code only shows a command hook's output to the user through a `systemMessage` field in JSON, so under `--quiet` the script prints nothing when the wiki matches, and otherwise one JSON line that appears as a notice when Claude finishes a response:

```
{"systemMessage": "docs-sync: 11 wiki problem(s), 9 fixable with --apply. Run /docs-sync."}
```

If a source file is missing or broken, or the check fails in any other unexpected way, the notice says `docs-sync: check skipped: <reason>`. Under `--quiet` the exit code is always 0, as long as `python` or `py` can run the script. The hook never edits the wiki; you decide when to run `--apply`.
