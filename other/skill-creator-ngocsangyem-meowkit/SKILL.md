---
name: mk:skill-creator
description: 'Create new skills with proper structure, compliance checks, and registration. Use when asked to create a skill, build a new skill, or scaffold a skill template. Enforces mk: prefix, sub-agents.md structure, and context engineering principles.'
argument-hint: '[skill-name] [description]'
source: local
original_path: .claude/skills/skill-creator/SKILL.md
adapted_for: claude-code
keywords:
  - skill-creator
  - new-skill
  - scaffold-skill
  - authoring-template
  - gotchas-section
when_to_use: Use when creating a new skill — scaffolds SKILL.md with required sections per skill-authoring-rules.
user-invocable: true
owner: portability
criticality: medium
status: active
runtime: claude-code
---

# Skill Creator

Create new skills with proper structure, compliance, and registration.

> **Path convention:** Commands below assume cwd is `$CLAUDE_PROJECT_DIR` (project root). Prefix paths with `"$CLAUDE_PROJECT_DIR/"` when invoking from subdirectories.

## When to Use

- User asks to "create a skill", "build a new skill", "make a skill for [X]"
- Converting external skill for adoption
- Scaffolding a skill from a workflow pattern

Explicit: `/mk:skill-creator [name] [description]`

## Workflow Integration

Meta skill — not tied to a specific Phase. Invoked on-demand for skill development.

## Scripts

**Script-first approach** — Python scripts handle scaffolding and validation. Claude reviews and fills in the content.

```bash
# Scaffold a new skill (creates directory + template SKILL.md)
.claude/skills/.venv/bin/python3 .claude/skills/skill-creator/scripts/init-skill.py mk:my-feature --path .claude/skills

# Validate an existing skill against compliance checklist
.claude/skills/.venv/bin/python3 .claude/skills/skill-creator/scripts/validate-skill.py .claude/skills/my-feature
```

## Process

1. **Gather intent** — what should the skill do? When should it trigger? What output format?
2. **Scaffold** — run `init-skill.py` to create directory + template SKILL.md with TODO markers
3. **Fill content** — Claude completes each TODO section in the generated template
4. **Add references/** — if skill body would exceed ~100 lines, split into references
5. **Security boundaries** — load `mk:skill-template-secure` template for trust model if needed
6. **Validate** — run `validate-skill.py` to check compliance (8-point checklist)
7. **Fix failures** — if validation score < 7/8, fix failing items
8. **Register** — add row to `SKILLS_ATTRIBUTION.md`
9. **Report** — output creation summary

## Required Sections in Generated SKILL.md

Every skill MUST have:

```yaml
# Frontmatter
name: "{name}"
description: "{specific trigger keywords + what it does}"
```

If the name already exist then use with prefix `mk:`

```yaml
# Frontmatter
name: mk:{name}
description: "{specific trigger keywords + what it does}"
```

```markdown
## Overview — what + when (2-3 sentences)

## When to Use — auto-triggers + explicit syntax

## Process — numbered steps (not prose)

## Output Format — template with placeholders

## Failure Handling — per-failure table

## Workflow Integration — which Phase (0-6)

## Handoff Protocol — next agent + action
```

## Compliance Evaluation

After generating, check:

- [ ] `mk:` prefix in skill name
- [ ] Workflow phase anchoring (Phase 0-6 stated)
- [ ] Handoff protocol (next agent specified)
- [ ] Output format uses template with placeholders
- [ ] Failure handling covers identified failure modes
- [ ] SKILL.md ≤ 500 lines (per `skill-authoring-rules.md` Rule 3; overflow → references/ or step files)
- [ ] `## Gotchas` section present (per Rule 1 — mandatory, placeholder acceptable day-1)
- [ ] No conflict with existing `.claude/rules/`

**Score:** X/8 — PASS (≥7) / FAIL (<7)

If FAIL: fix failing items before registering.

## Output Format

```
## Skill Created: mk:{name}

**Directory:** .claude/skills/{name}/
**Files:** SKILL.md{, references/*.md}
**Compliance:** {X}/7 — {PASS|FAIL}
**Registered:** {yes|no — in SKILLS_ATTRIBUTION.md}

### Compliance Details
{checklist with ✓/✗ per item}
```

<!-- research-citation -->
## Anthropic Skill-Building Lessons

1. **Skills are folders** — use scripts/, references/, assets/, lib/ creatively. See `references/filesystem-patterns.md`.
2. **Gotchas = highest signal** — every skill MUST have a `## Gotchas` section. A day-1 placeholder is allowed; replace it as real failures emerge.
3. **Progressive disclosure** — SKILL.md stays under 500 lines per `skill-authoring-rules.md` Rule 3. Details live in references/ loaded on-demand. Step-file skills (with `workflow.md`) auto-pass.
4. **Avoid railroading** — describe outcomes, not step-by-step procedures. See `references/good-vs-bad-examples.md`.
5. **Description = trigger condition** — must answer "When should I use this?" not "What does this do?" Start with "Use when..."
6. **On-demand hooks** — skills can register session-scoped hooks in frontmatter for enforcement during execution.
7. **config.json for setup** — if skill needs user-specific values, store in config.json. Agent asks on first use.
8. **Memory strategy** — stateful skills should document what they persist and where.
9. **Don't state the obvious** — only include knowledge that pushes Claude beyond its defaults.
10. **One skill type** — classify using the 9-type taxonomy. See `references/skill-types.md`.

### Mandatory checklist before finalizing any skill

- [ ] Description starts with "Use when..." (trigger condition)
- [ ] Has `## Gotchas` section header (Rule 1 — placeholder acceptable day-1; grow over time)
- [ ] SKILL.md is under 500 lines (Rule 3 — or decomposed via references/ / step files)
- [ ] Steps are outcome-focused (no railroading)
- [ ] Uses filesystem beyond SKILL.md (or documents why not needed)
<!-- research-citation -->
- [ ] Classified into one Anthropic skill type
- [ ] Persistent state (if any) writes to `${CLAUDE_PLUGIN_DATA}`, NOT skill directory (Rule 2)

## References

- [creation-workflow.md](./references/creation-workflow.md) — Step 4: section-by-section guidance and examples
- [skill-types.md](./references/skill-types.md) — 9-type taxonomy with examples
- [good-vs-bad-examples.md](./references/good-vs-bad-examples.md) — writing descriptions, gotchas, and steps
- [filesystem-patterns.md](./references/filesystem-patterns.md) — when to use scripts/, references/, assets/, lib/, config.json

## Failure Handling

| Failure                   | Recovery                                   |
| ------------------------- | ------------------------------------------ |
| Name missing mk: prefix | Auto-prepend and warn                      |
| Duplicate skill name      | Suggest alternative or update existing     |
| Compliance check fails    | List failing items, fix before registering |

## Gotchas

- **Template must include `## Gotchas` header** — even as a placeholder. `skill-authoring-rules.md` Rule 1 is hard-enforced by `validate-skill.py`. Day-1 skills may use `(none yet — grow from observed failures)` but the header itself is mandatory.
<!-- research-citation -->
- **Line cap is 500, not 150** — the canonical threshold comes from `skill-authoring-rules.md` Rule 3 (Anthropic progressive-disclosure guidance). Step-file skills (with `workflow.md`) auto-pass regardless of line count.
- **Persistent state goes to `${CLAUDE_PLUGIN_DATA}`, not skill directory** — Rule 2 prevents data loss on plugin upgrade. framework-internal paths (`.meowkit/memory/`, `session-state/`) are exempt.
