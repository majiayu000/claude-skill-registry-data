---
name: nextjs-vitest-test-authoring
description: Test Next.js components, routes, and server boundaries with Vitest.
---

# Next.js Vitest test authoring

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/nextjs-vitest-test-authoring/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Apply [vitest-test-authoring](../vitest-test-authoring/SKILL.md) first.

- Mock framework navigation, headers, and server-only boundaries at the framework edge.
- Test component behavior through rendered output and user-visible state.
- Keep API-response fixtures representative. Do not test framework internals.
- Use a browser test for behavior the test runtime cannot represent.
- Read [framework boundaries](references/framework-boundaries.md) for module shape and server-only
  cases.

Consumer wrapper owns: framework mock helpers, render libraries, and route fixture conventions.
