---
name: tooling
description: "Set up repo tooling: monorepo (Turborepo/Nx/pnpm workspaces), micro-frontends, microservices, pre-commit hooks, lint/format/typecheck (Biome/ESLint/Ruff), test wiring and CI."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "honey-stack research 2026-10-18 (Turborepo/pnpm, Module Federation 2, Pact, Husky v9/Lefthook, ESLint 10 flat config, Biome 2, Ruff, Vitest 3). Configs in references/."
---

# tooling

Set up or standardize the plumbing of a repo. Match what's already there (package manager, existing configs, CI) before adding anything, and reach for the simplest option that fits — most of these are overkill for most projects.

## Default to boring
- **One modular app in one repo** beats a monorepo, micro-frontends, or microservices for most teams. Add complexity only when a concrete pain justifies it.
- **Monorepo tooling** (Turborepo) only when multiple shared packages make rebuilds/tests slow. Add Turborepo first (incremental, removable); reach for Nx only at enterprise scale (generators, boundary enforcement); Bazel/Moon only for large polyglot.
- **Micro-frontends** solve an *org/deploy* problem (many teams, independent deploys), not a code-splitting one. Cost: version skew, runtime integration bugs, bundle bloat. Default to a modular monolith.
- **Microservices** — extract a service only for a distinct scaling profile, independent deploy cadence, or separate team ownership. Services that must deploy together with a shared DB are a distributed monolith, worse than a monolith.

## Pick and set up

| Need | Use (default first) | Config in |
|---|---|---|
| Monorepo | pnpm workspaces + **Turborepo**; Nx (enterprise); Bazel/Moon (large polyglot) | `references/monorepo.md` |
| Versioning/publishing packages | **Changesets** | `references/monorepo.md` |
| Micro-frontend (if truly needed) | **Module Federation 2** (Webpack 5 / Rspack), Native Federation, single-spa | `references/microfrontend.md` |
| Microservices & contracts | OpenAPI / gRPC + **Pact** contract tests; docker-compose/Tilt local dev | `references/microservices.md` |
| Pre-commit hooks | **Husky + lint-staged** (JS/TS); **Lefthook** (fast/polyglot); `pre-commit` (Python/polyglot) | `references/hooks.md` |
| Lint/format/typecheck | **Biome** (new standard projects); ESLint 10 flat config + Prettier (when plugins needed); **Ruff** (Python) | `references/lint-format.md` |
| Test runner + CI glue | **Vitest 3** (or Jest 30); one GitHub Actions pipeline with Turborepo affected + remote cache | `references/ci.md` |

## Version traps (verify before relying on them)
- **ESLint 10** — flat `eslint.config.js` only; legacy `.eslintrc` removed; needs typescript-eslint v8+. Type-aware rules need `projectService: true` or they silently don't fire.
- **Turborepo 2** — the key is `tasks`, not `pipeline` (`npx @turbo/codemod rename-pipeline`).
- **Husky v9+** — `husky install`/`husky add` are gone; use `husky init`, hooks are plain scripts with no boilerplate header, and keep `"prepare": "husky"`.
- **Vitest 3** — inline `projects` in `vitest.config.ts`; `vitest.workspace.ts` is deprecated.
- **Biome 2** — type-aware linting without `tsc`; custom rules are GritQL, not JS. Don't run Biome and ESLint+Prettier on the same files.

## Keep hooks fast
Run linters on **staged files only** (lint-staged or Lefthook's `{staged_files}`), re-stage auto-fixes, add a `commit-msg` commitlint hook for Conventional Commits, and a `gitleaks` hook for secrets. Slow hooks get disabled by developers.

Done when: the tool is installed with its exact config files, its npm/CLI scripts are wired, a dry run or `--help` confirms it runs, and you've named the one or two setup mistakes avoided.
