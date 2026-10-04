---
name: imagen
description: "Explicit Vertex AI Image Generation Skill using Imagen (Supports Brand Guidelines & Versions)"
risk: safe
---

# Imagen - Explicit Vertex AI Image Generation

## Overview
This skill executes 100% visible image generation directly on the `bulachak` Vertex AI project. It supports version routing (Imagen 3, Imagen 4, Ultra) and optional brand guideline injection to ensure marketing assets match client constraints without requiring external apps.

## When to Use This Skill
Activate this skill when the user runs the `/imagen` command or explicitly requests an image from Vertex AI Imagen.

## Usage
Run the script using the python interpreter in the virtual environment.

**Arguments:**
- `--prompt`: (Required) The base prompt for generation.
- `--version`: (Optional) The model variant (e.g., `3`, `4`, `ultra`). Defaults to `3`.
- `--brand`: (Optional) Path or name of the brand guideline file. If just a name (e.g., `Baza`), it checks `06_SOUL_KITCHEN/Brand_Books/`.

**Example: Standalone Image**
```bash
python app/tools/model_garden/imagen_cli.py --prompt "A sleek cyberpunk robot" --version ultra
```

**Example: Brand-Aware Image Generation**
```bash
python app/tools/model_garden/imagen_cli.py --prompt "A promotional banner" --version 4 --brand BazaCreative
```

## Expected Output
The script will save the generated image to `03_TECHNICAL_EXPERIMENTS` and print the exact file path. If a brand file is injected, it will confirm the injection in the console.
