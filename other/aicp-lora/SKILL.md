---
name: aicp-lora
description: Manage LoRA (Low-Rank Adaptation) adapters on AICP's loaded base models — list currently-attached adapters, attach a new adapter to specialize a base model for coding/analysis/creative tasks. Replaces the deprecated aicp_lora_load + aicp_lora_list MCP tools per `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md`. Loads when the operator says "load a lora" / "attach adapter X to model Y" / "list lora adapters" / "specialize qwen for code" / "what loras are loaded".
allowed-tools: Bash, Read
effort: low
---

# aicp-lora

Manage LoRA adapters via AICP's `--lora-cmd` CLI surface. LoRA adapters
specialize a loaded base model for specific tasks (coding, analysis, creative
writing) without reloading the full model. This skill teaches the inspection
+ attachment workflow using the CLI surface, NOT the deprecated `aicp_lora_*`
MCP tools.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "load a lora", "attach adapter X to model Y",
  "list lora adapters", "specialize qwen for code", "what loras are loaded",
  "swap the lora on this model"
- **Specialization workflow**: operator wants to use a base model with a
  task-specific adapter (e.g., qwen3-8b + code-instruct lora for refactoring)
- **Multi-tenant testing**: comparing inference quality with vs without a
  LoRA adapter on the same base
- **Adapter inventory**: auditing which adapters are currently in use across
  the model fleet

Do NOT load when:

- The concern is the BASE model (load `aicp-model-mgmt` for model lifecycle —
  install/unload/delete) — LoRA is a layer ON a base model, not a model itself
- The concern is fine-tuning a model (LoRA load is RUNTIME ATTACHMENT, not
  training; training is a different workflow not covered here)
- The concern is downloading the LoRA file (operator-deliberate; download via
  `huggingface-cli` or curl, then attach via this skill)

## Operations

### Operation 1 — List currently-attached LoRA adapters

**When**: operator wants to see what adapters are currently active on which
base models.

**Process**:

1. Run `aicp --lora-cmd list`
2. Output shows each base model with its attached adapter(s), or "No LoRA
   adapters loaded" if none
3. The output's closing `NEXT:` line recommends loading an adapter (if empty)
   or proceeding with inference (if populated)

**Quality bar**: a healthy fleet should have predictable LoRA state — operators
shouldn't be surprised by "this base has 3 adapters" when only 1 was expected.
Drift signals an external process is mutating LocalAI state.

### Operation 2 — Attach a LoRA adapter to a base model

**When**: operator wants to specialize a loaded base model with a task-specific
LoRA.

**Process**:

1. Verify the base model is loaded: `aicp --models list` (look for the model
   name in the catalog with non-zero gpu_layers)
2. Verify the adapter file exists at the path or URL the operator provides
3. Run `aicp --lora-cmd load --lora-arg <model> --lora-arg2 <adapter-path-or-url>`
4. Output confirms the attachment: `LoRA adapter loaded: <model> ← <adapter>`
5. The output's closing `NEXT:` recommends verifying with `--lora-cmd list` or
   testing with an inference prompt

**Quality bar**: after attachment, an inference call to the base model should
exhibit the specialization (e.g., better code completion if a code-instruct
LoRA was attached). If output looks identical, the adapter may not have loaded
correctly — re-check with `--lora-cmd list`.

### Operation 3 — Diagnose a LoRA load failure

**When**: `aicp --lora-cmd load` returns an error.

**Process**:

1. Read the error string — common causes:
   - "Cannot connect to LocalAI" → run `aicp --check`; verify Docker container
   - "Model not found" → `aicp --models list` to verify base model name
   - "Adapter not found" → verify the adapter path/URL is reachable from the
     LocalAI container (path inside container vs host can differ)
   - "Adapter format invalid" → some LoRA formats (PEFT vs raw) need conversion
2. The error's NEXT line points to the most likely fix
3. If the underlying issue is unclear, fall back to direct LocalAI logs:
   `docker logs aicp-localai 2>&1 | tail -50`

**Quality bar**: never blame the LoRA without first ruling out base-model
issues — a not-loaded base model can't accept an adapter.

## Gotchas

- **Detection**: agent uses `aicp_lora_load` or `aicp_lora_list` MCP tool.
  **Rule**: NEVER call deprecated MCP tools — use `aicp --lora-cmd list/load`.
  **Reasoning**: MCP overhead is paid per turn for tools used during specific
  workflows; CLI+Skills loads this skill on demand only when needed.

- **Detection**: agent attempts to attach a LoRA without verifying the base model is loaded.
  **Rule**: always run `aicp --models list` first to confirm the base model
  has gpu_layers > 0 (i.e., is GPU-resident).
  **Reasoning**: LoRA attachment to an unloaded base may succeed silently but
  produce no specialization at inference time. The `single-active-backend`
  pattern means only one GPU model is loaded at a time — verify before attaching.

- **Detection**: agent uses host filesystem path for adapter when LocalAI runs in Docker.
  **Rule**: paths must be reachable from INSIDE the LocalAI container; either
  use a URL (HTTPS) or a path under `models/` (which is volume-mounted into the
  container at `/models`).
  **Reasoning**: Docker volume mounts are explicit; arbitrary host paths won't
  resolve from the container. Same gotcha as for base model GGUF files.

- **Detection**: agent attempts to load multiple LoRAs simultaneously on the same base.
  **Rule**: most LoRA implementations support only ONE adapter per base at a time;
  loading a second replaces the first. If multi-adapter is needed, that's a base
  model architecture decision, not a runtime workflow.
  **Reasoning**: LoRA attachment overwrites by default; multi-adapter is a
  specialized capability not standard in llama.cpp at this writing.

- **Detection**: agent treats LoRA as a permanent state change.
  **Rule**: LoRA attachment is RUNTIME state — lost on container restart,
  model reload, or VRAM eviction. To make it persistent, edit the model's
  YAML config or set up a startup script.
  **Reasoning**: per the single-active-backend + LRU eviction pattern, models
  swap; runtime LoRA attachments don't survive swaps.

## Reference exemplars

- `aicp/cli/main.py` `_run_lora_cmd()` — the implementation behind this skill
- `aicp/backends/localai.py` `lora_load()` / `lora_list()` — the underlying API calls
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` — Category E rationale for this skill's existence
- `wiki/decisions/00_inbox/aicp-cli-mcp-outputs-adopt-gateway-output-contract.md` — explains the `NEXT:` lines this skill's commands produce
- `wiki/patterns/01_drafts/single-active-backend-with-lru-eviction.md` — the pattern that constrains LoRA persistence

## Domain context

LoRA (Low-Rank Adaptation) attaches a small set of trainable parameters to
a frozen base model, providing task specialization without retraining the
base. AICP exposes LocalAI's LoRA API via the `--lora-cmd` CLI flag (replaces
deprecated MCP tools). Per the single-active-backend pattern, only one base
GPU model is active at a time; LoRA layers attach to that active base.

## Related skills

| Skill | When to use |
|-------|-------------|
| `aicp-model-mgmt` (pending) | When the concern is the BASE model lifecycle (install/unload/delete) — LoRA is on top of base |
| `aicp-ops-metrics` | When verifying inference performance with vs without LoRA |
| `quality-performance` | When measuring specialization quality empirically |
