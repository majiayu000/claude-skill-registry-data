---
name: ai-scientist
description: "SakanaAI AI-Scientist integration — automated scientific discovery via Hermes. Generate ideas, run experiments, write papers, review output — all through MCP tools."
version: 1.0.0
author: SakanaAI, Hermes Agent
license: Apache 2.0
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [scientist, research, paper-generation, experiment, automated-science]
    triggers: [scientist, research-paper, experiment, idea-generation, paper-writing, scientific-discovery]
    related_skills: [open-coscientist, gpt-researcher, arxiv]
---

# AI Scientist — SakanaAI Integration

## Overview

The AI Scientist is a fully automated scientific discovery system from [SakanaAI](https://github.com/SakanaAI/AI-Scientist). It runs through a **complete research lifecycle**:

1. **Idea Generation** → LLM proposes novel research directions
2. **Experiment Execution** → AI writes and runs PyTorch experiments (on GPU)
3. **Paper Writing** → LaTeX paper generation with plots and citations
4. **Review** → LLM-based peer review of the output

This skill connects the AI Scientist to Hermes via an **MCP server** exposing these capabilities as callable tools.

## Prerequisites

- **NVIDIA GPU** (RTX 3090+ recommended) with CUDA 12.4+
- **Python 3.11** (managed via repo venv)
- **OpenRouter API key** — required for all LLM calls
- **LaTeX** (pdflatex + chktex) — for paper generation (optional, can skip)

## API Key Setup (First Step Before Anything Else)

The OpenRouter API key goes in **exactly one place** for Hermes-driven use:

```
${USER_HOME}\AppData\Local\hermes\.env
```

The line is already there commented out — uncomment it and add your key:

```bash
# Find this line:
# OPENROUTER_API_KEY=***

# Change to:
OPENROUTER_API_KEY=sk-or-v1-...
```

This single location feeds the MCP server, cron jobs, and gateway sessions because the Hermes config resolves `${OPENROUTER_API_KEY}` into subprocess environments.

Optional — also set it in the AI Scientist project directory for manual CLI runs:

```
${MY_REPOS}\Documents\github\AI-Scientist\.env
```

## Architecture

```
Hermes Agent
    │
    ▼  (MCP tools)
AI Scientist MCP Server  ─── stdio/SSE ───> hermes_mcp_server.py
    │
    ├── Calls launch_scientist.py (full pipeline)
    ├── Runs subprocesses via AI-Scientist venv
    └── Returns structured JSON results
```

## MCP Tools Available

After adding `ai-scientist` to your Hermes `mcp_servers` config, these tools auto-register:

| Tool | Purpose |
|------|---------|
| `list_templates` | List available experiment templates |
| `list_results` | List completed experiments |
| `generate_ideas` | Generate novel research ideas for a template |
| `run_experiment` | Run full pipeline: ideas → experiments → paper → review |
| `prepare_baseline` | Create baseline runs (required first step) |
| `review_paper` | LLM-based peer review of a generated PDF |
| `system_status` | Check GPU, venv, templates, API keys |
| `read_template_info` | Read template description and seed ideas |
| `run_command` | Execute arbitrary commands in the AI-Scientist venv |

## Quick Start Workflow

### 0. Set API Key (required once)
Add to `${USER_HOME}\AppData\Local\hermes\.env`:
```
OPENROUTER_API_KEY=sk-or-...
```

### 1. Check system readiness:
```
system_status()
```

### 2. List available templates:
```
list_templates()
```

### 3. Prepare a baseline experiment:
```
prepare_baseline(experiment="nanoGPT_lite")
```

### 4. Generate ideas (FREE OpenRouter model):
```
generate_ideas(
    experiment="nanoGPT_lite",
    model="openrouter/qwen/qwen3-coder:free",
    num_ideas=5
)
```

### 5. Run the full pipeline:
```
run_experiment(
    experiment="nanoGPT_lite",
    model="openrouter/qwen/qwen3-coder:free",
    num_ideas=1
)
```

### 6. Review results:
```
list_results(experiment="nanoGPT_lite")
review_paper(pdf_path="${MY_REPOS}/Documents/github/AI-Scientist/results/nanoGPT_lite/.../paper.pdf")
```

## Verification

After setup, confirm the MCP server is live:

```bash
hermes mcp test ai-scientist
# Expected:
#   ✓ Connected (985ms)
#   ✓ Tools discovered: 9

hermes mcp list | grep ai-scientist
#   ai-scientist   ✓ enabled
```

Check imports, GPU, and templates:

```python
from ai_scientist.llm import _is_openrouter_model
assert _is_openrouter_model('google/gemma-4-31b-it:free')
assert not _is_openrouter_model('gpt-4o')

import torch
print(torch.cuda.is_available(), torch.cuda.get_device_name(0))
# → True NVIDIA GeForce RTX 3090

from pathlib import Path
ts = [d.name for d in Path('templates').iterdir() if (d/'experiment.py').exists()]
print(len(ts))  # → 11
```

## OpenRouter Model Support (FREE Models)

The LLM integration supports **any OpenRouter model**. Best **FREE models** ($0/token) per task:

| Task | Model | Context | Why |
|------|-------|---------|-----|
| **Idea Generation** | `openrouter/owl-alpha` | 1M | Free, strong agentic model |
| **Code Writing** | `openrouter/qwen/qwen3-coder:free` | 1M | Code-specialized, structured output |
| **Paper Writing** | `openrouter/owl-alpha` | 1M | Long context, academic writing |
| **Review** | `openrouter/nousresearch/hermes-3-llama-3.1-405b:free` | 131K | 405B param, strongest free |
| **Fallback** | `openrouter/qwen/qwen3-coder:free` | 1M | Code + general all-rounder |

Also good:
- `openrouter/deepseek/deepseek-v4-flash:free` — 1M ctx, fast, the model I'm running on
- `openrouter/nvidia/nemotron-3-super-120b-a12b:free` — 1M ctx, NVIDIA's strongest open model
- `openrouter/moonshotai/kimi-k2.6:free` — 262K ctx, strong multimodal
- `openrouter/meta-llama/llama-3.3-70b-instruct:free` — 131K ctx, reliable

Use the format: `openrouter/provider/model-name:free` (explicit OpenRouter prefix) or just `provider/model-name` (auto-detected).


## Key Files

| File | Purpose |
|------|---------|
| `hermes_mcp_server.py` | Hermes MCP server with all tools |
| `launch_scientist.py` | Main entry point (patched for OpenRouter) |
| `ai_scientist/llm.py` | LLM client factory (patched for generic OpenRouter) |
| `venv/` | Python virtualenv with CUDA PyTorch |
| `templates/` | Experiment templates (nanoGPT, grokking, 2d_diffusion, etc.) |
| `results/` | Generated papers and experiment outputs |

## Pitfalls

- **GPU required**: AI Scientist runs PyTorch experiments. CPU-only runs will be impractically slow. On this machine: RTX 3090 (24 GB) with CUDA 12.4 via PyTorch 2.6.0+cu124.
- **OpenRouter API key**: The single source of truth is `${USER_HOME}\AppData\Local\hermes\.env`. The `.env.example` file in the repo has `***` as a placeholder — DO NOT put the real key there for Hermes-driven workflows, it must go in the Hermes `.env` so `${OPENROUTER_API_KEY}` resolution works in the MCP server config.
- **Aider integration**: The experiment coding phase uses `aider-chat` which needs `OPENROUTER_API_KEY` in the subprocess environment. Since the MCP server config passes it via `env:`, this is handled — but standalone CLI runs need it in the shell.
- **Review was hardcoded to OpenAI**: The original `launch_scientist.py` had two places hardcoding `model="gpt-4o-2024-05-13"` with `openai.OpenAI()` (line 270 for review, line 301 for improvement review). Both were patched to use OpenRouter with `openrouter/google/gemma-4-31b-it:free` and `api_key=os.environ.get("OPENROUTER_API_KEY", ...)`. If you ever re-clone the repo, re-apply these patches.
- **Template baselines**: Each template needs a baseline run (`prepare_baseline`) before `run_experiment` will work. The baseline creates `run_0/final_info.json` which the experiment phase reads. NanoGPT also needs data preparation scripts (`data/enwik8/prepare.py`, etc.).
- **LaTeX (MiKTeX) on Windows**: MiKTeX is installed at `${USER_HOME}\AppData\Local\Programs\MiKTeX\miktex\bin\x64\` but NOT in the system PATH. `shutil.which('pdflatex')` (used by `check_latex_dependencies()`) will fail. The MCP server config injects PATH via the `env:` block. See `references/latex-on-windows.md`.
- **OpenRouter model name resolution**: Models with `openrouter/` prefix are handled explicitly. Models like `google/gemma-4-31b-it:free` (bare `provider/model:free` format) are auto-detected by `_is_openrouter_model()` because they contain `/` and don't match bedrock/vertex_ai/deepseek/gemini prefixes. The `:free` suffix is passed through as part of the model name — OpenRouter handles it.
- **Long runs**: Full experiments can take hours. `run_experiment` launches asynchronously via threading.
- **Windows path note**: All paths in the MCP server use forward-slash paths (`${MY_REPOS}/...`) which work fine on MSYS2/bash and in subprocess calls. The Hermes config uses forward slashes for args and env vars consistently.
- `**launch_scientist.py note`: The `do_idea()` function references `args.engine` from the global scope (line 254). This is a pre-existing bug that works in CLI mode but may fail if the function is imported — the fix would be to pass `engine` as a parameter.

## Reference Files

- `references/setup-and-usage.md` — Venv setup commands, exact patch details, MCP config, verification steps.
- `references/free-openrouter-models.md` — Live-quoted catalog of 27 free OpenRouter models with per-task recommendations.
- `references/latex-on-windows.md` — MiKTeX PATH quirks, version info, config.yaml injection.
