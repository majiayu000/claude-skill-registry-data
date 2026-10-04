---
name: storybook-file-pattern-sync
description: >-
  Use when the set of Storybook story file extensions changes — adding a .stories.js, .stories.jsx
  or .stories.mjs alongside .stories.tsx, renaming a story file, or widening the stories glob in
  .storybook/main.ts. Symptoms include a new story file counted by the 100 percent coverage gate,
  flagged as an orphan by dependency-cruiser, mutated by Stryker, emitted into a declaration build,
  or linted with the wrong rule set.
---

# Storybook story file pattern sync

## Profile keys consumed

- `capabilities.storybook`
- `capabilities.mutation_testing`
- `make.test_unit_client`
- `make.test_mutation`
- `make.lint_deps`
- `make.lint_eslint`
- `quality.coverage_statements`
- `architecture.source_root`

Skip the whole skill with a recorded capability-absent note when `capabilities.storybook` is
`false`. Verify the change through the targets mapped by `make.test_unit_client` (the coverage
gate held to `quality.coverage_statements`), `make.lint_eslint`, `make.lint_deps`, and
`make.test_mutation` — skip any of them with a recorded note when the key maps to `null`, and skip
the mutation lane entirely when `capabilities.mutation_testing` is `false`. The story files the
patterns have to match live under `architecture.source_root`.

## Overview

The story glob in `.storybook/main.ts` is only one of several places that name story files. Every
other gate — coverage, mutation, orphan detection, lint scoping, declaration emit — carries its own
copy of the pattern, and a narrower copy does not error; it silently pulls a story into a gate that
was never meant to see it.

## When to use

- Adding a story in a file extension the repository has not used before.
- Widening or narrowing the `stories` glob in `.storybook/main.ts`.
- A story file appears in a coverage report, a mutation report, or a dependency-cruiser `no-orphans`
  finding.
- Not for: adding another story to an extension the repository already handles everywhere.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — `.storybook/main.ts`, `jest.config.ts` coverage exclusion, `stryker.config.mjs`
  ignore list, `scripts/ci/mutation-scope.mjs`, `eslint.config.mjs` story globs, and
  `.dependency-cruiser.js`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — only
  `.storybook/main.ts`, the `jest.config.ts` coverage exclusion and the `eslint.config.mjs` story
  globs carry the pattern; Stryker mutates a curated file allowlist rather than an extension
  pattern, and dependency-cruiser scopes Storybook by the `.storybook/` directory.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — the React
  SPA shape's set minus `scripts/ci/mutation-scope.mjs`, plus `tsconfig.dts.json`, whose `exclude`
  keeps stories out of the published declaration build.

## Quick reference

| Location                        | What the pattern controls                                   |
| ------------------------------- | ----------------------------------------------------------- |
| `.storybook/main.ts`            | Which files Storybook loads as stories                      |
| `jest.config.ts`                | Coverage exclusion under the 100 percent gate               |
| `eslint.config.mjs`             | The relaxed story rule block and ignores                    |
| `stryker.config.mjs`            | Mutation exclusion (React SPA and component-library shapes) |
| `scripts/ci/mutation-scope.mjs` | The mutated file list (React SPA shape)                     |
| `.dependency-cruiser.js`        | Orphan allowlist, no-prod-import rule                       |
| `tsconfig.dts.json`             | Declaration emit exclude (component-library shape)          |

The loader glob is the widest of these in all three repository shapes today — it accepts `js`,
`jsx`, `ts` and `tsx` (plus `mjs` in the Next.js and component-library shapes) while the downstream
configs name only `tsx` or `ts`/`tsx`. That gap is the failure mode, not a hypothetical.

## Procedure

1. Decide the extension set once and write it the same way everywhere.
2. Grep the configs together and read every hit as one diff — a config the repository does not have
   is a miss, not a hit:

   ```bash # profile-example
   grep -n "stories" .storybook/main.ts jest.config.ts stryker.config.mjs \
     eslint.config.mjs .dependency-cruiser.js tsconfig.dts.json \
     scripts/ci/mutation-scope.mjs 2>/dev/null
   ```

3. Land one real story file in the new extension in the same change. A pattern that no file
   exercises is untested, and the first such file is what discovers a missed config.
4. Run the coverage, lint, dependency-cruiser and mutation targets. The correct fix for any finding
   is to add the extension to the config that missed it — never to delete the story or to drop the
   file from a gate's scope.

## Common mistakes

- Updating the loader glob only, so Storybook renders the new file while every other gate treats it
  as production source.
- Writing the same set three different ways (`{ts,tsx}`, `@(ts|tsx)`, `\.stories\.tsx$`) and
  assuming they agree; they must be re-derived per config syntax, not copy-pasted.
- Adding the pattern with no story file to prove it, so the divergence surfaces later in CI.
- Treating a coverage or orphan finding on a story as a coverage problem rather than a config gap.
