---
name: aiwf-typescript-coding
description: Use for TypeScript tsconfig, strict types, module resolution, JSX/TSX, generated types, and tsc validation.
---

# AIWF TypeScript Coding

## Core Rule

Treat TypeScript changes as both runtime JavaScript changes and static contract changes. Inspect the local TypeScript version, `tsconfig`, framework, module resolution, JSX mode, generated types, and build pipeline before editing.

## Workflow

1. Inspect `package.json`, lockfile, `tsconfig*.json`, framework config, generated type directories, API clients, lint config, and test/build commands.
2. Confirm strictness settings, module/moduleResolution, target/lib, JSX mode, path aliases, and whether files are emitted or typecheck-only.
3. Patch types at the boundary first: API inputs/outputs, component props, event handlers, async results, discriminated unions, and generated clients.
4. Avoid widening with `any`, `unknown` casts, non-null assertions, or type-only lies unless there is a documented boundary and runtime check.
5. Validate with the repo's `tsc`, lint, tests, and build.

## TypeScript Guardrails

- Preserve runtime behavior. Types should describe reality, not silence errors.
- Use discriminated unions and exhaustive checks for state machines, API variants, and UI modes.
- Keep generated types generated. Do not hand-edit generated files unless the project explicitly does so.
- Match framework rules for TSX, server/client modules, and environment types.
- Avoid changing `skipLibCheck`, `strict`, module resolution, or path aliases unless the task is a build-system fix and tests prove it.
- Add `aiwf-react-coding` when the change is TSX component behavior, not only types.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
npm run typecheck
npx tsc --noEmit
npm run lint
npm test
npm run build
```

Use the repo's package manager and configured TypeScript version; do not rely on a global `tsc`.

## Primary Source Anchors

- TypeScript documentation: https://www.typescriptlang.org/
- TypeScript repository: https://github.com/microsoft/TypeScript

Verify local compiler version and framework constraints before using the newest TypeScript syntax or flags.
