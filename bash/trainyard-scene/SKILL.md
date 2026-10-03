---
name: trainyard-scene
description: This prompt specifies a cinematic, photochemically inspired video scene on an urban commuter platform at dawn, detailing camera behavior, lens and filtration choices, color grade, lighting, atmosphere, sound design, and a two-part shot progression, with placeholders for subject, extras, and props. The outcome is a tightly art-directed, realistic-feeling sequence featuring an arriving train in misty morning light, culminating in an intimate character moment and a defined “poster frame” for finishing and delivery.
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

This prompt specifies a cinematic, photochemically inspired video scene on an urban commuter platform at dawn, detailing camera behavior, lens and filtration choices, color grade, lighting, atmosphere, sound design, and a two-part shot progression, with placeholders for subject, extras, and props. The outcome is a tightly art-directed, realistic-feeling sequence featuring an arriving train in misty morning light, culminating in an intimate character moment and a defined “poster frame” for finishing and delivery.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `props` | Optional | any prop you want to include in the shot | `paper coffee cup, rolling luggage, LED departure board (generic destinations)` |
| `extras` | Optional | Describe extras in your scene | `commuters in muted tones; one cyclist pushing bike` |
| `main_subject` | Optional | Describe your main subject | `mid-30s traveler, navy coat, backpack slung on one shoulder, holding phone loosely at side` |



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
    - `props` (default: `paper coffee cup, rolling luggage, LED departure board (generic destinations)`)
  - `extras` (default: `commuters in muted tones; one cyclist pushing bike`)
  - `main_subject` (default: `mid-30s traveler, navy coat, backpack slung on one shoulder, holding phone loosely at side`)
- Optional: model and options.
  - Present the human with the default model **`sora-2`** and its available options. Look up `sora-2` in the `betterprompt resources` output (filtered to modality `"video"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"seconds":"8","size":"720x1280"}`.
  - If the human does not specify, defaults are used: model `sora-2`, options `{"seconds":"8","size":"720x1280"}`. Other models from the resources call are also available.


### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `trainyard-scene`).

Command form:

```bash
betterprompt generate trainyard-scene \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`sora-2`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"seconds":"8","size":"720x1280"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate trainyard-scene \
  --input 'props=paper coffee cup, rolling luggage, LED departure board (generic destinations)' \
  --input 'extras=commuters in muted tones; one cyclist pushing bike' \
  --input 'main_subject=mid-30s traveler, navy coat, backpack slung on one shoulder, holding phone loosely at side' \
  --model sora-2 \
  --options '{"seconds":"8","size":"720x1280"}'
```