---
name: help
description: "Passive on-demand index of installed user-invoke skills, grouped by category. Bundled with super-bootstrap. Invoke as `/super-bootstrap:help` (namespaced to avoid colliding with Claude Code's built-in `/help`); `/super-bootstrap:help <category>` filters. Reads installed-plugin registry + project skills + each enabled plugin's skills via a bundled script — zero-dispatch. No active reminders — discovery is pull-only, zero ambient cost."
tags: [help, discovery, menu, pipeline]
---

# Help — User-Invoke Skill Discovery Surface

Render an on-demand menu of slash commands the user can invoke in this project. Cold-by-nature user-invoke skills (slash commands the user must remember) need a discovery surface; passive `/super-bootstrap:help` is the right shape.

Extraction is mechanical (structured JSON + YAML frontmatter), so a bundled script does it in one tool call with zero model tokens; the one judgment in the pipeline — which discovered skills a *user* would actually invoke — stays with the gateway.

## When to Use

- User forgot which slash commands are available
- User just installed a new plugin and wants to see what it added
- User wants to filter by category (`/super-bootstrap:help git`, `/super-bootstrap:help docs`)

## Execution (gateway-inline)

When the user invokes `/super-bootstrap:help [category]`:

1. **Extract** — run the bundled script, passing the project root (the session's working directory — `pwd`):
   `python3 "${CLAUDE_PLUGIN_ROOT}/skills/help/assets/render-menu.py" "$(pwd)"`
   (The script body is opaque to the permission engine — the grant to carve is the invocation itself, e.g. `Bash(python3 *)`.)
   It emits one candidate per line (`category<TAB>command<TAB>description`) from the installed-plugin registry, `enabledPlugins`, each enabled plugin's skills, and project `.claude/skills`. It deliberately over-reports — no filter lives in the script.
2. **Filter to user-invoke** — drop rows a user would never type: delegation-only skills (dispatched by other skills or the model, e.g. process/reference skills another skill invokes), hook-fired skills, and reference-material bundles. Keep anything a user plausibly types as a slash command. This is the judgment step; do it from the emitted descriptions — no file reads.
3. **Render** — group surviving rows under their category headers (`[meta]` `[pipeline]` `[git]` `[docs]` `[dev]` `[utils]`), one line per skill: command + one-line summary. Header: `Available slash commands ({N} total):`. A category argument renders only that category; unknown category → list available categories. **Anomaly footer:** the script's stderr carries an `# anomalies:` line only when a source emitted fewer rows than it declared or held — render everything after its `# anomalies: ` prefix as a footer line beneath the menu, contents unaltered and itself prefixed `incomplete: `. A short source is a discovery failure, and without the footer it is indistinguishable from a plugin that ships no commands. No `# anomalies:` line → no footer.
4. **Fallback** — `python3` missing on the device: scan the same sources manually with Read/Grep (structure documented in the script header) and render the same shape.

## Rules

- **No active reminders.** Discovery is pull-only — the user invokes; nothing fires ambiently.
- **Namespaced invocation.** Always `/super-bootstrap:help` — bare `/help` is Claude Code's built-in. Footer hints elsewhere in this plugin must use the namespaced form too.
- **Script over-reports by design.** The user-invoke filter is the gateway's judgment at render time; never push it down into the script.
