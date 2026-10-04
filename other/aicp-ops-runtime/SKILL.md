---
name: aicp-ops-runtime
description: Validate AICP runtime health, observe live state, benchmark performance, audit capabilities, and auto-tune model configs via the CLI surface (`aicp --check`, `--self-test`, `--observe`, `--bench`, `--capabilities`, `--auto-config`). The "is everything working" toolbelt for setup, post-deploy verification, and incident triage. Loads when the operator says "is AICP working" / "verify setup" / "self-test" / "show live status" / "benchmark performance" / "what features do we have" / "auto-detect optimal config" / "diagnose AICP".
allowed-tools: Bash, Read
effort: low
---

# aicp-ops-runtime

Operate AICP's runtime validation + observation toolbelt via CLI: confirm
the system is working (`--check`/`--self-test`), observe live state
(`--observe`/`--metrics`), benchmark performance (`--bench`), audit
capabilities (`--capabilities`), and auto-tune model configs
(`--auto-config`). Distinct from `aicp-ops-metrics` (which focuses on
metrics specifically); this skill is the broader "verify it works" surface.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Setup / verification**: "is AICP working", "verify setup", "self-test",
  "did the deploy succeed", "what's broken"
- **Live observation**: "show live status", "what's running on GPU", "is
  LocalAI responsive", "diagnose AICP"
- **Performance**: "benchmark performance", "is X slow", "TTFT / tok/s",
  "compare to baseline"
- **Capability inventory**: "what features do we have", "what endpoints",
  "what tools, models, profiles"
- **Tuning**: "auto-detect optimal config", "tune for this hardware",
  "GPU passthrough working"

Do NOT load when:

- The concern is metrics-only summaries (load `aicp-ops-metrics` for the
  focused metrics workflow)
- The concern is task lifecycle (load `aicp-ops-tasks`)
- The concern is reliability triage of failed tasks (load `aicp-ops-dlq`)
- The concern is full-stack performance regression (load `quality-performance`
  for benchmarking AICP-specific dimensions)

## Operations

### Operation 1 — Quick validation (`--check`)

**When**: confirm AICP can serve requests right now (config valid + backends
available + GPU + Docker passthrough + KB collection).

**Process**:

1. Run `aicp --check`
2. Output sections (per `_run_check()` at `aicp/cli/main.py`):
   - Config validation (OK / INVALID with errors)
   - GPU detection + Docker GPU passthrough verification
   - Backend availability (per backend: detail string + ok flag)
   - LocalAI health/ready probes
   - KB collection (`aicp-kb`) check
   - Cluster nodes status (if configured)
   - Routing config (auto-route flags + failover chain)
   - Offload summary (% local vs % claude)
   - Final "All systems ready" or "Some backends unavailable"
3. The output's `NEXT:` adapts:
   - All OK → recommends `--self-test` for end-to-end OR `aicp "<prompt>"`
   - Failures → recommends triaging the FAIL items and re-running

**Quality bar**: this is the FIRST diagnostic to run; faster than `--self-test`
(no inference call), broader coverage than `--observe` (includes config validation).

### Operation 2 — End-to-end self-test (`--self-test`)

**When**: confirm not just availability but actual operational success on
real LocalAI endpoints (chat, embeddings, transcribe, etc.).

**Process**:

1. Run `aicp --self-test`
2. Each subsystem probed in sequence: health, readiness, API reachability,
   chat completions, embeddings, audio (transcribe/speak/VAD), image gen,
   reranking, KB search, MCP tools, etc.
3. Output marks each as PASS / FAIL / SKIP with summary at end
4. The output's `NEXT:` adapts:
   - All passed → `--bench` for performance baseline OR start using AICP
   - Failures → triage FAIL items above (likely LocalAI / KB / Docker config)

**Quality bar**: SKIP is acceptable (e.g., LoRA without an adapter file is
SKIP, not FAIL). FAIL is actionable. Investigate every FAIL.

### Operation 3 — Live state snapshot (`--observe`)

**When**: see what's currently happening — health probes, GPU active model,
goroutines, API call rates, P2P, feature flags.

**Process**:

1. Run `aicp --observe`
2. Output is "right now" view — health, readiness, LocalAI state, GPU,
   P2P cluster, detected features
3. The output's `NEXT:` recommends `--metrics` for prometheus details or
   `--check` for full validation

**Quality bar**: a healthy snapshot has health=healthy + ready=ready, GPU
active model present, GPU memory <70%, no P2P errors. Anomalies signal
investigation.

### Operation 4 — Performance benchmark (`--bench`)

**When**: measure AICP's current performance across chat (cold + warm),
grammar-constrained, embeddings, reranking.

**Process**:

1. Run `aicp --bench`
2. Output sections:
   - Chat (3 runs): TTFT, generation_ms, tok/s — first run is cold, next 2 warm
   - Grammar-constrained (yes/no)
   - Embedding (nomic-embed): total_ms + dim + chars
   - Reranking (bge-reranker-v2-m3): total_ms + docs + results
3. The output's `NEXT:` recommends `--metrics` for live snapshot or `--stats`
   for aggregated comparison vs other runs

**Quality bar**: a healthy 7-8B model on 8GB+ GPU should warm-inference at
~30-50 tok/s. Cold start can be 10-30s. Departures from these baselines
warrant investigation.

