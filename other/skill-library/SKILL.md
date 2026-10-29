---
name: skill-library
description: Find installed specialist skills outside the default catalog when a task needs domain-specific guidance, or the user asks for an installed skill that is not visible. Search the local library before searching for new skills to install.
---

# Use the installed skill library

Run `scripts/skill-library list` from this skill's directory. It reads the generated
host catalog at `${XDG_STATE_HOME:-~/.local/state}/agent-skills/catalog.json`.
The catalog covers all default-disabled local plugins and declared upstream
plugins resolved through Claude's user installation inventory. These files can
be read from either Codex or Claude; their presence does not enable a plugin.
Unavailable installations appear as coverage diagnostics.

Choose only entries relevant to the user's task. Preserve the full description's
conditions, including requests that must name a skill explicitly. If no entry
fits, continue the task without loading one. Prefer a skill already available in
the current native catalog over loading another copy from this library.

Run `scripts/skill-library read MARKETPLACE/PLUGIN/SKILL` for a selected `read`
entry. Read its complete instructions before proceeding, and honor any narrower
conditions in its body. Resolve supporting files and scripts from the printed
skill directory. Reading instructions does not authorize their side effects.

Entries marked `explicit` remain searchable but require the user to request that
skill. Only then pass `--explicit`. Entries marked `native` require native plugin
invocation; do not emulate their hooks, tools, permissions, argument expansion,
model selection or fork behavior through a file read. Explain the needed native
enablement when it blocks the requested task; never change activation merely to
search the library.

If the catalog is absent, stale, or a path is missing, report that limitation.
In the dotfiles checkout, regenerate it with
`.agents/skills/agent-skill-management/scripts/generate-skill-library` after
materialization. Normal script 36 apply also regenerates it. Do not guess cache
versions or search unselected vendor trees for substitutes.

The library loads instructions into the current conversation. It does not
register slash commands, unload instructions, or guarantee retention after
compaction. Resume through the same verified entry if its instructions are needed
again.
