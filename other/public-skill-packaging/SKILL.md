---
name: public-skill-packaging
description: Use when a user asks to prepare AI skills for public sharing, sanitize private workflows, create a skill-pack draft, review public-release scope, check for private paths, or design README/license/security boundaries before publishing.
---

# Public Skill Packaging

Prepare skill packs for sharing without leaking private data.

## Package Checklist

- Each skill has `SKILL.md` with `name` and `description`.
- Public files use placeholders such as `<PROJECT_ROOT>`, `<GAME_URL>`, and `<REPORT_DIR>`.
- Private paths and private reports are removed.
- Runtime edits are approval-gated.
- External code adoption is review-gated.
- Deployment and publishing are explicit approval tasks.

## Suggested Structure

```text
skills/
  sentinel-router/
  browser-game-playtest-sentinel/
  game-ui-review/
  game-design-review/
  safe-learning-governance/
  public-skill-packaging/
docs/
  PUBLIC_SCOPE.md
  PRIVATE_DATA_POLICY.md
```

## Sanitation Scan

Search public candidates for private paths, credentials, personal machine names, and risky commands before sharing.

## Stop Rules

Do not create a public repository, push code, publish a release, use credentials, or include private project files without explicit approval.
