---
name: rewrite-descriptions
description: >
  Propose description rewrites to resolve skill collisions. Given a collision pair
  from a gardener audit, reads both skills' descriptions, generates before/after
  rewrites with negative discriminators, and writes a proposal Markdown the user
  applies manually. Uses current Claude prompting discipline: positive imperatives,
  motivation clauses, scope explicit. Use when the user asks to fix a collision,
  rewrite a description, disambiguate two skills, or mentions resolving a
  gardener-flagged pair.
arguments:
  - name: pair
    description: "Collision pair as `skill-a,skill-b` (e.g., 'research,internal-research') or a single skill name to rewrite against siblings."
    required: true
context: fork
user_facing: true
---

## Contents

| Reference                            | When to load                           |
| ------------------------------------ | -------------------------------------- |
| `../../references/write-protocol.md` | Write discipline for the proposal file |
| `references/rewriting-patterns.md`   | Patterns specific to description fixes |
| `templates/proposal-skeleton.md`     | Output file shape                      |

# Rewrite descriptions

Given a collision pair, produce a concrete description rewrite proposal for each side. The output is a Markdown file with before/after blocks the user copies into the SKILL.md files manually.

## Inputs

- `{{ pair }}` — either `skill-a,skill-b` or a single skill name. If single, read `plugin-gardener/audit/` for the latest `collisions.md` and pick the top unresolved collision involving that skill.

## How it works

1. Resolve each skill path. Read both SKILL.md files and capture the current `description` + optional `when_to_use`.
2. Apply the rewriting patterns in `references/rewriting-patterns.md`. Every rewrite must:
   - Keep each description under 1,024 characters (hard Anthropic cap).
   - Combined `description + when_to_use` under 1,536 characters (skill listing cap).
   - Add a negative discriminator on each side that points at the other: `Do NOT use when the user mentions [sibling-domain-term]`.
   - Use third-person voice, positive imperatives, one motivation clause where non-obvious.
   - Preserve the `Use when the user asks to …` clause structure if it was already there.
3. Write `plugin-gardener/audit/ad-hoc/rewrite-<skill-a>-vs-<skill-b>-<YYYY-MM-DD>.md` using `templates/proposal-skeleton.md`.
4. Present the proposal inline so the user can copy-paste without opening the file.

## What this does not do

- Edit SKILL.md.
- Commit changes.
- Regenerate SKILL.md bodies. Description-only changes; the skill content is untouched.

The user applies the rewrite manually. After applying, invoke `/audit-skill <name>` on both sides to confirm the collision is resolved.
