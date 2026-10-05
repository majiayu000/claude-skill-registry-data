---
name: typescript-config
description: tsconfig.json shape for ESM/gradle Hub modules. Use when configuring TypeScript or diagnosing build errors.
---

# tsconfig.json

The generator scaffolds the canonical `tsconfig.json`. Every module uses the same shape; agents validate against it and refuse to edit it without a documented reason.

## Canonical shape

```json
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "noImplicitAny": false,
    "target": "ES2022",
    "strict": true,
    "removeComments": true,
    "sourceMap": true,
    "noLib": false,
    "allowJs": true,
    "declaration": true,
    "lib": ["ES2022"],
    "outDir": "dist",
    "typeRoots": ["node_modules/@types"],
    "esModuleInterop": true,
    "useUnknownInCatchVariables": false
  },
  "include": ["src/**/*", "test/**/*", "generated/**/*"],
  "exclude": ["dist", "node_modules"]
}
```

That's what `yo @zerobias-org/module` writes. If a module on disk differs, either it predates the current generator or it's been edited — both worth flagging.

## Why each setting matters

| Setting                                    | Reason                                                                                  |
|--------------------------------------------|-----------------------------------------------------------------------------------------|
| `module: NodeNext` + `moduleResolution: NodeNext` | ESM. Required so the compiler honors `"type": "module"` and the `.js`-suffixed imports. |
| `target: ES2022` / `lib: ["ES2022"]`        | Matches Node 22 runtime. No down-leveling.                                              |
| `strict: true`                              | All strict flags. Module code must compile cleanly under this.                          |
| `noImplicitAny: false`                      | Relaxed for generated code (the codegen emits some loose types).                        |
| `useUnknownInCatchVariables: false`         | Keeps `catch (e)` typed as `any` to match the `@zerobias-org/types-core` error pattern. |
| `declaration: true`                         | Generates `.d.ts` files into `dist/` so the npm consumer gets types.                    |
| `sourceMap: true`                           | Stack traces from `zbb testDirect` point back to TypeScript source.                     |
| `outDir: "dist"`                            | Gradle's compile task expects this; package.json's `main` is `dist/src/index.js`.       |
| `esModuleInterop: true` + `allowJs: true`   | Required for some legacy CJS deps that still appear under `node_modules`.               |
| `typeRoots: ["node_modules/@types"]`        | Explicit because no workspace hoisting — each module has its own `node_modules`.        |
| `include: src + test + generated`           | Compile sources, tests, and codegen output. Omit any and the compile fails.             |
| `exclude: dist + node_modules`              | Prevents double-compilation of build output and dependency code.                        |

## What's deliberately absent

- **`skipLibCheck`** — not enabled. The generator's deps are pinned to versions that pass strict checking. If a dep update introduces `@types` errors, fix the dep, don't paper over it.
- **`paths` / `baseUrl`** — relative imports only. Path aliases interact badly with the codegen and `tsx/esm`.
- **`incremental` / `tsBuildInfoFile`** — gradle caches the compile task; an additional layer of incremental state is just one more thing to invalidate.
- **`experimentalDecorators` / `emitDecoratorMetadata`** — no decorators in module code today. Add only if a specific module actually uses them, and document why in a PR.
- **`resolveJsonModule`** — none of the generator's stubs need it. Add per-module with a comment if you genuinely need to import `*.json`.
- **`hub-sdk` in `exclude`** — not needed. `hub-sdk/` is a sibling npm package with its own `tsconfig.json` (gitignored, written by gradle's generate task). The root `include` patterns don't reach into it.

## When to deviate

Almost never. Valid reasons:

1. Module legitimately needs a feature absent from this template (e.g. `resolveJsonModule`)
2. A dep ships broken types and you need a targeted exclude

In both cases:
- Add the option with a `//` comment explaining why
- Reference the gradle task that needs it (`compileTs`, etc.)
- Mention it in the PR description

## ESM import discipline (enforced by `module: NodeNext`)

Relative imports must end in `.js`:

```typescript
import { FooImpl } from './FooImpl.js';
import { Bar } from '../generated/model/index.js';
```

Package imports do not:

```typescript
import { LoggerEngine } from '@zerobias-org/logger';
```

`tsx/esm` (used by `.mocharc.json`) honors the same rules at test time.

## Quick validation

```bash
# Generator-canonical fields
jq -r '.compilerOptions | "module=\(.module) target=\(.target) strict=\(.strict)"' tsconfig.json
# Expect: module=NodeNext target=ES2022 strict=true

# Includes generated/ and test/
jq -r '.include[]' tsconfig.json
# Expect: src/**/*  test/**/*  generated/**/*

# tsc dry-run (gradle handles real compile)
npx tsc --noEmit
```

## Common issues

- **`Cannot find module './Foo' or its corresponding type declarations`** — relative import missing `.js` extension. Run the audit grep in `@.claude/skills/tool-requirements/SKILL.md`.
- **`Cannot find name 'describe'`** — `@types/mocha` missing or `typeRoots` removed. Restore the canonical `typeRoots` line.
- **`Module '"@zerobias-org/util-connector"' has no exported member 'ConnectionMetadata'`** — `ConnectionMetadata`/`ConnectionStatus` live in `@zerobias-org/types-core-js`, not `util-connector`. Update the import.
- **`Cannot use import statement outside a module`** — `package.json` is missing `"type": "module"`. Add it (the generator template always includes it).

## Related

- @.claude/skills/module-exports/SKILL.md — `src/index.ts` shape (re-exports + factory)
- @.claude/skills/tool-requirements/SKILL.md — `zbb compile` and audit greps
