---
name: cgagentharness-config-guard
description: Statically assert assets/config.default.yaml still honors harness security contracts — flag_is_true semantics, confirm never defaulted, shipped execution gates closed, loopback posture. Use before merging config.default.yaml changes or when asked to check config.
---

# Config Guard (CG-agent-harness)

**Persona:** One question — does `assets/config.default.yaml` still honor the
contracts the running system assumes? Not a code/topology review (see
`cgagentharness-invariant-guard`). Config is the single source of every tunable
(`AGENTS.md`); relations and fail-closed defaults are load-bearing.

**Checker (FACT):** Rust tests — primarily
`tests/invariant_guard.rs::shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed` and
`quoted_true_is_off` and `security_switches_require_boolean_values` in
`tests/common_layer.rs`. Inspect the assertions; a filter matching zero tests
is not evidence.

## Contract checks

| ID | Severity | Contract |
|---|---|---|
| H1 | FAIL | `flag_is_true`: unquoted YAML `true` only; quoted `"true"` / `"false"` / other strings are **OFF** |
| H2 | FAIL | Shipped gates closed: `agentic.enabled`, `agentic.deepagent_github.enabled`, `agentic.deepagent_github.allow_git_write_tools`, `unslop.enabled`, `mcp.enabled`, `mcp.sse_allow_loopback`, `mcp.server.enabled`; inbound MCP tools stay empty. Fresh web settings start enabled with an empty URL allowlist; existing choices and missing/invalid legacy web values stay unchanged/off. Fresh `auth.enabled` and `tls.enabled` must be true. Config gates are locked by `shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed`; web seeding and legacy preservation by the home/settings tests in `tests/common_layer.rs`. `security.api_key_optional` remains true but is deprecated metadata, not an account bypass |
| H11 | FAIL | Fresh `memory.enabled` and all nine `structured_memory` feature gates are true; persisted explicit off choices still win. Proposals never auto-apply facts. Memory defaults do not arm repository execution/write gates |
| H10 | FAIL | Invalid auth/TLS switch types refuse configuration; missing legacy fields remain off. Do not apply the generic quoted-gate OFF behavior to these security switches |
| H3 | FAIL | Literal YAML needles: `api_key_optional: true` and `allow_git_write_tools: false`; shipped YAML must not contain `allow_git_write_tools: true` (string forms hide mistakes) |
| H4 | FAIL | Write path still requires human `reason` + per-call `confirm` (never defaulted) — behavior locked in writer + `real_repo_loop` / shim routes; config must not document or enable a bypass |
| H5 | FAIL | Kill switch remains disable-only env `CGAGENTHARNESS_AGENTIC_WRITE_DISABLE` (AND-ed); `EXECUTION_ENABLED` does not flip itself closed |
| H6 | FAIL | Loopback posture: serve binds loopback only; model `base_url` examples stay `127.0.0.1`; non-loopback refused in code |
| H7 | FAIL | Mode/write-enabled defaults alone cannot authorize mutation. Fresh disk policy also requires master/deepagent/clone-write gates, reason, confirm and the disable-only kill switch (`tests/write_policy.rs`) |
| H8 | FAIL | `policy.prompt_filter.banned_patterns` length stays aligned with the documentary CyClaw-port count (asserted 40 in `shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed`) |
| H9 | FAIL | Protected paths (e.g. `AGENTS.md` in `protected_write_paths`) still present (`shipped_defaults_protect_agents_md`) |

## Run

```text
GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --test invariant_guard shipped_config -- --nocapture

GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --test common_layer quoted_true_is_off -- --nocapture
```

Also run `security_switches_require_boolean_values` in `common_layer`. Check
`notifications.enabled` and `agentic.deepagent_github.retrieval.enabled` remain
false in shipped YAML; select `notifications` and `real_repo_loop` tests when
changed.

### Interpret

1. **Broken contract** — fix the YAML (or the code if code is truth and YAML
   drifted); re-run until green. Do not delete the assert.
2. **Deliberate re-tune** — same change set must update comments +
   `INVARIANTS.md` / `AGENTS.md` as needed, with an explicit PR invariant
   statement. Changed defaults require current behavioral evidence.
3. **Env/test failure** — blank planner keys; do not require developer
   `GROK_API_KEY`.

### Report (pasteable)

```text
Config Guard: PASS|FAIL
Evidence: <test names + results>
Gates: <each H1–H11 one line>
Re-tune: <none | list>
Verdict: safe to merge / fix required: ...
```

## Guardrails

- Read-oriented skill: report; do not edit config solely to silence a check
  without an authorized change set.
- Never open a shipped gate to green a convenience path.
- Never weaken `flag_is_true` or ship quoted `"true"` as ON.
- Pair with `cgagentharness-invariant-guard` for core-path merges.
- No CyClaw soul/RAG/triple-gate transplantation; this is harness config only.
- Skill ≠ publish authorization.
