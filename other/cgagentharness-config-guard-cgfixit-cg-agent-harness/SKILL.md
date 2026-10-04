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
`flag_is_true` coverage in `tests/common_layer.rs`. **Do not invent a Python
parser** as the merge gate. A FUTURE stdlib/PyYAML companion checker is
INFERENCE only if labeled as such and never replaces cargo evidence.

## Contract checks

| ID | Severity | Contract |
|---|---|---|
| H1 | FAIL | `flag_is_true`: unquoted YAML `true` only; quoted `"true"` / `"false"` / other strings are **OFF** |
| H2 | FAIL | Shipped gates closed: `agentic.enabled`, `agentic.deepagent_github.enabled`, `agentic.deepagent_github.allow_git_write_tools`, `unslop.enabled`. Fresh web settings start enabled with an empty URL allowlist; existing choices and missing/invalid legacy web values stay unchanged/off. Fresh `auth.enabled` and `tls.enabled` must be true. Config gates are locked by `shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed`; web seeding and legacy preservation by the home/settings tests in `tests/common_layer.rs`. `security.api_key_optional` remains true but is deprecated metadata, not an account bypass |
| H11 | FAIL | Fresh `memory.enabled` and all nine `structured_memory` feature gates are true; persisted explicit off choices still win. Proposals never auto-apply facts. Memory defaults do not arm repository execution/write gates |
| H10 | FAIL | Invalid auth/TLS switch types refuse configuration; missing legacy fields remain off. Do not apply the generic quoted-gate OFF behavior to these security switches |
| H3 | FAIL | Literal YAML needles: `api_key_optional: true` and `allow_git_write_tools: false`; shipped YAML must not contain `allow_git_write_tools: true` (string forms hide mistakes) |
| H4 | FAIL | Write path still requires human `reason` + per-call `confirm` (never defaulted) — behavior locked in writer + `real_repo_loop` / shim routes; config must not document or enable a bypass |
| H5 | FAIL | Kill switch remains disable-only env `CGAGENTHARNESS_AGENTIC_WRITE_DISABLE` (AND-ed); `EXECUTION_ENABLED` does not flip itself closed |
| H6 | FAIL | Loopback posture: serve binds loopback only; model `base_url` examples stay `127.0.0.1`; non-loopback refused in code |
| H7 | WARN | `writes_enabled: true` in shipped agentic block is **armed-by-construction** and held closed by `agentic.enabled` + kill switch — changing either without an invariant statement is conscious risk |
| H8 | WARN | `policy.prompt_filter.banned_patterns` length stays aligned with the documentary CyClaw-port count (asserted 40 in `shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed`) |
| H9 | WARN | Protected paths (e.g. `AGENTS.md` in `protected_write_paths`) still present (`shipped_defaults_protect_agents_md`) |

## Run

```text
GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --test invariant_guard shipped_config -- --nocapture

GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --test common_layer flag_is_true -- --nocapture
```

When the change is semantically load-bearing for writes/jails, also run
`real_repo_loop` writer tests and `agentic_foundations` as needed. Diff-read
`assets/config.default.yaml` for accidental quoted booleans or opened gates.

### Interpret

1. **Broken contract** — fix the YAML (or the code if code is truth and YAML
   drifted); re-run until green. Do not delete the assert.
2. **Deliberate re-tune** — same change set must update comments +
   `INVARIANTS.md` / `AGENTS.md` as needed, with an explicit PR invariant
   statement. WARN items exist so re-tunes are conscious.
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
- Pair with `cgagentharness-invariant-guard` for core-path merges — it's manual-only
  (`disable-model-invocation: true`); ask the operator to run `/cgagentharness-invariant-guard`.
- No CyClaw soul/RAG/triple-gate transplantation; this is harness config only.
- Skill ≠ publish authorization.

## FUTURE (INFERENCE)

A no-import stdlib/YAML static checker mirroring CyClaw `config-guard` could be
added later for fresh-clone CI without compiling — label any such proposal
FUTURE; until then **cargo tests are authoritative**.
