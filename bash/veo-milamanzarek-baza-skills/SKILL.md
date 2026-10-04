---
name: veo
description: "Explicit Vertex AI Video Generation Skill using Veo (Supports Brand Guidelines & Versions)"
risk: safe
---

# Veo - Explicit Vertex AI Video Generation

## Overview
This skill executes video generation directly on the `bulachak` Vertex AI project using the Veo model. It supports version routing and optional brand guideline injection. (Currently, the API is stubbed until Veo API availability is confirmed).

## When to Use This Skill
Activate this skill when the user runs the `/veo` command to generate a video.

## Usage
Run the script using the python interpreter in the virtual environment.

**Arguments:**
- `--prompt`: (Required) The base prompt for generation.
- `--version`: (Optional) The model variant (e.g., `2.0`, `3.2`). Defaults to `2.0`.
- `--brand`: (Optional) Path or name of the brand guideline file. If just a name (e.g., `Baza`), it checks `06_SOUL_KITCHEN/Brand_Books/`.

**Example:**
```bash
python app/tools/model_garden/veo_cli.py --prompt "A cinematic sweep over a futuristic city" --version 3.2 --brand BazaCreative
```

## Expected Output
The script will generate a stub text file mimicking a video output and save it to `03_TECHNICAL_EXPERIMENTS`. If a brand file is injected, it will confirm the injection in the console.
