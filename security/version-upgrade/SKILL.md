---
name: version-upgrade
description: Safely plan and apply a project release version bump with ecosystem-aware file discovery, previewed diffs, changelog evidence, validation, and rollback. Use.
---

# Safe Version Upgrade

Prepare releases without blind repository-wide replacement. Preserve behavior and make every edit reviewable.

## Operating rules

1. Inspect the repository, package ecosystem, current version sources, release policy, tags, and dirty-worktree state.
2. Treat one ecosystem-native manifest as the version authority when the project defines one. Record derived files separately.
3. Determine the target from the user's explicit version or release policy. If neither exists, infer a recommendation from actual changes but do not silently choose a major bump.
4. Build a change plan listing every file, old value, new value, reason, and validation command.
5. Before mutation, preserve the dirty worktree and create a timestamped backup of every file to be edited outside version control. Never discard unrelated user changes.
6. Apply narrow, syntax-aware edits. Do not replace arbitrary version-looking strings, dependency versions, API versions, schema versions, fixtures, or historical documentation.
7. Generate changelog entries only from verified commits, issues, and diffs. Separate breaking changes, features, fixes, security, deprecations, and migrations. Never invent entries.
8. Regenerate lockfiles or generated metadata only with the project's existing package manager and only when the requested release requires it.
9. Run parser checks, project tests, version-consistency checks, and packaging/build checks proportionate to risk.
10. Show the final diff, commands run, validation results, remaining risks, and exact rollback path.

## Authority boundaries

- A request to prepare or bump a version authorizes the scoped file edits and local validation, not publishing a release.
- Do not push, publish packages, create a hosted release, sign artifacts, or change remote state without explicit authorization.
- Do not commit or tag unless the user requested it. If requested, verify the final diff and tests immediately before doing so.
- Never expose tokens, signing keys, registry credentials, or private changelog material.

## Ecosystem discovery

Prefer authoritative files already used by the project, such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` plus release metadata, `.csproj`, Gradle files, or a dedicated version file. Follow repository instructions and existing release automation. Verify current official tooling documentation when behavior may have changed.

## Completion gate

A release bump is complete only when:

- the declared target is consistent across authoritative and derived files;
- unrelated numbers and dependencies are unchanged;
- changelog claims are traceable to evidence;
- required tests/builds pass or failures are reported with logs;
- no publish, push, tag, or commit occurred outside the user's authorization;
- rollback instructions identify the backup or reversible commit.
