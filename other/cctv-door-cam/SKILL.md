---
name: cctv-door-cam
description: This prompt instructs an AI video generator to create a short, photorealistic vertical CCTV-style clip of a suburban front yard viewed from a fixed camera above a front door, with bright natural sunlight and subtle grain. A specified subject approaches along the pathway, stops beneath the camera, looks up, smiles, and says “Hello,” while realistic ambient outdoor sounds and a voice matched to the subject’s characteristics complete the scene.
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

This prompt instructs an AI video generator to create a short, photorealistic vertical CCTV-style clip of a suburban front yard viewed from a fixed camera above a front door, with bright natural sunlight and subtle grain. A specified subject approaches along the pathway, stops beneath the camera, looks up, smiles, and says “Hello,” while realistic ambient outdoor sounds and a voice matched to the subject’s characteristics complete the scene.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `subject` | Optional | Describe who or what is approaching the camera — include appearance, clothing, or type of animal if applicable. | `An American young woman` |



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
    - `subject` (default: `An American young woman`)
- Optional: model and options.
  - Present the human with the default model **`sora-2`** and its available options. Look up `sora-2` in the `betterprompt resources` output (filtered to modality `"video"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"seconds":"4","size":"720x1280"}`.
  - If the human does not specify, defaults are used: model `sora-2`, options `{"seconds":"4","size":"720x1280"}`. Other models from the resources call are also available.


### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `cctv-door-cam`).

Command form:

```bash
betterprompt generate cctv-door-cam \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`sora-2`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"seconds":"4","size":"720x1280"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate cctv-door-cam \
  --input 'subject=An American young woman' \
  --model sora-2 \
  --options '{"seconds":"4","size":"720x1280"}'
```