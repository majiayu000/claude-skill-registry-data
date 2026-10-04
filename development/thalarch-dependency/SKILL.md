---
name: thalarch-dependency
description: >
  Safe dependency and toolchain upgrade workflow. Use when adding, replacing, or upgrading
  libraries, language runtimes, plugins, build tools, frameworks, lockfiles, or transitive
  dependency constraints. Minimizes unrelated churn and verifies version-specific APIs.
---

# Thalarch Dependency Engineering

Dependency work changes code, build behavior, and supply-chain surface. Treat it as a compatibility
migration rather than a version-number edit.

## Preflight

Identify:

- current direct/transitive version;
- version constraint and lockfile;
- runtime/compiler/toolchain compatibility;
- why the dependency is needed;
- affected code paths and generated artifacts;
- repository policy for lockfiles/vendor directories.

## Current-source rule

When internet/research tools are available, use primary current documentation, release notes,
changelogs, migration guides, and vulnerability advisories for version-sensitive decisions.

Do not assume an API exists because a newer example online uses it; verify the exact selected
version and the project's resolved graph.

## Minimal-upgrade rule

- Change only the requested/required dependency set.
- Avoid opportunistic mass updates.
- Preserve lockfile determinism.
- Do not switch package managers/build systems as part of an ordinary library upgrade.
- Separate toolchain migrations from feature work when practical.

## Compatibility matrix

Check as relevant:

- source/API compatibility;
- binary/ABI compatibility;
- runtime minimums;
- compiler/plugin compatibility;
- serialization/schema behavior;
- platform/target compatibility;
- configuration/default changes;
- transitive dependency conflicts.

## Verification

Use repository-native dependency resolution plus targeted compile/test/static analysis and the
real behavior affected by the upgrade.

For high-risk framework/toolchain upgrades, inspect deprecations/warnings and run broader build or
multi-module/target checks.

Do not call an upgrade safe when only the manifest parses. Report unresolved ecosystem or runtime
compatibility as `UNVERIFIED`.
