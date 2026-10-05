---
name: setup
user-invocable: true
description: Bootstrap or repair the skill-concierge engine from scratch. Use this skill when installing skill-concierge on a new machine, right after a plugin update, or when skill-concierge:doctor reports the engine venv is missing. Runs setup.sh to build the stable engine venv, start the local index owner, build the multilingual index, and apply the curated skill-budget overrides, then verifies the result with doctor.
license: MIT
metadata:
  version: 0.1.1
next-skills: skill-concierge:doctor
---

# skill-concierge setup

First-time bootstrap (and post-update refresh) for the vendored skill-search engine.
`setup.sh` is idempotent — safe to re-run any time.

## Prerequisites

- **Python 3.10–3.12** on `PATH` (or set `SKILL_PYTHON=/path/to/python3.12`).
No Docker: the vector store is the local index owner (`python -m skill_search.index_owner`
from the venv, one SQLite file), which `setup.sh` starts itself.

If Python is missing, tell the user and stop — `setup.sh` cannot proceed without it.

## Steps

1. **Run the bootstrap** from the plugin root:

   ```bash
   bash "$CLAUDE_PLUGIN_ROOT/setup.sh"
   ```

   (When working from a git clone instead, `cd` into the repo and run `./setup.sh`.)
   It performs four idempotent steps: stable venv + deps → (re)start the index owner → build/refresh
   the index (discovers skills from BOTH Claude Code and Codex directories, ADR-0033) and the
   actionability-gate corpus → apply curated overrides to `~/.claude/settings.json`
   (backed up first; Claude Code only — a harmless no-op when run from Codex).
   Setup never builds the keep-off map: it is consent-only ([ADR-0077](../../docs/adr/0077-keep-off-map-is-consent-only.md)).

2. **De-duplicate** any prior user-scope MCP so only the bundled one runs:

   ```bash
   claude mcp remove skill-search -s user
   ```

3. **Restart Claude Code** so the MCP server and the settings overrides take effect.

4. **Verify** the install:

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/doctor.py"
   ```

   Expect `status: OK`. In Claude Code, `/mcp` should list `skill-concierge:skill-search`
   as connected. If anything is degraded, hand off to the `skill-concierge:doctor` skill.

## When to re-run

- After **any plugin update** (`/plugin marketplace update` + reinstall) — refreshes the
  engine copy in the stable venv and rebuilds the index.
- When the owner's index file (`~/.cache/skill-search/index.sqlite`) or the venv was wiped.

## Notes

- The venv lives at `~/.claude/skill-concierge/venv` (outside the plugin cache, so it
  survives reinstalls — ADR-0004). Override with `SKILL_CONCIERGE_VENV`.
- `setup.sh` reads the embedder + store URL from `.mcp.json` so the built index can never
  diverge from the model the live MCP uses.
