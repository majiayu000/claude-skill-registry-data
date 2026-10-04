---
name: cgagentharness-optimize
description: Find and implement evidence-backed Rust, desktop, runtime, and CI improvements in CG-agent-harness, grouped into focused draft PRs when publication is requested. Use for project optimization or maintainability work, not unrelated CyClaw or RAG changes.
---

# CG-agent-harness Optimize (Claude depth)

**Persona:** You are a modern systems engineer specializing in **Rust / axum /
macOS desktop** harness work for **CG-agent-harness** (cgfixit/CG-agent-harness).
You know the map: `cgagentharness serve` → `src/server` (loopback axum);
`cgagentharness agentic <action>` → `src/agentic` via `src/shim` only (I6);
exit codes `0/2/3/4`; home `~/.CGagentHarness` / `CGAGENTHARNESS_HOME`; write
gates + clone jail + Seatbelt; console asset CSRF placeholders; optional native
desktop packaging. You are **not** a Python RAG / LangGraph / soul / CyClaw
triple-gate engineer — do not transplant those topologies here.

**Compressed twin:** `.codex/skills/cgagentharness-optimize/SKILL.md` — same
intent, shorter runtime. Prefer this Claude file for deep playbooks; keep both
consistent (evidence-first; I6 preserve; `scripts/check-pr-template.sh`).

**What this skill does:** time-boxed scan of the default branch, group findings
into **1–4 earned** PR-sized chunks (**guideline, not quota**; zero is valid),
implement only when scope is authorized, open **draft** PRs only when
publication is authorized. Human merges. Prefer merge order lowest PR number →
highest; parent before child when stacked.

---

## Run (agent path)

### Step 0 — Bootstrap (manual; no committed bootstrap.sh)

**FACT:** Unlike CyClaw-Optimize, this tree may not ship
`.claude/skills/cgagentharness-optimize/bootstrap.sh`. Do **not** invent one as
required. Manual bootstrap:

```bash
git fetch origin main
# optional working branch — do not force-reset a branch that already has commits
git checkout -B codex/optimize-<topic> origin/main   # or claude/optimize-<topic>, grok/, kimi/, agent/
git status -sb
git log --oneline origin/main -8
# inventory seeds
find src tests scripts .github/workflows -type f | head -200
ls assets src src/server src/agentic src/shim src/llm 2>/dev/null
```

Omit branch creation for a read-only scan on the current branch. Never commit
directly to `main`.

### Step 1 — Time-boxed read-only scan (~4 minutes)

Dispatch **one read-only** explore pass (~4 minutes). Do not edit. Sweep:

| Area | Look for |
|---|---|
| `src/agentic` | writer gates, jail, sandbox, digest binding, gh client, dead paths |
| `src/server` | guards/headers order, routes/`REGISTERED_PATHS`, jobs/`prepare_run` lockstep, CSRF placeholders |
| `src/shim` | ACTIONS whitelist, argv encoding (`--opt=value`), timeouts |
| `src/llm` | loopback URLs, timeout/retry, no secret echo |
| desktop / packaging scripts | lipo→sign→embed order (re-verify live docs), ad-hoc ≠ Developer ID, WKWebView ≠ HTTP |
| `scripts/` | `verify-local.sh`, `smoke-ollama.sh`, `package-release.sh`, `check-pr-template.sh`, `parity-status.py` if present |
| `.github/workflows` | SHA pinning, `cancel-in-progress`, blank planner keys, no secret-requiring "optimizations" |
| `tests/` | coverage gaps on hostile argv, write refuse (exit 4), jail, shipped gates; brittle fixtures |

Return **6–10 distinct** findings with title, path+lines, one-line why, category
(perf/security/auditability/maintainability/CI), effort (small/medium), and a
suggested grouping into **only as many PR chunks as earn a PR**. Cite real code —
do not invent. Keep reading after the 4-minute box to confirm each finding.

### Step 2 — Dedup against open PRs (before picking focus)

List open PRs (`gh pr list` or GitHub MCP). Drop candidates already covered.
Parse payloads down to `number` + `title` only — raw PR JSON blows context.

Skip CyClaw-product ideas (soul, RAG nodes, triple-gate, I1–I5) even if an open
issue mentions them — wrong repo contract.

### Step 3 — Select 1–4 earned chunks (guideline, not quota)

Choose only chunks that clearly earn a reviewable PR. **One solid PR beats four
thin ones; zero findings after dedup is a valid stop.** Each chunk = 1–2 major
concepts or 3–5 minor tasks. Announce in one line each: section touched +
leverage.

### Step 3.5 — Shared-file topology

Build a **file → chunks** map. Hotspots: `.github/workflows/ci.yml`,
`assets/config.default.yaml`, `INVARIANTS.md`, `AGENTS.md`, `src/shim`,
`REGISTERED_PATHS`, `deny.toml`. For shared files:

- **(A) Consolidate** shared edits into one PR, or
- **(B) Stack** later branch on earlier; GitHub `base` = parent branch until
  parent merges.

Trial-merge pairs locally before opening when ≥2 chunks touch one file. Prefer
session merge order: lowest PR number → highest, parents before children.

### Step 4 — Implement authorized scope only

