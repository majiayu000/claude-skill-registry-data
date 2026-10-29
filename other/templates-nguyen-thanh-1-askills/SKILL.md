---
name: replace-with-kebab-case-name
description: State what the skill does and the concrete requests that should trigger it; include a meaningful boundary when a nearby skill could be confused with it.
metadata:
  risk: unknown
  source: self
  source_type: self
  date_added: YYYY-MM-DD
---

# Skill title

Describe the outcome this skill enables. Keep shared instructions concise and
move mode-specific detail into `references/` when that reduces context cost.

## When to Use

- Use for ...
- Do not use for ...

## Workflow

1. Identify the minimum inputs required for the requested outcome.
2. Apply the domain-specific procedure and preserve the user's scope.
3. Verify observable results in proportion to risk.

## Safety and Permissions

- Distinguish read-only work from external or destructive mutations.
- Ask for authorization immediately before an action that needs it.

## Limitations

- Document real limitations and environment assumptions only.
