---
name: engineering
description: "Engineering umbrella skill for implementation, debugging, review, architecture, and technical optimization. Use when Codex should make a technically grounded, minimally scoped, verifiable change or recommendation. Turkish triggers: yazılım mühendisliği işi, kodla veya düzelt, teknik görevi doğru akışa yönlendir."
---

# Engineering

Classify build, debug, review, refactor, or architecture work, then route to the most relevant specialist skill.

## Default checks for non-trivial work

1. State material assumptions and contradictions; do not silently choose an ambiguous interpretation.
2. Choose the simplest viable change that satisfies the stated acceptance criteria. Avoid speculative flexibility and one-use abstractions.
3. Touch only files and behavior tied to the request. Do not “clean up” unrelated code, comments, or formatting.
4. Define observable success evidence before editing and verify it afterward.

Favor evidence, small validated steps, explicit tradeoffs, and the project’s existing conventions. Do not hand-wave behavior that can be checked or hide uncertainty behind jargon.
