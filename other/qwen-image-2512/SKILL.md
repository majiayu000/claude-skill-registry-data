---
name: qwen-image-2512
description: Adapt model-neutral still-image briefs into Qwen Image 2512 prompts for portraits, general images, exact visible text, character look development, locations, props, keyframes, and production stills.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Qwen Image 2512 Prompting

Use the Qwen 2512 production prompt grammar while preserving project canon.

## Input

Read one image brief plus canon and any named reference descriptions.

## Workflow

1. Classify the task as portrait, text-containing image, or general image.
2. Write one continuous English description rather than a tag dump.
3. Preserve proper names exactly.
4. Add visual detail only when it is consistent with canon and useful to composition, lighting, material, atmosphere, or style.
5. If visible text is required, quote every exact string and state placement, orientation, typography characteristics, color, and carrier. Do not translate or rewrite supplied text.
6. If no visible text is required, explicitly state that the image contains no recognizable text when that constraint matters.
7. For a character, use only identity, age, physical, wardrobe, and grooming facts established by canon. Do not invent ethnicity, age, or body traits merely to make the prompt longer.
8. Aim for a concise but complete production description. Remove redundant quality words.
9. Write the prompt under `04_generation/prompts/qwen-image-2512/<source-id>.md`.

## Output

```text
SOURCE_ID: ...
MODEL: qwen-image-2512
PROMPT:
<single continuous image description>
CONSTRAINTS:
- ...
```

## Done

The prompt preserves every hard visual fact and every exact text string from the source brief without adding conflicting canon.
