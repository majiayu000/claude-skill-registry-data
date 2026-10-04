---
name: heretic-abliteration
category: models
description: "Heretic — fully automatic LLM censorship removal (abliteration) and serving the result via Ollama. Wraps p-e-w/heretic: directional ablation (difference-of-means refusal directions, orthogonalizing attn.o_proj + mlp.down_proj) with an Optuna/TPE search that co-minimizes refusal count and KL divergence. Automates the full local workflow with the dependency + device fixes that make it actually run: clean-venv install (+ kernels/jinja2 fixes), device-correct run (CPU on Apple Silicon — MPS is blocked by a PyTorch GQA matmul bug; CUDA for real models), and the HF→GGUF→Ollama bridge. Includes a no-compute fast path: pull a pre-abliterated GGUF straight into Ollama. Use when: (1) decensoring / uncensoring an open-weight LLM locally, (2) running heretic-llm and hitting install or MPS/CUDA errors, (3) converting a Heretic/abliterated HF model to GGUF and serving it via Ollama CLI, (4) pulling a ready-made abliterated model into Ollama, (5) understanding abliteration as an evaluator-governed (EGRI) optimization loop. Triggers on: 'heretic', 'abliteration', 'abliterate', 'decensor', 'uncensor', 'remove refusals', 'refusal direction', 'heretic-llm', 'uncensored model', 'ollama abliterated', 'run heretic locally'. NOT FOR training/fine-tuning safety in, or for API-only models (abliteration needs local weights)."
---

# Heretic — Abliteration + Ollama Serving

Remove refusals from open-weight LLMs with [`p-e-w/heretic`](https://github.com/p-e-w/heretic),
then serve the result locally through the Ollama CLI. Heretic combines directional
ablation ("abliteration") with an Optuna/TPE search that **co-minimizes refusals and
KL divergence** — decensoring the model while preserving its intelligence, no
fine-tuning required.

> **The one architectural fact:** Ollama can't be Heretic's *backend*. Heretic edits
> raw HF weights and reads activations (PyTorch/transformers); Ollama is inference-only
> over GGUF. The link is downstream: **Heretic → GGUF → Ollama**. See
> [references/troubleshooting.md](references/troubleshooting.md).

## Quick Start — pick your path

**Path A — Serve now, zero compute (recommended on Apple Silicon / no GPU):**
```bash
./scripts/ollama-pull-abliterated.sh huihui_ai/llama3.2-abliterate:3b
```

**Path B — Run Heretic yourself, then to Ollama (needs a GPU for real models):**
```bash
./scripts/heretic-install.sh                       # clean venv + dependency fixes
./scripts/heretic-doctor.sh                         # confirm device/tooling
./scripts/heretic-run.sh Qwen/Qwen3-4B-Instruct-2507   # run in a REAL terminal (TTY) to save
./scripts/heretic-to-ollama.sh ./<saved-model> my-heretic Q4_K_M
ollama run my-heretic
```

**Path C — Smoke test on Apple Silicon CPU (tiny model, proves the pipeline):**
```bash
./scripts/heretic-install.sh
./scripts/heretic-run.sh Qwen/Qwen3-0.6B --batch-size 8 --max-batch-size 8 --n-trials 4
```

## Prerequisites

| Tool | Install | Required for |
|------|---------|--------------|
| Python 3.10+ | (system / pyenv — **not** conda base) | running Heretic |
| Ollama | `brew install ollama` | serving (Paths A/B) |
| llama.cpp | `brew install llama.cpp` | GGUF conversion (Path B) — `llama-quantize` + `convert_hf_to_gguf.py` |
| CUDA GPU | local or `broomva/remote-gpu` | running real (4–12B) models |

Apple Silicon note: a GPU is **not** present for Heretic's purposes — MPS is blocked
(see Limitations). Treat Macs as serve-only unless you attach a CUDA box.

## Operations

### Install (clean venv + the two fixes)
```bash
./scripts/heretic-install.sh        # HERETIC_VENV=~/.venvs/heretic by default
```
Creates a dedicated venv (never the conda base env), installs `heretic-llm`, then
applies the dogfood-validated fixes: removes the broken optional `kernels` package
and ensures `jinja2 >= 3.1`. Verifies `import heretic.main` succeeds.

### Doctor (what can I run here?)
```bash
./scripts/heretic-doctor.sh
```
Reports platform, accelerator (CUDA / MPS-blocked / CPU), venv + heretic import,
Ollama daemon, llama.cpp tooling, disk — and the recommended path.

### Run an abliteration
```bash
./scripts/heretic-run.sh <hf-model-id> [extra heretic args]
```
Auto-selects device flags: CUDA → full speed; Apple Silicon / CPU → `--device-map cpu
--quantization NONE` (+ `PYTORCH_ENABLE_MPS_FALLBACK=1`). **Run it in a real terminal**
— Heretic's save menu needs a TTY (piped stdin crashes after optimization, losing the
model). Useful flags: `--n-trials N`, `--batch-size N`, `--kl-divergence-target F`,
`--study-checkpoint-dir DIR` (fresh dir avoids the resume menu).

### Convert a saved model to Ollama
```bash
./scripts/heretic-to-ollama.sh <hf-model-dir> <ollama-name> [quant=Q4_K_M]
```
`HF safetensors → convert_hf_to_gguf.py → llama-quantize → ollama create`.

