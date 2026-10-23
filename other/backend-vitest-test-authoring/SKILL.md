---
name: backend-vitest-test-authoring
description: Test backend persistence, providers, services, and queues with Vitest.
---

# Backend Vitest test authoring

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/backend-vitest-test-authoring/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Apply [vitest-test-authoring](../vitest-test-authoring/SKILL.md) first.

- Exercise a real integration boundary only when the test environment controls its lifecycle.
  Otherwise mock the network or provider edge.
- Randomize fixture identities where a shared store can collide.
- Assert authorization and retry behavior at the boundary.
- Clean up resources deterministically.
- Read [integration boundaries](references/integration-boundaries.md) for fixture and collision
  safety.

Consumer wrapper owns: database setup, queue providers, test projects, and rate-limit policy.
