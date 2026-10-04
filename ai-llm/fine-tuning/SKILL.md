---
name: fine-tuning
description: "Training and tuning LLMs — Unsloth LoRA/QLoRA/full fine-tuning, GRPO reinforcement learning, VRAM sizing, hyperparameters (rank, alpha, learning rate, epochs, batch), export to GGUF/vLLM/Ollama/merged weights, plus hosted tuning (OpenAI fine-tuning API, Vertex AI Gemini SFT). WHEN: \"fine-tune a model\", \"Unsloth\", \"LoRA\", \"QLoRA\", \"LoRA rank\", \"lora_alpha\", \"GRPO\", \"train a reasoning model\", \"reward function\", \"save_pretrained_gguf\", \"push_to_hub_merged\", \"merged_16bit\", \"how much VRAM to train\", \"fine-tune vs RAG\", \"tuningJobs\", \"fine_tuning/jobs\", \"adapter_size\", \"learning_rate_multiplier\". Do NOT use for building or cleaning the training corpus itself (chat/JSONL schemas, dataset types, synthetic data generation, quality filtering) — that is the training-datasets skill; for measuring a tuned model's quality (graders, LLM-as-judge, regression suites) — that is the evals skill; for picking an off-the-shelf frontier model instead of training one — that is the model-selection skill; for prompt/tool/caching work on the hosted Claude API — that is the claude-api skill. GPU scheduling on Kubernetes belongs to the containers plugin."
license: MIT
---

# Fine-Tuning LLMs

Covers deciding whether to train at all, then doing it: Unsloth (LoRA/QLoRA/FFT, GRPO), hardware sizing, hyperparameters, export/deployment, and the hosted alternatives (OpenAI, Vertex AI). All facts here are sourced from vendor docs fetched 2026-08-05; anything the sources did not settle is marked **unverified** and must be checked live, never filled in from memory.

## Decide before you train

Always answer "should this be a fine-tune?" before touching a GPU. Wrong-layer fixes are the most expensive failure mode in this skill.

| Symptom | Right tool |
|---|---|
| Model lacks facts that change often (docs, tickets, prices) | RAG — retrieval never touches weights, so updates need no retrain |
| Model must sound a fixed way, follow a house format, or reason in a domain idiom | Fine-tune — behavior/style is what weights encode |
| Task is specialized, repetitive, nuanced; latency and one-less-moving-part matter | Fine-tune — no retrieval hop at inference |
| Both knowledge freshness *and* behavior control | Both. Unsloth calls the hybrid the best-results default: greater accuracy, better usability, fewer hallucinations |

Unsloth's framing: fine-tuning can replicate all of RAG's capabilities, but not vice versa — which is a capability claim, not a cost claim. Cheaper, faster options still win when they suffice.

**Unverified:** the corpus sources frame this decision as fine-tune vs RAG only. They do not rank prompt engineering as a third alternative. Do not attribute a "try prompting first" rule to Unsloth or OpenAI docs — say it is general practice, or route the architecture question to the `overview` skill.

Never promise a fine-tune will "add knowledge" cheaply when the knowledge is volatile. Never propose full fine-tuning as the default: Unsloth states FFT is usually unnecessary because a correctly-tuned LoRA can match it.

## Pick the method

| Method | What it trains | Memory | Use when |
|---|---|---|---|
| **QLoRA** | LoRA adapters over a 4-bit base | ~75% less than 16-bit LoRA | Default. Cheapest entry point; with Unsloth dynamic 4-bit quants the accuracy loss vs 16-bit LoRA is described as negligible |
| **LoRA** | Adapters over a frozen 16-bit base | ~4× less VRAM than FFT | You have headroom and want the 16-bit base path |
| **FFT** | All weights | Highest | Rare — only with evidence LoRA plateaued |

