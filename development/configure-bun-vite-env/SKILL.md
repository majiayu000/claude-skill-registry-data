---
name: configure-bun-vite-env
description: >-
  Load this skill when setting up or configuring a Bun + Vite frontend: scripts, dependencies,
  TypeScript, linting, formatting. Auto-load when bun runs, or eslint.config.js, .prettierrc, or
  tsconfig.json is created or modified.
disable-model-invocation: false
user-invocable: false
compatibility: >-
  Requires `bun` on PATH (the repo's package manager and script runner; Node.js 20+ with npm works
  as a fallback) and network access to the npm registry. TypeScript, Vite, ESLint, and Prettier
  are project dev dependencies installed by `bun install`, not assumed to be global.
license: Apache-2.0
---

# Configure the Bun + Vite Environment

Keep a frontend project on Bun and Vite with strict TypeScript and one lint and format config. Done
when `lint`, `format:check`, `typecheck`, and (SvelteKit) `check` all pass.

## Procedure

1. Run scripts and change dependencies only through `bun`, and leave `bun.lock` alone.
2. Read browser-safe env vars through the framework's static env module, and keep secrets server-side.
3. Write TypeScript to the style below.
4. Before opening a PR, run the four checks under Linting and quality checks.
5. Install the pre-commit hook once per clone, per Pre-commit hook below.

## Rules

### Environment

- Runtime and package manager: **Bun** | Build tool: **Vite** | Framework: **SvelteKit** or **React**
- Lockfile: `bun.lock` — authoritative, never edit manually
- Never commit `.env`; keep a `.env.example` with placeholder values
- Browser-safe env vars are prefixed and read via the framework's static env module (`$env/static/public` in SvelteKit, `import.meta.env.VITE_*` in React+Vite). Server-only secrets never reach the client.

### Commands

| Action                                 | Command                |
| -------------------------------------- | ---------------------- |
| Install all dependencies               | `bun install`          |
| Add a production dependency            | `bun add <package>`    |
| Add a dev dependency                   | `bun add -d <package>` |
| Start dev server                       | `bun run dev`          |
| Production build                       | `bun run build`        |
| Run unit + component tests             | `bun run test`         |
| Type check (tsc)                       | `bun run typecheck`    |
| Svelte template check (SvelteKit only) | `bun run check`        |
| Lint                                   | `bun run lint`         |
| Format check                           | `bun run format:check` |

### TypeScript style

- Line length: **100 characters** (Prettier: `printWidth` 100, single quotes, `prettier-plugin-svelte`)
- Local imports use the path alias (`$lib` in SvelteKit, the configured alias in React), never deep relative paths
- Never use `any` — use `unknown` with type narrowing if the type is truly unknown
- Prefer `undefined` over `null` for optional values: optional properties and default parameters
  already produce `undefined`, so one "absent" value avoids mismatches
- Use `?.` and `??`; do not use `||` for defaults on falsy inputs (it collapses `0`, `''`, `false`)
- Set `strict: true` in `tsconfig.json`. Fix a type error instead of suppressing it with `// @ts-ignore`.

#### `type` is the default, `interface` is the exception

`type` also covers unions and aliases, and it never merges declarations by accident, so one keyword
does the job.

```ts
// Good — use type for data shapes, unions, and aliases
type Status = "active" | "archived" | "deleted";
type SessionState = { sessionId: string; items: Item[] };

// Only use interface when you intentionally need declaration merging (rare)
interface PluginExtension {
  onLoad(): void;
}
```

#### No TypeScript `enum`: use `const` assertions

An `enum` emits runtime code that behaves unlike plain JavaScript. A `const` object is a plain value
with a derived union type.

```ts
const ItemStatus = {
  Open: "open",
  Resolved: "resolved",
  Archived: "archived",
} as const;
type ItemStatus = (typeof ItemStatus)[keyof typeof ItemStatus];
```

#### JSDoc (required on all exported symbols)

```ts
/**
 * Sends a user message and returns the updated session state.
 * @param sessionId - Active session identifier.
 * @param content - User's message text.
 * @returns Updated state snapshot.
 * @throws {ApiRequestError} On non-2xx response.
 */
export async function sendMessage(
  sessionId: string,
  content: string,
): Promise<SessionState>;
```

### Linting and quality checks

All checks must pass before a PR is opened:

```bash
bun run lint          # ESLint (typescript-eslint recommended-type-checked + framework plugin)
bun run format:check  # Prettier (does not modify files)
bun run check         # svelte-check — SvelteKit only; catches template errors ESLint cannot see
bun run typecheck     # tsc --noEmit
```

`svelte-check` is not optional in SvelteKit projects — it catches prop type mismatches, missing required props, and a11y warnings ESLint cannot see.

#### Pre-commit hook

Run lint and the format check on every commit, so neither fails first in a PR. Git runs hooks from
a committed directory with no package needed: add `.githooks/pre-commit` (executable, LF line
endings) and point git at it once per clone with `git config core.hooksPath .githooks`.

```sh
#!/bin/sh
# .githooks/pre-commit
set -e
bun run lint
bun run format:check
```

`typecheck` and `check` stay out of the hook: they check the whole program, which is too slow for
every commit, so they run before the PR. Never commit with `--no-verify` to get past a hook.

#### ESLint configuration

```js
// eslint.config.js
import ts from "@typescript-eslint/eslint-plugin";
import svelte from "eslint-plugin-svelte"; // SvelteKit projects
// import react from 'eslint-plugin-react';   // React projects
// import reactHooks from 'eslint-plugin-react-hooks';

export default [
  ...ts.configs["recommended-type-checked"],
  ...svelte.configs["flat/recommended"], // or react / react-hooks configs
  {
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_" },
      ],
    },
  },
];
```
