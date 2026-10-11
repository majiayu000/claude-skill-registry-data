---
name: skill-creator
description: Creates and updates skills per agentskills.io spec.
---

# Skill Creator — Project Extension

This skill extends `anthropic-skills:skill-creator` with validation rules required by this project. Always invoke the official skill first, then apply the checklist below before finalizing.

## Activation Flow

1. Invoke `anthropic-skills:skill-creator` to drive the main authoring flow
2. On completion, run the **Validation Checklist** below
3. Fix any violations before presenting the result to the user

## agentskills.io Spec Compliance

Every skill must conform to https://agentskills.io/specification:

| Field | Rule |
|-------|------|
| `name` | 1–64 chars · lowercase alphanumeric + hyphens only · must match directory name exactly · no leading, trailing, or consecutive hyphens |
| `description` | 1–1024 chars · describes what the skill does AND when to use it |
| Body | ≤ 500 lines · move long reference content to `references/` subdirectory |
| Directory layout | `SKILL.md` required · optional: `scripts/`, `references/`, `assets/` |

## Validation Checklist

Run before finalizing any skill:

- [ ] `name` in frontmatter matches the skill's directory name exactly
- [ ] `description` is specific enough to trigger correctly (answers: what does it do + when to invoke it)
- [ ] Body is ≤ 500 lines (count and verify)
- [ ] Long reference material is in `references/` files, not inline
- [ ] If `skills-ref` CLI is available: run `skills-ref validate ./skill-dir`

## Project-Specific Rules

- All content written in English
- File path: `skills/<category>/<skill-name>/SKILL.md`
- If the skill is user-invocable (triggered by a slash command), register it in `CLAUDE.md` under the appropriate section
- Do not include change history, "was replaced by", or narrative about past versions in the body — body is current rules only
