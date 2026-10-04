---
id: authoring-adept-skills
description: "Write a good, portable adept skill: pick the right activation, craft a triggering description, keep it scan-safe and within harness byte budgets. Apply when creating or editing a SKILL.md or running `adept skill add`."
activation: agent
allowed-tools:
  - "Bash"
  - "Read"
  - "Edit"
  - "Write"
---

# Authoring a good adept skill

A skill is a directory `<root>/skills/<id>/` with one `SKILL.md` (YAML frontmatter +
markdown body) and optional sidecars. `adept` renders it into every enabled harness, so
write it **once, well, and harness-neutral**.

## Canonical SKILL.md format

```markdown
---
id: pr-review                 # ^[a-z0-9](?:[a-z0-9-]{0,48}[a-z0-9])?$ — matches the directory name
description: Use before opening a PR. Tests, security, performance.   # <= 280 chars
activation: agent             # always | globs | agent | manual
globs: []                     # REQUIRED when activation: globs (e.g. ["**/*.go"])
allowed-tools: [Read, Grep]   # carried into Claude Code
targets: []                   # empty = all enabled harnesses
tags: [review, quality]
---
# PR Review Checklist
- [ ] Tests added or updated
- [ ] No secrets in the diff
```

Validated against `pkg/adeptschema/skill.schema.json` on every load — `adept sync` fails
loudly on a malformed skill, so let it catch your mistakes.

## Pick activation deliberately — this is the whole game

| activation | Fires when | Use for |
|---|---|---|
| `agent`  | The model decides from the **description** | Most skills. Procedures, checklists, how-tos. |
| `globs`  | A matching file is in context | Language/path-specific rules (`**/*.go`, `**/*.tsx`). |
| `always` | Every request | Rare. Project-wide invariants only — costs budget on every turn. |
| `manual` | Only when explicitly invoked | Heavy or destructive procedures you don't want auto-firing. |

## The description is the trigger — write it like one

For `activation: agent`, the description is the **only** thing the model sees when deciding
whether to load the skill. Make it earn the load:

- Lead with **when to apply**, not what it is: *"Use before opening a PR…"* beats *"A PR
  helper."*
- Name concrete nouns the user will say (file types, commands, tools, error strings).
- One line, ≤ 280 chars. If you can't say when it applies in one line, the skill is too broad
  — split it.

## Keep it portable and lean

- **Harness-neutral body.** Don't say "in Cursor, click…"; describe the behavior, not the UI.
- **Budget-aware.** Aggregator harnesses (Codex/Copilot) cap total bytes; a bloated skill
  gets dropped first. Tighten prose; move long reference material into `references/` sidecars.
- **Scan-safe.** Installs run a safety scan. Avoid anything that reads like prompt injection,
  exfiltrates secrets, or runs opaque remote code — it will flag (`critical` hard-blocks).
- **Sidecars** (`scripts/`, `references/`, `assets/`) ride along to harnesses that support
  them; keep the SKILL.md body self-sufficient for those that don't.

## Loop

```bash
adept skill add my-skill --edit   # scaffold + open $EDITOR
adept sync                        # render to every enabled harness
adept status && adept diff        # confirm it landed clean
```

Run `adept skill --help` (and `adept skill add --help`) for the current flags and
subcommands — prefer it over memory; it never drifts. Edit canonical, `adept sync`, never
hand-edit rendered files. See [[using-adept]] for the
full CLI and [[adept-self-improve]] for turning a one-off lesson into a durable skill.
