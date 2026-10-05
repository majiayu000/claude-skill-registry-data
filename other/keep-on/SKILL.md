---
name: keep-on
user-invocable: true
description: Manage skill-concierge's always-ON allowlist — the skills kept fully described in every turn instead of name-only. Use this skill when the user wants to view, add, or remove always-on skills, asks "which skills are always on", "add X to always-on", "remove X from the keep-on list", "manage the always-on skills", or wants to curate what stays injected vs retrieved on demand. Runs scripts/keep-on.py (list / add / remove), which edits the always-on allowlist under the canonical durable home (~/.claude/skill-concierge/keep-on.json) and re-applies the settings.json overrides.
argument-hint: "[list | add <skill> | remove <skill>]"
license: MIT
metadata:
  version: 0.1.1
---

# skill-concierge keep-on

Curate the **always-ON allowlist** — the skills kept fully described in every turn's
context. Every skill NOT on this list is "name-only" (just its name is injected; its
description is retrieved on demand via search). The allowlist lives at
`~/.claude/skill-concierge/keep-on.json` — the canonical durable home, seeded once from the
plugin's shipped default `config/keep-on.json` and preserved across `/plugin update`. This
skill is the seamless surface for reading and editing it.

> The autonomous session-start reconcile (`hooks/scripts/auto_overrides.py`) keeps
> `settings.json` in sync with the installed catalogue on its own. This skill is for
> **changing the policy** — which skills you *want* always-on — not for fixing drift
> (that self-heals).

## Steps

1. **View the current always-on set:**

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/keep-on.py" list
   ```

2. **Add skill(s)** to always-on — it reconciles `settings.json` immediately:

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/keep-on.py" add <skill-name> [<skill-name> ...]
   ```

3. **Remove skill(s)** from always-on:

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/scripts/keep-on.py" remove <skill-name> [<skill-name> ...]
   ```

## Names must be catalogue-namespaced

Skill names are as the index knows them — plugin skills carry their namespace
(`ck:plan`, `superpowers:brainstorming`, `skill-concierge:doctor`); bare skills are just
their name (`skill-search`, `come-clean`). Copy the exact name from `keep-on.py list` or a
`search_skills` result. An unknown name is stored but simply never matches a discovered
skill (apply-overrides reports it as "not present on this machine").

## Notes

- **Takes effect next session.** add/remove rewrite the allowlist
  (`~/.claude/skill-concierge/keep-on.json`, which survives `/plugin update`) and re-apply the
  overrides to `~/.claude/settings.json` (backed up first). Claude Code reads
  `settings.json` at session start, so a new always-on set applies on the next session.
- **Don't remove the router.** Removing `skill-search` / `skill-concierge:skill-search`
  makes the retriever entry point name-only — retrieval degrades. The script warns if you do.
- **This is policy, not maintenance.** Drift between the catalogue and `settings.json`
  heals itself (auto_overrides); use this skill only to change *which* skills you want always-on.
