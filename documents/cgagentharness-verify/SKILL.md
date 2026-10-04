---
name: cgagentharness-verify
description: Verify CG-agent-harness backend, native desktop and local model behavior using isolated fixtures and evidence tied to the tested source and binary. Use for smoke tests, regression checks or release acceptance.
---

# Verify the harness

Read `AGENTS.md`, `INVARIANTS.md`, current CI and nearest tests. Identify the real
checkout, source SHA, dirty state, binary and architecture. Preserve operator
homes/services. Inspect fixtures and current test assertions.

Choose checks by the changed contract:
- Backend quality: root-toolchain fmt, Clippy with warnings denied, all-target
  tests and cargo-deny, as documented in `AGENTS.md`.
- Contracts: use `cgagentharness-invariant-guard` for current test mapping,
  including ownership, memory, MCP, web, reload, schedules and notifications.
  Documentation edits still run `invariant_guard` for the Markdown budget.
- Native execution: `tests/macos_cargo.rs` and process lifecycle tests need real
  macOS Seatbelt; sandbox permission errors are not application regressions.
- Desktop: package before compiling the shell, then desktop-toolchain fmt,
  Clippy/tests and `scripts/test-desktop-backend.py` against the packaged backend.
- Model/runtime: inspect actual inventory and exact configured model tag; do not
  equate similarly named GGUF/MLX variants or turn on cloud fallback for a smoke test.

For live acceptance, use an owned temporary home and unique port. Record the
known binary, environment and listener, issue harmless local chat, then stop it.
Fake model/provider tests prove protocol behavior,
not availability or live quality. App launch alone is not UI acceptance.
Follow `docs/DESKTOP_ACCEPTANCE.md` for outstanding UI
checks and record only interactions actually observed.

Run a failing-case reproducer when correcting behavior. Never delete assertions or
weaken guards to make tests pass. Baseline failures must be diagnosed before further
implementation. Keep source changes out of runtime fixtures and close only processes
started by this verification. Report commands, exit statuses, tested SHA/architecture,
artifact hashes, skips and remaining limits without including credentials or home data.
