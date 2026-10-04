---
name: dart-resolve-package-conflicts
description: Workflow for fixing package version conflicts. Use this when `pub get` fails due to incompatible package versions.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Fri, 24 Apr 2026 15:11:14 GMT
---

## Contents
- [Core Concepts](#core-concepts)
- [Version Constraints](#version-constraints)
- [Workflow: Auditing Dependencies](#workflow-auditing-dependencies)
- [Workflow: Upgrading Dependencies](#workflow-upgrading-dependencies)
- [Workflow: Resolving Version Conflicts](#workflow-resolving-version-conflicts)
- [Examples](#examples)

## Core Concepts
Dart enforces a strict single-version rule: a project and all its transitive dependencies must resolve to a single, shared version of any given package.

Understand `dart pub outdated` columns:
*   **Current:** Version in `pubspec.lock`.
*   **Upgradable:** Latest version allowed by `pubspec.yaml` constraints.
*   **Resolvable:** Latest version factoring in all other dependencies.
*   **Latest:** Latest published version (excluding prereleases).

## Version Constraints
*   **Use Caret Syntax:** Always use `^1.2.3` for dependencies.
*   **Tighten Dev Dependencies:** Set lower bound to exact version currently used.
*   **Enforce Lockfiles in CI:** Use `dart pub get --enforce-lockfile`.

## Workflow: Auditing Dependencies
- [ ] Run `dart pub outdated`.
- [ ] Review **Upgradable** column.
- [ ] Review **Resolvable** column.
- [ ] Identify retracted or discontinued packages.

## Workflow: Upgrading Dependencies
- [ ] **If updating to "Upgradable" versions:**
  - [ ] Run `dart pub upgrade`.
  - [ ] Run `dart pub upgrade --tighten`.
- [ ] **If updating to "Resolvable" versions (Major updates):**
  - [ ] Manually edit `pubspec.yaml` to bump the version constraint.
  - [ ] Run `dart pub upgrade`.
- [ ] **Feedback Loop:**
  - [ ] Run `dart analyze` -> review errors -> fix.
  - [ ] Run `dart test` -> review failures -> fix.

## Workflow: Resolving Version Conflicts
**NEVER** delete the entire `pubspec.lock` file.

- [ ] Open `pubspec.lock`.
- [ ] Locate the specific YAML block for the conflicting package.
- [ ] Delete ONLY that package's entry from the lockfile.
- [ ] Run `dart pub get`.
- [ ] **Feedback Loop:**
  - [ ] Run `dart pub deps` -> verify the dependency graph.
  - [ ] If resolution fails, update its constraint in `pubspec.yaml` and retry.

### Example: Tightening Constraints
```bash
dart pub upgrade --tighten http
```
```yaml
# Before: http: ^0.13.0
# After:  http: ^0.13.5
```

### Example: Surgical Lockfile Removal
Delete only the conflicting package block from `pubspec.lock`, leave others untouched, then run `dart pub get`.
