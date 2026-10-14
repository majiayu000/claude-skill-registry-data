---
name: civiltekk-install-assistant
description: >-
  Catalog install assistant for civiltekk skills, subagents, and dep-shipped
  plugins — find by intent, install with mandatory dry-run and consent-gated
  global scope, maintain via update/prune/remove; offers additive AGENTS.md
  enforcement. Triggers: find a skill, install skill into project, add
  subagent, update installed skills, is there a skill for,
  @civiltekk-install-assistant, /civiltekk-install-assistant.
license: Apache-2.0
compatibility: opencode
metadata:
  harness: "opencode"
category: Configuration
---

# Skill: civiltekk-install-assistant

Guided front door to the civiltekk catalog (skills + subagents; plugins ship
automatically as dependency artifacts). The npx installer is the engine — I
never hand-copy files or resolve dependencies myself; I route intent to the
right installer surface and enforce its safety rails. Sibling: I am to
skills/subagents what `mcp-install-assistant-skill` is to MCP servers.

## Route detection (explicit > inferred > ask-once)

| Ask | Route |
|-----|-------|
| "is there a skill for X", "find a skill", "what skills exist", "recommend" | `find` — load `references/find.md` |
| "install skill X", "add subagent Y to this project", "use the installer" | `install` — load `references/install.md` |
| "what's installed", "update my skills", "remove skill X" | `maintain` — load `references/maintain.md` |
| Invoked by handle (`@civiltekk-install-assistant` / `/civiltekk-install-assistant`) | fast path — run the tree immediately; classify by content; bare ask defaults to `find` |
| Ambiguous ("set me up with X") | ask once, then route — one ask per run |

Find often chains into install ("yes, add it") and install into maintain —
re-enter a route by re-reading its file; never hold all three in context.

## Side files (load rules)

| Read | When | Use |
|------|------|-----|
| `references/find.md` | route `find` | Catalog search: `--list` read modes, `--describe`, `--expand` presets, in-repo shortcut, ranking + offer |
| `references/install.md` | route `install` | The only mutating route: describe → dry-run → scope choice → add → verify; AGENTS.md wire-up block |
| `references/maintain.md` | route `maintain` | Inventory, `update`, `update --prune`, `remove`; honest state reporting |

Side files carry VALUES (commands, flags, block text); this file carries the
METHOD. Shared rules live here once — never restated in a side file.

## Shared invariants (all routes)

- `--dry-run` before every write; show the resolved set (the entry + its
  transitive `requiresSkills`) to the user before the real `add`.
- `--no-deps` only on an explicit user ask — never proactively.
- Global (user-scope) installs require consent; project scope is the default.
- Never hand-edit an installed skill copy — fix at the source repo, then
  `update`. Installed files are deploy artifacts, not working files.
- Report exact installer errors verbatim; no blind retries, no invented flags.

## Capability bindings

Interactive prompts during route work.
- OpenCode: `question` tool (one question, 2-4 options)
- Claude Code: `AskUserQuestion` multiple-choice tool
- Other/none: number the options in a plain reply and wait for the pick

Requires bash (git-bash/WSL on Windows) for the npx/git steps; Node is
guaranteed wherever the installer runs.

## Boundaries

- MCP server enablement → `mcp-install-assistant-skill` (different config
  surface; installer `--list mcps` is read-only triage, not enabling).
- Authoring a new skill/agent → `civiltekk-opencode-creation-skill`; search
  the catalog first (this skill, `find`) so nothing is authored twice.
- Harness detection / cross-harness parity setup →
  `civiltekk-coding-harness-setup-skill`; `--target` here only picks the
  install destination.
- I am a skill, invoked via the skill tool or my handles — not a subagent;
  no `task` delegation.
