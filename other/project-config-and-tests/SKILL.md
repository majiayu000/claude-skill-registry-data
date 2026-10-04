---
name: project-config-and-tests
description: Project overlay for config precedence, defaults, parsing, normalization, path helpers, and deterministic tests at those seams. Not for general test strategy or unrelated test implementation.
---

# Project Config And Tests

This is a composable project overlay, not a standalone implementation workflow.
Use it with matching language or discipline guidance when the main task is a
configuration contract or deterministic tests at that boundary.

For review, inspect these contracts and report findings without editing config,
tests, or process state. For implementation, apply only the requested changes
and use isolated fixtures for validation.

## When to use

The task involves configuration sources or precedence, defaults, parsing,
normalization, path resolution, or deterministic tests around those seams.

## Not for

Do not use this for general feature work (use the matching principle skill and
add `project-core-dev` only when repository-specific completion evidence is not
concrete), general test strategy (`tester-mindset`), framework-specific test
implementation, vendored dependency changes (`project-vendor-boundary`),
release-only work (`project-release-maintainer`), or environment diagnosis whose
cause has not been isolated (`project-platform-diagnose`).

## Workflow

1. Establish the contract before editing: sources, precedence, defaults, and
   the behavior of missing, empty, malformed, and unsupported values.
2. Preserve help, version, and recovery paths when they can operate safely
   without valid config. Fail fast or fail closed when continuing would be
   unsafe or would silently apply misleading behavior.
3. Separate pure parsing and normalization from environment, filesystem, and
   process-global lookup when the existing design permits it.
4. Make tests independent of ambient environment, current directory, user home,
   wall-clock time, and shared filesystem state. Use the repo's fixtures and
   temporary-directory helpers, and clean up any remaining state.
5. Cover precedence and representative missing, empty, invalid, override,
   relative, absolute, and platform-sensitive path cases that belong to the
   supported contract. Do not simulate unsupported platforms and present the
   result as observed evidence.
6. Keep defaults, example config, help text, and documentation aligned. Avoid
   printing secret values in diagnostics or test output.

## Completion

- Run the narrowest relevant config and path tests plus the checks required by
  any selected principle skill.
- Use coverage or benchmarks only when they answer a concrete risk; do not make
  percentage coverage or routine benchmarking the objective.
- Report untested platform behavior, unavailable tooling, and any remaining
  dependence on ambient state.