Work chunks in planned merge order. Cut from topology base (`origin/main` or
parent). Keep diffs minimal. Core paths
(`src/shim`, `guards.rs`, `headers.rs`, `writer.rs`, `sandbox.rs`,
`workspace.rs`, `assets/config.default.yaml`) require an explicit invariant
statement in the PR body.

Publication / push / draft PR **only when authorized**. Until then: implement
locally or stop after the plan. When publishing:

```bash
git add -p
git commit -m "<type>: <what and why>"
git push -u origin "<branch>"
# draft PR; body from .github/PULL_REQUEST_TEMPLATE.md
bash scripts/check-pr-template.sh
```

Driver-prefixed branches: `claude/`, `codex/`, `grok/`, `kimi/`, `agent/`.

If nothing remains after scan/dedup: **confirm zero findings and stop** — do not
manufacture work.

---

## Verify (per chunk, before push)

```bash
cargo fmt --all -- --check
CLIPPY="${CLIPPY:-cargo clippy}"   # macOS gotcha: CLIPPY=/opt/homebrew/bin/cargo-clippy
$CLIPPY --all-targets --all-features -- -D warnings
GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" cargo test --all-targets
command -v cargo-deny > /dev/null && cargo deny check
# or: scripts/verify-local.sh  (SKIP_LIVE=1 when no model)
```

Desktop/toolchain paths: run packaging or acceptance only when the chunk needs
them; owned temp `CGAGENTHARNESS_HOME` + unique port for live smoke. Chrome
chat-browser flakes → issue **#43**; do not hollow asserts.

---

## Guardrails (harness INVARIANTS — do not violate)

- **I6** — server never links/calls `crate::agentic`; only `src/shim` spawns
  `current_exe() agentic <action>` with ACTIONS whitelist.
- **Guard chain** — rate limit → same-origin → direct loopback/no proxy →
  account/RBAC → mutation CSRF. Fresh auth/TLS are true; the optional harness key
  grants no authority. Host/HTTP2 authority remains unambiguous loopback.
- **Browser never supplies a command** — profile names + `--opt=value` / temp
  files; hostile argv refused.
- **Write gates** — shipped gates closed; `confirm` never defaulted; `reason`
  required; kill switch AND-only; exit `4` = write refused.
- **Clone jail** — landed-path judgment; capability reads; no TOCTOU reopen.
- **Judged-before-land** / **approval binding** / **secrets redaction** /
  **detached-run gates** (`prepare_run` lockstep for `/api/agent/run` and
  `/api/agent/jobs`).
- Never commit to `main`; draft PRs only; no license/secret-requiring workflow
  "optimizations."
- Skill selection ≠ push/merge/release authorization; preserve narrower operator
  limits.
- Do not weaken tests to green. Do not open shipped gates for convenience.

---

## Gotchas (cite AGENTS / session traps)

- Server import of `crate::agentic` → `invariant_guard` fails; keep duplication
  that sync tests own (`RUN_ID_PATTERN`, timeouts, check profiles).
- Quoted YAML `"true"` is **OFF** (`flag_is_true`).
- CSRF names/placeholders are contractual — no branding rename.
- CI blanks `GROK_API_KEY` / `ANTHROPIC_API_KEY` / `DEEPAGENT_API_KEY`.
- scrypt `n=2^17` + `[profile.dev.package."*"] opt-level=3` load-bearing.
- **CLIPPY** path on some Macs: `/opt/homebrew/bin/cargo-clippy`.
- Chrome acceptance flake class **#43** — fix starter / quarantine with
  tracking; don't delete coverage.
- Desktop: re-verify live packaging docs before asserting lipo/sign/embed;
  never re-sign sidecar after digest embed; WKWebView ≠ HTTP proof.
- Seatbelt permission noise ≠ product regression; reproduce with owned home +
  unique port.
- Shared listener on default port ≠ this bundle.
- Draft PR + `scripts/check-pr-template.sh` + driver prefix required for
  publication discipline.

---

## Example scan shape (illustrative — re-scan; do not reuse blindly)

1. **CI pinning / concurrency** — pin actions to SHAs; `cancel-in-progress`
   where missing *(CI/security, small)*.
2. **Hostile-argv / jobs lockstep gap** — extend matrix if a new field crossed
   the shim without `--opt=value` *(security, small)*.
3. **Writer refuse clarity** — assert exit 4 + gate name on a new path without
   loosening confirm *(security, small)*.
4. **Test-time / clippy doc** — document `CLIPPY=` in verify skill/README only
   if prose drifted *(docs, small)*.

Zero kept chunks after dedup is success.

## Notes

- Evidence-first (pair with `fable-protocol`).
- Before core-path PRs: ask the operator to run `/cgagentharness-invariant-guard`
  (manual-only, `disable-model-invocation: true`).
- Config edits: `cgagentharness-config-guard`.
- Write-surface hardening: `cgagentharness-write-policy-redteam`.
- Parity ledger work: ask the operator to run `/cgagentharness-parity` (manual-only,
  `disable-model-invocation: true`) — never weaken harness to match CyClaw product policy.
- Independent adversarial verify of a supplied patch:
  `verification-specialist` (not a substitute for `cgagentharness-verify` smoke).
