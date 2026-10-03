---
name: customer-persona
description: This prompt instructs the AI to create five distinct customer personas for a specified brand using the requested language, each detailing demographics, psychographics, and behavioral patterns, then summarizing key purchase drivers and barriers; the outcome is a clear markdown table that helps the user understand who the target customers are, how they think and behave, and what motivates or prevents them from buying or using the brand’s offering.
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

This prompt instructs the AI to create five distinct customer personas for a specified brand using the requested language, each detailing demographics, psychographics, and behavioral patterns, then summarizing key purchase drivers and barriers; the outcome is a clear markdown table that helps the user understand who the target customers are, how they think and behave, and what motivates or prevents them from buying or using the brand’s offering.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Language` | Optional |  | `Vietnamese` |
| `Brand_Name` | Optional |  | `Upcontent` |
| `Descriptions` | Optional |  | `Providing graphic design and content marketing solutions for SMEs including designing profiles, catalogs, menus, advertising images, website banners, fanpage care and website content, email marketing, scripts` |



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

- Optional text inputs (use defaults if not provided by the human):
    - `Language` (default: `Vietnamese`)
  - `Brand_Name` (default: `Upcontent`)
  - `Descriptions` (default: `Providing graphic design and content marketing solutions for SMEs including designing profiles, catalogs, menus, advertising images, website banners, fanpage care and website content, email marketing, scripts`)
- Optional: model and options.
  - Present the human with the default model **`gpt-5-mini`** and its available options. Look up `gpt-5-mini` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{}`.
  - If the human does not specify, defaults are used: model `gpt-5-mini`, options `{}`. Other models from the resources call are also available.


### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `customer-persona`).

Command form:

```bash
betterprompt generate customer-persona \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-5-mini`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate customer-persona \
  --input Language=Vietnamese \
  --input Brand_Name=Upcontent \
  --input 'Descriptions=Providing graphic design and content marketing solutions for SMEs including designing profiles, catalogs, menus, advertising images, website banners, fanpage care and website content, email marketing, scripts' \
  --model gpt-5-mini \
  --options '{}'
```