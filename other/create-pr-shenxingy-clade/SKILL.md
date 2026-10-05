---
name: create-pr
description: Publish or update one repository-adaptive, exact-SHA pull request without duplicating or broadening authority
when_to_use: "create PR, update PR, open pull request, 提 PR, 开 PR, publish this delivery — NOT release aggregation (use /ship)"
argument-hint: '[--draft] [--base <branch>] [--dry-run]'
user_invocable: true
---

# Create or update PR

Publish one independently reviewable and reversible delivery unit. Use the
shared `$delivery` context/state controller; do not assume GitHub, `origin`,
`main`, branch ownership, or autonomous PR authority.

**One PR = one independently reviewable and reversible delivery unit.**

Tests, migrations, generated files, and documentation for that same behavior
belong together. Independent behavior becomes independent or explicitly
stacked delivery records.
