---
name: manage-rule-system
description: Convention for creating, updating, or modifying rule files in .agents/rules/. Use when adding, editing, or restructuring rule files to ensure compatibility across Claude Code, GitHub Copilot, Cursor, and OpenAI Codex.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash(.agents/skills/manage-rule-system/scripts/inject-context.sh:*)
models:
  claude: sonnet      # medium-complexity; cross-tool frontmatter authoring requires structured reasoning
  copilot: auto
  codex: gpt-5.4
---

# Manage Rule System — Skill

Triggered automatically by `.agents/hooks/manage-rule-system-context.sh` (UserPromptSubmit) when the user mentions creating, updating, modifying, adding, or editing a rule. Also triggers when an agent Reads/Edits/Writes a file under `.agents/rules/` via the `load-agents-context` PostToolUse hook.

## Rule Directory

All rule files live under a single `.agents/rules/` tree, organized into category subfolders. Every `.md` file in the tree is auto-loaded by the AI tool at session start; applicability is scoped **per-file** via the `paths`/`globs`/`applyTo` frontmatter (there is no separate scoped/injected directory).

| Location | Use for |
|----------|---------|
| `.agents/rules/*.instructions.md` (flat) | Cross-cutting rules that don't share a category with ≥1 other rule (AI workflow, code-review false-positive guidance, project overview) |
| `.agents/rules/<category>/` | A category folder is created when 2+ rules share a topic. Current: `backend/` (.NET / EF Core / API+Mediator / migrations / WireMock / logging), `git/` (git policy, PR standards), `meta/` (rule-file convention, AGENTS.md quality) |

To make a rule narrow to certain files, set its frontmatter scope fields (e.g. `paths: ["**/*.cs"]`); to make it always-apply, use `"**"` / `alwaysApply: true`. The folder is organizational only — it does not change loading.

To defer a prompt-scoped rule for Claude only (saving session tokens) and re-inject it on demand via a `UserPromptSubmit` hook, see "Hook-deferred rules" in `.agents/rules/meta/rules.instructions.md` — e.g. `code-review-standards`.

## File Format

Every rule file MUST:

1. **Use `.instructions.md` extension** (kebab-case filename)
2. **Include YAML frontmatter** (Copilot/Cursor metadata)

### Frontmatter Template

```yaml
---
description: 'Short description of what the rule covers'
globs: "<glob-pattern>"
paths:
  - "<glob-pattern>"
applyTo: '<glob-pattern>'
alwaysApply: <true|false>
---
```

The three scope fields mirror the same pattern(s) — one per tool. For multiple patterns, `globs`/`applyTo` take a comma-separated string while `paths` takes a YAML list.

| Field | Used by | Purpose |
|-------|---------|---------|
| `description` | Copilot, Cursor | Displayed in UI; Cursor uses it for agent-mode rule selection |
| `globs` | Cursor | File pattern for auto-attach; quote the value |
| `paths` | Claude Code | YAML list of file patterns for path-scoped applicability. Mirror `globs`. Use `["**"]` for always-apply |
| `applyTo` | Copilot | File pattern for `.github/instructions/**` loading. Mirror `globs`; use `'**'` for always-apply |
| `alwaysApply` | Cursor | `true` = always loaded; `false` = only on glob match |

Claude Code auto-loads every `.md` file under `.claude/rules/` (symlink → `.agents/rules/` → `.github/instructions/`) at session start, recursing into category subfolders. Scoping is **per-file** via the frontmatter above — there is no separate injected directory.

### Scoping Guidelines

| Rule scope | Place in | `alwaysApply` | `globs` / `paths` / `applyTo` |
|------------|----------|---------------|-------------------------------|
| Project-wide (git, PR, workflow) | `.agents/rules/` (flat) or a category folder | `true` | `"**"` |
| Backend only | `.agents/rules/backend/` | `false` | `"**/*.cs"` |
| Domain-specific | nearest `*AGENTS.md` instead | n/a | n/a |

Create a `<category>/` subfolder when 2+ rules share a topic; otherwise keep the rule flat in `.agents/rules/`.

## Creating a New Rule

```bash
touch .agents/rules/my-new-rule.instructions.md            # cross-cutting (flat)
touch .agents/rules/backend/my-rule.instructions.md        # backend category
```

Then add frontmatter + content. After saving:

- Add a one-line changelog entry inside the rule file's `## Changelog` table (this repo retains in-file changelogs; the AI loading note tells agents to skip the section at runtime)
- If you created a new category folder, reflect it in root `AGENTS.md` (Rules section) and in `smooth-ai-stockanalysis.slnx`

## Tool Compatibility Matrix

| Tool | Reads from | Scoping mechanism | Extension |
|------|-----------|-------------------|-----------|
| Claude Code | `.claude/rules/` (symlink → `.agents/rules/` → `.github/instructions/`) | `paths` frontmatter | `.md` |
| Copilot | `.github/instructions/` (**real directory** — no symlink) | `applyTo` frontmatter | `.instructions.md` |
| Cursor | `.cursor/rules/` (symlink → `.agents/rules/` → `.github/instructions/`) | `globs` + `alwaysApply` frontmatter | `.instructions.md` |
| Codex | `.codex/` (symlink → `.agents/`) | invokes `context-load-agents-context` skill explicitly | `AGENTS.md` |

The rule files physically live in `.github/instructions/` (a **real directory**, so Copilot's github.com-hosted agent reads them without resolving a symlink). `.agents/rules`, `.claude/rules`, and `.cursor/rules` are symlinks resolving back to it — all tools share one source of truth.

## Non-Negotiables

- **Scope per-file, not per-directory.** Every rule carries `paths`/`globs`/`applyTo` frontmatter that mirrors the same pattern(s). Category subfolders are organizational only and do not affect loading.
- **Never reference a moved rule by its old path.** After moving a rule, sweep cross-references with `rg -l <old-path>` and update every hit (including hardcoded paths in `load-agents-context.sh` and skill docs).
