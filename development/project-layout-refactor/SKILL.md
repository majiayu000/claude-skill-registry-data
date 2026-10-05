---
name: project-layout-refactor
description: Audit and safely refactor a repository's directory layout while preserving behavior, imports, build tooling, history, generated-file rules, and user.
license: MIT
---

# Project Layout Refactor

## Analyze first

Read project instructions, manifests, build/test configs, import aliases, package boundaries, generated/vendor rules, CI/deploy files, documentation links, code owners, and dirty-worktree state. Map each proposed move to consumers: imports, scripts, globs, assets, tests, docs, workflows, packaging, and runtime paths.

Classify files as source, tests, configuration, documentation, assets, generated, cache, local-only, secrets, or unknown. Never move/delete an unknown file merely because its name looks untidy.

## Plan

Propose the smallest coherent target tree. For each move list source, destination, reason, references to update, collision/case-sensitivity risk, and validation. Respect ecosystem conventions and the repository's established structure; avoid a grand taxonomy that adds empty folders or breaks discoverability.

## Apply safely

- Preserve unrelated user changes and create a backup when version control is insufficient.
- Use native filesystem moves within one verified workspace; check case-only renames and Windows path rules.
- Update imports, aliases, manifests, scripts, CI, docs, tests, and ignore rules in the same atomic slice.
- Do not delete generated/cache content unless its regeneration command is verified and deletion is in scope.
- Do not move secrets into tracked paths.
- Keep public APIs and package entry points stable or document a deliberate migration.

Implement in small slices and validate after each risky boundary move. Stop and roll back the slice that causes unexplained behavior changes.

## Validation

Run project format/lint/typecheck/build/tests, package/import resolution, startup/smoke tests, docs/link checks, CI config parsing, and a search for stale old paths. Compare file counts and verify no unexpected untracked or missing files. On case-insensitive filesystems, test the final casing explicitly.

## Deliverable

Return old/new tree summaries, move map, updated consumers, commands run, validation, remaining compatibility risks, and rollback path. Invocation is by natural-language request or the host's supported skill mechanism; never assume a particular slash command or provider directory.
