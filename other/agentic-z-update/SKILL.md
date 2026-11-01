---
name: agentic-z-update
description: "Pulls the latest Agentic-Z template files (agents, skills, docs) from upstream into this clone and commits them, leaving workspace/ mod work untouched. Use when the user asks to update Agentic-Z or pull template improvements, or when the SessionStart nudge says upstream is ahead."
argument-hint: "[--check [--quiet]] [--yes] [--per-file] [--force] [--dry-run] [--no-sync]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\<other>\`.

# /agentic-z-update

Pull template improvements (agents, skills, conventions, docs) from upstream `DayZ-n-Chill/Agentic-Z`'s `main` branch into the current clone. Three guarantees:

1. **`workspace/` mod work is never touched.** All changes are limited to template-managed paths.
2. **Local customizations to template files are not overwritten silently.** A three-way per-file classification (local file, file at the baseline, upstream file) detects when both the clone and upstream edited the same file and leaves it alone unless the user picks "take" in `--per-file` mode. File contents are never merged: each file is either kept or replaced whole.
3. **No two updates can apply at once.** A PID-based lock covers the first-run baseline write and the apply phase (checkout, delete, commit, baseline write); previews and `--check` do not take it. The lock file is created atomically with its content already in it, so two runs that start together cannot both get it. A lock left by a dead process is taken over under a short-lived second lock (`.claude/.upstream-update.lock.takeover`), and the stale lock is removed only if it is still the one that was judged stale, so two runs that find the same dead lock cannot both end up holding it.

The first run records the commit your clone was made from (the merge base with upstream main) as the baseline, so changes upstream made since you cloned are offered; with no shared history it records upstream HEAD and adds nothing. A template file that is in the baseline but missing locally is treated as one you deleted on purpose (`locally-deleted`): it is left alone and offered for restore in `--per-file`. Every later run compares the local file, the file at the baseline and upstream's current file to decide what to do per file. The comparison uses git blob ids, with the local file hashed through the clone's line-ending settings (`git hash-object --stdin-paths`, which applies the same filters as `git add`), so a CRLF checkout under `core.autocrlf=true` is not mistaken for a local edit. The ids come from one `git ls-tree` per revision and one `git hash-object` for the working tree, so the check costs the same handful of git calls whether 3 or 500 files drifted. The script works from the repo root (`git rev-parse --show-toplevel`), so it can be started from any subfolder.

## How to run

```cmd
python "<skill-dir>\update.py" [--check] [--quiet] [--yes] [--per-file] [--force] [--dry-run] [--no-sync]
```

## Flags

| Flag | Behavior |
|---|---|
| (default) | Preview drift, prompt y/N, apply safe changes (conflicts left alone). When the only drift is `local-only-edit` or `locally-deleted` files, it lists them, says `Up to date.` and exits 0 without prompting (with `--per-file`, a `locally-deleted` file still gets the prompt so it can be restored) |
| `--check` | Preview only: fetches upstream (adding the upstream remote if it is missing) and writes no files; exits 1 if upstream changes are pending or no baseline exists yet, 0 if up to date (`local-only-edit` and `locally-deleted` files do not count) |
| `--quiet` | With `--check`: single-line output for hooks, and always exits 0 so the hook shows the line. Rejected without `--check` |
| `--yes` | Skip the confirmation prompt (CI / scripted use) |
| `--per-file` | Walk each conflict and `locally-deleted` file interactively: keep / take / diff / skip. Keep is a decision: the file stays yours and no longer holds the baseline back. Skip (also Enter, or no terminal) decides later: the file is offered again on the next run |
| `--force` | Override the dirty-tree check |
| `--dry-run` | Show preview, do not apply. With no baseline yet, previews against the baseline the first real run would record, without writing it |
| `--no-sync` | Skip the post-update `sync-skills` run (useful when Claude Code is the only agent CLI in use) |

## Automatic commit

When at least one file is applied, the skill stages exactly the applied paths and commits only those paths (`git commit --only`), so anything else you had staged stays staged and out of the commit. The path list goes to git on stdin (`--pathspec-from-file`) and is matched literally, so a large first update is not stopped by the Windows command-line length limit and a name with `*` or `[` in it matches only that file:

```
chore: pull Agentic-Z upstream (<first 8 chars of upstream SHA>)
```

It then records the upstream SHA in `.claude/.upstream-baseline`, but only when the commit succeeded and nothing upstream changed is still unapplied (a `conflict` or `deleted-conflict` that was skipped or never walked, or a file whose checkout or delete failed; `local-only-edit` and `locally-deleted` files, and conflicts you chose to keep in `--per-file`, do not hold it back). Otherwise the baseline stays put and the next run offers those files again. If `git commit` fails (for example, a pre-commit hook rejects it), the changes stay staged, the skill prints a warning and exits 1; nothing is rolled back. Unresolved conflicts are never part of the commit. Tell the user about this commit when reporting results.

