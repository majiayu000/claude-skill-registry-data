---
name: init-rules
description: 'Installs coding rules per project or globally, fitted to the stack it reads itself. Use when the user wants the same habits in a project or every session ("init rules", "install rules", "onboard project"). Not for Obsidian vaults (use obsidian-init).'
argument-hint: '[project|global] [--target=rules|claudemd] [--force] [--uninstall]'
allowed-tools: Read, Write, Edit, Bash(git rev-parse *), Bash(git check-ignore *), Bash(mkdir *), Bash(date *), Bash(test *), Bash([ *), Bash(command -v *), Bash(jq *), Bash(dirname *), Bash(printf *), Bash(mv *), Bash(rm *), Glob, Grep, AskUserQuestion
---

# Init Rules

## Overview

Install curated development rules based on detected project context. Two delivery modes:

- `--target=rules` (default) — write rule files into `.claude/rules/` (project) or `<CONFIG_DIR>/rules/` (global). Files with `paths:` frontmatter stay path-scoped.
- `--target=claudemd` — inject rule content directly into `./CLAUDE.md` (project) or `<CONFIG_DIR>/CLAUDE.md` (global), wrapped in sentinel blocks for idempotent re-runs and clean uninstall.

Personal preference groups install only when the user picks them, and so does the Delegation group, which routes web research, wide searches and docs writing to specialised agents. Every install also proposes a few settings entries that Claude Code enforces on its own (ask before `git push`, deny `.env` reads, a pre-commit Stop hook, attribution off). Re-runs also clean up stale content: rules this skill has retired, installs from older versions, and hand-written CLAUDE.md copies of retired or rewritten sections. One approval gate covers all of it together with the settings.

## When to Use

Installing, refreshing or uninstalling curated development rules for one project or globally, as rule files or CLAUDE.md blocks.

### When NOT to use

- Setting up an Obsidian vault rather than a code repo's rules — use `obsidian-init` (mz-knowledge).
- The user wants to edit rule content itself — open the rule file directly.
- The user wants per-file rule scoping — use `--target=rules`; claudemd mode cannot path-scope.
- The target directory or CLAUDE.md is managed by another tool and should not be touched.

## Arguments

- `project` (default) → scope to working directory
- `global` → scope to `<CONFIG_DIR>` (`~/.claude/` unless `CLAUDE_CONFIG_DIR` is set)
- `--target=rules` (default) → write as individual rule files
- `--target=claudemd` → inject into CLAUDE.md with sentinel blocks
- `--force` → overwrite existing rule files / replace existing sentinel blocks, including unmarked legacy files from older installs
- `--uninstall` → remove rules previously installed by this skill (mode-aware) and the settings entries it adds, exact matches only

Parse from `$ARGUMENTS`. Unknown or conflicting tokens → AskUserQuestion; never guess.

## Constants

- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **CONFIG_DIR**: resolved once in setup with `printf '%s\n' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"`. Claude Code reads user rules, the user CLAUDE.md and user settings from there, so global scope writes all three under it.

Phase files write `<SKILL_DIR>`, `<PLUGIN_ROOT>`, `<PROJECT_ROOT>` and `<CONFIG_DIR>` because they get no variable substitution when read. Replace each with the absolute path above before reading a file or running a Bash command.

## Core Process

### Phase Overview

| Phase | Goal                                    | Details                                         |
| ----- | --------------------------------------- | ----------------------------------------------- |
| 0     | Setup                                   | Inline below                                    |
| 1     | Select, approve, and apply rule changes | `phases/run.md`                                 |
| 1     | Plan and apply settings entries         | `phases/enforce.md`, from run.md Steps 5 and 7d |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below. Resolve `CONFIG_DIR` the same way.
1. Parse `$ARGUMENTS`: scope (`project`/`global`), target (`rules`/`claudemd`), `--force`, `--uninstall`. Unknown token → AskUserQuestion.
1. `task_name` = `<YYYY_MM_DD>_init_rules_<scope>_<target>` where `<YYYY_MM_DD>` is today's date (underscores); on same-day collision append `_v2`, `_v3`.
1. Create `<TASK_DIR><task_name>/`.
1. Write `state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO>`, `phase_complete: false`, `what_remains: []`, `Scope: <project|global>`, `Target: <rules|claudemd>`, `Force: <bool>`, `Uninstall: <bool>`, `DetectedContexts: []`, `AgentsMd: n/a`, `PersonalGroups: []`, `Delegation: skip`, `Installed: []`, `Replaced: []`, `Upgraded: []`, `Skipped: []`, `Removed: []`, `Retired: []`, `HandRemoved: []`, `SettingsAdded: []`, `SettingsRemoved: []`. `schema_version: 2` is the first line of the file.
1. Emit setup block: task_name, resolved target path, mode flags.

Every run, in both modes and for uninstall, passes the single approval gate in Phase 1 Step 6 before its first write. That one confirmation covers every write in the run.

Read `phases/run.md` and proceed to Phase 1.

## References

- `${CLAUDE_SKILL_DIR}/references/retired.md`: the retired rule ids and the renamed or rewritten CLAUDE.md sections that the stale scan looks for. Read it in full in Phase 1 Step 5 on install, and again in Step 7c on uninstall before deleting rule files.

## Error Handling

- **Empty / ambiguous argument** → AskUserQuestion; never guess.
- **Missing tooling** — if `<SKILL_DIR>` is still a literal `${...}` token or the bundled `rules/` directory is not readable, AskUserQuestion with the failing path.
- **No detected contexts** → still install universal rules; if target not writable, retry once then AskUserQuestion.
- **CLAUDE.md unreadable or unwritable** → AskUserQuestion with the exact path and error; do not fall back silently.
- **Project loads AGENTS.md and claudemd mode would create CLAUDE.md** → Phase 1 Step 1 asks first, because the new file would stop AGENTS.md from loading.
- **Duplicate sentinel IDs found in CLAUDE.md** (manual edit or prior bug) → stop, report the conflicting lines, ask the user to resolve before re-running.
- **Plugin version unreadable** → use literal `unknown` for the version tag and note it in the report.
- **Settings file is not valid JSON** → AskUserQuestion with the path and jq's message; never overwrite it.
- **`jq` not installed** → skip the settings step, say so in the plan, and print the settings fragment in the report for manual use.
- Never guess — any ambiguity escalates via AskUserQuestion rather than silent overwrite or skip.

## State Management

After each phase, update `<TASK_DIR><task_name>/state.md` with:

- `Status:` `pending` | `running` | `blocked` | `complete` | `aborted_by_user` | `failed`
- `Phase:` current phase number
- `DetectedContexts:` list of detected language/tooling tags
- `AgentsMd:` the AGENTS.md guard answer from Phase 1 Step 1 (`import`, `rules`, `claudemd-only`, or `n/a`)
- `PersonalGroups:` personal groups chosen in Phase 1 Step 4
- `Delegation:` the Delegation group answer from Phase 1 Step 4 (`install`, `installed` or `skip`)
- `Installed:` / `Replaced:` / `Upgraded:` / `Skipped:` / `Removed:` / `Retired:` filenames or rule ids touched in this run
- `HandRemoved:` headings of hand-written CLAUDE.md sections removed by the stale scan
- `SettingsAdded:` / `SettingsRemoved:` settings entries written or removed
- `Excluded:` paths appended to `.git/info/exclude` (`.mz/`, `.claude/settings.local.json`)

Never rely on conversation memory for cross-phase state — context compaction destroys specific paths and decisions.

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
