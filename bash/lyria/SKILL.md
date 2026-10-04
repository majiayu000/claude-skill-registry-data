---
name: lyria
description: "Explicit Vertex AI Audio Generation Skill using Lyria (Supports Brand Guidelines & Versions)"
risk: safe
---

# Lyria - Explicit Vertex AI Audio Generation

## Overview
This skill executes music generation directly on the `bulachak` Vertex AI project using the Lyria model. It supports brand guideline injection. (Currently, the API is stubbed).

## When to Use This Skill
Activate this skill when the user runs the `/lyria` command to generate music or audio.

## Usage
Run the script using the python interpreter in the virtual environment.

**Arguments:**
- `--prompt`: (Required) The base prompt for generation.
- `--brand`: (Optional) Path or name of the brand guideline file.

**Example:**
```bash
python app/tools/model_garden/lyria_cli.py --prompt "Uplifting synthwave" --brand BazaCreative
```

## Expected Output
The script will generate a stub audio file mimicking a Lyria output and save it to `03_TECHNICAL_EXPERIMENTS`.
