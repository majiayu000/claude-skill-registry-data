---
name: dependency-purpose-summary
description: Explains why each declared project dependency exists and flags packages whose purpose is unclear, unused, misplaced, or duplicated. Use when the user asks for a dependency inventory, package-purpose audit, dependency justification, or overlapping-library review.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: code-review
  task_type: review
  audience: javascript-and-typescript-maintainers
  tags:
    - dependencies
    - package-json
    - dependency-audit
    - maintainability
    - duplication
  status: draft
  side_effects: none
---

# Dependency Purpose Summary

## Purpose

Produce an evidence-backed inventory that explains the role of every declared dependency and highlights packages with unclear justification, overlapping responsibilities, suspicious placement, or no visible use.

## When to use this skill

Use this skill when:

- The user asks what the packages in a project are for.
- A maintainer wants every direct dependency justified before cleanup, handoff, or review.
- The task is to find overlapping libraries or packages with unclear purpose.
- A dependency list needs to be made understandable without changing it.

Do not use this skill when:

- The user primarily wants vulnerability, license, version-currency, or supply-chain analysis.
- The task is to remove, replace, upgrade, or install packages rather than review them.
- The user only wants transitive dependency or bundle-size analysis.

## Inputs to inspect

Start with the smallest relevant set:

- Package manifests such as `package.json`, workspace manifests, or equivalent dependency files.
- Lockfiles, only when needed to distinguish aliases, workspace links, optional packages, or transitive packages.
- Source, tests, scripts, configuration, build tooling, examples, and documentation that reference declared packages.
- Monorepo or workspace configuration that explains package scope and ownership.

Do not infer purpose from a package name alone when repository evidence is available.

## Workflow

1. Identify the review scope: one package, selected workspaces, or the whole repository. Separate direct declarations from transitive lockfile entries.
2. Inventory every declared runtime, development, peer, optional, bundled, and platform-specific dependency in scope. Preserve the manifest section and workspace that owns each declaration.
3. Search imports, requires, dynamic loads, configuration keys, command scripts, plugins, type references, tests, examples, and build or release workflows for evidence of use.
4. Assign each package a concise purpose grounded in evidence. Record the strongest file, field, or script reference and a confidence level of `high`, `medium`, or `low`.
5. Classify packages with no direct code import carefully. Configuration-only tools, CLIs, plugins, peer contracts, type packages, platform adapters, and published-package metadata may still be justified.
6. Compare packages by actual responsibility, not broad category. Flag duplication only when two or more packages materially overlap in the same scope and the repository does not demonstrate distinct roles.
7. Flag unclear-purpose packages when evidence is absent, ambiguous, generated, indirect, or limited to stale documentation. Use `needs verification` rather than claiming a package is unused.
8. Check whether each package appears in the appropriate manifest section. Report likely runtime/development/peer misclassification separately from unclear purpose.
9. Summarize findings without modifying manifests or recommending removal as a certainty. State the validation needed before any dependency change.

## Output format

Return:

```md
## Summary

Brief scope, dependency counts, and overall clarity.

## Dependency inventory

| Dependency | Declared as | Purpose | Evidence | Confidence | Assessment |
|---|---|---|---|---|---|

## Unclear or potentially duplicated packages

| Priority | Package(s) | Concern | Evidence | Next check |
|---|---|---|---|---|

## Manifest placement findings

- ...

## Validation before changes

- [ ] ...
```

Use `clear`, `needs verification`, `potential overlap`, or `possibly misplaced` in the assessment column. If no concerns are found, say so explicitly.

## Quality bar

The task is complete only when:

- Every direct dependency in scope appears exactly once in the inventory.
- Each purpose statement cites repository evidence or clearly states that evidence is missing.
- Runtime, development, peer, optional, and workspace-specific roles remain distinct.
- Duplication findings identify the overlapping responsibility and account for legitimate separate use cases.
- Unused-package claims are not based solely on a missing static import.
- Recommendations distinguish confirmed facts from hypotheses and include a safe next check.
- No dependency files are changed unless the user separately requests implementation.

## Edge cases

- In monorepos, the same package may have different purposes in different workspaces; report each ownership context.
- Framework plugins and presets may be referenced only by naming convention or configuration.
- Type-only, peer, optional, and platform-specific dependencies may not appear in ordinary runtime paths.
- Dependencies used by generated files, package-manager hooks, or external consumers require lower-confidence wording when local evidence is incomplete.
- Aliases, forks, compatibility layers, and migration periods can make apparent duplication intentional.
- A lockfile entry alone proves installation resolution, not direct purpose.

## Related skills

- `dead-code-spotter`
- `small-refactor-planner`