### Operation 5 — Capability inventory (`--capabilities`)

**When**: operator wants to see all AICP integrated features at a glance —
endpoints, tools, slash commands, models, routing.

**Process**:

1. Run `aicp --capabilities`
2. Output: structured listing of LocalAI endpoints, MCP tools, supported
   features, routing setup, model catalog
3. The output's `NEXT:` recommends `--check` for live status or `--self-test`
   for end-to-end validation

**Quality bar**: this is documentation-mode output, not diagnostic — use it
for inventory, not troubleshooting.

### Operation 6 — Auto-tune model configs for current hardware (`--auto-config`)

**When**: GPU changed (added/removed/swapped) and operator wants AICP to
detect optimal `gpu_layers`, `context_size`, `tensor_split` per model.

**Process**:

1. Run `aicp --auto-config`
2. Output:
   - Detected GPUs table (index, name, VRAM total/free, driver)
   - Per-model: estimated VRAM + optimal config + diff vs current
3. For each "Config differs from optimal" prompt, operator decides yes/no
4. After tuning, output's `NEXT:` recommends `make local-up` to apply

**Quality bar**: NEVER auto-confirm the per-model update prompts. The
operator must approve each change — the optimal calculator is heuristic-based
and may not account for application-level constraints (e.g., the
asymmetric-KV-cache decision's specific cache_type_k/v values are NOT
auto-detected by the tuner).

## Gotchas

- **Detection**: agent uses `aicp_health` / `aicp_deep_health` / `aicp_system` MCP tools.
  **Rule**: NEVER call deprecated MCP tools — use `aicp --check` (broadest)
  or `aicp --observe` (live snapshot).
  **Reasoning**: per audit decision, MCP overhead is paid per turn for tools
  used during specific workflows; CLI+Skills loads on demand.

- **Detection**: agent runs `--bench` repeatedly without operator request.
  **Rule**: `--bench` consumes inference budget (3 chat runs + multiple other
  endpoint calls). Run on demand, not periodically.
  **Reasoning**: benchmarking is point-in-time; periodic benchmarking IS the
  scope of `quality-performance` skill, not this one.

- **Detection**: agent runs `--auto-config` and applies changes without operator confirmation.
  **Rule**: each model's "Update?" prompt requires explicit `y` from operator.
  Don't pipe `y` automatically.
  **Reasoning**: auto-config is heuristic; per the asymmetric-KV-cache decision,
  some optimal configs (KV cache types, flash_attention) require domain knowledge
  the auto-tuner doesn't have. Operator-in-the-loop is the safety gate.

- **Detection**: agent confuses `--check` (lightweight validation) with `--self-test` (heavyweight inference probes).
  **Rule**: `--check` is the first diagnostic (fast, no inference); `--self-test`
  is the deeper end-to-end validation (slower, real inference calls).
  **Reasoning**: use `--check` for "did config / Docker / GPU work?" and
  `--self-test` for "does inference actually succeed across all modalities?"

- **Detection**: agent treats `--observe` and `--metrics` as redundant.
  **Rule**: `--observe` is broader (health + GPU + P2P + features all-in-one);
  `--metrics` is deeper on Prometheus + GPU + API call stats specifically.
  Use `--observe` for "show me state"; `--metrics` for "show me numbers".
  **Reasoning**: different scope, different output shape; not interchangeable.

## Reference exemplars

- `aicp/cli/main.py` `_run_check()` (line ~771) — the validation pipeline
- `aicp/cli/main.py` `_run_self_test()` (line ~955) — end-to-end probes
- `aicp/cli/main.py` `_run_capabilities()` (line ~1252) — capability listing
- `aicp/cli/main.py` `_run_auto_config()` (line ~1525) — GPU detection + tuning
- `aicp/cli/main.py` `_run_metrics()` (line ~1388) — live Prometheus snapshot
- `aicp/core/observability.py` — get_system_status / get_loaded_models / measure_request helpers
- `wiki/decisions/01_drafts/asymmetric-kv-cache-quantization-q4-keys-q2-values.md` — why auto-config doesn't tune KV cache types
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` — Category D rationale for this skill's existence

## Domain context

AICP's runtime ops surface is intentionally layered: `--check` (fast,
config + availability), `--self-test` (slower, end-to-end inference probes),
`--observe` (live state snapshot), `--metrics` (deep Prometheus), `--bench`
(performance measurement), `--capabilities` (inventory), `--auto-config`
(GPU-aware tuning). Each has a focused purpose; the contract-compliant NEXT
lines guide the operator from one to the next as needed.

## Related skills

| Skill | When to use |
|-------|-------------|
| `aicp-ops-metrics` | When the focus is metrics + cost (per-backend tokens/cost/latency) specifically |
| `aicp-ops-dlq` | When `--check` flagged failures and DLQ has entries to investigate |
| `aicp-ops-tasks` | When the diagnosis points to workflow stage gates blocking ops |
| `aicp-model-mgmt` | When `--auto-config` reveals models not yet installed |
| `quality-performance` | When `--bench` results need rigorous regression analysis |
| `infra-monitoring` | When setting up dashboards/alerts (this skill consumes; that one builds) |
| `infra-security` | When the runtime exposure surface (LocalAI port + MCP server) is the concern |
