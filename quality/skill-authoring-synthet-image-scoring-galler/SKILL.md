---
name: skill-authoring
description: >-
  Use when creating, reviewing, or improving first-party agent skills in this repo.
  Apply whenever a user asks to add a skill, edit SKILL.md, optimize skill triggering,
  or adapt patterns from Anthropic's public skills into the canonical .cursor skill tree.
---

# Skill authoring

## Purpose

Create and improve durable first-party agent skills. A good skill is a compact routing layer: its
frontmatter makes the agent load it at the right time, its body gives the next few decisions, and
any large or deterministic material lives in bundled resources.

**Canonical source:** `.cursor/skills/` (this repo is Cursor-first). After edits, run
`python scripts/sync_assistant_trees.py` so `.claude/skills/` mirrors stay in sync.

## When to use

- create, add, update, improve, optimize, or test a skill
- edit `SKILL.md`, skill frontmatter, or bundled resources
- diagnose under-trigger / over-trigger behavior
- AST10-style review for first-party skill changes

## Authoring workflow

1. **Capture intent** — what the skill enables, when it triggers, expected outputs, edge cases.
2. **Smallest change** — improve an existing skill when triggers overlap; create a new skill only for
   a distinct trigger surface.
3. **Author canonical files first** — edit `.cursor/skills/<name>/SKILL.md` and optional
   `{references,scripts,assets}/`. Do not hand-edit generated `.claude/skills/` copies.
4. **Run sync** — `python scripts/sync_assistant_trees.py`
5. **Validate** — `python scripts/sync_assistant_trees.py --check` and
   `python scripts/ci/check_agent_frontmatter.py`
6. **Safety** — apply `.agent/SKILL_CHANGE_AST10_REVIEW.md`; update `.agent/SKILL_INVENTORY.md`

## Skill structure

```text
.cursor/skills/<skill-name>/
├── SKILL.md              # required: frontmatter + compact instructions
├── references/           # optional
├── scripts/              # optional (prefer scripts/agent_skills/ for shared harnesses)
└── assets/               # optional
```

Compiled procedural skills may use thin bootloaders pointing at `scripts/agent_skills/*.py`.
See [`.agent/SKILL_COMPILATION.md`](../../../.agent/SKILL_COMPILATION.md).

## Frontmatter

`name` must be the **first** key and match the directory name; `description` must be non-empty.

```yaml
---
name: example-skill
description: Use when ...
---
```

## Verification checklist

- [ ] Canonical source changed under `.cursor/skills/`
- [ ] `python scripts/sync_assistant_trees.py` and `--check` pass
- [ ] `python scripts/ci/check_agent_frontmatter.py` passes
- [ ] `.agent/SKILL_INVENTORY.md` updated
- [ ] AST10 notes in PR summary for material changes
