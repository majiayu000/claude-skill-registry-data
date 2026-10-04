---
name: cgagentharness-write-policy-redteam
description: Adversarially exercise CG-agent-harness write/git approval, confirm+reason, clone jail, and shim argv boundaries ("browser never supplies a command"). Use when hardening or changing writer, write gates, git approval, shim argv encoding, or clone jail; do not silently close known gaps or loosen asserts to green.
---

# Write-policy Redteam

The browser never supplies a command; repository writes are gated; the clone
jail contains landed paths;
`confirm` is never defaulted; `reason` is required; kill switch
`CGAGENTHARNESS_AGENTIC_WRITE_DISABLE` is AND-only. Exit code `4` = write
refused.

Use the Rust suites below. Inspect fresh-policy, approval and rollback
assertions before selecting probes; an old end-to-end success test alone does
not establish those boundaries.

| Surface | Primary corpus |
|---|---|
| Writer / gate order / plan integrity | `tests/real_repo_loop.rs::writer_gates_in_order_and_plan_integrity` (+ publish/confirm paths in the same file) |
| Fresh policy / separate intent | `tests/write_policy.rs`, `tests/write_kill_switch.rs` |
| Git approval / digest, mode, origin, exact commit, index lock, disabled extensions | `tests/git_approval.rs` |
| Exact edits / preflight / failed rollback quarantine | `tests/exact_edits.rs`, unit tests in `src/agentic/workspace.rs` |
| Retrieval / sensitive reads / cloud refusal | `tests/real_repo_loop.rs` repository-retrieval and denied-basename cases |
| Clone / read jail | `agentic_foundations::apply_proposal_refuses_jail_escapes_and_oversize_content`, `read_jail_refuses_symlink_escapes_without_following_the_leaf` |
| Hostile argv / confirm never manufactured | `tests/shim_and_agent_routes.rs` hostile-argv matrix, `a_request_can_never_carry_an_argv`, publish-missing-confirm → child exit 4 |
| Kill switch AND-only / shipped gates | `invariant_guard::writer_kill_switch_is_and_not_or`, `shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed` |

Completion requires executed refusal cases and regression assertions for
newly closed bypasses, without weakening existing checks.

## The loop

### Step 1 — Run the write-policy corpus

```text
GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --test real_repo_loop -- --nocapture

GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --test agentic_foundations -- --nocapture

GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --test shim_and_agent_routes -- --nocapture

GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" \
  cargo test --test invariant_guard --test write_policy --test write_kill_switch \
    --test git_approval --test exact_edits -- --nocapture
```

Narrow filters only after checking that they select the intended tests.

### Step 2 — Classify results into buckets

| Bucket | Meaning | Action |
|---|---|---|
| **new_bypasses** | Attack that should refuse (exit 4 / 422 / jail) now succeeds or assert was deleted | **Regression.** Fix before anything else. Never loosen the assert. |
| **known_gaps** | Documented residual / weaker-than-name signal already called out in `INVARIANTS.md` | Work list only with explicit owner decision; do not silently "close" by relaxing policy. |
| **fixed_findings** | Prior gap now refuses with evidence | Bank a durable regression test; keep the assert. |
| **false_greens** | Suite green because confirm was defaulted, kill switch OR-ed, Seatbelt skipped, or shared listener used | Treat as FAIL of the verification method — reproduce with owned temp `CGAGENTHARNESS_HOME` + unique port. |

### Step 3 — Pick one new_bypass / known_gap; name the family

Work one finding at a time. Map to a family so the fix lands in the right
module:

- **Gate order** — `agentic.enabled` / mode / `writes_enabled` / reason /
  confirm / `allow_git_write_tools` (`src/agentic/writer.rs`)
- **Confirm+reason** — never defaulted; missing confirm → exit 4
- **Kill switch** — AND-only env disable
- **Argv boundary** — `--opt=value` single elements; browser never supplies argv
  (`src/shim`, `src/server/agent_policy.rs`)
- **Clone jail** — landed-path judgment, symlink / `.git` name-equivalence
  (`src/agentic/workspace.rs`)
- **Approval binding** — digest, modes, live tree, index, origin and approved commit
- **Policy revocation** — recheck disk at each mutation; confirm for run,
  approval, push and publication are separate intents

### Step 4 — Close with a minimal gate + regression test

- Prefer the smallest refuse path that restores the invariant (one gate check,
  one argv validation, one jail predicate).
- Add or extend a Rust test assert in the matching file above — same style as
  existing hostile matrices.
- Re-run Step 1 for the touched tests, then the related
  `invariant_guard` / `auth_guards` set if shared routing changed.
- **Never** default `confirm`, make `reason` optional, OR the kill switch, or
  delete/skip an assert to green.

### Step 5 — Report

End with FACT vs INFERENCE, buckets counts, commands + exit codes, and whether
exit-4 paths still hold. Skill completion ≠ publish authorization.

## Guardrails

- Apply current harness contracts from `INVARIANTS.md`.
- Retain rollback recovery backups after quarantine; do not claim crash atomicity.
- Pair with `cgagentharness-invariant-guard` before merging core-path diffs.
