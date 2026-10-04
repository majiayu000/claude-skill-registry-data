---
name: cgagentharness-invariant-guard
description: Assert CG-agent-harness security invariants still hold against the current tree or a diff. Use before merging changes to src/shim, guards/headers, writer, sandbox, workspace, or assets/config.default.yaml; when asked to check invariants; or as the first gate of a harness security review.
---

# CG-agent-harness invariant guard

Check the current contracts against the supplied diff. Read `INVARIANTS.md`
end-to-end, then `AGENTS.md`, affected code and tests. Core paths listed in
`AGENTS.md` always require this check; other authority changes also qualify.
Code wins over stale prose. Never weaken an assertion to obtain a pass.

## Select evidence

Run the structural suite first:

```sh
GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --locked --test invariant_guard -- --nocapture
```

Map every changed contract to behavioral tests below. Test targets denote
`tests/<target>.rs`; `src/` entries contain additional unit tests. Inspect the
actual assertions and exercise relevant refusal paths. A green structural
suite alone does not establish behavioral coverage.

| Contract | Evidence to select |
|---|---|
| I6, action whitelist, duplicated constants, CSRF placeholders, route registration | `invariant_guard`, `shim_and_agent_routes`; `src/shim/mod.rs`, `src/server/routes/mod.rs` |
| Account bootstrap, roles, TLS, Host/origin, CSRF, redaction | `auth_guards`, `secure_portal`, `security_headers`, `common_layer`, `panels` |
| Fresh mutation policy, separate approval/push/publication intent, kill switch | `write_policy`, `write_kill_switch`, `real_repo_loop` |
| Reviewed tree/mode/origin binding, index lock, Git extensions refused | `git_approval`, `agentic_foundations` |
| Clone/read jail, denied basenames, local-only retrieval, hash revalidation | `agentic_foundations`, `real_repo_loop`; `src/agentic/repo_retrieval.rs` |
| Whole-proposal preflight, rollback/quarantine, exact edits | `exact_edits`, `real_repo_loop`; `src/agentic/workspace.rs` |
| Sandbox, bounded capture, cancellation and descendant-cleanup limits | `macos_cargo`, `linux_bwrap`, `process_lifecycle`, `process_writer_outcome`; `docs/PROCESS_LIFECYCLE.md` |
| Sync/jobs/schedules share preparation, owner checks, reviewed goals, at-most-once occurrences | `shim_and_agent_routes`, `agent_schedules`, `owner_isolation` |
| Owned sessions/export/adoption, memory gates, pending-only proposals, recall revalidation | `owner_isolation`, `session_export`, `structured_memory`, `structured_memory_phase7`, `structured_memory_suggestions` |
| Web authority, DNS pinning, revocation, listings grant no page access | `web_research`, `web_phase2_redteam`, `chat_web`; `src/server/web_policy.rs` |
| Outbound MCP capabilities, broker confirmation, platform containment, tool-free loop | `mcp_client`, `mcp_lifecycle`, `mcp_windows`; `docs/MCP_CLIENT.md` |
| Inbound MCP machine-key authority, owner-only reads, empty grants, revocation | `mcp_server`; `src/server/mcp_keys.rs` |
| Atomic limit reload, unchanged authority/rate history, restart-only settings | `secure_portal`; `src/server/config_reload.rs::RELOADABLE` |
| Compaction preserves history on failure, reply reservations, bounded web calls | `chat_and_sessions`, `chat_web`; `src/server/compaction.rs` |
| Incomplete billed replies, prediction versus usage, private notification retries | `spend_ledger`, `notifications`; `src/llm/cloud_chat.rs` |
| Loopback Ollama pull/warmup, no num_ctx, native sidecar identity | `ollama_manage`, `scripts/test-desktop-backend.py`; `docs/DESKTOP.md` |

## Inspect boundaries and report

Only the shim dispatches the agentic child. Declared MCP children use
`src/common/mcp.rs`; do not mistake that separate boundary for an I6 violation.
Inspect new routes in `REGISTERED_PATHS` and new actions in shim, CLI and tests.
Check shipped defaults with `cgagentharness-config-guard`.

Respect documented limits: process-global CSRF is not session-bound;
process-group cleanup is not strict containment; private storage is not
encryption; external policy edits and syscalls are not one transaction.

Report each applicable contract as PASS, FAIL or NOT RUN with commands,
results and tested SHA. Identify uncovered assertions and platform gaps.
Check every current invariant section for applicability, including sections
added after this map. Skill completion grants no publication authority.
