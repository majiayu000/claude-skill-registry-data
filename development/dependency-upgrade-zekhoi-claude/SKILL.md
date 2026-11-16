---
name: kit-dependency-upgrade
description: Upgrade one or more project dependencies safely by reading their changelogs and breaking changes, updating the manifest and lockfile with the project's package manager, adapting code to API changes, and verifying with the build and tests. Use when the user asks to upgrade, update, or bump a dependency, framework, or runtime version, or to fix a vulnerable dependency version. Do not use for auditing which dependencies are vulnerable (use kit-security-audit), for adding a new dependency as part of a feature (use kit-feature-implementation), or for unrelated build failures (use kit-debugging).
---

# Dependency upgrade

## 1. Scope the upgrade

- Identify the package manager and lockfile (pnpm, npm, yarn, uv, Poetry, pip-tools, Go modules, Cargo) and use only it. Find the current and target versions; if no target was given, use the latest stable release and say so.
- Check what depends on the package (direct imports, peer dependencies, plugins tied to its major version) and whether the runtime or other packages must move with it.

## 2. Read what changed

- Read the changelog, release notes, or migration guide for every version between current and target, focusing on breaking changes, deprecations, changed defaults, and minimum runtime versions. Prefer the project's official sources: find the repository with `npm view <pkg> repository.url` (or the registry page) and fetch its releases page or `CHANGELOG.md`. If they cannot be fetched (no network), read the changelog or README shipped in the installed package (for example `node_modules/<pkg>/CHANGELOG.md` after installing the target, or the `npm view <pkg>@<version>` metadata), or compare the package's exports and types before and after; report which source you used and what you could not check.
- Search the codebase for each affected API so the changes needed are known before editing.

## 3. Upgrade

- Upgrade one package or one coupled group at a time. Use the package manager's command (`pnpm up <pkg>@<version>`, with `-r` or `--filter` in a workspace; `uv lock --upgrade-package <pkg>` within the existing constraint, or `uv add` to change it; `go get <module>@<version>` and `go mod tidy`, updating import paths to `/vN` for a Go major version) so the lockfile is regenerated, not hand-edited.
- Keep the lockfile diff limited to the target and what it requires; do not refresh unrelated dependencies.
- Adapt the code to breaking changes, replace deprecated APIs the release notes call out, and update configuration files that changed format.

## 4. Verify and report

- Run install, the build, the type checker, the linter, and the tests. Investigate new warnings that the upgrade introduced.
- Report old and new versions, the breaking changes that applied and how they were handled, changes that did not apply, verification results, and anything left for the user, such as a runtime upgrade in CI or deployment.

## Examples

- Use: "Upgrade Fastify to v5." "Bump all patch versions." "Update lodash to fix the advisory."
- Skip: "Which of our dependencies are vulnerable?" (kit-security-audit) "Add zod for validation in this new endpoint."
