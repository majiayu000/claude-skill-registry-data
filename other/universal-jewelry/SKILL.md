---
name: universal-jewelry
description: This prompt instructs the AI to produce a 3–8 second, ultra-photorealistic 4K macro marketing video of a specified jewelry piece, using an uploaded reference image plus material, key design details, and a complementary background color to preserve accurate form and finish. The result is a luxury-style cinematic shot featuring shallow depth of field, physically realistic reflections and gemstone sparkle, and only subtle camera/object motion (e.g., slow pan or gentle rotation). It explicitly restricts the scene to the jewelry and its presentation surface—no humans, body parts, logos, text, or stylized/CGI-looking rendering—so the output resembles a professional high-end jewelry brand reel.
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

This prompt instructs the AI to produce a 3–8 second, ultra-photorealistic 4K macro marketing video of a specified jewelry piece, using an uploaded reference image plus material, key design details, and a complementary background color to preserve accurate form and finish. The result is a luxury-style cinematic shot featuring shallow depth of field, physically realistic reflections and gemstone sparkle, and only subtle camera/object motion (e.g., slow pan or gentle rotation). It explicitly restricts the scene to the jewelry and its presentation surface—no humans, body parts, logos, text, or stylized/CGI-looking rendering—so the output resembles a professional high-end jewelry brand reel.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `material` | Optional | The primary metal or base material of the jewelry. Influences color tone, shine, and how reflections behave under cinematic lighting.    | `18k white gold` |
| `key_details` | Optional | Unique design or gem-related elements that make the jewelry visually distinctive. This helps the model focus on fine craftsmanship and sparkle details.    | `2-carat round brilliant diamond with pavé band` |
| `background_color` | Optional | The main backdrop tone that sets the mood and visual contrast for the jewelry. Should complement the material color and lighting tone.    | `Deep emerald green` |



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Upload an image of the jewelry item you want to turn into a cinematic video. | `--image-input-url <url>` or `--image-input-path <path>` |


### Models and options

This skill's modality is: **`video`**.

To discover which `model` values you can use (and which `options` keys/values are valid for each model), run:

```bash
betterprompt resources --models-only --json
```

Then filter the returned JSON array to entries where `modality` is `"video"`.

## How to run

### Step 1: Collect inputs

First, run `betterprompt resources --models-only --json` and filter to `modality: "video"` to discover valid models and available options:

```bash
betterprompt resources --models-only --json
```

Use only the models and option values that appear in the filtered results.

Then collect all inputs from the human:

- Optional text inputs (use defaults if not provided by the human):
    - `material` (default: `18k white gold`)
  - `key_details` (default: `2-carat round brilliant diamond with pavé band`)
  - `background_color` (default: `Deep emerald green`)
- Required images:
  - **Exactly 1** images: image 1 (Upload an image of the jewelry item you want to turn into a cinematic video.). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`sora-2`** and its available options. Look up `sora-2` in the `betterprompt resources` output (filtered to modality `"video"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"seconds":"4","size":"720x1280"}`.
  - If the human does not specify, defaults are used: model `sora-2`, options `{"seconds":"4","size":"720x1280"}`. Other models from the resources call are also available.

If the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Upload an image of the jewelry item you want to turn into a cinematic video.)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `universal-jewelry`).

Command form:

```bash
betterprompt generate universal-jewelry \
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
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`sora-2`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"seconds":"4","size":"720x1280"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate universal-jewelry \
  --input 'material=18k white gold' \
  --input 'key_details=2-carat round brilliant diamond with pavé band' \
  --input 'background_color=Deep emerald green' \
  --image-input-url https://example.com/image1.png \
  --model sora-2 \
  --options '{"seconds":"4","size":"720x1280"}'
```