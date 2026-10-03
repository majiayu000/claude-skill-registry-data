---
name: tdd
description: "Use for explicit TDD or when Roblox logic has a cheap deterministic Luau regression target that can fail before the fix."
---

# TDD for Roblox

Use TDD for pure or isolated logic with an existing local test harness. Good targets include reducers, state machines, serialization, migrations, cooldown calculations, target selection, validation, wave composition, and deterministic adapters.

1. Write the smallest test that proves the reported failure or new contract.
2. Run it and record the expected failure.
3. Make the smallest implementation change.
4. Run the focused test, then the relevant suite and project assembly check.
5. Keep the test about behavior. Avoid mocks that reproduce the implementation.

Skip test-first when the repository has no suitable harness and creating one would exceed the task, or when proof requires Studio rendering, physics, networking, or input behavior. In that case, use a local deterministic probe when possible and hand the exact Studio test to the user. Never invoke Roblox Studio MCP playtest controls. `rojo build` validates assembly, not Luau runtime behavior.
