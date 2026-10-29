---
name: product-description-writer
description: "Use when someone asks to write a product description, turn product features into copy, or generate an e-commerce listing description."
argument-hint: [product-name]
---

## Purpose

Create a ready-to-publish product description from a product name and feature/spec bullet points.

## Inputs

- Required: product name.
- Required: product features or specifications in bullet-point form.
- Optional: tone or format preference (for example, shorter, more technical, more casual).
- Optional: target length.

## Steps

1. If the product name or the core product features are missing, ask the user to provide them instead of inventing details.
2. Interpret the provided features and keep the output in a clear, benefit-focused UK English tone.
3. Draft a short product title if one is not already supplied.
4. Expand the input into 2–4 short paragraphs, or a short paragraph plus a bulleted spec list when appropriate.
5. Lead with the main customer benefit, then describe the key features and what makes the product useful.
6. Keep the copy concise and direct; avoid unnecessary salesy language.
7. Present the final result as plain text or simple markdown, ready to copy and paste into a product listing.
8. End with `AskUserQuestion`: **Looks good, no changes needed (Recommended)** / **Adjust tone** / **Adjust length**. If they pick a refinement, ask directly as free text what direction to adjust it (e.g. "more technical" or "shorter"), then redraft and offer this menu again.

## Output

- A polished product title line if needed.
- A final product description in plain text or simple markdown.
- No file creation, no external API calls.

## Guardrails

- Do not fabricate product details when information is missing.
- Do not produce meta commentary about how the description was generated.
- Avoid overly promotional or overly verbose language.

## Notes

- Default tone: Digitweb Lanka standard e-commerce tone — clear, benefit-focused, concise, UK English.
- If the user asks for a specific tone, apply it while preserving the product’s key benefits.
- Clickable-question convention: the Step 8 revise offer uses `AskUserQuestion` (finite set of good answers). The product name, features, and any refinement direction stay free text -- genuine content the skill cannot meaningfully offer a menu for.
