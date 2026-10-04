---
name: handoff
description: >
  Deprecated name. Use session-handoff; load this notice only when handoff is explicitly requested.
license: MIT
metadata:
  source: iuliandita/skills
  date_added: "2026-09-20"
  effort: low
  deprecated: "true"
---

# Deprecated: handoff

This old skill name is retained temporarily to explain the catalog migration. It provides migration guidance only and does not contain the former task workflow.

## When to use

Only when the user explicitly invokes the old **handoff** name or asks how to migrate it.

## When NOT to use

Do not select this notice for ordinary domain tasks or treat it as an active skill.

## Workflow

1. Explain that this skill was renamed or merged into **session-handoff**.
2. If **session-handoff** is installed, offer it by name and use its own instructions when the request authorizes that work.
3. If it is missing, explain how to install the replacement and remove this old entry after backing up customizations. Do not read a sibling path or install anything silently.

See `MIGRATION.md` in the [collection repository](https://github.com/iuliandita/skills)
for installer-specific steps and the complete mapping.

## Rules

- Keep this notice for one transition release and at least seven days after publication.
- Never claim an installed copy will update or disappear automatically.
- Preserve local edits and private overlays before removing an installed entry.