### Fast path — pull a pre-abliterated model
```bash
./scripts/ollama-pull-abliterated.sh [ollama-model]
```
Pulls a community pre-abliterated GGUF and runs two smoke checks (capability
preserved + false-refusal removed) via the Ollama API.

### Use it AS Claude Code's backend (uncensored local agent)

Ollama serves the **Anthropic Messages API natively** at `/v1/messages` — the exact
protocol Claude Code speaks — so you can point Claude Code at your local abliterated
model with **no proxy** (no claude-code-router, no LiteLLM):

```bash
./scripts/claude-code-on-ollama.sh huihui_ai/qwen2.5-coder-abliterate:14b --smoke   # tool-use probe
./scripts/claude-code-on-ollama.sh huihui_ai/qwen2.5-coder-abliterate:14b           # interactive
```

Under the hood: `ANTHROPIC_BASE_URL=http://localhost:11434  ANTHROPIC_API_KEY=ollama  claude --model <m>` (dummy key — Ollama ignores auth).

**What works — and what doesn't** (validated M4 Pro / 24 GB · Ollama 0.20.7 · 2026-05-31):

**1. Text round-trip** — ✅ chat/Q&A routes Claude Code → Ollama → back. No proxy.

**2. Tool-calling is MODEL-FAMILY-specific** — *not* abliteration, *not* the endpoint.
Same 1-tool probe across `/api/chat`, `/v1/chat/completions`, `/v1/messages`:

| Model | Ollama parses its tool call into a `tool_use` block? |
|-------|------------------------------------------------------|
| `llama3.1:8b` (official) | ✅ all 3 endpoints |
| `llama3.2-abliterate:1b` | ✅ on `/v1/messages` — **abliterated, still works** |
| `qwen2.5-coder:7b` (official) | ❌ emits bare JSON Ollama can't parse |
| `qwen2.5-coder-abliterate:14b` | ❌ emits `<tools>`/`<xml>`-wrapped JSON |

→ Llama-3.x emits the format Ollama extracts; **Qwen2.5 does not** (both official and
abliterated). For any agentic intent, pick a **Llama-3.x** abliterated model.

**3. The full Claude Code agent loop on 24 GB** — ❌ **doesn't complete.** Claude Code's
system prompt + ~32 tool schemas demands a large context, and 24 GB has no room:
- llama3.1 at native **128K ctx ⇒ 30 GB** → overflows RAM → CPU-thrash → empty result.
- capped to **32K ctx ⇒ 11 GB** (fits GPU) → prompt nearly fills the window → empty /
  `llama_decode` crash in the Ollama log.

Small context starves generation; large context overflows RAM — no operating point on
24 GB. Latency is brutal too (a 14B turn ≈ 3.6 min).

**Bottom line:** on a 24 GB Mac a local abliterated model is a usable Claude Code
**chat backend**, but **not a working tool-using agent**. A real local uncensored agent
needs (a) a **Llama-family** abliterated model (tool-format compatible) *and* (b) far
more unified RAM (64–128 GB) or a GPU box — see `broomva/remote-gpu`.

`--smoke` classifies **agentic** / **chat-only** / **no-attempt**. **Dual-use:** an
uncensored backend — use responsibly.

## How abliteration works (and why the KL term matters)

Heretic runs harmful vs. harmless prompts, takes the **difference-of-means** of the
residual-stream activations to get per-layer "refusal directions", then
**orthogonalizes** the attention out-projection (`attn.o_proj`) and MLP down-projection
(`mlp.down_proj`) against them. The Optuna/TPE loop searches the kernel-shape
parameters to **minimize refusals while keeping KL divergence low** on harmless
prompts — the KL leash is what prevents the "lobotomized" failure mode. This is a
textbook evaluator-governed (EGRI) loop: mutable weights, an immutable refusal/KL
evaluator, an Optuna harness, Pareto selection. See
[references/egri-mapping.md](references/egri-mapping.md).

## Validated results (this skill's dogfood, 2026-05-30, M4 Pro)

| Check | Result |
|-------|--------|
| Install + import (after fixes) | ✅ heretic-llm 1.3.0 |
| Full abliteration, Qwen3-0.6B, CPU | ✅ refusals **6/8 → 1/8**, KL **0.0026** |
| Serve `huihui_ai/llama3.2-abliterate:1b` via Ollama | ✅ "Canberra" + benign `kill <pid>` answered |
| MPS forward pass | ✗ PyTorch GQA matmul LLVM abort → CPU |

## Limitations

- **Apple Silicon MPS is blocked** for GQA models (Qwen3, Llama-3, Mistral…) by a
  PyTorch `mps.matmul` bug → must use CPU (slow). Real models need CUDA.
- **CPU is impractical for >1B models** (≈50–110 tok/s). Use `broomva/remote-gpu`.
- **Saving requires a TTY** — Heretic's menus use `questionary`; never pipe stdin.
- **`BNB_4BIT` quantization is CUDA-only** (bitsandbytes).
- **Local weights required** — abliteration cannot touch API-only models.
- **Dual-use.** This removes safety guardrails from models you run. Use responsibly
  and within applicable terms and law.

## References
- [references/troubleshooting.md](references/troubleshooting.md) — every blocker + fix, perf table
- [references/egri-mapping.md](references/egri-mapping.md) — abliteration as an EGRI / RCS loop
- [references/models.md](references/models.md) — input models + pre-abliterated catalog + quant guide
- Upstream: [github.com/p-e-w/heretic](https://github.com/p-e-w/heretic) · [heretic-project.org](https://heretic-project.org)
