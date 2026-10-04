---
name: authoring-agent-skills
description: >-
  Meta-skill for creating Agent Forge skills under .claude/skills/ with SKILL.md,
  optional references/ and scripts/, and Bun scaffolds. Use when the user wants to
  add or author a skill, scaffold a new skill folder, or align skill docs with harness
  conventions (JSON script output, Beads for tasks).
---

# authoring-agent-skills

Creates well-structured skills for this harness. **Upstream port:** concepts from mattpocock **write-a-skill** are folded in here so one meta-skill stays canonical for Agent Forge.

## When to Use

- Creating a new repeatable workflow or tool as a skill
- Explaining how `description:` in YAML routes agents to the right skill
- Deciding whether logic belongs in markdown steps vs `scripts/*.ts`

## Process

1. **Gather requirements** — task/domain, main use cases, scripts vs docs only, any reference material to bundle.
2. **Draft** — `SKILL.md` first; add `references/` or `scripts/` only when needed.
3. **Review** — use the checklist in `references/AUTHORING-GUIDE.md`.

## Skill anatomy

A skill lives in `.claude/skills/<name>/`:

| Piece | Role |
|--------|------|
| `SKILL.md` | Required instructions and entrypoint |
| `references/` | Optional deep docs (progressive disclosure) |
| `scripts/` | Optional Bun TypeScript; emit JSON per AGENTS.md |

### SKILL.md frontmatter

```yaml
---
name: <skill-name>
description: <one line + Use when … triggers>
---
```

See **Description field** and **checklist** in [references/AUTHORING-GUIDE.md](references/AUTHORING-GUIDE.md).

## Harness conventions

1. Single responsibility per skill.
2. Numbered steps with exact commands where possible.
3. **Scripts** return structured JSON (`ok`, `data`, `error`).
4. Idempotent scripts when reruns are likely.
5. Tracked work uses **Beads** (`bd`), not TODO files or TODO comments.
6. **Ship self-contained — never depend on `repos/`.** `repos/` holds cloned sub-repos and is **gitignored**, so anything under it is absent for other users. A command or skill must not reference `repos/skills/...` (or any other `repos/<x>` dependency) as something it *needs to read*. Vendor a copy into the harness (e.g. `.claude/skills/<name>/`) and reference that. Referring to `repos/<repo>/` as the **runtime location of the user's own sub-repos** (e.g. `--repo ./repos/<name>`, `repos/repos.json`) is fine — that is user data, not a harness dependency.

## Scaffold

Creates `.claude/skills/<name>/` with `SKILL.md`, `scripts/`, and `references/`:

```bash
bun run .claude/skills/authoring-agent-skills/scripts/scaffold.ts <skill-name> "<description>"
```

Use a **slug** for `<skill-name>` (kebab-case, matches `name:` in frontmatter).

## Long-form template and split-file guidance

[references/AUTHORING-GUIDE.md](references/AUTHORING-GUIDE.md) — full template, description examples, when to script vs split, review checklist.
