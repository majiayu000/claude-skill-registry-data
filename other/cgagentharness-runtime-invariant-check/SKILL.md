---
name: cgagentharness-runtime-invariant-check
description: |
  Verify that core security invariants still hold after code changes. Run this before pushing core-path PRs (touching src/shim, guards.rs, headers.rs, writer.rs, sandbox.rs, workspace.rs, or config.default.yaml). Checks: I6 process isolation (server never imports agentic), guard chain order, CSRF contracts, write gates closed by default, RUN_ID_PATTERN consistency across boundary, clone jail contracts, and config fail-closed defaults. Complements tests/invariant_guard.rs by providing human-readable guidance on what to check and how to fix violations.
compatibility: |
  Requires: ripgrep, cargo test infrastructure
  Context: Rust codebase with INVARIANTS.md, tests/invariant_guard.rs, and security-critical modules
---

# Runtime invariant verification

Use current `INVARIANTS.md` and source, not historical guard diagrams. Read the
shared guard, route inventory, shim and execution boundaries before testing.
This checks the supplied implementation; it does not authorize policy changes.

| Boundary | Current contract | Runnable evidence |
|---|---|---|
| I6 | Server/common/LLM/shim never call pipeline code; only shim spawns the whitelisted child | `cargo test --locked --test invariant_guard` |
| Requests | Rate, exact origin, direct loopback/no proxy, account/RBAC, mutation CSRF | `cargo test --locked --test auth_guards --test secure_portal --test security_headers` |
| Browser arguments | Fixed check-profile names, bounded arguments, no arbitrary command; reason/confirm explicit | `cargo test --locked --test shim_and_agent_routes` |
| Default configuration | Master/deepagent/clone-write gates false; fresh auth/TLS and web settings true, empty URL allowlist; existing choices retained; quoted security switches invalid | `cargo test --locked --test invariant_guard --test common_layer` |
| Mutation policy | Reloaded write gates, clone jail, exact edits and reviewed-tree approval before commit/push/publication | `cargo test --locked --test write_policy --test real_repo_loop` |
| Web evidence | Exact/wildcard permission, checked DNS pinning, bounded retrieval and current-policy revocation | `cargo test --locked --test panels --test web_research` |
| Native TLS | Owned handshake, exact certificate/origin and platform trust validation | Desktop tests plus actual native acceptance in `docs/DESKTOP_ACCEPTANCE.md` |

The optional harness API key grants no authority and cannot bypass login.
`writes_enabled: true` and mode `write` do not arm the combined coding policy.
Public login/minimal status still get early guards. Research selection is private
to the account; chat sessions/jobs/persona/notes remain shared portal resources.

Run with isolated homes and provider credentials excluded. Check Cargo's own
exit status and every failure/skip. Required native sandbox tests may need the
operator's normal terminal rather than an outer restricted sandbox; never weaken
the application profile. Backend/fixture tests do not prove native GUI or live
model behavior. Record tested source, commands, outcomes and unresolved limits.
