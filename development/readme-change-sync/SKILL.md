---
name: readme-change-sync
description: Reviews a code change to determine whether README documentation must be updated. Use when a diff, pull request, feature, fix, refactor, or release changes public imports, installation, usage examples, options, defaults, events, callbacks, browser or runtime support, compatibility behavior, or other user-facing contracts.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: docs-seo
  task_type: review
  audience: package-maintainers
  tags:
    - readme
    - documentation
    - code-diff
    - api-contracts
    - examples
    - compatibility
  status: draft
  side_effects: none
---

# README Change Sync

## Purpose

Compare a code change with the repository's README and identify documentation that became missing, stale, misleading, or newly necessary. Focus on user-visible contracts rather than assuming every internal change needs a README edit.

This skill is review-first. Do not edit documentation unless the user explicitly requests implementation.

## When to use this skill

Use this skill when:

- A pull request, branch, commit, or working-tree diff may affect documented behavior.
- A public API, import path, option, default, event, callback, command, or return value changed.
- Installation, initialization, examples, or compatibility requirements may have changed.
- The user asks whether a code change also requires a README update.
- A release review needs to verify that README guidance still matches implementation.

Do not use this skill when:

- The task is a general README quality or discoverability audit without a specific code change.
- The change is demonstrably internal and preserves every documented user-facing contract.
- The user wants broad documentation architecture or SEO analysis.
- The task is only to write release notes or a changelog entry.

## Inputs to inspect

Inspect the smallest relevant set of available evidence:

- the target diff, commit, pull request patch, or changed-file list
- `README.md` and package-level README files
- public entry points and export declarations
- changed source files, types, schemas, and configuration
- tests that demonstrate new or changed behavior
- `package.json` or equivalent package metadata
- examples, demos, and documentation linked from the README
- compatibility configuration such as engines, browsers, peer dependencies, and supported runtimes
- migration notes or changelog entries when they clarify intent

If no concrete change evidence is available, state that the result is provisional and list what is needed for a reliable comparison.

## Workflow

1. Define the change boundary.
   - Identify the exact diff, commit range, pull request, or changed files under review.
   - Separate production behavior changes from tests, formatting, generated output, and internal refactors.

2. Extract user-visible contract changes.
   Check whether the change adds, removes, renames, or alters:
   - package names, entry points, import paths, exports, or initialization
   - installation steps, peer dependencies, environment requirements, or setup order
   - functions, methods, parameters, return values, types, or accepted inputs
   - options, allowed values, defaults, validation rules, or option interactions
   - events, event names, payloads, callbacks, lifecycle timing, or error behavior
   - commands, flags, output, configuration keys, or environment variables
   - browser, framework, runtime, platform, or version compatibility
   - accessibility, security, performance, or progressive-enhancement behavior explicitly promised by the README

3. Locate matching README claims.
   - Search headings, prose, tables, code blocks, badges, links, and compatibility notes.
   - Trace README examples through their imports, setup, options, events, and expected results.
   - Include package-level README files when a monorepo has more than one documentation owner.

4. Compare implementation evidence with documentation.
   Classify each relevant contract as:
   - `update required`: existing README content is now inaccurate or incomplete
   - `addition required`: a new public capability or requirement lacks essential guidance
   - `no update required`: the README remains accurate and sufficient
   - `uncertain`: intent or public exposure cannot be established from available evidence

5. Apply a README-worthiness test.
   Recommend a README change when users need the information to install, import, configure, invoke, understand, or safely upgrade the project. Do not require README coverage for every implementation detail; route detailed API material to dedicated docs when the README should only provide an entry point or concise example.

6. Specify the smallest coherent documentation change.
   - Name the README section or code example affected.
   - State what must change and why.
   - Preserve the repository's terminology and example style.
   - Identify related examples or linked docs that would otherwise contradict the README.

7. Validate the conclusion.
   - Recheck every changed public contract against the README.
   - Confirm unchanged examples still compile or plausibly match the current API when validation tools are available.
   - Distinguish evidence from inference and avoid claiming compatibility that the repository does not establish.

## Output format

Return:

```md
## Summary

README update required: Yes | No | Uncertain

Brief explanation of the decision and the user-visible change boundary.

## Findings

| Priority | Change evidence | README location | Status | Required update |
|---|---|---|---|---|
| ... | ... | ... | update required / addition required / no update required / uncertain | ... |

## Recommended changes

- `README.md` — section or example: exact documentation adjustment and reason.

## Validation

- [ ] Imports and installation instructions match current package entry points.
- [ ] Examples use current APIs, options, defaults, and events.
- [ ] Compatibility notes match repository evidence.
- [ ] Linked examples or detailed docs do not contradict the README.
```

If no README update is required, explain why the change is internal or already documented and still list the contracts checked. If evidence is insufficient, identify the missing diff, API intent, or compatibility source.

## Quality bar

The task is complete only when:

- The review is anchored to a specific code change.
- Every required update cites both implementation evidence and a README location or documented omission.
- Imports, examples, options, events, and compatibility are explicitly considered when relevant.
- Required corrections are separated from optional documentation improvements.
- A `No` conclusion names the user-facing contracts checked rather than relying on the absence of obvious changes.
- Recommendations are minimal, actionable, and consistent with the README's role.
- No files are edited unless the user explicitly asks for implementation.

## Edge cases

- In monorepos, determine which root or package README owns the changed contract.
- Generated README sections should be fixed at their source rather than edited only in generated output.
- Type-only changes can require documentation updates when they alter accepted inputs or public TypeScript usage.
- A bug fix may require an example or compatibility correction if the README documented the previous behavior.
- New advanced APIs may need only a README link to detailed documentation, not a full reference section.
- Breaking changes usually require migration or changelog documentation in addition to README synchronization; report that boundary without expanding this review into a release audit.
- If tests and implementation disagree, mark the documentation decision uncertain and report the contradiction.

## Related skills

- `docs-discoverability-audit`
- `repo-demo-copywriter`
- `before-after-diff-summary`
- `repository-area-impact-planner`
