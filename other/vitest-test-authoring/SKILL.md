---
name: vitest-test-authoring
description: Author deterministic Vitest assertions, mocks, and factories.
---

# Vitest test authoring

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/vitest-test-authoring/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Apply [test-authoring](../test-authoring/SKILL.md) first.

- Isolate tests with Vitest lifecycle hooks. Restore spies and globals after each test.
- Prefer a deterministic async assertion over a timing wait.
- Mock an external boundary. Do not mock the module under test.
- Use a typed factory when the project supplies one.
- Run the selected file or project before broader validation.
- Read [mock boundaries](references/mock-boundaries.md) when adding a module mock or changing an
  export.

Consumer wrapper owns: project selection, mock boundaries, fixture names, and coverage policy.
