---
name: image-gen-nano-banana
description: Self-contained Nano Banana skill for direct Gemini image generation and editing. Use when you want one local skill that handles Flash or Pro generation directly, while doing Kousen-style prompt rewriting instructionally in the skill rather than inside the runner.
---

# Image Gen Nano Banana

Use this skill when the user asks to generate or edit an image with Nano Banana through the local Gemini runner.

## Run the workflow

1. Decide whether the user's prompt is ready to use or needs help.
2. If it needs help, refine it conversationally using [Prompt rewriting](#prompt-rewriting).
3. Run `scripts/nano_banana_skill.py` with the final prompt. Pass that prompt as-is; the runner performs generation or editing directly.

Prompt authoring belongs in this skill's instructions. The runner has no scripted `plan` flow, retrieval step, exemplar lookup, or dependency on benchmark reference repositories.

## Prompt rewriting

Rewrite when the user asks for help with the prompt, the request is vague, or the image needs a polished result for a hero, poster, mascot, or marketing use. Ask up to two or three focused questions, then cover the fields that matter:

- subject and setting
- mood and atmosphere
- style or medium
- composition and framing
- lighting and materials
- purpose or use case
- exact text, when present

Turn the answers into a natural-language prompt rather than a list of tags. Use specific details, explain the use case, guide composition, lighting, and material choices, and preserve quoted text exactly. Briefly explain the main choices and offer one refinement pass.

Use the user's prompt directly when it is already precise, when editing should preserve a reference, or when grounded realism and factual fidelity matter more than reinterpretation.

### Raw prompts

The user can opt out of rewriting with a `RAW:` prefix, a `[RAW]` marker anywhere in the request, or clear wording such as “use this exactly,” “do not rewrite,” or “pass this through raw.” Treat `RAW:` and `[RAW]` case-insensitively. In this mode:

1. Do not ask prompt-authoring questions or polish, expand, or reinterpret the prompt.
2. Remove the `RAW:` prefix or `[RAW]` marker.
3. Pass the remaining prompt verbatim to the runner.

Examples:

- `RAW: A photoreal portrait of a violinist in soft studio light.`
- `A photoreal portrait of a violinist in soft studio light. [RAW]`
- `RAW: Convert this dark UI screenshot into a light theme while preserving layout.`

For exact-text tasks, keep the quoted wording unchanged in the final prompt. Image text fidelity is imperfect, so set that expectation with the user.

## Choose a model

Use `flash` by default. It maps to `gemini-3.1-flash-image-preview`, supports `512`, `1K`, `2K`, and `4K`, supports aspect-ratio overrides including `1:4`, `1:8`, `4:1`, and `8:1`, and accepts up to 14 input images.

Choose `pro` when the user wants the higher-fidelity path. It maps to `gemini-3-pro-image-preview`, supports `1K`, `2K`, and `4K`, accepts at most one input image, and does not support aspect-ratio overrides in this skill.

## Run examples

Generate an image:

```bash
skills/image-gen-nano-banana/scripts/nano_banana_skill.py \
  --model flash \
  --prompt "Friendly octopus-robot mascot sticker for a developer tool. Distinct silhouette, expressive face, polished shading, transparent background, production-usable asset." \
  --output /tmp/mascot.png
```

Edit an image while preserving its reference:

```bash
skills/image-gen-nano-banana/scripts/nano_banana_skill.py \
  --model flash \
  --prompt "Convert this dark product UI screenshot into a polished light-theme version while preserving layout, information hierarchy, and product identity." \
  --input-image /path/to/source-ui.png \
  --filename /tmp/ui-light.png
```

Generate with Pro:

```bash
skills/image-gen-nano-banana/scripts/nano_banana_skill.py \
  --model pro \
  --prompt "Photoreal portrait of a violinist in soft studio light." \
  --output /tmp/portrait.png
```

`--filename` is an alias for `--output`, retained for direct-style compatibility. When the prompt includes `RAW:` or `[RAW]`, remove the marker before passing the prompt through unchanged. Preserve the user's wording directly when fidelity matters more than reinterpretation.

## Authentication and output

The runner checks credentials in this order: `--api-key`, `GEMINI_API_KEY`, then `GOOGLE_API_KEY`. In this experiment repository it also reads a local `.env` file automatically.

The runner writes the generated image file or files and a `.json` sidecar containing the model, prompt, resolution, aspect ratio, reference paths, output paths, any model text, and an auto-resolution note when applicable. With no explicit resolution, it normally uses `1K`; when reference images are supplied it can choose a resolution from their dimensions, including downshifting Flash to `512` for very small inputs.
