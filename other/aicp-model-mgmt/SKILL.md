---
name: aicp-model-mgmt
description: Manage AICP's base model lifecycle — install/unload/delete/status/update via `aicp --models` and `aicp --model-cmd` CLI. Replaces the deprecated aicp_model_install/unload/delete/status/config/config_update MCP tools per `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md`. Loads when the operator says "install model X" / "unload qwen3-8b" / "delete a model" / "is model X downloaded yet" / "swap models" / "free up VRAM" / "update model config".
allowed-tools: Bash, Read, Edit
effort: low
---

# aicp-model-mgmt

Manage base model lifecycle — install from gallery, check download/load
status, unload from VRAM, delete from disk, update yaml config — via AICP's
`--models` and `--model-cmd` CLI surface. This skill teaches the workflow
using CLI flags, NOT the deprecated `aicp_model_*` MCP tools.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "install model X", "unload qwen3-8b",
  "delete the old codellama", "is model X downloaded yet", "swap models",
  "free up VRAM", "update qwen3-8b config", "what models are installed"
- **VRAM pressure**: operator wants to free GPU memory by unloading the
  current model (single-active-backend pattern means only one base GPU model
  loaded at a time)
- **Pre-deployment setup**: installing the model the active profile depends on
- **Catalog audit**: reviewing which models are configured + which are
  actually downloaded vs gallery-only

Do NOT load when:

- The concern is LoRA adapters layered on a base model (load `aicp-lora` for
  adapter lifecycle — distinct from base model lifecycle)
- The concern is choosing which model is the right default (load
  `quality-performance` for benchmarking, then this skill to install the winner)
- The concern is GPU detection / auto-config (load `--auto-config` workflow —
  separate from manual model lifecycle)

## Operations

### Operation 1 — Install a model from the gallery

**When**: operator wants to add a new model that isn't yet downloaded.

**Process**:

1. Browse: `aicp --models gallery [--models-arg <search>]` to see options
2. Install: `aicp --models download --models-arg <model-id>` (NOT the
   deprecated `--models install` — `download` is the maintained CLI flag)
3. Track progress: `aicp --models job --models-arg <uuid>` (UUID printed by
   the install step) or `aicp --model-cmd status --model-arg <uuid>`
4. After "Download complete", verify: `aicp --models list` shows the model
   in the catalog
5. Activate to use: `aicp --models activate --models-arg <name>` then
   `make local-up` to apply

**Quality bar**: a fresh install should produce a model YAML in
`config/models/<name>.yaml` with sane defaults (gpu_layers, context_size,
KV cache settings per the asymmetric-KV-cache decision). Inspect the YAML
before activating.

### Operation 2 — Unload a model to free VRAM

**When**: operator needs the GPU for a different model (per single-active-backend
pattern, only one base GPU model fits at a time).

**Process**:

1. Verify what's loaded: `aicp --check` (shows GPU active model)
2. Unload: `aicp --model-cmd unload --model-arg <name>` (replaces deprecated
   `aicp_model_unload` MCP tool)
3. Verify VRAM freed: `aicp --check` again — GPU memory should drop
4. To load a different one: `aicp --models activate --models-arg <other>` →
   `make local-up`

**Quality bar**: unload is idempotent — calling it on an already-unloaded
model returns "Failed to unload" but isn't an error condition. Check
`aicp --check` to confirm actual state.

### Operation 3 — Delete a model from disk

**When**: operator wants to permanently remove model files (recover disk space).

**Process**:

1. List: `aicp --models list` to see installed models with file sizes
2. Delete: `aicp --model-cmd delete --model-arg <name>` (replaces deprecated
   `aicp_model_delete` MCP tool) — **interactive confirmation prompt** prevents
   accidental deletion
3. Confirm at the prompt only if intentional — destructive, irreversible
4. Verify: `aicp --models list` should no longer show the model

**Quality bar**: NEVER auto-confirm the delete prompt. The single-character
confirmation is the safety gate the audit decision specifically called out
for destructive admin operations.

### Operation 4 — Check status of a model or download job

**When**: operator wants to know if a model is loaded, downloading, or in
error state.

**Process**:

1. For a model name: `aicp --model-cmd status --model-arg <name>`
   - Output shows state (uninitialized/busy/ready/error) + memory breakdown
2. For a job UUID (from a recent install): `aicp --model-cmd status --model-arg <uuid>`
   - Output shows download progress + status message
