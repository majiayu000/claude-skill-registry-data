---
name: boundary-probe
description: Trust-boundary security audit of cqs — fans out unbiddable-auditor agents across 6 categories (RT-INJ/RT-FS/RT-RES/RT-DATA/RT-RELAY/RT-EXFIL), attacker mindset, run-the-attack PoC + regression guard.
disable-model-invocation: true
---

# Red Team Audit

Trust-boundary security audit — attacker mindset, attacks RUN against the local binary, every finding pinned as a regression guard.

This skill is the orchestrator. **The contract — threat model, two attack vectors, method, finding format, rules, the cqs-tools block — lives in `.claude/agents/unbiddable-auditor.md`.** Each spawned agent IS an `unbiddable-auditor`; its prompt carries only the category scope below. Do not re-embed the contract here (it drifts — the old inlined threat model went stale against SECURITY.md).

## Arguments

- (none) — runs all 6 categories

## Process

### Setup
1. **Read `SECURITY.md`** — the auditor def re-derives the threat model from it per run, but read it yourself to sanity-check the category scopes against the current trust boundaries before dispatching.
2. **Read prior triage** (`docs/audit-triage-v*.md`) and **current findings** (`docs/audit-findings.md`) — pass the skip-list to each agent.
3. **Enable audit mode**: `cqs audit-mode on --expires 4h` (no `-q` on this subcommand).

### Execution
4. **Create team**: `boundary-probe`.
5. **Spawn one `unbiddable-auditor` (subagent_type: unbiddable-auditor, model opus) per category.** Each prompt carries ONLY: the category's scope/key-question/targets/files below, the prior-findings skip-list, and "append findings to `docs/audit-findings.md` under `## Trust-Boundary`." Everything else is in the def.
6. A category lead may fan out per-PoC verifiers (the def grants `Agent`).

### Cleanup
7. **Shutdown team** after all agents complete.
8. **Incorporate findings** into main triage (`docs/audit-triage.md`).
9. **Disable audit mode**: `cqs audit-mode off`.

## Categories

### RT-INJ — Input Injection
**Key question:** can agent-controlled query/CLI/wire input escape its intended context?
**Targets:** batch pipeline (`|` chaining), FTS5 construction (`normalize_for_fts` bypass on ANY path to MATCH), notes-text → TOML metacharacters, `--ref` names in SQL + fs paths (`/`, `..`, `\0`), `shell-words` split, `CQS_PDF_SCRIPT` script-path validation, `--path` globset ReDoS, `--overlay-root` path handling.
**Files:** `src/cli/batch/`, `src/note.rs` + `src/store/notes.rs`, `src/nl/fts.rs`, `src/search/`, `src/project.rs`, `src/convert/pdf.rs`, `src/cli/batch/handlers/`.

### RT-FS — Filesystem Boundary Violations
**Key question:** can any path reach a file outside the project root despite canonicalize+starts_with?
**Targets:** completeness of the canonicalize+starts_with guard across ALL file-reading paths (incl. the worktree-overlay build's `--overlay-root` reindex), `convert --output` escape, reference-index path construction (`../` escaping the refs dir), function-name-as-path-component, stale index entries serving wrong content.
**Files:** `src/cli/commands/io/read.rs`, `src/project.rs`, `src/convert/`, `src/store/mod.rs`, `src/worktree_overlay.rs`, `src/cli/batch/handlers/`.

### RT-RES — Robustness (security angle only)
**Key question:** can a crafted-but-valid input crash/hang/OOM the daemon as a denial channel? **Cede** generic malformed-input robustness to property-auditor and concurrency hangs to interleaving-auditor — keep the *attacker-reachable resource-exhaustion* angle.
**Targets:** pipeline fan-out bomb, BFS depth bomb, token-budget extremes, query-length OOM (100KB → tokenizer), batch-session unbounded memory, watch event storm. Bare `unwrap()/expect()` only where attacker input reaches it.
**Files:** `src/cli/batch/`, `src/gather.rs`, `src/impact/`, `src/hnsw/`, `src/cli/watch/`, `src/embedder/`.

### RT-DATA — Silent Corruption (security angle only)
**Key question:** can attacker-influenced input leave the index inconsistent / serve wrong results without error? **Cede** concurrent-race corruption to interleaving-auditor and migration atomicity to legacy-state-auditor — keep the *crafted-input-driven* corruption.
**Targets:** embedding-dimension confusion via a crafted model id, NaN/ordering injection breaking sort, batch cache staleness reachable by input, HNSW/SQLite desync via attacker-triggered delete/gc.
**Files:** `src/store/`, `src/hnsw/`, `src/note.rs`, `src/index.rs`, `src/embedder/`.

### RT-RELAY — Indirect Injection via Indexed Content (the agent-consumer axis)
**Key question:** can crafted content already in the corpus (a contributor's comment, an upstream dependency, a `cqs ref add` source, a developer note, an LLM summary) manipulate the consuming agent? This is SECURITY.md's longest section and the reason the trust-signal suite exists.
**Targets:** indirect prompt-injection payloads surviving the relay without `injection_flags` firing or `CQS_TRUST_DELIMITERS` wrapping; forging a trust signal (`trust_level: user-code` on vendored/ref content, fake `note_boost`, mislabelled `edge_kind`); `validate_summary` bypass on the LLM-summary path; making `suggest`/`dead` recommend a harmful action (e.g. deleting live code) to an agent that acts on it; ranked-result poisoning that blends untrusted content as trusted.
**Files:** `src/vendored.rs`, `src/cli/json_envelope.rs`, `src/llm/validation.rs`, `src/store/notes.rs`, `src/search/` (RRF blending + rank_signals), `src/cli/batch/handlers/search.rs`, `src/note.rs`.

### RT-EXFIL — Data Egress / Privacy (the dual oracle)
**Key question:** does data flow OUT beyond its PRIVACY.md-declared boundary — no adversary required, just an honest leak? The other categories check intrusion *inward*; this checks egress *outward*. The boundary held when nothing leaves beyond what was declared.
**Targets:** the LLM-summary Batches API payload — does `cqs index --llm-summaries` send only the chunk to Anthropic, or more (the whole file, neighbouring context)?; `tracing` spans/events logging chunk content, full paths, or secrets that persist; `cqs telemetry` recording query text / content; error-message content leaking paths/content to a socket client (verify the redacted `err-<id>` discipline holds on EVERY error path, not just the overlay one); the embeddings/summary caches persisting content beyond intent.
**Files:** `src/llm/` (Batches client + exactly what it sends), `src/cli/watch/` (daemon logging), the telemetry module, `src/cli/json_envelope.rs` (error redaction), `src/store/` (cache contents).

## Notes

- **Model:** opus, always — security is the documented Fable exception (the def states why). Do not switch to fable in a model sweep.
- **New surfaces since the last sweep** worth attention: the worktree overlay (`--overlay-root`, the overlay reindex reading worktree content) and the result-trust metadata (`trust_level` / `injection_flags` / `rank_signals` / `edge_kind` — forging these is RT-RELAY's core).
