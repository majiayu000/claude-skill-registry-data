---
name: reference-to-video
description: "Use this skill when creators, video editors, advertisers, e-commerce teams, social-commerce teams, and short-form story producers need to generate video from image, video, or audio references with AI Hive through the AI Hive OpenAPI. It handles required media uploads, live model and price lookup, task submission, progress polling, and result downloads. Useful for ads, TVCs, product videos, e-commerce listings, social commerce, UGC-style seeding content, short dramas, motion comics, and storyboards. Search intents include reference-to-video, R2V, reference-guided video generation."
license: MIT
---

# Reference to Video

## Overview

Reference to Video helps creators, video editors, advertisers, e-commerce teams, social-commerce teams, and short-form story producers generate video from image, video, or audio references with AI Hive. Describe the intended subject, action, camera, lighting, pacing, and constraints; the bundled CLI handles AI Hive OpenAPI calls and downloads the finished video.

### Why use this skill

- **Brief to result:** work from plain-English creative direction instead of writing API requests
- **Controlled inputs:** use the exact first frame, last frame, image, video, or audio references required by this capability
- **Predictable model selection:** the skill name matches the public model ID used by the script
- **Live pricing:** fetch the active model configuration and pricing snapshot before submission
- **Production-friendly delivery:** preserve the task ID, poll one task safely, and download results automatically

### Best for

Ads, tvcs, product videos, e-commerce listings, social commerce, ugc-style seeding content, short dramas, motion comics, and storyboards. It is also useful when users search for reference-to-video, R2V, reference-guided video generation.

## Capabilities

| Mode | Capability | publicModelId |
|---|---|---|
| `r2v` | Reference to Video | `public_model_seedance_2_5_r2v` |

The default route is `COST_FIRST`. Pass live model options with `--param key=value`; supported values come from the current AI Hive `videoConfig`.

## Quick Start

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name reference-to-video
python3 "$SKILL_PATH/scripts/videogen.py" generate \
  --mode r2v \
  --prompt "Reference to Video: polished motion, clear subject, coherent action, stable camera, commercial finish" \
+  --image /path/to/reference.png
```

## Usage Scenarios

### 1. Core generation

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --prompt "Create a polished reference to video result with coherent motion, stable identity, and a clear ending" \
+  --image /path/to/reference.png
```

### 2. Advertising and TVC

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --prompt "Premium product commercial: establish the product, reveal materials with controlled camera movement, finish on a clean brand-ready hero frame" \
+  --image /path/to/reference.png
```

### 3. E-commerce and product showcase

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --prompt "E-commerce product video: centered subject, move from full product view to material close-ups, show one real use case, leave space for product copy" \
+  --image /path/to/reference.png
```

### 4. Social commerce and seeding content

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --prompt "Vertical social-commerce video: open with the customer problem, demonstrate the product naturally, show the practical benefit, end with a clean call-to-action frame" \
+  --image /path/to/reference.png
```

### 5. Short drama and motion comic

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --prompt "Short-drama shot: a young detective opens an abandoned warehouse door, pauses, and looks inside; slow over-shoulder push-in, cold suspense lighting, one continuous action" \
+  --image /path/to/reference.png
```

### 6. Reference-controlled or channel-specific version

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --prompt "Keep the subject and visual identity consistent; use the reference for motion and camera rhythm; create a tighter social-media version with a brand-ready ending" \
+  --video /path/to/reference.mp4
```

### 7. Submit now and check later

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v --prompt "Complex production brief" --no-download \
+  --image /path/to/reference.png
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

## Command Reference

| Option | Purpose |
|---|---|
| `--mode` | Select a supported mode; capability-specific skills already fix it |
| `--prompt` | Describe the video or edit |
| `--first-frame` / `--last-frame` | Supply controlled keyframes |
| `--image` / `--video` / `--audio` | Supply reference media |
| `--param key=value` | Pass live model parameters |
| `--routing COST_FIRST` | Select the cost-first route |
| `--no-download` | Submit and return the task ID without waiting |

## API Key

Run the `init` command above, or set `AI_HIVE_API_KEY`, use `--api-key`, or create `~/.ai-hive/config.json`. API keys use the `sk-api-*` format. Never commit a real API key.

## Reliability and Cost

The script looks up the live model entry and pricing snapshot at runtime. Model availability, accepted media, parameters, and prices can change. Keep a returned task ID and query the existing task instead of submitting a duplicate that may be billed twice.

## Troubleshooting

- Missing media: provide the first frame, reference image, reference video, or reference audio required by this skill.
- `401 Unauthorized`: verify that the API key is complete, active, and not committed to source control.
- Invalid parameter: inspect the current `videoConfig` for accepted values and media limits.
- Local timeout: keep the task ID and use the `task` command later.
