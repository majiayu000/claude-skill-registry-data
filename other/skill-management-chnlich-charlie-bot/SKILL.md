---
name: skill-management
description: >
  CharlieBot skill directory layout, sync rules, and CLI tool mappings.
  Use when creating, installing, or syncing skills across Claude Code, Codex, Gemini, OpenCode, and Antigravity.
---

# Skill Management

## Skill Sources (canonical)

| Location | Scope | Description |
|----------|-------|-------------|
| `<charlie-bot-repo>/skills/` | General (shared across hosts) | Integration skills, self-knowledge |
| `$CHARLIEBOT_HOME/skills/` | Host-specific (per-machine) | Domain skills tied to local repos/hardware |

Shared and host-specific skills both sync into `~/.claude/skills/`.
`$CHARLIEBOT_HOME` holds host-specific skills, sessions, config, and credentials.
Claude Code auto-loads skills with `user-invocable: false` when they are relevant to the task.

## CLI Tool Skill Directories

| CLI Tool | User Skills Path | Shared Standard | Notes |
|----------|-----------------|-----------------|-------|
| **Claude Code** | `~/.claude/skills/<name>/SKILL.md` | Proprietary | Also reads `.claude/skills/` at project level |
| **Codex CLI** | `~/.agents/skills/<name>/SKILL.md` | Agent Skills (open standard) | `.system/` in `~/.codex/skills/` is Codex built-in; user skills go in `~/.agents/skills/` |
| **Gemini CLI** | `~/.gemini/skills/<name>/SKILL.md` OR `~/.agents/skills/<name>/SKILL.md` | Agent Skills (open standard) | `~/.agents/skills/` takes precedence over `~/.gemini/skills/` |
| **OpenCode** | scans `~/.claude/` and `~/.agents/` | reuses both standards | No dedicated target — auto-discovers Claude Code + Agent Skills. Disable via `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1` |
| **Antigravity (`agy`)** | `~/.gemini/antigravity-cli/skills/<name>/SKILL.md` | Agent Skills (open standard) | Global customizations root (also scans `~/.gemini/skills/`); does NOT read `~/.claude`/`~/.agents` |
| **charlie-code** | scans `~/.claude/skills/` and `~/.agents/skills/` | reuses both standards | No dedicated target. Also reads `.claude/skills/` and `.agents/skills/` at the git worktree root of its cwd; a repo skill wins a name collision. `--skills-root DIR` replaces the host roots for one run |

### Deduplication

Four sync targets cover all five CLIs:

1. `~/.claude/skills/` — Claude Code
2. `~/.agents/skills/` — Codex + Gemini (shared open standard)
3. `~/.gemini/antigravity-cli/skills/` — Antigravity (`agy`)
4. `$CHARLIEBOT_HOME/.claude/skills/` — Claude Code cwd-ancestor root. Claude Code collects `.claude/skills/` from every ancestor of its cwd up to `$HOME`, independent of the logged-in account, and a master session's cwd sits under `$CHARLIEBOT_HOME/`, so this one root reaches every Claude account's masters; the per-account config dirs get no target. The same file visible through two roots (this one and `~/.claude/skills/`) loads once.

OpenCode and charlie-code need **no** target: both auto-scan `~/.claude/skills/` and `~/.agents/skills/`, already populated above.

Outside `-n` runs and when `claude` is on `PATH`, a real sync fails if Claude reports no discovery count or its count
differs from target 4's symlink count.

## Sync Rules

- Each skill entry in target dirs is a **symlink** pointing to the canonical source
- Never overwrite non-symlink entries or dotfiles (e.g. Codex `.system/`)
- Remove stale symlinks whose targets no longer exist
- Sync script: `<charlie-bot-repo>/scripts/sync-skills.sh`
- Workers see skills through the backend CLI's skill dir — not directly from
  `$CHARLIEBOT_HOME/skills/`.

## Host-Specific Content Boundary

Repo-level shared files (`<charlie-bot-repo>/skills/**`, `<charlie-bot-repo>/prompts/**`) MUST NOT contain host-specific info — hostnames, local paths, GPU specs, per-host ports/IPs. Anything host-specific belongs in the memory store's `host` topic (`$CHARLIEBOT_HOME/memory/entries/host/`) or `$CHARLIEBOT_HOME/skills/<name>/`. Rules like "feature X is local-host only" must be flagged in the repo-level skill so that workers running anywhere see them.

Repo-level skills must also stay free of session-specific debug artifacts: dated transcripts (`observed in D4`, `2026-05-04 run`), internal task IDs, specific bug strings (`bytes-vs-str + train_ranges API mismatches`), or any phrasing that reads like a LESSONS.md entry. Workers loading shared skills cannot see `$CHARLIEBOT_HOME/LESSONS.md` and have no context for those references. Keep shared skills as static principles; only promote a finding into a shared skill once the debug is closed and the lesson rewrites cleanly as a generic rule.

`dev/git-hooks/pre-commit` checks staged files for host-specific identifiers.
Edit profile-home files in place; never stage, commit, or push them, even when `$CHARLIEBOT_HOME` is a git repository.

## Person-Identifying Session Content Boundary

Repo-level shared files also carry no material that identifies a real
person when read together with the repository's public authorship: names,
orders, preferences, schedules, or other session-derived personal data.
Examples in skills and docs are synthetic end to end, covering people,
items, and quantities alike, even when a real session supplies the
template. The authoring-time test: a reader who knows this repository's
owner learns nothing about any real person from the content.
dev/check-skills-host-leak.sh scans for host identifiers only, so
this boundary rides on the author's judgment; a skill drafted from a live
session applies the test to every example before it lands.

## File Name Convention

All CLIs require `SKILL.md` (exact name, case-sensitive) as the entry point file.

## Updating Existing Skills

When new lessons surface and a skill needs an update, follow these rules:

Before a subagent returns or a reviewer merges, the master skims its context or transcript for recurring pain points.
When a pattern is confirmed, update the relevant skill.

- **Reorganize, don't append.** If related content already lives in the skill, edit the existing section in place rather than tacking on a new paragraph. Skills must stay concise so they remain scannable; growing them by accretion (one new bullet per session) defeats the purpose. Re-read the whole skill first, then propose the smallest diff that captures the new lesson.
- **Ask before modifying any local skill.** Surface the intended edit to the user before writing it — never silently mutate a skill file, even when "just adding a clarifying line".
- **Always present the change as a file diff.** Show the actual before/after (or `Edit` patch) so the user can see surrounding context and judge whether the edit fits. Don't summarize the change as "I'd add a note about X" — the user needs to see the literal lines being added/changed/removed to approve.
