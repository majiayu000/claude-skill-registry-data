---
name: ad-refinery-360
description: This prompt guides an AI to act as an advertising strategist and behavioral psychologist by taking product details, performance goals, market context, and a desired style to build three target personas, generate three ad concepts, run multiple rounds of persona-based critique and iterative refinement, and then select the best-performing ad with clear reasoning and actionable targeting and optimization recommendations.
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

This prompt guides an AI to act as an advertising strategist and behavioral psychologist by taking product details, performance goals, market context, and a desired style to build three target personas, generate three ad concepts, run multiple rounds of persona-based critique and iterative refinement, and then select the best-performing ad with clear reasoning and actionable targeting and optimization recommendations.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `ad_style` | Required |  | (none) |
| `market_context` | Required |  | (none) |
| `ENTER_PRODUCT_INFO_HERE` | Required |  | (none) |
| `ENTER_PERFORMANCE_TARGETS_HERE` | Required |  | (none) |



### Models and options

This skill's modality is: **`text`**.

To discover which `model` values you can use (and which `options` keys/values are valid for each model), run:

```bash
betterprompt resources --models-only --json
```

Then filter the returned JSON array to entries where `modality` is `"text"`.

## How to run

### Step 1: Collect inputs

First, run `betterprompt resources --models-only --json` and filter to `modality: "text"` to discover valid models and available options:

```bash
betterprompt resources --models-only --json
```

Use only the models and option values that appear in the filtered results.

Then collect all inputs from the human:


- Required text inputs:
    - `ad_style`
  - `market_context`
  - `ENTER_PRODUCT_INFO_HERE`
  - `ENTER_PERFORMANCE_TARGETS_HERE`
- Optional: model and options.
  - Present the human with the default model **`gpt-4.1-mini`** and its available options. Look up `gpt-4.1-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-4.1-mini`, options `{}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `ad-refinery-360`).

Command form:

```bash
betterprompt generate ad-refinery-360 \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-4.1-mini`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate ad-refinery-360 \
  --input ad_style=<value> \
  --input market_context=<value> \
  --input ENTER_PRODUCT_INFO_HERE=<value> \
  --input ENTER_PERFORMANCE_TARGETS_HERE=<value> \
  --model gpt-4.1-mini \
  --options '{}'
```