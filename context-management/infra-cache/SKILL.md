---
name: infra-cache
description: Manage AICP's caching surfaces — LocalAI prompt cache (`prompt_cache_path`/`prompt_cache_all` per model YAML), KV cache quantization (`cache_type_k`/`cache_type_v` per asymmetric-KV-cache decision), Anthropic prompt caching (cloud backend), nomic-embed embedding cache. AICP has no general-purpose Redis/Memcached layer — these are inference-specific caches. Loads when the operator says "tune prompt cache" / "KV cache settings" / "Anthropic cache hit rate" / "embedding cache" / "why is LocalAI re-processing the same prompt".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: low
---

# infra-cache

Manage AICP's inference-specific caching surfaces. AICP does NOT use a
general-purpose application cache (Redis, Memcached); caching is scoped
to the inference path:

1. **LocalAI prompt cache** — per-model YAML keys (`prompt_cache_path`,
   `prompt_cache_all`) — caches tokenized prompt prefix on disk
2. **KV cache quantization** — per-model YAML keys (`cache_type_k`,
   `cache_type_v`) — controls VRAM footprint of attention KV cache
3. **Anthropic prompt caching** — cloud backend feature (cache_control
   blocks in API messages) — reduces token cost for stable prompt prefixes
4. **Embedding cache** — nomic-embed's internal cache for repeated text

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "tune prompt cache", "KV cache settings",
  "Anthropic cache hit rate", "embedding cache", "cache eviction"
- **Performance**: "why is LocalAI re-processing the same prompt",
  "first call slow second fast", "VRAM growing with context"
- **Cost**: "Anthropic bill is high", "reduce token cost via caching"
- **Storage**: "prompt cache directory growing", "where do prompt
  caches live"

Do NOT load when:

- The concern is the LRU eviction of MODELS (load `aicp-model-mgmt`;
  per single-active-backend pattern, model swap is different from cache)
