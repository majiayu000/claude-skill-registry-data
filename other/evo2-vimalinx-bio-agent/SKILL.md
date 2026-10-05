---
name: evo2
description: Use when working from the local Evo 2 repository for DNA-sequence scoring, embeddings, generation, or phage-genome design experiments.
allowed-tools: Bash
---

# evo2

Workspace-local gateway for the Evo 2 repository at `/home/vimalinx/Projects/bio_studio/repositories/active/evo2`. The repo includes the upstream README, `examples/run_evo2.py`, and a `phage_gen/` subproject, but the current Python environment is not fully ready for direct imports.

## Quick Start

- **Repository:** `/home/vimalinx/Projects/bio_studio/repositories/active/evo2`
- **Documented repo check:** `python -m evo2.test.test_evo2_generation --model_name evo2_7b`
- **Docker path:** `docker build -t evo2 .`

## When To Use This Tool

- Scoring DNA sequences with Evo 2 forward passes
- Extracting embeddings for downstream genomics tasks
- Generating new DNA sequence continuations from prompts
- Exploring the local Evo 2 phage-design subproject

## Common Patterns

```bash
# Build the local Evo 2 Docker image from the repo
cd /home/vimalinx/Projects/bio_studio/repositories/active/evo2
docker build -t evo2 .
```

```bash
# Run the upstream generation smoke test after installation
python -m evo2.test.test_evo2_generation --model_name evo2_7b
```

```bash
# Run the local example script inside a prepared Evo 2 environment/container
python /home/vimalinx/Projects/bio_studio/repositories/active/evo2/examples/run_evo2.py
```

## Recommended Workflow

1. Decide first whether you want a native install or Docker-based execution.
2. Satisfy the upstream prerequisites before trying imports: CUDA-capable Linux plus the extra inference dependencies the README calls out.
3. Verify the installation with the upstream test module before running custom examples.
4. Use `examples/run_evo2.py` for workspace-local scoring, generation, and embedding patterns, and use `phage_gen/` only after the base Evo 2 stack is working.

## Guardrails

- Direct local import currently fails: `import evo2` raised `ModuleNotFoundError: No module named 'vortex'`.
- Docker images are not prebuilt in this workspace. `docker image inspect evo2` failed with `No such image: evo2:latest`.
- The upstream README requires Linux, CUDA `12.1+`, Python `3.12`, and additional packages such as Transformer Engine and Flash Attention.
- The `40b` checkpoints require multiple GPUs. The example script recommends smaller checkpoints like `evo2_1b_base` for limited VRAM.
- The local `phage_gen/` project depends on Evo 2 being operational first; it is not a self-contained replacement for the base repo setup.
