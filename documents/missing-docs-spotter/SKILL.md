---
name: missing-docs-spotter
description: Identifies public APIs, configuration options, events, behaviors, and useful examples that exist in code but are absent from Markdown or HTML documentation. Use when the user asks for documentation coverage gaps, undocumented exports or options, code-to-docs comparison, or a list of missing README, guide, reference, or example content.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: docs-seo
  task_type: review
  audience: library-and-documentation-maintainers
  tags:
    - documentation
    - api-coverage
    - code-to-docs
    - readme
    - examples
    - developer-experience
  status: draft
  side_effects: none
---

# Missing Docs Spotter

## Purpose

Compare a repository's implemented public surface with its Markdown and HTML documentation, then report specific APIs, options, events, behaviors, or examples that users can access in code but cannot discover or understand from the docs.

This is a review-first skill. It identifies coverage gaps and recommends the smallest useful documentation destination; it does not edit documentation unless the user explicitly asks for implementation.

## When to use this skill

Use this skill when:

- The user asks which public features are undocumented.
- A package needs a code-to-documentation coverage review.
- The README, guides, API reference, or examples may be behind the implementation.
- The repository exposes options, callbacks, events, methods, commands, attributes, or return values that users need to know about.
- The user wants evidence-backed documentation TODOs before a release.

Do not use this skill when:

- The task is only to improve documentation navigation, metadata, or search discoverability.
- The user only wants to check whether one recent code diff requires a README update; use `readme-change-sync` instead.
- The task is to find unused code rather than undocumented public code.
- The user wants prose editing without a code-to-docs comparison.

## Inputs to inspect

Start with the smallest files that define the supported public contract.

### Public implementation surface

- package entry points and export maps, such as `package.json`
- exported modules, functions, classes, types, constants, and components
- public constructors, methods, properties, parameters, and return values
- configuration schemas, defaults, option types, and validation logic
- emitted events, callbacks, hooks, custom events, and payload shapes
- CLI commands, flags, environment variables, attributes, and data attributes
- public error behavior, lifecycle requirements, and cleanup methods
- tests and fixtures that demonstrate supported user-facing behavior

### Documentation surface

- `README.md` and package-level README files
- Markdown files under `docs/`, `guides/`, or similar directories
- HTML documentation and demo pages
- example source files and explanatory copy
- generated API reference sources or output, when present
- migration guides, troubleshooting pages, and changelogs when they serve as user guidance

Ignore internal implementation details unless they are exported, supported, or required for correct public usage.

## Workflow

1. Define scope. Identify the package, entry points, documentation formats, and intended public audience. State any excluded generated files or private modules.
2. Build a public-surface inventory from authoritative code and configuration. Record each item with its source file and the evidence that makes it public.
3. Group related details into user-meaningful units: APIs, options and defaults, events and payloads, lifecycle behavior, errors, and example-worthy workflows.
4. Inventory the relevant Markdown and HTML documentation. Treat a symbol name appearing in navigation, generated indexes, or source snippets as a lead, not proof of adequate documentation.
5. Map each public unit to documentation evidence. Classify it as:
   - `covered`: users can find its purpose and essential usage
   - `partial`: named or shown, but missing important contract details
   - `missing`: no meaningful documentation found
   - `uncertain`: public status or documentation coverage cannot be established confidently
6. Validate each gap against tests, types, defaults, schemas, and call sites. Do not infer a supported contract from an internal helper or incidental implementation.
7. Prioritize confirmed gaps by user impact:
   - `high`: required for installation, basic use, safe use, compatibility, or avoiding failure
   - `medium`: meaningful feature, option, event, or common workflow
   - `low`: advanced, uncommon, or convenience behavior
8. Recommend one suitable destination for each gap, such as the README, API reference, guide, example, migration note, or troubleshooting page. Avoid duplicating the same full explanation across multiple files.
9. Report uncertainties separately and name the evidence needed to resolve them.

## Coverage rules

- A bare symbol name is not sufficient coverage.
- A code example may cover basic usage but still omit options, defaults, event payloads, errors, cleanup, or accessibility requirements.
- Type declarations document shape, but not necessarily purpose, timing, side effects, constraints, or realistic usage.
- Generated API docs count only when users can access them and they contain useful contract information.
- Tests are implementation evidence, not user documentation.
- Deprecated or compatibility-only APIs need deprecation or migration guidance rather than ordinary feature promotion.
- Do not require documentation for private helpers, test utilities, build internals, or unsupported implementation details.

## Output format

Return:

```md
## Summary

Scope reviewed, number of confirmed gaps, and the most consequential omission.

## Documentation gaps

| Priority | Public surface | Coverage | Code evidence | Docs checked | Missing information | Recommended destination |
|---|---|---|---|---|---|---|

## Uncertain items

| Item | Why uncertain | Evidence needed |
|---|---|---|

## Recommended documentation order

1. ...

## Validation notes

- Scope limitations, generated-doc caveats, and areas checked with no gaps.
```

Use repository-relative paths and line references when available. If no gaps are confirmed, say so and list the public and documentation surfaces checked.

## Quality bar

The task is complete only when:

- Public-surface claims are supported by exports, schemas, types, tests, or other authoritative code evidence.
- Every confirmed gap names the documentation files or areas searched.
- Missing, partial, covered, and uncertain items are not conflated.
- Findings explain what users need to learn, not merely which symbol is absent.
- Recommendations identify an appropriate documentation destination and avoid unnecessary duplication.
- High-impact gaps appear before completeness polish.
- Internal details are excluded unless they affect the supported public contract.

## Edge cases

- For monorepos, review one package at a time unless cross-package scope is explicit.
- For dynamic exports, generated clients, reflection, or metaprogramming, report inventory limits and inspect generation sources where available.
- For overloaded APIs or framework adapters, compare each supported public variant separately.
- For localized or versioned docs, identify the canonical language and version before declaring a gap.
- For HTML containing rendered Markdown or generated API output, avoid counting the same content twice.
- If documentation lives outside the repository and is unavailable, report only repository-local coverage and do not claim the external docs are missing.

## Related skills

- `readme-change-sync`
- `docs-discoverability-audit`
- `developer-note-writer`

