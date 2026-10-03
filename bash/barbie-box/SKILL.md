---
name: barbie-box
description: This prompt instructs an image generator to design a premium, collector-style Barbie box on a store shelf containing a doll inspired by an uploaded person’s look, while explicitly avoiding a direct copy of the real face by rendering a classic Barbie (or Ken-style, if male) plastic doll visage. It specifies a horizontal deluxe packaging layout with signature branding elements (logo, clear window, vibrant color theme), and directs the model to match the outfit, hair, makeup vibe, interior background, and included accessories from provided parameters to produce a polished retail-ready collector’s edition set.
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

This prompt instructs an image generator to design a premium, collector-style Barbie box on a store shelf containing a doll inspired by an uploaded person’s look, while explicitly avoiding a direct copy of the real face by rendering a classic Barbie (or Ken-style, if male) plastic doll visage. It specifies a horizontal deluxe packaging layout with signature branding elements (logo, clear window, vibrant color theme), and directs the model to match the outfit, hair, makeup vibe, interior background, and included accessories from provided parameters to produce a polished retail-ready collector’s edition set.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `BOX_COLOR` | Required |  | (none) |
| `LIST_ITEMS` | Required |  | (none) |
| `Gender_of_the_doll` | Required |  | (none) |
| `the_outfit_you_want` | Required |  | (none) |
| `Background_inside_the_box` | Required |  | (none) |



### imageInputs

This prompt requires **exactly 1 image**. You **must pass exactly 1 image flag** (no more, no fewer), in the order matching the descriptions below.

| Index | Required | Description | Allowed CLI flags |
| ---: | ---: | --- | --- |
| 1 | Yes | Your Image | `--image-input-url <url>` or `--image-input-path <path>` |


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


- Required text inputs:
    - `BOX_COLOR`
  - `LIST_ITEMS`
  - `Gender_of_the_doll`
  - `the_outfit_you_want`
  - `Background_inside_the_box`
- Required images:
  - **Exactly 1** images: image 1 (Your Image). Images must be provided in this order.
- Optional: model and options.
  - Present the human with the default model **`gpt-image-1`** and its available options. Look up `gpt-image-1` in the `betterprompt resources` output (filtered to modality `"image"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"quality":"high"}`.
  - If the human does not specify, defaults are used: model `gpt-image-1`, options `{"quality":"high"}`. Other models from the resources call are also available.

If any required text input or the required images are missing, **ask the human for what's missing**. Do not assume or fabricate values. Tell the human: **"Please provide images in this order: image 1 (Your Image)"**.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `barbie-box`).

Command form:

```bash
betterprompt generate barbie-box \
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
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-image-1`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"quality":"high"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate barbie-box \
  --input BOX_COLOR=<value> \
  --input LIST_ITEMS=<value> \
  --input Gender_of_the_doll=<value> \
  --input the_outfit_you_want=<value> \
  --input Background_inside_the_box=<value> \
  --image-input-url https://example.com/image1.png \
  --model gpt-image-1 \
  --options '{"quality":"high"}'
```