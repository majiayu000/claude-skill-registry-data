---
name: swift-test-authoring
description: Test Swift and SwiftUI state, networking, and view behavior.
---

# Swift test authoring

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/swift-test-authoring/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Apply [test-authoring](../test-authoring/SKILL.md).

- Test public behavior with deterministic inputs and injected dependencies.
- For SwiftUI, inspect or interact through the project's supported test approach.
- For networking, use a protocol-level test double. Keep request and response synchronization
  explicit.
- Avoid sleeps and global state. Keep fixtures small enough that a failure is readable.
- Read [network test doubles](references/network-test-doubles.md) for cancellation and shared-state
  safety.

Consumer wrapper owns: test targets, coverage thresholds, view-inspection libraries, and fixture
APIs.
