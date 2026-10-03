---
name: ls-typescript-code-quality
description: "Guide TypeScript code quality work. Use when touching TypeScript, TSX, tsconfig, typed ESLint or Biome config, Node TypeScript scripts, or TypeScript-heavy framework code."
metadata:
  version: "1.0"
---

# TypeScript Code Quality

Use this skill when reviewing or changing TypeScript projects, TSX UI code,
TypeScript configuration, typed linting, Node TypeScript scripts, or frameworks
whose behavior depends on TypeScript tooling.

## Start With The Pinned Toolchain

Before recommending upgrades or changing compiler/linter settings, inspect the
project's actual toolchain:

- `package.json`: package manager, scripts, `type`, `engines`, framework packages,
  TypeScript, ESLint, typescript-eslint, Biome, build tools, and test runners.
- Lockfile: confirm the installed versions rather than assuming the manifest was
  resolved recently.
- TypeScript configs: `tsconfig.json`, project references, framework-specific
  configs, and separate lint/test/build configs.
- Framework version: Next.js, Vite, Angular, SvelteKit, Remix, NestJS, or other
  toolchains may pin TypeScript, Node, module resolution, JSX, or build behavior.
- Existing commands: prefer the repo's scripts (`typecheck`, `lint`, `test`,
  `build`) over ad hoc runner invocations.

Do not upgrade TypeScript, Node, framework packages, or lint presets just because
a newer version exists. Treat framework and lockfile compatibility as the first
constraint.

When a TypeScript project needs a Node runtime baseline, target the latest
available production LTS line that the project's framework and deployment
platform support. Prefer Active LTS over Maintenance LTS, and do not choose a
Current release line for production unless the project explicitly requires it.

## Type Safety Rules

- Keep `strict` enabled for new code unless the project has a documented staged
  migration plan.
- Consider `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`,
  `noImplicitOverride`, and `noFallthroughCasesInSwitch` when the project can
  absorb the added friction.
- Avoid `any`, double assertions, broad object types, and `Function`. If an escape
  hatch is necessary, keep it local and add a short reason.
- Prefer discriminated unions, `unknown` plus narrowing, branded IDs where useful,
  and explicit return types on exported APIs.
- Validate external boundaries at runtime: CLI args, env vars, JSON, HTTP payloads,
  database rows, localStorage, queue messages, and plugin input.
- Keep generated types, schema validators, and API clients in sync. Do not edit
  generated files by hand unless the repo explicitly does so.

## Async, Errors, And Boundaries

- Await promises intentionally; do not leave floating promises unless a lint rule
  and local pattern mark them safe.
- Preserve causal error context with `cause` or wrapped messages when crossing
  module boundaries.
- Model recoverable failures as typed results only when that pattern already
  exists; otherwise use exceptions with actionable messages.
- Add cancellation, timeout, and cleanup behavior for long-running IO.
- Keep framework server/client boundaries clear. Do not import server-only modules
  into browser bundles or browser globals into Node-only code.

## Linting And Formatting

- Prefer typed linting when the project already uses ESLint with
  typescript-eslint and performance is acceptable.
- For typescript-eslint v8 and newer, prefer `parserOptions.projectService: true`
  unless the repo already has a stable `project` or `tsconfig.eslint.json` setup.
- With Biome, preserve the existing formatter/linter contract. If Biome is the
  only linter, keep `tsc --noEmit` or the framework type checker as the type
  safety gate.
- Keep formatting changes separate from semantic changes when the diff would be
  noisy.
- Do not replace a working ESLint/Biome setup without a project-specific reason.

## Module And Import Hygiene

- Match the repo's module system: CommonJS, ESM, `nodenext`, `bundler`, or
  framework-specific defaults.
- Do not change `module`, `moduleResolution`, `jsx`, `paths`, or package
  `exports` without checking runtime and bundler behavior.
- Prefer `import type` for type-only imports, especially when native Node type
  stripping, `verbatimModuleSyntax`, or isolated emit is in play.
- Keep path aliases consistent across TypeScript, bundler, test runner, and
  runtime. If one tool cannot resolve an alias, fix the shared config rather than
  scattering relative imports.
- Avoid deep imports from package internals unless the package documents them.

## Size And Maintainability Review

Use heuristics to decide where to focus, not as hard rules:

- Files over about 300 lines deserve a scan for mixed responsibilities.
- Functions over about 50 lines deserve a scan for hidden phases, nested control
  flow, and implicit state.
- Types that require repeated assertions or helper overloads may need a simpler
  domain model.
- React/TSX components that mix fetching, state orchestration, rendering, and
  formatting are good candidates for extraction.
- Shared utility modules should have focused names and low dependency fan-in.

## Validation

Prefer repo-native scripts, in this order when available:

```bash
npm run typecheck
npm run lint
npm test
npm run build
```

Adapt for the package manager (`pnpm`, `yarn`, `bun`) and monorepo task runner
already in use. If a repository script is missing, use a direct tool invocation
only after confirming that the specific tool is declared in the project
manifest, resolved by the lockfile, and installed locally. Use the repository
package manager's documented local-only mode that fails when the executable is
missing.

Do not use acquisition-capable fallbacks such as `npx`, default `npm exec`,
`pnpm dlx`, `yarn dlx`, or `bunx` to fill a missing validation tool. If the
executable is absent or local-only behavior is uncertain, stop and surface an
explicit dependency decision. Add or change the dependency only through the
repository package manager and lockfile after the required approval and
dependency-security review.

For framework projects, also run the framework build or checker that the repo
uses in CI. Record any skipped checks and why.

## Reference

- [TypeScript quality standards snapshot](./references/typescript-quality-standards.md)

## Strict Mode Refresh Note

For strict-mode work, inspect the current `tsconfig` inheritance tree before changing compiler options. Treat `strict` as the umbrella setting, and evaluate stricter flags such as `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` only when the project can absorb the migration.