Start with QLoRA on a small instruct model (Unsloth's beginner pick: Llama 3.1 8B). Escalate only on measured failure.

## Gate on VRAM first

Quote this table before recommending a model size — most "it OOM'd" tickets are a sizing mistake, not a code bug.

| Params | QLoRA (4-bit) | LoRA (16-bit) |
|---|---|---|
| 3B | 3.5 GB | 8 GB |
| 7B | 5 GB | 19 GB |
| 70B | 41 GB | 164 GB |
| 405B | 237 GB | 950 GB |

Rules of thumb from the docs: for reasoning/RL work, parameter count in billions ≈ VRAM in GB; a free 16 GB Colab GPU comfortably handles GRPO up to roughly 16B. Colab's free tier is 15 GB VRAM.

Hardware floor: NVIDIA CUDA Capability 7.0+ (2018 and newer), through Blackwell RTX 50. Confirmed working: V100, T4, Titan V, RTX 20/50 series, A100, H100, L40. GTX 1070/1080 run but are slow. AMD and Intel GPUs have platform-specific install guides. Apple Silicon/MLX was in development, not GA, at fetch date — never state it as supported.

When OOM hits, cut batch size first. Unsloth names batch size set too high as the explicit common cause.

## Choose the base model

Unsloth has dedicated support for Qwen (2 through 3.6), Llama (2 through 4), Gemma (2, 3, 3n, 4), DeepSeek (V3, V3.1, R1 and distills), Mistral (Small, Large, NeMo, Magistral, Devstral, Pixtral, Mixtral), GLM (4.5–5), Phi (3, 3.5, 4), Kimi (K2 through K3), plus NVIDIA Nemotron, gpt-oss, MiniMax, TinyLlama, and SmolLM. Sizes run 270M to 675B, but the practical working range is 3B–70B — anchor recommendations there unless the VRAM table says otherwise.

Each model ships in three shapes: GGUF (llama.cpp / Unsloth Studio), 4-bit safetensors (inference or QLoRA training), and 16-bit instruct/base weights. Pick the 4-bit safetensors for a QLoRA run and the 16-bit weights for LoRA.

Fine-tuning is not text-only. Unsloth ships notebooks for vision/multimodal (Gemma 4, Qwen3.5, Qwen3-VL, Ministral 3, DeepSeek-OCR, Llama 3.2 Vision), text-to-speech (Sesame-CSM, Orpheus-TTS, Llasa-TTS, Spark-TTS), speech-to-text (Whisper Large V3), and embeddings (EmbeddingGemma 300M, Qwen3-Embedding 4B, BGE M3, ModernBERT-large). Point users at the matching notebook rather than adapting a text recipe by hand.

For choosing a *hosted frontier model* instead of training one, hand off to the `model-selection` skill — this skill only covers models you can train.

## Install

```bash
uv pip install unsloth --torch-backend=auto     # recommended; auto-detects CUDA/torch
pip install unsloth                             # plain pip
uv pip install unsloth vllm --torch-backend=auto  # add vLLM for fast RL rollouts
```

Requirements: Linux/WSL (Ubuntu 20.04+), Windows 10/11 64-bit, or macOS 12+; Python ≥3.11 and <3.14 (3.13 supported); CUDA Toolkit 12.4+ (12.8+ on Blackwell); Git, CMake, a C++ compiler, and an env manager. Core deps: torch, xformers, bitsandbytes, triton.

Pin the CUDA/Torch combo only when auto-detection misfires — see `references/unsloth-setup.md` for the extras tags (`cu118`/`cu121`/`cu124`, `-ampere` suffix), the dedicated-venv recipe, and the bleeding-edge main-branch install.

Run `scripts/preflight-unsloth.sh` (read-only) to check a box against these requirements before debugging a failed install.

## Baseline training config

Start here, change one thing at a time, and justify every deviation.

| Knob | Start at | Why / range |
|---|---|---|
| `learning_rate` | `2e-4` | Range `2e-4` → `5e-6`; use `5e-6` for RL |
| `num_train_epochs` | 1–3 | Above 3, overfitting risk climbs sharply |
| LoRA rank `r` | 16 or 32 | Options 8/16/32/64/128. Bigger model + simpler data → smaller rank; smaller model + complex data → bigger rank |
| `lora_alpha` | `r` or `2r` | Keep `α/rank ≥ 1` |
| `lora_dropout` | 0 | Range 0–0.1; 0 is what Unsloth's kernels are optimized for |
| `weight_decay` | 0.01 | Range 0.01–0.1 |
| warmup steps | 5–10% of total | Gradual LR ramp |
| `per_device_train_batch_size` | 2 | Primary VRAM driver |
| `gradient_accumulation_steps` | 8 | Raises effective batch without extra VRAM |
| effective batch | 16 | `batch × accum`; `2×8` ≡ `32×1` ≡ `16×2` in update quality |
| `bias` | `"none"` | Fewer trainable params, minimal quality cost |
| `target_modules` | `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` | Always all major linear layers — targeting fewer saves only "minimal" memory for real quality loss |
| scheduler / seed | linear or cosine / any int (42, 3407) | Reproducibility |

Update math: standard LoRA is `W' = W + (α/rank)·A·B`. Rank-stabilized LoRA is `W' = W + (α/√rank)·A·B`, enabled with `use_rslora=True`.

Always train on completions only (mask prompt tokens out of the loss) — the docs report it "increases accuracy by quite a bit."

**Read `references/lora-hyperparameters.md`** before tuning LR, rank, or alpha beyond the defaults, or when a run under- or over-fits.

### Reading the run

- Training loss below **0.2** → treat as an overfitting signal, not a win.
- Short run converging too slowly → raise LR. Long run struggling → lower LR instead. The docs say to experiment with both.
- Model not following the training data closely enough (classification/extraction) → more epochs. Output diversity unexpectedly collapsing → fewer epochs. Not converging at all → higher LR.
- Always validate on held-out data; training loss alone never establishes quality. Build the actual scoring harness with the `evals` skill.

Dataset shape drives more of the outcome than any knob here — quality beats quantity, and a doubling of data yields roughly one more increment of improvement each time. Take dataset construction to the `training-datasets` skill; `references/lora-hyperparameters.md` keeps only the data-quality checks OpenAI ties directly to a tuning run.

## GRPO and reinforcement learning

GRPO (Group Relative Policy Optimization) is the technique DeepSeek used for R1-style reasoning models: each generation is scored relative to its peers for the same prompt, so no separate critic/value model is needed as in PPO.

Prerequisites, in order: understand the standard fine-tuning path first, then be able to write reward functions — a GRPO run without a meaningful reward function optimizes noise. Use `max_steps ≥ 300` (the docs' recommended minimum) and enable `use_vllm` for fast in-loop rollouts.

```python
loss_type = 'grpo',          # or 'dr_grpo', 'dapo', 'bnpo'
epsilon = 0.2,
epsilon_high = 0.28,         # one-sided clipping
delta = 1.5,                 # two-sided clipping
mask_truncated_completions = True
```

Reward functions are plain Python (e.g. +1 for a required keyword, −1 for excessive length); Unsloth ships pre-built ones for GSM8K-style math with five evaluation methods. Data stays question/answer pairs plus a system prompt that forces structured reasoning (`<reasoning>` / `<answer>` tags).

**Read `references/grpo-rl.md`** for the full `GRPOConfig` field list, the reward-function and system-prompt patterns, and GRPO save paths.

## Export and deploy

Pick the export by target runtime — the wrong one is the second-most common post-training failure.

| Target | Call |
|---|---|
| llama.cpp / Ollama / LM Studio | `model.save_pretrained_gguf(dir, tokenizer, quantization_method="q4_k_m")` |
| vLLM native serving | `model.save_pretrained_merged(dir, tokenizer, save_method="merged_16bit")` then `vllm serve dir` |
| HF Hub (merged) | `model.push_to_hub_merged("hf/model", tokenizer, save_method="merged_16bit", token="")` |
| HF Hub (GGUF) | `model.push_to_hub_gguf("hf_user/dir", tokenizer, quantization_method="q4_k_m")` |
| Adapter-only serving | Save the LoRA adapter (~100 MB) and load it against the base |

Quantization choices: `q4_k_m` (quality/size hybrid — Q6_K for half of `attention.wv` and `feed_forward.w2`, Q4_K elsewhere), `q5_k_m` (same strategy, higher precision), `q8_0` (fast, acceptable tradeoff), `f16` (fastest conversion, full accuracy, largest file). OOM during GGUF save → `maximum_memory_usage = 0.5`.

Never merge to 4-bit for general deployment — the docs explicitly discourage it unless you know exactly what the 4-bit model is for. vLLM's native path needs a full merged checkpoint, not a bare adapter.

**The chat template at inference must exactly match the one used in training.** Template mismatch is cited as the single most common cause of gibberish after export. Unsloth auto-generates a `Modelfile` next to the GGUF containing that template — inspect it before `ollama create`.

**Read `references/export-deployment.md`** for the manual llama.cpp conversion path, the full Ollama walkthrough, and quantization details.

## Hosted tuning alternatives

Reach for hosted tuning when you want no GPU ops and accept vendor lock-in and per-token training bills.

**OpenAI** — as of 2026-08-05 the fine-tuning platform is being wound down: closed to new users, existing users can create jobs "for the coming months," and already-tuned models stay servable until their base model is deprecated. Never recommend it as a greenfield path without stating this. Flow: upload JSONL (`purpose="fine-tune"`, chat-format lines, 10-line hard floor, 50+ recommended) → `POST /v1/fine_tuning/jobs` → poll → read `fine_tuned_model`.

**Vertex AI (Gemini SFT)** — JSONL with `role: user` / `role: model` (not `assistant`). Knobs: `epochs`, `learning_rate_multiplier`, `adapter_size` (Vertex's LoRA-rank equivalent); **default values and allowed ranges were not resolved from the fetched docs — unverified, check live**. Training billed as dataset tokens × epochs per 1M tokens; a tuned endpoint's inference price equals the base model's, with no premium.

**Read `references/hosted-tuning.md`** for endpoints, the OpenAI pricing table, Vertex surfaces and pricing, and the explicit list of unresolved gaps.

### Self-host vs hosted

| | Unsloth (self-host) | OpenAI | Vertex AI |
|---|---|---|---|
| Cost shape | GPU time you own or rent | Per training token, except o4-mini at $100/hour | Per 1M training tokens = dataset tokens × epochs |
| Inference premium | None — you serve the weights | Per-token rates above base tiers | None; tuned endpoint prices equal the base model |
| Weights | Yours; exportable to GGUF/vLLM/Ollama | Vendor-held, callable by model ID only | Vendor-held, served on a Vertex endpoint |
| Data-format schema | Your choice of chat template | `role: user` / `assistant` | `role: user` / `model` |
| Availability | Open | Winding down; closed to new users | Open |

Choose self-host whenever weight portability, on-prem inference, or GRPO-style RL matters — hosted tuning offers none of those in these sources.

## Common failure modes

| Symptom | Cause and fix |
|---|---|
| CUDA OOM during training | Batch size too high — the docs' named common cause. Lower `per_device_train_batch_size` and raise `gradient_accumulation_steps` to hold the effective batch constant |
| OOM during GGUF save | Pass `maximum_memory_usage = 0.5` to `save_pretrained_gguf` |
| Gibberish after export to Ollama | Chat template at inference differs from training — the docs' most common cause. Inspect the auto-generated `Modelfile` |
| vLLM won't load the model | vLLM's native path needs merged 16-bit weights, not a bare LoRA adapter |
| Training loss ≈ 0.05, real outputs worse | Overfitting — loss below 0.2 is a warning, not a win. Cut epochs (stay in 1–3) or reduce rank |
| Output diversity collapsed | Too many epochs; reduce them |
| Model ignores the training data | Too few epochs, or LR too low; raise epochs first for classification/extraction, then LR |
| Run never converges | Raise LR — but on a *long* run prefer lowering it and training longer |
| Quality worse than expected at any rank | Check `target_modules` covers all seven linear layers before touching rank |
| Install fails / wrong CUDA wheel | Pin the CUDA+Torch extras tag instead of relying on auto-detection |
| Deployed 4-bit merge behaves oddly | Docs discourage merging to 4-bit for general deployment; export merged 16-bit or GGUF instead |

## Reference files

- `references/unsloth-setup.md` — full requirements matrix, all install variants and CUDA/Torch pins, GPU support, VRAM table, supported model families, notebook coverage for vision/TTS/embedding modalities.
- `references/lora-hyperparameters.md` — LoRA vs QLoRA vs FFT detail, the 8-step workflow, complete hyperparameter table with ranges, RSLoRA, LR heuristics, overfitting signals, OpenAI's data-quality checks for an in-flight run.
- `references/grpo-rl.md` — GRPO mechanics, `GRPOConfig`, reward functions, reasoning data format, saving GRPO models.
- `references/export-deployment.md` — GGUF/vLLM/Ollama/merged export in full, quantization methods, manual llama.cpp build, chat-template gotcha.
- `references/hosted-tuning.md` — OpenAI fine-tuning API (schema, endpoints, hyperparameters, pricing, wind-down status) and Vertex AI Gemini SFT (format, knobs, pricing), with gaps marked.

## Diagnostic scripts

- `scripts/preflight-unsloth.sh` — read-only check of OS, Python version, CUDA toolkit, GPU compute capability and VRAM against Unsloth's documented requirements. Run before debugging install or OOM failures.

## Sources

- https://docs.unsloth.ai/get-started/beginner-start-here/unsloth-requirements
- https://docs.unsloth.ai/get-started/install-and-update
- https://docs.unsloth.ai/get-started/unsloth-model-catalog
- https://docs.unsloth.ai/get-started/unsloth-notebooks
- https://docs.unsloth.ai/get-started/fine-tuning-llms-guide
- https://docs.unsloth.ai/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide
- https://docs.unsloth.ai/get-started/fine-tuning-for-beginners
- https://docs.unsloth.ai/get-started/fine-tuning-for-beginners/faq-+-is-fine-tuning-right-for-me
- https://docs.unsloth.ai/get-started/reinforcement-learning-rl-guide/tutorial-train-your-own-reasoning-model-with-grpo
- https://docs.unsloth.ai/basics/inference-and-deployment/saving-to-gguf
- https://docs.unsloth.ai/basics/inference-and-deployment/vllm-guide
- https://docs.unsloth.ai/basics/inference-and-deployment/saving-to-ollama
- https://platform.openai.com/docs/guides/supervised-fine-tuning
- https://platform.openai.com/docs/guides/fine-tuning-best-practices
- https://platform.openai.com/docs/pricing
- https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-supervised-tuning
- https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-use-supervised-tuning
- https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/tuning
- https://cloud.google.com/vertex-ai/generative-ai/pricing

Fetched: 2026-08-05
