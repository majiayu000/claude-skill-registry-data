---
name: kit-typescript-rules
description: "TypeScript conventions for this project. Use when reading, writing, or reviewing files matching `**/*.ts`, `**/*.tsx`, `**/*.mts`, `**/*.cts`. Do not use for other files."
---

# TypeScript conventions

- Follow the project's `tsconfig` strictness. Do not loosen compiler options or add `@ts-ignore` / `@ts-expect-error` to silence errors without a comment explaining why.
- Avoid `any`. Use `unknown` at untrusted boundaries and narrow it with type guards or the project's validation library.
- Prefer types inferred from runtime schemas or existing declarations over duplicated hand-written types.
- Use non-null assertions (`!`) only where an invariant guarantees a value; prefer explicit checks.
- Model alternatives with discriminated unions rather than optional flags that can contradict each other.
- Keep exported APIs explicitly typed; let local variables infer.
- Match the project's module system (ESM or CommonJS) and import style, including file extensions where required.
- Handle rejected promises: await them, return them, or attach handling. Do not leave floating promises.
- Run the project's type check after changes, not only the tests.
