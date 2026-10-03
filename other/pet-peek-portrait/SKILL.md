---
name: pet-peek-portrait
description: This prompt instructs the AI to take a user-provided, front-facing pet portrait and generate a photorealistic editorial-style image where the pet appears to peek through a central torn-paper opening with curled edges, showing its face and one paw. The result is a clean, minimal composition with a customizable solid-color background, specified emotional expression, and chosen lighting mood, while strictly preserving the pet’s true identity and realism and avoiding any stylization, distortions, text, logos, or added accessories.
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

This prompt instructs the AI to take a user-provided, front-facing pet portrait and generate a photorealistic editorial-style image where the pet appears to peek through a central torn-paper opening with curled edges, showing its face and one paw. The result is a clean, minimal composition with a customizable solid-color background, specified emotional expression, and chosen lighting mood, while strictly preserving the pet’s true identity and realism and avoiding any stylization, distortions, text, logos, or added accessories.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `pet_emotion` | Optional | Desired emotion or expression for the pet. | `Happy with a gentle smile` |
| `lighting_effect` | Optional | Overall lighting mood for the scene. | `Soft warm light` |
| `background_color` | Optional | The solid color of the paper wall background. | `Lavender purple` |



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Clear portrait of your pet | `--image-input-url <url>` or `--image-input-path <path>` |


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

- Optional text inputs (use defaults if not provided by the human):
    - `pet_emotion` (default: `Happy with a gentle smile`)
  - `lighting_effect` (default: `Soft warm light`)
  - `background_color` (default: `Lavender purple`)
- Required images:
  - **Exactly 1** images: image 1 (Clear portrait of your pet). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gemini-2.5-flash-image-preview`** and its available options. Look up `gemini-2.5-flash-image-preview` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gemini-2.5-flash-image-preview`, options `{}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Clear portrait of your pet)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `pet-peek-portrait`).

Command form:

```bash
betterprompt generate pet-peek-portrait \
  [--input <key>=<value>] \
  [--image-input-url <url>] \
  [--image-input-path <path>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- Pass each image using `--image-input-url` or `--image-input-path`, in the order matching the imageInputs descriptions (image 1 first, then image 2, etc.).
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gemini-2.5-flash-image-preview`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate pet-peek-portrait \
  --input 'pet_emotion=Happy with a gentle smile' \
  --input 'lighting_effect=Soft warm light' \
  --input 'background_color=Lavender purple' \
  --image-input-url https://example.com/image1.png \
  --model gemini-2.5-flash-image-preview \
  --options '{}'
```