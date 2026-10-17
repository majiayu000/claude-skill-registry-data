---
name: dead-code-spotter
description: Finds likely unused exports, functions, CSS selectors, assets, dependencies, and obsolete files in a repository. Use when the user asks to identify dead code, unused code, stale files, unreferenced assets, cleanup candidates, or safe removal opportunities before refactoring or maintenance.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: maintenance
  task_type: review
  audience: repository-maintainers
  tags:
    - dead-code
    - cleanup
    - unused-exports
    - unused-assets
    - css
    - maintenance
  status: draft
  side_effects: none
---

# Dead Code Spotter

## Purpose

Review a repository for likely unused code and stale artifacts, separating high-confidence removal candidates from items that need human or runtime verification.

## When to use this skill

Use this skill when:

- The user asks to find dead code, unused exports, unused functions, stale modules, or obsolete files.
- The user wants a cleanup review before a refactor, migration, release, or dependency update.
- The repository may contain unreferenced CSS selectors, images, fonts, fixtures, examples, generated outputs, or documentation pages.
- The user wants evidence-backed removal candidates without immediately deleting files.

Do not use this skill when:

- The user asks for broad architecture or style review rather than cleanup candidates.
- The task is only to remove one known file or symbol.
- The repository requires runtime telemetry, production usage logs, or package registry data that is unavailable.
- Another more specific cleanup, migration, or package-publishing skill covers the requested scope better.

## Inputs to inspect

Inspect relevant files such as:

- Project manifests and entry points: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, build configs, framework configs, CLI entry files.
- Source trees: `src/`, `lib/`, `app/`, `pages/`, `components/`, `packages/`, `server/`, `client/`.
- Tests and demos: `test/`, `tests/`, `spec/`, `__tests__/`, `examples/`, `demo/`, `storybook/`, fixtures.
- Styling and templates: `css/`, `styles/`, `*.css`, `*.scss`, `*.html`, JSX/TSX/Vue/Svelte templates.
- Assets and static files: `public/`, `static/`, `assets/`, images, fonts, icons, media, generated bundles.
- Documentation and automation: `README.md`, `docs/`, `.github/workflows/`, scripts, task runners, deployment configs.
- Ignore and generated-file hints: `.gitignore`, `.npmignore`, lockfiles, build output directories.

## Workflow

1. Define the scan boundary from the user's request and repository layout. Exclude dependencies, generated directories, build output, vendored code, lockfiles, and caches unless the user explicitly includes them.
2. Identify public entry points before labeling code unused. Check manifests, routing conventions, exported package APIs, CLI binaries, framework file conventions, plugin hooks, and documented imports.
3. Build an evidence map with fast local searches. Prefer tools such as `rg`, language-aware search, typecheckers, linters, dependency analyzers, bundler reports, or existing project scripts when available.
4. Check exported symbols and functions. Compare declarations against imports, re-exports, dynamic lookups, tests, examples, docs, configuration strings, and framework conventions.
5. Check CSS selectors. Search templates, components, generated class names, CSS modules, utility-class composition, JavaScript selector strings, tests, and documentation screenshots before marking selectors unused.
6. Check assets. Search file names, hashed variants, metadata references, CSS `url()` usage, HTML/Markdown links, config references, favicons, social images, manifest icons, and runtime asset loaders.
7. Check obsolete files. Look for files disconnected from build scripts, routes, navigation, exports, docs indexes, tests, or current configuration. Treat archived examples and migration leftovers as candidates, not proof.
8. Classify each candidate by confidence:
   - **High**: no references found, not an entry point, not framework-conventional, and covered by tests or build checks.
   - **Medium**: no static references found, but dynamic use, docs use, or runtime convention is plausible.
   - **Low**: suspicious or stale, but evidence is incomplete or deletion risk is unclear.
9. Recommend the safest next action for each candidate: delete, deprecate, move to archive, add a TODO, document as public API, add a test, or run a runtime/manual verification.
10. Do not delete code unless the user explicitly asks for implementation. If implementing cleanup, remove the smallest high-confidence set first and run relevant validation.

## Output format

Return the result using this structure:

```md
## Summary

Brief outcome and overall cleanup risk.

## Findings

| Confidence | Candidate | Evidence | Risk | Recommendation |
|---|---|---|---|---|

## Safe cleanup plan

1. ...

## Needs verification

- ...

## Validation

- [ ] Static searches covered source, tests, docs, config, and assets.
- [ ] Public entry points and framework conventions were checked.
- [ ] Dynamic or runtime-only usage risks were called out.
- [ ] Recommended checks are listed before deletion.
```

If no likely dead code is found, say what was inspected and which checks supported that conclusion.

## Quality bar

The task is complete only when:

- Each finding cites concrete evidence such as a file path, export name, selector, asset name, command, or missing reference.
- Public APIs, generated files, framework conventions, and dynamic references are considered before recommending removal.
- Findings are ranked by confidence and deletion risk.
- The final answer distinguishes safe cleanup candidates from items needing manual or runtime verification.
- Validation commands or follow-up checks are recommended for any removal plan.

## Edge cases

- Dynamic imports, reflection, dependency injection, plugin registration, string-built paths, and runtime routing can hide legitimate usage from static search.
- CSS utility frameworks, CSS modules, scoped styles, generated class names, and arbitrary variants can make selector usage hard to prove.
- Assets may be referenced by metadata, favicons, web manifests, social cards, email templates, CMS data, or deployment platforms outside the repository.
- Public package exports, CLI commands, examples, and documented APIs may be used externally even when no internal references exist.
- Monorepos may reference code across package boundaries through workspace aliases or built artifacts.
- Generated files should usually be regenerated or ignored rather than manually deleted.

## Related skills

- `repo-next-steps-review`
- `project-plan-reconciler`
- `refactor-roadmap-builder`
