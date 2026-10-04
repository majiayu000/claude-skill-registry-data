---
name: cgagentharness-invariant-guard
description: Assert CG-agent-harness security invariants still hold against the current tree or a diff. Use before merging changes to src/shim, guards/headers, writer, sandbox, workspace, or assets/config.default.yaml; when asked to check invariants; or as the first gate of a harness security review.
disable-model-invocation: true
---

# CG-agent-harness Invariant Guard

Persona: answer only **"do the invariants still hold?"** — not style, not
performance, not roadmap. Unlike CyClaw, the checker is **Rust integration
tests**, not a Python stdlib script. Do not invent a Python checker.

Core paths that always trigger this skill:

- `src/shim`
- `src/server/guards.rs`, `src/server/headers.rs`
- `src/agentic/writer.rs`
- `src/agentic/executor/sandbox.rs`
- `src/agentic/workspace.rs`
- `assets/config.default.yaml`

## Workflow

1. **Read the contracts.** Open `INVARIANTS.md` end-to-end and the core-path
   list in `AGENTS.md`. Note I6, guard chain, browser-never-supplies-command,
   write gates, clone jail, judged-before-land, approval binding, secrets
   redaction, detached-run gates, and weaker-than-name signals. Code wins if
   prose disagrees — then the doc must be fixed, not the test deleted.

2. **Run the locking tests that apply.** Prefer the narrowest set that covers
   the diff; expand when the change is shared routing/config/security:

   ```text
   GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
     cargo test --test invariant_guard -- --nocapture

   GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
     cargo test --test shim_and_agent_routes -- --nocapture

   GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
     cargo test --test real_repo_loop -- --nocapture

   GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
     cargo test --test agentic_foundations -- --nocapture

   GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
     cargo test --test auth_guards --test security_headers -- --nocapture
   ```

   Map areas to evidence (non-exhaustive):

   | Concern | Primary evidence |
   |---|---|
   | I6 import / spawn boundary | `invariant_guard::server_side_never_references_agentic`, `only_the_shim_spawns_a_child_on_the_server_side`, `agentic_side_never_references_server_or_shim`, ACTIONS whitelist assertions |
   | Shipped gates closed | `invariant_guard::shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed` |
   | Write-policy / kill switch | `real_repo_loop::writer_gates_in_order_and_plan_integrity`, `invariant_guard::writer_kill_switch_is_and_not_or` |
   | Git / approval binding | `real_repo_loop::loop_iterates_on_feedback_then_accepts_and_finalizes`, `agentic_foundations::manifest_digest_binds_files_and_head` |
   | Clone / read jail | `agentic_foundations::apply_proposal_refuses_jail_escapes_and_oversize_content`, `read_jail_refuses_symlink_escapes_without_following_the_leaf` |
   | Argv / confirm / run_id | `shim_and_agent_routes` hostile-argv matrix |
   | Detached jobs lockstep | `invariant_guard::agent_run_and_jobs_share_prepare_run`, job cancel/finish tests in `shim_and_agent_routes` |
   | CSRF placeholders | `invariant_guard::console_asset_is_verbatim_with_both_placeholders` |
   | Auth / headers | `auth_guards`, `security_headers` |

3. **Diff-read the boundary.** Manually inspect imports across `src/server` ↔
   `src/agentic` (only `src/shim` may spawn). Check that new routes landed in
   `REGISTERED_PATHS`, new actions updated `shim::ACTIONS` + CLI + whitelist
   together, and that gate defaults in `assets/config.default.yaml` remain
   fail-closed (`flag_is_true` — quoted `"true"` is OFF). Confirm
   `/api/agent/run` and `/api/agent/jobs` still share `prepare_run`.

4. **Report PASS/FAIL per invariant section** with evidence: test name + result,
   or file:line for structural scans. Separate FACT (observed) from INFERENCE.
   Residual risk and skipped coverage must be explicit.

5. **Never weaken tests to green.** A failing assertion is a blocking finding.
   Do not delete, skip, or loosen invariant coverage to obtain a pass. Quarantine
   only with an explicit human decision and a tracked follow-up.

## Boundary

- This skill does not change runtime gates, config defaults, or checker rules.
- It does not authorize push, merge, or release.
- CyClaw I1–I5 / soul / RAG / triple-gate do not apply here; do not grade this
  tree against them.
- Pair structural passes with behavioral tests for the changed path; a green
  `invariant_guard` alone is not a full security review.
