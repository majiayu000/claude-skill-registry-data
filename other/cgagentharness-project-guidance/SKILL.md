---
name: cgagentharness-project-guidance
description: Read current CG-agent-harness architecture, operating rules, configuration, and verification sources before substantive repository work.
---

# CG-agent-harness Project Guidance

Read the smallest current source set below before substantive work. Code and
config outrank copied snapshots. This skill is repository guidance for agents
editing the tree — **not** a runtime `/api/skills` plugin, and **not**
authorization to push, merge, or release.

## 1. Truth order (always)

1. Code under `src/`
2. `assets/config.default.yaml` (every tunable; no hardcoded tunables elsewhere)
3. `INVARIANTS.md`
4. `AGENTS.md`
5. `README.md` (then `SECURITY.md` as needed)

If prose and code disagree, code wins — fix the doc in the same change set when
you touch the behavior.

## 2. Architecture map

| Entry | Implementation |
|---|---|
| `cgagentharness serve` | `src/server` (axum, bind `127.0.0.1` only) |
| `cgagentharness agentic <action>` | `src/agentic`, spawned only via `src/shim` |
| Exit codes | `0` ok, `2` failed, `3` env/config, `4` write refused |
| Home | `~/.CGagentHarness` / `CGAGENTHARNESS_HOME` |
| Allowed writes | Home directory, or pipeline clones under `data/agentic/workspaces` |
| Console asset | `assets/static/harness.html` (CSRF placeholders contractual) |
| Sync vs detached agent | `/api/agent/run` and `/api/agent/jobs` both via `prepare_run` |

Harness has persona and structured-memory
surfaces and opt-in local repository retrieval. Do not import CyClaw policy
assumptions. Preserve harness posture:
I6 isolation, guard chain, write gates, clone jail, judged-before-land,
approval binding, secrets redaction, detached-run gates.

## 3. Task → sources

| Task | Read first |
|---|---|
| Shim / I6 / ACTIONS whitelist | `src/shim`, `INVARIANTS.md` I6, `tests/invariant_guard.rs` |
| HTTP guards / headers / CSRF | `src/server/guards.rs`, `headers.rs`, `tests/auth_guards.rs`, `tests/security_headers.rs` |
| Write / publish path | `src/agentic/writer.rs`, write-gate sections of `INVARIANTS.md`, `tests/real_repo_loop.rs` |
| Clone jail / sandbox | `src/agentic/workspace.rs`, `src/agentic/executor/sandbox.rs`, `tests/agentic_foundations.rs` |
| Config defaults / gates | `assets/config.default.yaml`, `shipped_config_enforces_accounts_tls_and_keeps_execution_gates_closed` |
| Routes / console listing | `src/server/routes/mod.rs` (`REGISTERED_PATHS`), `views.rs` |
| Install / local verify | `scripts/verify-local.sh`, `scripts/smoke-ollama.sh`, `README.md`, `docs/INSTALL.md`, `docs/MODELS.md` |
| Packaging / release | `scripts/package-desktop.sh`, `docs/RELEASING.md`, `cgagentharness-release` |
| Ownership, memory, MCP, web, reload, schedules, notifications | Current contract/test map in `cgagentharness-invariant-guard`; select affected boundaries |

Core paths always require an invariant statement in the PR body when touched:
`src/shim`, `src/server/guards.rs`, `src/server/headers.rs`,
`src/agentic/writer.rs`, `src/agentic/executor/sandbox.rs`,
`src/agentic/workspace.rs`, `assets/config.default.yaml`.

## 4. When to load which `.codex` skill

| Skill | Load when |
|---|---|
| `cgagentharness-project-guidance` | Start of substantive repository work (this file) |
| `fable-protocol` | Evidence-first discipline before costly code/security/CI/GitHub claims |
| `cgagentharness-invariant-guard` | Before merging core-path security diffs; first gate of a harness security review |
| `cgagentharness-gotchas` | Install/verify, desktop packaging, Chrome acceptance CI, clippy fights, write-gate debugging, "hangs" / false greens |
| `cgagentharness-write-policy-redteam` | Hardening or changing writer, write gates, git approval, shim argv encoding, or clone jail |
| `cgagentharness-config-guard` | Before merging `assets/config.default.yaml` changes; when asked to check config |
| `cgagentharness-parity` | Updating CyClaw↔harness parity contracts; reading `docs/parity/*` or `scripts/parity-status.py` |
| `verification-specialist` | Adversarial independent verify of a *supplied* change (try to break it; no project mutation) |
| `cgagentharness-verify` | Running or extending the local/CI smoke/acceptance bar (distinct from verification-specialist) |
| `cgagentharness-release` | Packaging, signing, checksum embed, release artifacts |
| `cgagentharness-optimize` | Focused improvement scans that may open a draft PR |

Keep agent guidance within the existing `DOCS_BUDGET` rows in
`tests/invariant_guard.rs`. Edit the owner section, link instead of restating,
and put acceptance evidence in the PR body. Do not add Markdown files.

## 5. Quality bar (do not invent a lower one)

- `cargo fmt --all -- --check`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test --all-targets` with planner keys blanked
- `cargo deny check`
- New routes → `REGISTERED_PATHS` (+ console views if listed)
- New shim actions → `shim::ACTIONS` + CLI dispatch + invariant whitelist together
- Draft PRs, driver-prefixed branches (`claude/`, `codex/`, `grok/`, `kimi/`,
  `agent/`), based on `main`, `scripts/check-pr-template.sh`, one concern each

## 6. Authorization boundary

Loading or completing this skill does **not** grant push, merge, release, or
gate-arming rights. Preserve any narrower authorization the operator already
gave for the same task. Never expose secrets. Prefer draft PRs until evidence is
complete.

## 7. STOP

Proceed with the requested work and its relevant skill.
