---
name: local-ai-model-matcher
description: Safely auto-detect the current machine's hardware (GPU, VRAM, system RAM, OS) with read-only commands, then recommend the top 3 local AI models to run — most powerful that fits, best for coding, and best small-and-fast — each with download links. Use when someone asks "what AI models can my computer run" or "what's the best local model for my rig".
---

# Local AI Model Matcher

You read the user's **actual machine specs** and recommend exactly **3 local AI
models** with download links. You do NOT ask the user to type their specs — you
detect them yourself using safe, read-only commands.

Run this from the user's project root (or anywhere — it doesn't touch their files).

Model picks are grounded in a June 2026 sweep of public conversations
(r/LocalLLaMA, r/ollama, Hacker News, NVIDIA Developer Forums) plus David Ondrej's
0xSero interview. These are community signals to test, **not guarantees** — real
VRAM/speed depends on quant, KV cache, context length, runtime, and drivers.

## SAFETY RULES — read first, do not skip

- **Read-only only.** Only run the exact detection commands listed below.
- **Never** write, move, or delete files. **Never** use `sudo`. **Never** install
  anything. **Never** make network calls during detection.
- Before detecting, tell the user in one line what you'll read ("I'll read your GPU,
  VRAM, RAM, and OS — read-only, nothing is changed").
- If a command isn't found, skip it gracefully. Never guess specs you couldn't read.

## Step 1 — Detect the OS

- `uname -s` → `Darwin` = macOS, `Linux` = Linux
- Windows: PowerShell is typical; check `$PSVersionTable` or `ver`.

Prefer the bundled helper if present:
- macOS/Linux: `bash scripts/detect-specs.sh`
- Windows: `powershell -ExecutionPolicy Bypass -File scripts/detect-specs.ps1`

## Step 2 — Detect hardware (read-only)

### macOS (Apple Silicon shares unified memory)
```bash
sysctl -n hw.memsize                    # total RAM (bytes)
sysctl -n machdep.cpu.brand_string      # CPU / chip
system_profiler SPDisplaysDataType      # GPU / chip / cores
```
Apple Silicon: treat **~75% of unified memory** as usable for model weights.

### Linux
```bash
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader   # NVIDIA + VRAM
free -h                                                          # system RAM
lscpu | grep -E "Model name|^CPU\(s\)"                           # CPU
lspci | grep -Ei "vga|3d|display"                               # any GPU (fallback)
```
No `nvidia-smi` → likely no NVIDIA GPU; fall back to CPU/iGPU + small models.

### Windows (PowerShell)
```powershell
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
Get-CimInstance Win32_Processor | Select-Object Name
```
`AdapterRAM` can misreport — if it looks wrong, ask the user to confirm VRAM. Use
`nvidia-smi` if present (most reliable).

## Step 3 — Compute usable VRAM

- **Dedicated GPU:** usable = sum of VRAM minus ~1–2GB/card overhead.
- **Apple Silicon:** usable ≈ 75% of unified memory.
- **No dedicated GPU:** small models in system RAM on CPU only (slow) — cap at ≤9B 4-bit.

VRAM estimate: `VRAM_GB ≈ params_B × bytes_per_param × 1.2` (+ a few GB for KV cache).
`4-bit ≈ 0.6×params_B`, `8-bit ≈ 1.2×params_B`. For **MoE**, the *total* params must
fit in memory, but speed tracks the *active* params (e.g. `35B-A3B` = 35B total /
3B active). Always leave headroom for KV cache and your agent's context.

## Step 4 — Map specs to a tier, then pick 3 models

Use the tier closest to the detected usable VRAM (or unified memory):

