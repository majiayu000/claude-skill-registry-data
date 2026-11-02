---
name: principle-boundary-discipline
description: Apply when wiring validation, error handling or a framework adapter.
disable-model-invocation: true
---

# Boundary discipline

Check data where it enters the system and trust it after that.

- Validation, narrowing and error handling belong where data crosses a system
  boundary: CLI arguments, configuration, the network, an external API.
- At that boundary, a parse function turns raw input into typed domain values.
- Inside, trust data a boundary has validated and propagate errors rather
  than re-checking it in every layer. Add an inner check only on a failure
  path a defect has proven, as the bug-fix playbook's hardening step does.
- A public surface exposes domain concepts, never the transport, storage or
  framework types behind it.
- Business logic lives in pure functions with no framework dependencies; the
  shell around them stays thin and mechanical and only calls them.
