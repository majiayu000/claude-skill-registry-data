---
name: cgagentharness-write-policy-redteam
description: Adversarially exercise CG-agent-harness write/git approval, confirm+reason, clone jail, and shim argv boundaries ("browser never supplies a command"). Use when hardening or changing writer, write gates, git approval, shim argv encoding, or clone jail; do not silently close known gaps or loosen asserts to green.
---

# Write-policy Redteam

**Persona:** Offensive security engineer for the harness write surface — not
CyClaw's prompt sanitizer. The trust boundary is: browser never supplies a
command; every repository write is gated; clone jail contains landed paths;
`confirm` is never defaulted; `reason` is required; kill switch
`CGAGENTHARNESS_AGENTIC_WRITE_DISABLE` is AND-only. Exit code `4` = write
refused.

**Corpus (FACT):** Existing Rust integration tests — not a `probes.yaml`. Prefer
these as the living adversarial suite. A FUTURE companion YAML corpus is
optional only if labeled INFERENCE/future and never replaces the tests.

| Surface | Primary corpus |
|---|---|
| Writer / gate order / plan integrity | `tests/real_repo_loop.rs::writer_gates_in_order_and_plan_integrity` (+ publish/confirm paths in the same file) |
| Git approval / digest binding | `real_repo_loop::loop_iterates_on_feedback_then_accepts_and_finalizes`, `agentic_foundations::manifest_digest_binds_files_and_head` |
| Clone / read jail | `agentic_foundations::apply_proposal_refuses_jail_escapes_and_oversize_content`, `read_jail_refuses_symlink_escapes_without_following_the_leaf` |
| Hostile argv / confirm never manufactured | `tests/shim_and_agent_routes.rs` hostile-argv matrix, `a_request_can_never_carry_an_argv`, publish-missing-confirm → child exit 4 |
| Kill switch AND-only / shipped gates | `invariant_guard::writer_kill_switch_is_and_not_or`, `shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed` |

**What "done" looks like:** every targeted test still fails closed on the
attack; each newly closed bypass has a minimal gate fix + a regression assert;
no assert was loosened to green; confirm/reason/kill-switch contracts hold.

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
  cargo test --test invariant_guard writer_kill_switch shipped_config -- --nocapture
```

Narrow further with filter strings when the diff is local (`writer_gates`,
`hostile`, `write_jail`, `confirm`).

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
- **Approval binding** — digest vs live worktree (`pending_decision`)

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

- Harness-only: I6, write gates, clone jail, CSRF placeholders, loopback,
  secrets. Do **not** transplant CyClaw RAG / soul / triple-gate / LangGraph /
  I1–I5 as applying here.
- Never weaken security to pass the redteam.
- Do not invent `probes.yaml` as required; cite Rust tests. FUTURE YAML = labeled
  companion only.
- Pair with `cgagentharness-invariant-guard` before merging core-path diffs — it's
  manual-only (`disable-model-invocation: true`); ask the operator to run
  `/cgagentharness-invariant-guard`.
