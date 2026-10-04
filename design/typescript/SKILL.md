---
name: typescript
description: "Applies TypeScript/JavaScript rules for types, async behavior, APIs, tooling, tests, and architecture."
---

# Skill: typescript

## Purpose

Apply the shared engineering style to TypeScript and JavaScript projects while respecting existing tooling and architecture.

## Inspect First

Before changing TypeScript/JavaScript code, inspect relevant files when present:

- `package.json`
- `tsconfig.json`
- `eslint.config.*`
- `.eslintrc*`
- `prettier.config.*`
- `.prettierrc*`
- `vite.config.*`
- `next.config.*`
- `webpack.config.*`
- `vitest.config.*`
- `jest.config.*`
- lockfiles
- existing source and tests

Package manager detection:

- `pnpm-lock.yaml` -> use `pnpm`
- `yarn.lock` -> use `yarn`
- `package-lock.json` -> use `npm`
- `bun.lockb` / `bun.lock` -> use `bun` only if project uses it

Do not mix package managers.

## Style

- Follow existing module style.
- Prefer explicit types at boundaries.
- Keep modules cohesive.
- Avoid `utils` dumping grounds.
- Avoid mutation-heavy shared state.
- Avoid hidden singleton state unless project architecture intentionally uses it.
- Keep framework-specific code at framework boundaries.

## TypeScript Rules

- Prefer strict types.
- Avoid `any` unless justified.
- Use `unknown` instead of `any` for untrusted data, then narrow.
- Prefer discriminated unions for state machines and variant data.
- Prefer explicit return types for exported functions.
- Do not silence type errors with broad assertions.
- Avoid `as` casts unless narrowing cannot express the invariant; explain non-obvious casts.
- Respect existing runtime validation strategy.

## Runtime Validation

Do not assume TypeScript types validate runtime data.

For external input:

- validate at boundaries;
- use existing schema/validation library if present;
- do not introduce a new validator unless justified;
- handle invalid data explicitly.

## React / UI Code

If UI code is present:

- keep components cohesive;
- avoid god components;
- separate state management, data fetching, and presentation when complexity justifies it;
- keep side effects explicit;
- avoid over-abstraction for tiny components;
- preserve accessibility behavior.

## Node / Backend Code

If backend code is present:

- keep route handlers thin;
- validate input;
- avoid leaking internal errors;
- propagate cancellation/timeouts where supported;
- avoid blocking expensive work in request paths;
- keep persistence and business rules separated according to project architecture.

## Tests and Validation

Use existing test tooling.

Common commands, only when configured or clearly available:

```bash
pnpm test
pnpm lint
pnpm typecheck
npm test
npm run lint
npm run typecheck
yarn test
yarn lint
yarn typecheck
bun test
```

Report exact commands and results.
## Shared Cross-Ecosystem Style


Apply the shared engineering style from:

- `../../engineering/05_design_principles.md`
- `../../engineering/06_responsibility_model.md`
- `../../engineering/07_complexity_budget.md`
- `../../engineering/12_naming_bible.md`

Language-specific idioms control syntax and ecosystem details, but they must not weaken the core rules: small cohesive units, explicit boundaries, honest validation, no dumping grounds, and no fake placeholders.
