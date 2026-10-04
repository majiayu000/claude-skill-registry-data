---
name: gemma
description: "Explicit Vertex AI Text Generation Skill using Gemma Models (Supports Brand Guidelines & Variants)"
risk: safe
---

# Gemma - Explicit Vertex AI Model Garden Interaction

## Overview
This skill executes chat/generation requests against custom deployed Gemma endpoints or MaaS instances in the `bulachak` Vertex AI project. It supports variant routing (pointing to specific deployed Endpoints) and optional brand guideline injection.

## When to Use This Skill
Activate this skill when the user runs the `/gemma` command to generate text or interact with a Gemma variant.

## Usage
Run the script using the python interpreter in the virtual environment.

**Arguments:**
- `--prompt`: (Required) The base prompt for generation.
- `--variant`: (Optional) The Gemma variant or Endpoint mapping (e.g., `4-pro`). Defaults to the standard Gemma 4 MaaS endpoint.
- `--brand`: (Optional) Path or name of the brand guideline file. If just a name (e.g., `Baza`), it checks `06_SOUL_KITCHEN/Brand_Books/`.
- `--thinking`: (Optional) Flag to enable the reasoning/thinking mode (if supported by the model).

**Example:**
```bash
python app/tools/model_garden/gemma_cli.py --prompt "Write a short blog post" --variant 4-pro --brand BazaCreative
```

## Expected Output
The script will output the AI's response directly to the console. If a brand file is injected, it will confirm the injection prior to execution.