- The concern is HTTP response cache (AICP doesn't have one)
- The concern is application-level memoization (load `quality-performance`)

## Operations

### Operation 1 — Configure LocalAI prompt cache per model

**When**: a model frequently sees the same prompt prefix (e.g., system
prompt + tool definitions) and operator wants to skip re-tokenization.

**Process**:

1. Edit `config/models/<name>.yaml`, add:
   ```yaml
   prompt_cache_path: <name>-cache
   prompt_cache_all: true
   ```
2. The `<name>-cache` is a relative path under LocalAI's cache directory
   (auto-created)
3. Restart LocalAI: `docker compose restart localai`
4. Verify: first inference call tokenizes; second call with same prefix
   skips tokenization (visible in latency drop)

**Quality bar**: prompt cache helps when prefix STABILITY > 1KB tokens.
For short prompts (<500 tokens) the cache lookup overhead can exceed
the tokenization saving. Measure before enabling.

### Operation 2 — Tune KV cache quantization per asymmetric pattern

**When**: VRAM is tight or context window needs expanding.

**Process**:

1. Per the asymmetric-KV-cache decision
   (`wiki/decisions/01_drafts/asymmetric-kv-cache-quantization-q4-keys-q2-values.md`),
   Qwen3 family uses `cache_type_k: q4_0` + `cache_type_v: q2_K`
2. For NEW models, follow the same pattern unless empirically tested
   otherwise
3. For existing models, the values are already canonical — DON'T change
   without measuring quality impact (per the decision's gotchas)
4. Verify: model loads with the quant types active (`aicp --model-cmd
   status --model-arg <name>` shows memory usage; lower than f16 baseline
   confirms quantization)

**Quality bar**: NEVER change to `cache_type_k: q2_K` (keys at q2_K
destroy attention quality per the decision). Asymmetric-keys-stronger
is a hard rule.

### Operation 3 — Enable Anthropic prompt caching for cloud backend

**When**: AICP routes to Claude with stable prompt prefixes (system prompt
+ tool definitions) and operator wants to cut token cost.

**Process**:

1. Identify the stable prefix — typically system prompt + tool definitions
   that don't change per request
2. In the cloud backend client (`aicp/backends/...claude...`), wrap the
   stable prefix in a `cache_control: {"type": "ephemeral"}` block
3. Anthropic charges 25% of input cost for cache writes, 10% of input
   cost for cache reads — net savings only if the prefix is reused
4. Monitor cache hit rate via `aicp --metrics` or the response's
   `cache_creation_input_tokens` / `cache_read_input_tokens` fields

**Quality bar**: cache writes cost more than uncached reads — only enable
when reuse is reliable. A one-shot cache write with no read is a net loss.

### Operation 4 — Inspect / clean prompt cache directory

**When**: operator wants to know cache disk usage or reset stale entries.

**Process**:

1. Locate the cache: `docker exec aicp-localai ls /tmp/cache` (or wherever
   LocalAI's prompt_cache_path resolves to inside the container)
2. Inspect sizes — large entries are normal for long-prefix models
3. To reset: `docker exec aicp-localai rm /tmp/cache/<file>` then restart
   LocalAI
4. To prevent regrowth: set `prompt_cache_all: false` for models with
   frequently-changing prefixes

**Quality bar**: clearing the cache is reversible (it'll rebuild on next
call); deletion is per-file safe. Don't bulk-delete the whole cache dir
without restart — LocalAI may have file handles open.

## Gotchas

- **Detection**: agent treats AICP as if it has a Redis cache layer.
  **Rule**: AICP's caches are inference-specific (prompt + KV + cloud
  prompt cache). No general-purpose app cache.
  **Reasoning**: setting expectations correctly avoids architectural
  drift toward unneeded infrastructure.

- **Detection**: agent enables prompt cache for short-prefix models.
  **Rule**: prompt cache helps when prefix is >1KB tokens AND stable.
  Short prefixes don't benefit.
  **Reasoning**: cache lookup overhead is fixed; tokenization saving
  scales with prefix length. Below threshold, lookup costs more than it
  saves.

- **Detection**: agent changes `cache_type_k` to a value other than `q4_0`.
  **Rule**: per the asymmetric-KV-cache decision, keys at q4_0 + values
  at q2_K is the validated combination. Don't deviate without measurement.
  **Reasoning**: keys are quantization-sensitive (softmax exponentiates
  the dot product); q2_K keys destroy attention quality.

- **Detection**: agent enables Anthropic cache without measuring reuse.
  **Rule**: cache writes cost 25% of input; only enable when reuse is
  reliable (write once, read many).
  **Reasoning**: a single cached write with no reads is a net cost
  increase. Validate the access pattern first.

- **Detection**: agent bulk-deletes the prompt cache directory.
  **Rule**: per-file deletion is safe; bulk dir deletion can race with
  LocalAI's file handles. Restart LocalAI after bulk operations.
  **Reasoning**: files in use may be lazy-deleted; bulk operations
  produce transient errors.

## Reference exemplars

- `config/models/qwen3-8b.yaml` — `prompt_cache_path` + `prompt_cache_all`
  + asymmetric KV cache settings (canonical example)
- `config/models/qwen3-30b-a3b.yaml` — same pattern for MoE model
- `wiki/decisions/01_drafts/asymmetric-kv-cache-quantization-q4-keys-q2-values.md` —
  the design rationale
- `aicp/backends/localai.py` — passes through cache config to LocalAI
- (when implemented) `aicp/backends/claude_code.py` — cache_control blocks for Anthropic

## Domain context

AICP's caching is INFERENCE-CRITICAL: prompt cache reduces tokenization
latency, KV cache quantization reduces VRAM footprint enabling larger
context windows, Anthropic prompt caching reduces cloud token cost. Each
is independent and tunable per model. Per single-active-backend, the
prompt cache file is per-model — when models swap, the cache stays on
disk for the previous model's next activation.

## Related skills

| Skill | When to use |
|-------|-------------|
| `aicp-model-mgmt` | When the concern is the BASE model lifecycle (cache is downstream of model) |
| `quality-performance` | When measuring cache hit rate / latency impact |
| `aicp-ops-metrics` | When monitoring cache effectiveness at runtime |
| `infra-monitoring` | When setting up alerts on cache hit rate or growth |
