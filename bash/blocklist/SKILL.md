---
name: blocklist
user-invocable: true
description: Manage skill-concierge's DISABLE list — skills the user ordered off, regardless of origin (personal, plugin, external catalog, or command-files surfaced as skills). Use this skill when the user wants to view, disable, block, or re-enable a skill, says "disable X", "block X", "stop using/offering X", "X is turned off", "re-enable/unblock X", "which skills are disabled", or asks why a Skill invocation was denied by the blocklist guard. Runs scripts/blocklist.py (list / add / remove); the blocklist lives under the canonical durable home (~/.claude/skill-concierge/blocklist.json) and is enforced by the enforcer (no offers/hints/routes), the engine (no search hits, get_skill refuses), and the PreToolUse guard (invocation denied) — ADR-0046.
argument-hint: "[list | add <skill> | remove <skill>]"
license: MIT
metadata:
  version: 0.1.0
---

# skill-concierge blocklist

The **disable tier**: skills the user ordered OFF. A skill on the blocklist is
never offered by the enforcer, never returned by `search_skills`, never served
by `get_skill`, and its Skill-tool invocation is **denied** by the PreToolUse
guard (`hooks/scripts/skill_guard.py`). This works for ANY skill regardless of
origin — personal skills, plugin skills, external catalog entries, and
command-files surfaced as skills (`~/.claude/commands/*.md`), which the index
deliberately excludes (ADR-0001) and which therefore only the invocation guard
can catch.

The list lives at `~/.claude/skill-concierge/blocklist.json` (canonical durable
home, preserved across `/plugin update`) and is read LIVE at query time — an
edit applies immediately, with no reindex and no restart.

## Name semantics

- A **BARE** entry (`resume-session`) blocks every qualified twin —
  `plugin:name`, `alias:name`, any origin. "Disable X" means X, everywhere.
- A **QUALIFIED** entry (`skill-concierge:keep-on`) blocks only that exact form —
  for when one origin must die but a same-named sibling must live.

## Steps

1. **View the disabled set:**

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/blocklist.py" list
   ```

2. **Disable skill(s)** — reconciles the settings overrides immediately (a
   disabled skill is force-demoted from keep-on to name-only; `keep-on.json`
   itself is left untouched, so unblocking restores the allowlist):

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/blocklist.py" add <skill-name> [<skill-name> ...]
   ```

3. **Re-enable skill(s):**

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/blocklist.py" remove <skill-name> [<skill-name> ...]
   ```

## Layer map (what "disabled" means, mechanically)

| Layer | Effect |
|---|---|
| Enforcer (`hooks/scripts/enforcer.py`) | never offered, never hinted (CHAIN-HINT/ROUTE), never a deterministic route, no foreign-annex row |
| Engine (`vendor/skill-search/.../server.py`) | filtered from `search_skills` results; `get_skill` refuses to serve the body |
| Guard (`hooks/scripts/skill_guard.py`) | PreToolUse(Skill) **deny** — the deterministic layer that also catches command-files |
| Overrides (`scripts/apply-overrides.py`) | a blocked keep-on skill is forced name-only |

## Escape hatch

`SKILL_BLOCKLIST=0` turns the whole feature off everywhere (guard passes,
enforcer and engine stop filtering, overrides stop stripping) — the one-var
revert. `SKILL_CONCIERGE_BLOCKLIST` points all layers at an exact file (test
seam).
