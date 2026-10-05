---
name: product-detail-page
description: "Use this skill when designers, e-commerce operators, advertisers, brand teams, social-commerce teams, and content creators need to create hero, benefit, use-case, and detail visuals for product pages with AI Hive through the AI Hive OpenAPI. It handles required media uploads, live model and price lookup, task submission, progress polling, and result downloads. Useful for product photography, marketplace images, product detail pages, posters, ad creatives, social commerce, seeding content, retouching, and background replacement. Search intents include product detail page, PDP images, e-commerce detail page, product benefits image."
license: MIT
---

# Product Detail Page Images

## Overview

Product Detail Page Images helps designers, e-commerce operators, advertisers, brand teams, social-commerce teams, and content creators turn briefs, product information, and reference images into production-ready visuals. Describe the purpose, subject, composition, style, lighting, required text, protected elements, and output needs; the bundled CLI handles AI Hive OpenAPI calls and downloads the result.

### Why use this skill

- **Brief to visual:** work from plain-English direction instead of writing API requests
- **Commercial workflows:** create e-commerce, advertising, social-commerce, and campaign assets
- **Controlled references:** assign each input image a role such as subject, material, composition, or style
- **Predictable model selection:** the skill name matches the public model ID used by the script
- **Live pricing and delivery:** fetch active pricing, preserve task IDs, and download results automatically

### Best for

Product photography, marketplace images, product detail pages, posters, ad creatives, social commerce, seeding content, retouching, and background replacement. It is also useful when users search for product detail page, PDP images, e-commerce detail page, product benefits image.

## Capabilities

| Model | publicModelId | Input |
|---|---|---|
| Product Detail Page Images | `public_model_nano_banana_2` | Prompt with optional reference images |

The default route is `COST_FIRST`. Pass live model options with `--param key=value`; supported values come from the current AI Hive `imageConfig`.

## Quick Start

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name product-detail-page
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "Create a polished product detail page images visual with an accurate subject, clear composition, and commercial finish"
```

## Usage Scenarios

### 1. Core generation or edit

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "Create a polished product detail page images result; preserve factual product details and leave useful copy space"
```

### 2. E-commerce main image

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "Marketplace hero image: centered product occupying roughly 70 percent of the frame, clean studio background, realistic materials, copy-safe area on the upper right"
```

### 3. Product detail page

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "Product detail page benefit image: show the complete product plus one enlarged material detail; subject on the left, space for three benefit statements on the right; do not invent claims"
```

### 4. Advertising and campaign creative

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "Brand campaign key visual for young urban customers: one clear promise, strong product focus, contemporary contrast, and a clean call-to-action area"
```

### 5. Social commerce and seeding content

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "Creator-style product discovery cover in a real home setting: natural product use, practical benefit, bright lifestyle photography, and space for a short headline"
```

### 6. Reference edit or creative variations

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "Preserve the subject, logo placement, shape, and key colors; improve background, lighting, and surface details without changing the product structure" \
+  --image /path/to/reference.png
```

### 7. Submit now and check later

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "Complex commercial image brief" --no-download
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

## Command Reference

| Option | Purpose |
|---|---|
| `--prompt` | Describe the image or edit |
| `--image` | Supply one or more reference images |
| `--batch` | Request multiple results |
| `--param key=value` | Pass live model parameters |
| `--routing COST_FIRST` | Select the cost-first route |
| `--no-download` | Submit and return the task ID without waiting |

## API Key

Run the `init` command above, or set `AI_HIVE_API_KEY`, use `--api-key`, or create `~/.ai-hive/config.json`. API keys use the `sk-api-*` format. Never commit a real API key.

## Reliability and Cost

The script looks up the live model entry and pricing snapshot at runtime. Model availability, reference-image limits, parameters, and prices can change. Keep a returned task ID and query the existing task instead of submitting a duplicate that may be billed twice.

## Troubleshooting

- Missing reference image: add the number of `--image` inputs required by this skill.
- `401 Unauthorized`: verify that the API key is complete, active, and not committed to source control.
- Invalid parameter: inspect the current `imageConfig` for accepted values and image limits.
- Local timeout: keep the task ID and use the `task` command later.