| Tier | Hardware | Run these |
|---|---|---|
| **No GPU / 8–16GB RAM** | CPU-only, old 4GB GPU, GTX 1650-class | Phi-4 Mini, Qwen3.5 4B, Gemma 3/4 4B, Llama 3.2 3B. Not a real Claude-Code replacement |
| **Apple Silicon 16GB** | M-series 16GB unified | Qwen3.5 4B; small embedding + transcription. Avoid 9B+ if it swaps |
| **8GB VRAM + 32GB RAM** | RTX 4060/3050 8GB | Qwen3.5 9B Q4, Gemma4 E4B, Qwen3:8B Q4. Advanced: Qwen3.6-35B-A3B Q4 with expert offload |
| **12GB VRAM + 32–64GB** | RTX 3060/3080 Ti 12GB | Qwen3.6-35B-A3B Q4/Q5 (partial offload), Gemma-4-26B-A4B. Keep system prompts small |
| **16GB VRAM + 64GB** | RTX 5080/5070 Ti 16GB | Qwen3.6-27B-IQ4_XS (turbo KV) — aggressive pick; Qwen3 14B (safe); Devstral / Mistral Small 24B; Gemma4 E4B (fast) |
| **24GB VRAM** | RTX 3090 / 4090 24GB | qwen3-coder:30b, Qwen3.6 27B, Qwen3.6-35B-A3B, Gemma 4 26B-A4B. Don't assume 70B Q4 fits |
| **32GB+ / dual 3090 / unified** | RTX 5090 32GB, 2× 3090 48GB, DGX Spark/Strix Halo | Qwen3.6 27B, 35B-A3B, Gemma 31B Q4, Gemma 26B-A4B; 70B-class with enough VRAM/offload. On unified memory, prefer MoE |
| **96GB (RTX 6000 Pro)** | RTX PRO 6000 / 6000 96GB | Qwen3.6 27B Q8 @ up to 256k context, ~8 concurrent (Linux/vLLM); 70B–80B class |
| **192–512GB+ unified/system, or multi-node** | 256GB Mac Studio, 24GB GPU + 192–256GB RAM (offload), 4× GB10/DGX Spark cluster, 8× A100/H100-class | **GLM 5.2** — local GGUF only (`unsloth/GLM-5.2-GGUF`): 1-bit ~217–228GB · 2-bit ~238–254GB · Q4 ~365–467GB. 192GB → 1-bit only; 256GB → 2-bit; cluster → Q4/IQ4. Expect slow tok/s and quality loss at low bit. **`glm-5.2:cloud` is NOT local** |

### The 3 picks

1. **🔥 Most powerful you can run** — highest-quality model that fits usable VRAM
   with room for KV cache (prefer 4-bit if 8-bit won't fit). State the quant.
2. **💻 Best for coding** — strongest coding/agentic model that fits. Qwen3.6 27B,
   qwen3-coder:30b, and Qwen3.6-35B-A3B are the repeated community coding picks;
   Devstral / Mistral Small 24B as alternatives.
3. **⚡ Best small + fast** — leaves headroom, high tok/s for always-on tool routing:
   Gemma4 E4B, Qwen3:8B, Qwen3.5 4B, Phi-4 Mini.

If one model is the best answer for two slots, pick the next-best for the second so
the user gets variety. Honor the rule: small models for always-on routing, bigger
models for fewer, harder calls.

**Very-large-memory machines (≥192GB unified/system):** GLM 5.2 becomes the "🔥 most
powerful you can run" — but only as a local GGUF (`unsloth/GLM-5.2-GGUF`), sized to
memory (192GB → 1-bit, 256GB → 2-bit), and warn it's slow with quality loss at low
bit. Never recommend `ollama run glm-5.2:cloud` as "local" — that tag is cloud-routed.
Still give a fast 💻 coding and ⚡ small pick (Qwen3.6 27B, Gemma4 E4B) for daily use.

## Download links

Give clickable links for each pick. If unsure of the exact repo slug, link the
search page rather than inventing a slug:
- Ollama: `https://ollama.com/search?q=<model>` (e.g. `qwen3-coder`, `gemma`, `qwen3`)
- Hugging Face: `https://huggingface.co/models?search=<model>`
- LM Studio: `https://lmstudio.ai/models`
- For GLM 5.2 link the local GGUF, `https://huggingface.co/unsloth/GLM-5.2-GGUF`
  (via llama.cpp / LM Studio / Ollama HF pull) — not the cloud-routed `glm-5.2:cloud` tag.

## Output format

```
I read your machine (read-only):
- OS: <os>   CPU: <cpu>
- GPU: <gpu(s)>   Usable VRAM: <N> GB   System RAM: <N> GB
- Tier: <matched tier>

## Top 3 models for your rig

🔥 **Most powerful you can run:** <model> @ <quant>
   ~<VRAM> GB · <one-line why> · <Ollama> · <HF> · <LM Studio>

💻 **Best for coding:** <model> @ <quant>
   ~<VRAM> GB · <why it's strong for agentic coding> · <links>

⚡ **Best small + fast:** <model> @ <quant>
   ~<VRAM> GB · leaves headroom, great for always-on tool routing · <links>

**Want to run the next tier up?** <model> needs <hardware>. Plan it with the Rig
Planner skill: https://github.com/Maciejdziuba/local-ai-rig-planner
```

Community signals from June 2026 (r/LocalLLaMA, r/ollama, HN, NVIDIA forums) + the
0xSero podcast — candidates to test, not guarantees. Model tags vary by runtime;
verify the exact tag in Ollama / LM Studio / Hugging Face before downloading.
