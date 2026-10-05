---
name: dependency-tooling
description: Manage application dependencies, build tooling, upgrades, and package configuration using ecosystem-agnostic principles.
metadata:
  internal: true
---

# dependency-tooling

Use this skill for dependency installation, removal, upgrades, build tooling, package configuration, and runtime compatibility.

## Principles

Use the project's existing package manager and lockfile conventions.

Before changing a dependency consider:

- compatibility
- supported runtime versions
- transitive dependencies
- security
- maintenance status
- migration requirements

Avoid unnecessary dependencies when existing stack capabilities are sufficient.

Keep lockfiles consistent with declared dependencies.

For major upgrades:

1. identify breaking changes
2. identify deprecated APIs
3. update incrementally when practical
4. run relevant tests
5. verify build/runtime behavior

Do not assume the newest package version is compatible with the project.

## Adaptation

Use project evidence to determine the actual language, framework, runtime, and existing conventions.

When stack-specific implementation guidance is needed, prefer project evidence, native framework or language mechanisms, and relevant user-installed specialist skills. Technology-specific guidance must not redefine or weaken the core engineering requirement.