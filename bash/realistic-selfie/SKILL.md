---
name: realistic-selfie
description: This prompt instructs an image model to generate an ultra-realistic, high-angle close-up selfie of a young woman in a dark room, using strong flash lighting to create dramatic contrast and a minimalist background. It specifies detailed attributes for hair, makeup, clothing, accessories, nails, pose, expression, mood, and camera aesthetics to achieve a cool-toned, cinematic film-noir look with sharp facial illumination and textured knit details as the final outcome.
compatibility: Requires betterprompt >= 0.1.3
metadata:
  openclaw:
    homepage: https://github.com/BetterPromptme/skills
    emoji: 🧩
    requires:
      anyBins:
        - betterprompt
        - bp
    os:
      - linux
      - darwin
    install:
      - id: node
        kind: node
        package: betterprompt
        bins: [betterprompt, bp]
        label: Install BetterPrompt CLI (node)
---

## What it does

This prompt instructs an image model to generate an ultra-realistic, high-angle close-up selfie of a young woman in a dark room, using strong flash lighting to create dramatic contrast and a minimalist background. It specifies detailed attributes for hair, makeup, clothing, accessories, nails, pose, expression, mood, and camera aesthetics to achieve a cool-toned, cinematic film-noir look with sharp facial illumination and textured knit details as the final outcome.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs



### Models and options

This skill's modality is: **`image`**.

To discover which `model` values you can use (and which `options` keys/values are valid for each model), run:

```bash
betterprompt resources --models-only --json
```

Then filter the returned JSON array to entries where `modality` is `"image"`.

## How to run

### Step 1: Collect inputs

First, run `betterprompt resources --models-only --json` and filter to `modality: "image"` to discover valid models and available options:

```bash
betterprompt resources --models-only --json
```

Use only the models and option values that appear in the filtered results.

Then collect all inputs from the human:

- Optional: model and options.
  - Present the human with the default model **`imagen-4.0-ultra-generate-001`** and its available options. Look up `imagen-4.0-ultra-generate-001` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"aspectRatio":"1:1"}`.
  - If the human does not specify, defaults are used: model `imagen-4.0-ultra-generate-001`, options `{"aspectRatio":"1:1"}`. Other models from the resources call are also available.


### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `realistic-selfie`).

Command form:

```bash
betterprompt generate realistic-selfie \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`imagen-4.0-ultra-generate-001`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"aspectRatio":"1:1"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate realistic-selfie \
  --model imagen-4.0-ultra-generate-001 \
  --options '{"aspectRatio":"1:1"}'
```