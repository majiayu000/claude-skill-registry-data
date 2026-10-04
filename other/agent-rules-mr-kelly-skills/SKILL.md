---
name: agent-rules
license: MIT
description: Align all AI coding agents to a single source of truth. AGENTS.md for rules, .agents/skills/ for skills, symlinks for everything else. Use when setting up a repo for multiple agents, or when links are missing, broken, or out of date.
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
user-invocable: true
metadata:
  category: platform
  tags:
    - risk:local-write
---

# Agent Rules - Single Source of Truth

Every AI coding agent reads its own rules file and its own skills directory. This
skill keeps one real copy of each and points the rest at it with symlinks.

## Quick Start

```bash
/agent-rules                    # create or repair links in the current project
/agent-rules --check            # verify; exits 1 when something is broken
/agent-rules --status           # report only, never fails
/agent-rules --minimal          # skip links agents no longer need
/agent-rules --root <path>      # operate on a project other than $PWD
```

The target project is the git toplevel of your working directory (or `$PWD`
outside a repo), **not** wherever this skill happens to be installed.

## Single Source of Truth

Two sources, edited by hand:

1. **Rules** — `AGENTS.md` at the project root
2. **Skills** — `.agents/skills/<skill-name>/SKILL.md`

Everything else is a symlink into those two.

```
AGENTS.md                         ← edit rules here
.agents/skills/                   ← edit skills here

↓ symlinks ↓

CLAUDE.md                       → AGENTS.md
.gemini/GEMINI.md               → ../AGENTS.md
.github/copilot-instructions.md → ../AGENTS.md      (legacy)
.cursor/rules/main.md           → ../../AGENTS.md   (legacy)
.kiro/steering/main.md          → ../../AGENTS.md   (legacy)

.claude/skills/                 → ../.agents/skills
.kiro/skills/                   → ../.agents/skills
.github/skills/                 → ../.agents/skills (legacy)
.codex/skills/                  → ../.agents/skills (legacy)
```

## Agent Support

`.agents/skills/` and `AGENTS.md` are now read natively by several agents, so
some links exist purely for older versions. `--check` treats a missing **legacy**
link as a warning and a missing **required** link as an error.

| Agent | Rules | Skills | Tier |
|-------|-------|--------|------|
| Claude Code | `CLAUDE.md` → | `.claude/skills/` → | **required** — reads neither `AGENTS.md` nor `.agents/skills` |
| Gemini CLI | `.gemini/GEMINI.md` → | N/A | **required** — `AGENTS.md` only via `context.fileName` in settings.json |
| Kiro | `.kiro/steering/main.md` → | `.kiro/skills/` → | skills **required**; rules legacy (reads root `AGENTS.md`) |
| GitHub Copilot | `.github/copilot-instructions.md` → | `.github/skills/` → | legacy — reads `AGENTS.md` and `.agents/skills` natively |
| OpenAI Codex | `AGENTS.md` | `.codex/skills/` → | legacy — scans `.agents/skills` from CWD up to the repo root |
| Cursor | `.cursor/rules/main.md` → | N/A | legacy — reads `AGENTS.md` natively |

*Verified against vendor documentation on 2026-09-07. Run `--status` to see which
links a project still carries.*

Known quirk: some Kiro builds do not follow a symlinked steering file. If Kiro
ignores your rules, replace `.kiro/steering/main.md` with a real copy.

## Usage

```bash
vim AGENTS.md                    # edit rules once, every agent sees it

mkdir -p .agents/skills/my-skill # add a skill once, every agent sees it
vim .agents/skills/my-skill/SKILL.md
```

## Critical Rules

1. ✅ **Only edit `AGENTS.md`** — single source for rules
2. ✅ **Only edit `.agents/skills/`** — single source for skills
3. ❌ **Never edit a symlinked file** — you are editing the source through a
   confusing alias
4. ❌ **Never copy instead of linking** — copies drift

## Safety

- Existing real files are never overwritten. If `CLAUDE.md` holds hand-written
  content, it is left alone and reported; `--force` moves it to `CLAUDE.md.bak`
  first. (An exact copy of `AGENTS.md` is replaced silently — nothing is lost.)
- Missing parent directories are created.
- Re-running is idempotent.
- On Windows, symlinks need `git config core.symlinks true`; `--check` warns when
  the repo is configured otherwise.

## What About MCP Configs?

**Not symlinked.** Formats differ (`.json` vs `.toml`), settings are
agent-specific, and the files may hold API keys.

- Claude: `.claude/mcp.json` · Kiro: `.kiro/mcp.json` · Cursor: `.cursor/mcp.json` · Codex: `.codex/config.toml`

Sync them manually if you need to.

## Scripts

- `scripts/agent-rules.sh` — entry point (`--check` / `--status` / `--fix`)
- `scripts/create-symlinks.sh` — create and repair links
- `scripts/verify-architecture.sh` — verify; exit code reflects the result
- `scripts/lib.sh` — shared link table used by all three
- `scripts/test-agent-rules.sh` — self-test (`bash scripts/test-agent-rules.sh`)

Each script runs standalone and works on whichever project you are standing in.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Link broken or pointing elsewhere | `/agent-rules` |
| A stray `skills` entry inside `.agents/skills/` | `/agent-rules` removes it (planted by v4) |
| `--check` fails on a link you do not want | `--minimal` layout, or drop the agent from `scripts/lib.sh` |
| Agent still cannot see a skill | confirm `.agents/skills/<name>/SKILL.md` exists |

---

**Version**: 5.0
**Last Updated**: 2026-09-07

Changes since 4.0:
- Target project resolved from your working directory instead of the skill's
  install path — `--check` used to inspect the wrong directory whenever the skill
  was not vendored into the project
- Parent directories are created, so bootstrapping an empty repo works
- Directory links use `ln -sfn`; re-running no longer plants a broken
  `.agents/skills/skills` link inside the source directory
- Verification exits non-zero on failure, and no longer demands that `agent-rules`
  itself be vendored into the project it checks
- Real files are never clobbered; `--force` backs them up
- Links are tiered required/legacy against what agents read natively today
