---
name: package-json-checklist
description: Check package metadata, dependencies, entrypoints, and lockfiles.
---

# Package metadata checklist

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/package-json-checklist/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use before changing `package.json`, a lockfile, workspace metadata, or a package entrypoint. Read
every applicable `AGENTS.md` from the repository root through the owning package,
applying the closest file only when rules conflict. Those instructions own package-manager version,
dependency age/version policy, registry, release process, and package layout.

1. Identify the owning package and every consumer of the changed script, dependency, export, or
   binary. Prefer existing workspace utilities before adding a dependency.
2. Use the repository's package manager for dependency changes. Update the lockfile when it records
   the affected metadata; avoid lockfile churn for metadata-only edits it does not record. Keep
   peer,
   optional, development, and runtime dependencies in their intended sections.
3. For a published package, verify exports, types, files, binaries, and build output match the
   package's supported import and installation paths.
4. Run the package manager's integrity check, focused tests, typecheck, build, and local policy
   checks required by the affected package. Do not publish or alter registry state without explicit
   authorization.
5. Review the lockfile and generated metadata for unrelated churn before committing.

Local instructions or the consumer wrapper own: version range, workspace topology, registry,
package-manager command, and release convention.
