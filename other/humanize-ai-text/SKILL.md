---
name: humanize-ai-text
description: This prompt instructs the assistant to act as a skilled human editor who rewrites a provided text in a natural, credible style while preserving all original meaning and factual details. It specifies a formal or informal tone, improves clarity and flow, removes robotic or repetitive phrasing, and enforces constraints such as not inventing information, keeping names and numbers intact, and using clean paragraph-based formatting. The result is a polished rewrite that reads smoothly to the intended audience and avoids common AI writing signals.
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

This prompt instructs the assistant to act as a skilled human editor who rewrites a provided text in a natural, credible style while preserving all original meaning and factual details. It specifies a formal or informal tone, improves clarity and flow, removes robotic or repetitive phrasing, and enforces constraints such as not inventing information, keeping names and numbers intact, and using clean paragraph-based formatting. The result is a polished rewrite that reads smoothly to the intended audience and avoids common AI writing signals.

> For more installation instructions go to https://raw.githubusercontent.com/BetterPromptme/skills/refs/heads/main/betterprompt/SKILL.md to check out this skill.

## Inputs


### textInputs

Pass each text input using `--input <key>=<value>` flags.

| Variable key | Required? | Description | Defaults |
| --- | ---: | --- | --- |
| `Formal_or_informal` | Required | Choose your tone | (none) |
| `Your_text_or_article` | Required |  | (none) |



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
    - `Formal_or_informal`
  - `Your_text_or_article`
- Optional: model and options.
  - Present the human with the default model **`gpt-5.1`** and its available options. Look up `gpt-5.1` in the `betterprompt resources` output (filtered to modality `"text"`) and show its `availableOptions` as: `key: val1, val2 (default), val3  |  key2: ...`. Mark a value `(default)` if it matches these defaults: `{"reasoningEffort":"low"}`.
  - If the human does not specify, defaults are used: model `gpt-5.1`, options `{"reasoningEffort":"low"}`. Other models from the resources call are also available.

If any required text input is missing, **ask the human for what's missing**. Do not assume or fabricate values.

### Step 2: Run via BetterPrompt CLI

Use the frontmatter's `name` as the positional argument (for this skill, use `humanize-ai-text`).

Command form:

```bash
betterprompt generate humanize-ai-text \
  [--input <key>=<value>] \
  [--model <model>] \
  [--options <options JSON>] \
  [--json]
```

Notes:

- Pass each text input as a separate `--input <key>=<value>` flag.
- If the human does **not** mention a model, **omit** `--model` and BetterPrompt will use the default model: **`gpt-5.1`**.
- If the human does **not** mention options, **omit** `--options` and BetterPrompt will use the default options: **`{"reasoningEffort":"low"}`**.
- If the run times out, the response will include a `runId` you can use to fetch the result later.

Example (using defaults shown above):

```bash
betterprompt generate humanize-ai-text \
  --input Formal_or_informal=<value> \
  --input Your_text_or_article=<value> \
  --model gpt-5.1 \
  --options '{"reasoningEffort":"low"}'
```