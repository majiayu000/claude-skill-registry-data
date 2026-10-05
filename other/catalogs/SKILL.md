---
name: catalogs
user-invocable: true
description: Manage external skill-catalog roots — third-party skill collections indexed for retrieval WITHOUT being installed (ADR-0031). Use this skill when the user wants to register, list, or remove an external skills directory ("add my cloned skills repo to search", "index this skill collection without installing it", "which external catalogs are configured"), promote an external skill into ~/.claude/skills, or asks why a search hit is marked "[external]". Runs scripts/catalogs.py (list / add / remove / promote), which edits the operator-owned ~/.claude/skill-concierge/catalog-roots.json; the index follows at the next reindex.
argument-hint: "[list | add <alias> <path> | remove <alias> | promote <alias>:<skill>]"
license: MIT
metadata:
  version: 0.1.0
---

# skill-concierge catalogs

Register **external catalog roots** — local directories of third-party skills (each
child dir carrying a `SKILL.md`, e.g. a cloned awesome-skills repo) that get indexed
for semantic retrieval **without being installed**: they never appear in Claude Code's
per-turn context and never enter the per-turn offer preview (search-only tier). Their
skills index as `<alias>:<dirname>` and surface only via `search_skills`, marked
`[external: <alias>]`.

**Consumption:** an external skill cannot be invoked by the Skill tool. `USING:` one
means pulling its body with `get_skill("<alias>:<name>")` and following that SKILL.md
inline. For a proven keeper, `promote` symlinks it into `~/.claude/skills/` and it
becomes a normal installed skill (with the normal per-turn context cost).

## Steps

1. **View configured catalogs** (paths, skill counts, broken promotions):

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/catalogs.py" list
   ```

2. **Register a catalog root** (alias must be `[a-z0-9][a-z0-9_-]*`; optional
   include/exclude globs match skill DIRECTORY names):

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/catalogs.py" add <alias> <path> \
       [--include 'glob' ...] [--exclude 'glob' ...]
   ```

3. **Remove a catalog** — its `catalog:<alias>` points prune at the next reindex:

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/catalogs.py" remove <alias>
   ```

4. **Promote a proven external skill** into `~/.claude/skills/` (symlink, bare name;
   refuses on name collision):

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/catalogs.py" promote <alias>:<skill>
   ```

5. **Land the index change now** (otherwise the session-start auto-reindex catches it):
   call the `reindex()` MCP tool, or report to the user that the next session start
   will pick it up.

## Notes

- Config lives at `~/.claude/skill-concierge/catalog-roots.json` (operator-owned
  durable home; survives plugin updates; env seam `SKILL_CONCIERGE_CATALOG_ROOTS`).
  Absent file = feature off, byte-identical behavior.
- External skills get embeddings + body-derived triggers only; the flywheel utterance
  layer deliberately skips them (deferred phase, ADR-0031).
- Telemetry: `get_skill` pulls are ledgered; `analyze.py` reports external takes
  (epoch-scoped — window from the catalog's registration date).
- First registered catalog on this machine: `antigravity` →
  `/Users/thinhkhuat/env-DEV/antigravity-awesome-skills/skills` (2026-08-23).
