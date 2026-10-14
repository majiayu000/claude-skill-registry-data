---
name: package-management
description: "Package management: uv/pip/pyproject, Maven/Gradle, npm/pnpm/yarn/bun, Cargo, go.mod. Lockfiles, scopes, workspaces. Never bump versions casually."
---

# package-management

Lockfiles committed, versions pinned deliberately, bumps reviewed like code.

## Activate when

- Adding/updating/removing dependencies, setting up workspaces, or fixing resolution conflicts.

## Do NOT activate for

- Dependency selection audits (see research/dependency-evaluation); build failures (see build-systems).

## Inspection

Read the manifest + lockfile state: direct vs transitive, version ranges vs pins, workspace boundaries, and what the failing or proposed change touches.

## Decision rules

- Lockfiles always committed; ranges narrow and deliberate; bumps are PRs with changelog + test evidence, never drive-bys.
- One manager per ecosystem per repo (uv OR pip, npm OR pnpm OR yarn OR bun); workspaces declare boundaries the tooling enforces.
- Scopes correct (dev vs prod vs peer); no dev-only packages in production images; no committed secrets in rc files or mirror configs.

## Procedure

1. Change the manifest minimally; update the lockfile with the project's tool (never hand-edit).
2. Review the lockfile diff (new packages, version jumps, removed entries) like code.
3. Run the full verification (install from scratch + tests) before merging.
4. Verify: clean install green, lockfile diff sane, audit clean or triaged.

## Failure modes

- Uncommitted lockfiles ("works on my machine"); range drift breaking CI overnight; mixed managers in one repo; phantom dependencies (undeclared but resolvable); bump PRs without test runs.

## Escalation

Ecosystem specifics via registry (uv, npm, pnpm, bun, maven, gradle, cargo); version facts → research/documentation-search.

## References

- Registry: `../../research/documentation-search/references/framework-registry.yaml`.
- Related: `../type-checking/` (tool configs), `../../research/dependency-evaluation/`.