3. Alternative for catalog: `aicp --models list` (configured models, not
   runtime status) or `aicp --models monitor --models-arg <name>` (similar
   to `--model-cmd status` but via the `--models` flag)

**Quality bar**: state="ready" + non-zero memory = model is GPU-resident and
serving inference. state="uninitialized" + zero memory = model is configured
but not loaded (will load on first request).

### Operation 5 — Update a model's runtime config

**When**: operator wants to tune a model's parameters (context_size,
gpu_layers, KV cache settings, etc.).

**Process**:

1. Identify the config: `aicp --model-cmd update --model-arg <name>` prints
   the YAML path
2. Edit `config/models/<name>.yaml` in your editor
3. Per the asymmetric-KV-cache decision (see references below), runtime
   `model_config_update` is DISCOURAGED — durable yaml + restart is the
   correct workflow
4. Apply: `docker compose restart localai`
5. Verify: `aicp --check` shows the model loads with the new config

**Quality bar**: changes to `cache_type_k`/`cache_type_v` should follow the
asymmetric pattern (q4_0 keys + q2_K values for Qwen3 family). Don't change
to symmetric without measuring quality regression first.

## Gotchas

- **Detection**: agent uses any `aicp_model_*` MCP tool.
  **Rule**: NEVER call deprecated MCP tools — use `aicp --models` or
  `aicp --model-cmd` CLI.
  **Reasoning**: MCP overhead is paid per turn for tools used during specific
  workflows; CLI+Skills loads this skill on demand only.

- **Detection**: agent attempts to install a model without checking if it's already in the catalog.
  **Rule**: always run `aicp --models list` first. If the model is already
  installed, no download is needed.
  **Reasoning**: re-installing wastes bandwidth + disk and can confuse the
  catalog if the install creates a duplicate config.

- **Detection**: agent runs `aicp --model-cmd delete` without operator confirmation.
  **Rule**: the CLI's interactive `[y/N]` prompt is the safety gate. Don't
  pipe `y` automatically; the operator must explicitly confirm.
  **Reasoning**: per the audit decision, destructive operations should NEVER
  be agent-callable without operator-in-the-loop confirmation.

- **Detection**: agent treats unload + delete as the same operation.
  **Rule**: unload removes from VRAM (reversible by re-loading); delete
  removes from disk (irreversible without re-download).
  **Reasoning**: unload is for VRAM management (single-active-backend swap);
  delete is for disk cleanup (catalog management). Different concerns.

- **Detection**: agent uses runtime `--model-cmd update` to change config.
  **Rule**: per the asymmetric-KV-cache decision, runtime config updates are
  discouraged — edit the yaml file + restart LocalAI for durable changes.
  **Reasoning**: runtime updates don't survive container restart and create
  drift between the yaml (source of truth) and the running config.

## Reference exemplars

- `aicp/cli/main.py` `_run_model_cmd()` — implementation behind this skill's `--model-cmd` ops
- `aicp/cli/main.py` `_run_models()` — implementation behind `--models list/info/activate/download/gallery/etc.`
- `config/models/qwen3-8b.yaml` — canonical model YAML with asymmetric KV cache + flash_attention + prompt cache settings
- `wiki/decisions/01_drafts/asymmetric-kv-cache-quantization-q4-keys-q2-values.md` — why config edits should go through yaml + restart, not runtime mutation
- `wiki/patterns/01_drafts/single-active-backend-with-lru-eviction.md` — why only one GPU model loaded at a time
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` — Category E rationale for this skill's existence

## Domain context

AICP exposes 14 model configs in `config/models/` (Qwen3 family +
Gemma 4 family + legacy + specialized). Per single-active-backend, one base
GPU model is loaded at a time; LRU evicts inactive ones when MAX_ACTIVE_BACKENDS
is exceeded. The `--models` CLI flag covers the most-common workflow (list,
info, activate, download, benchmark, gallery); the `--model-cmd` flag adds
the lifecycle ops migrated from deprecated MCP tools (unload, delete, status,
update).

## Related skills

| Skill | When to use |
|-------|-------------|
| `aicp-lora` | When attaching/listing LoRA adapters on top of a loaded base model |
| `quality-performance` | When benchmarking model variants to choose a winner |
| `aicp-ops-metrics` | When monitoring per-model resource usage |
| `infra-monitoring` | When setting up alerts on model load/swap behavior |