## Per-file status meanings

| Status | What it means | Default action |
|---|---|---|
| `unchanged` | Local file matches upstream | nothing |
| `safe-overwrite` | Not edited locally, upstream changed it | apply upstream |
| `new` | Upstream has it, the baseline and the clone do not | apply upstream |
| `locally-deleted` | In the baseline, missing in the clone, and once committed in the clone (you deleted it) | leave alone (`--per-file` take restores it) |
| `local-only-edit` | Only the clone edited it (upstream unchanged) | leave alone |
| `conflict` | Both the clone and upstream edited it | leave alone (use `--per-file` to resolve) |
| `deleted-clean` | Upstream removed it, not customized locally | delete |
| `deleted-conflict` | Upstream removed it, customized locally | leave alone |

## What gets updated

Template-managed paths only:

```
agents/
skills/
.claude/agents/
.claude/skills/
.claude/mcp/
.claude/settings.json
.claude-plugin/
.mcp.json
hooks/
mods/
evals/
docs/
scripts/
.claude/CLAUDE.md
AGENTS.md
GEMINI.md
README.md
.gitignore
pytest.ini
.env.example
package.json
package-lock.json
.github/
CONTRIBUTING.md
LICENSE
.markdownlint.json
.markdownlint-cli2.jsonc
.markdownlintignore
```

What stays untouched:

```
workspace/                  # in-progress mods
output/                     # one-shot deliverables
.claude/local-memory/       # gitignored, per-clone notes
.claude/settings.local.json # local Claude Code settings
.env                        # gitignored API keys
```

## When to run

- After a new Agentic-Z release.
- When a new agent or skill has shipped upstream.
- Periodically (monthly is fine).

## When not to run

- Mid-merge, mid-rebase, mid-cherry-pick or mid-revert (it refuses; finish or abort first).
- With uncommitted changes to tracked template files (it refuses; commit first, or pass `--force`). Untracked files, such as a skill you just added, do not block it.
- On a fork that has diverged heavily from upstream main (manual cherry-pick is safer).

## Files this skill creates

- `.claude/.upstream-baseline` — upstream SHA of the last completed update. Gitignored.
- `.claude/.upstream-update.lock` — concurrency lock during apply phase. Gitignored.
- `.claude/.upstream-update.lock.takeover` — held for a moment while a stale lock is replaced, then removed. Gitignored.

## SessionStart hook

A `SessionStart` hook runs `update.py --check --quiet` at the start of every Claude Code session in this repo. It prints a one-line nudge if upstream is ahead, if a newer prebuilt search index is available, or if no baseline has been recorded yet (run `/agentic-z-update` once to record it). Silent on no-change. The hook has a 20 second timeout, which leaves room for the `git fetch` plus the 5 second GitHub release check on a slow network; the drift check itself takes well under a second even with hundreds of files behind. It always exits 0: Claude Code drops plain output from a hook that exits non-zero, so a failing exit code would hide the nudge. Configured in `.claude/settings.json`.

To disable temporarily: comment out the `SessionStart` block in `.claude/settings.json`.

## Search index notification

If `/dayz-search-download` was run before, this skill also checks whether the installed GitHub release of the search index has been superseded. The check is read-only and never downloads; it only suggests running `/dayz-search-download`.

To skip the check: ensure `~/.claude/dayz-search-index/release-tag.txt` doesn't exist (the check is silent when no installed tag is recorded).

## After updating

- Restart the agent CLIs (Claude Code, Codex, Gemini) so they pick up new agents and skills.
- Run `/dayz-preflight` to confirm the environment still works.

## Refuse rules (exit 1)

- Not a git repo: "Run from inside an Agentic-Z clone." With `--check --quiet` this prints that one line and exits 0, so the hook shows it.
- Uncommitted changes to tracked files in template paths (skipped with `--force`, and not checked by `--check`). Untracked files are ignored: the update leaves a file only you have alone, and treats one at a path upstream adds as a conflict. Nothing is fetched or changed.
- A merge, rebase, cherry-pick or revert is in progress (checked even with `--force`; not checked by `--check` or `--dry-run`, which write nothing). Its commit would fail and leave the applied files staged inside your operation, so nothing is fetched or changed.
- The `upstream` remote points somewhere else: prints the `git remote set-url` fix. With `--check --quiet` the fix is one line and the exit is 0.
- `git fetch` fails (with `--check --quiet` this exits 0 silently so the hook stays quiet).
- Non-interactive shell at the confirmation prompt without `--yes`.
- `git commit` of the applied files fails (changes left staged, baseline not moved).
