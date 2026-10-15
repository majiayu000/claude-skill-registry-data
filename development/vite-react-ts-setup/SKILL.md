---
name: vite-react-ts-setup
description: >-
  Set up, audit, harden, upgrade or migrate Vite + React + TypeScript repos (pnpm default; npm/yarn/bun supported): ESLint 9, Vitest, Tailwind 4, CRA migration, framework choice. Use for new React apps or reviewing Vite repos.
---

# Vite + React + TypeScript Setup

Use this skill to choose the correct Vite-based branch first, then scaffold, audit, harden, or migrate the repo with modern defaults.

## Working model

1. Classify the request and repo.
   - Greenfield or existing repo?
   - Raw Vite SPA or framework/starter built on Vite?
   - Single package or monorepo/workspace?
   - Plain client app, or likely SSR/server functions/RSC?

2. Inspect before editing.
   - Detect package manager, lockfile, and `packageManager` field.
   - Detect Node/runtime pinning.
   - Detect Vite/React/TypeScript shape.
   - Detect lint/test/format/hooks/CI state.
   - Detect framework-specific files such as `react-router.config.*`, route modules, server adapters, or `@vitejs/plugin-rsc`.

3. Choose the branch.
   - **Raw Vite SPA**: use `references/scaffolding-and-variants.md`, `references/tsconfig.md`, `references/eslint.md`, `references/prettier.md`, `references/husky.md`, `references/vitest.md`, `references/package-scripts.md`, and `references/ci-github-actions.md`.
   - **Framework or advanced branch**: use `references/frameworks.md`.
   - **Monorepo/workspace**: use `references/monorepo.md`.
   - **Migration**: use `references/migrations.md` and `references/runtime-and-package-managers.md`.
   - **Optional Tailwind CSS 4**: use `references/tailwind-v4.md`.

4. Apply changes conservatively.
   - Preserve working architecture unless the user explicitly wants a migration.
   - Do not add React Compiler, Tailwind, RSC, SSR, or framework conventions during a basic lint/test/tooling audit unless the repo already uses them or the user asks for them.
   - Do not force pnpm migration if the repo intentionally uses npm, Yarn, or Bun. Prefer pnpm for new repos.

5. Verify with the smallest relevant command set.
   - Install.
   - Lint.
   - Typecheck.
   - Test.
   - Build.

## Default stance

- Prefer a React framework or starter when the app needs SSR, route modules, loaders/actions, static prerender, server functions, or is likely to need them soon.
- Prefer raw Vite for pure SPAs, internal tools, component playgrounds, and teams that want minimal conventions.
- Prefer pnpm for new repos, but respect the repo's current package manager unless the user wants migration or the repo is inconsistent.
- Prefer `eslint.config.js` or `eslint.config.mjs` as the safe default. Use `eslint.config.ts` only when the repo intentionally wants it and the runtime/setup supports it.
- Prefer typed linting for production-ish apps, but do not force it in every prototype or giant monorepo. It is slower and should be justified.
- Prefer `tsc -b` or an equivalent explicit typecheck step separate from Vite. Vite does not do full typechecking.
- Prefer explicit version/risk checks when the task depends on current package versions, Node floors, or security patches.

## Quick inspection

Run or emulate these checks before proposing changes:

```bash
ls -la package.json pnpm-lock.yaml package-lock.json npm-shrinkwrap.json yarn.lock bun.lockb bun.lock pnpm-workspace.yaml .nvmrc .node-version 2>/dev/null
cat package.json
find . -maxdepth 2 \( -name 'vite.config.*' -o -name 'react-router.config.*' -o -name 'eslint.config.*' -o -name 'tsconfig*.json' -o -name 'vitest.config.*' -o -name '.prettierrc*' -o -name '.editorconfig' -o -path '*/.husky/*' -o -path './.github/*' \)
```

If it is a monorepo, inspect package boundaries before suggesting root-level scripts or config moves.

## Guardrails and edge cases

- Do not assume raw Vite is the right answer just because the user says “React + Vite”. Check whether a framework branch is more appropriate.
- Do not replace a framework starter's build pipeline with `vite build`. React Router framework mode, Vike, RedwoodSDK, and similar setups have their own expectations.
- Do not assume `eslint.config.ts` is friction-free. It has runtime-specific requirements; JavaScript config files are the safe default.
- Do not assume `vitest.workspace.*` is the preferred monorepo setup. Use `test.projects`.
- Do not assume path alias plugins are still required. Vite can now resolve `tsconfig.paths` directly, but that feature has a performance cost and is not always the best choice.
- Treat React Server Components as an advanced/high-risk branch. If the repo uses RSC, verify patched versions before recommending changes.
- If the repo already uses TanStack Router, React Router framework mode, Vike, or RedwoodSDK, preserve that architecture unless the user explicitly requests a migration.
- When the user asks for “latest” versions or current recommendations, verify them from current official docs before pinning or naming versions.

## Output shape

For a **greenfield setup**:
1. State the chosen branch and why.
2. List the files/configs to create or update.
3. Give install commands and scripts only for that branch.
4. End with verification commands.

For an **audit**:
1. Report what was detected.
2. Report what is missing, inconsistent, outdated, or risky.
3. Recommend the smallest set of changes first.
4. End with verification commands.

For a **migration**:
1. State the source setup and target setup.
2. List breaking changes or likely manual work.
3. Give ordered migration steps.
4. End with verification commands and rollback notes when useful.

## Resource map

- `references/scaffolding-and-variants.md`: raw Vite, starter choices, plugin selection, alias strategy, and low-level SSR cautions.
- `references/frameworks.md`: React Router modes, TanStack Router/Start, Vike, RedwoodSDK, React Compiler, and RSC.
- `references/runtime-and-package-managers.md`: Node and package manager strategy, Corepack, pnpm pinning, and migrations to pnpm.
- `references/tsconfig.md`: modern split TypeScript config for Vite apps and optional stricter flags.
- `references/eslint.md`: ESLint 9 flat config, typed linting, TS config file caveats, and compiler-aware linting guidance.
- `references/prettier.md`: Prettier, EditorConfig, and formatting strategy.
- `references/husky.md`: Husky and lint-staged with local-hook guardrails.
- `references/vitest.md`: Vitest 4, Browser Mode, coverage, and monorepo projects.
- `references/package-scripts.md`: scripts for raw Vite apps, framework starters, and monorepos.
- `references/ci-github-actions.md`: GitHub Actions with explicit Node pinning and pnpm-aware caching.
- `references/monorepo.md`: pnpm workspaces, `workspace:` protocol, shared lockfile strategy, and filtered commands.
- `references/migrations.md`: CRA to Vite, older Vite to current Vite, ESLint flat-config migration, and Vitest projects migration.
- `references/tailwind-v4.md`: optional Tailwind CSS 4 integration for Vite.
- `references/audit-checklist.md`: high-signal audit checklist and common red flags.

## Verification

Always end with the smallest relevant verification set. Adapt commands to the repo's actual package manager and starter:

```bash
pnpm install
pnpm lint
pnpm typecheck
pnpm test --run
pnpm build
```
