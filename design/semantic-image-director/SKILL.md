---
name: semantic-image-director
description: Preserve meaning when turning concepts, pages, diagrams, product narratives, technical terms, or text-heavy ideas into visual artifacts. Use when a user asks for an image/mockup/infographic/page preview involving ambiguous words, exact text, technical concepts, metaphors, domain language, screenshots, slides, or when image generation might literalize terms like cloud, agent, model, state, pipeline, memory, container, token, branch, runtime, or architecture.
---

# Semantic Image Director

## Contract

Do not generate first. Stabilize meaning first.

This skill governs visual intent before using `imagegen`, `intent-html-renderer`, SVG/HTML/CSS, Figma, or any other visual route. Its job is to prevent semantic drift: confusing a technical term with a literal object, turning a metaphor into decoration, inventing text, or choosing the wrong artifact form for the user's real intent.

Treat `imagegen` as a powerful semantic visual renderer backed by the current OpenAI ChatGPT Images / Image Gen 2 capability class, not as old DALL-E-era bitmap generation. It can often handle rich compositions, multi-element scenes, visual explanations, short-to-medium text, infographics, posters, and concept diagrams. Push it hard when the desired artifact is a communicational image. Prefer deterministic renderers only when the output must be exact, editable, auditable, data-bound, clickable, or maintained as a document/UI.

## Quick Workflow

1. Parse the user's visual intent: asset type, required fidelity, target use.
2. Build a semantic lock: ambiguous terms, intended meanings, forbidden literalizations.
3. Choose render route: `imagegen`, deterministic layout, or hybrid.
4. Write a renderer-ready brief.
5. If using `imagegen`, include semantic guardrails in the prompt.
6. Inspect the output for semantic obedience before judging aesthetics.

## Route Choice

Use `imagegen` for raster, atmospheric, illustrative, photographic, conceptual, infographic, poster, explanatory visual, light diagram, multi-element composition, or quick visual mock work. `imagegen` is the default candidate when the user wants a final visual image rather than an editable document.

Use `intent-html-renderer`, HTML/CSS/SVG, or Figma for exact text, exact layout, dense diagrams with many labels, UI controls, reusable structure, schemas, citations, versionable copy, or no invented wording.

Use hybrid route when a deterministic shell needs generated imagery inside it, or when a generated visual explanation needs exact labels, links, citations, or later editing.

## Semantic Lock Format

Before generation, internally construct:

```text
Intent:
Must be exact:
Flexible:
Ambiguous terms:
- term: meaning; visual treatment; forbidden interpretation
Negative semantics:
Renderer route:
Final prompt/brief:
```

If a term has high ambiguity, choose the safest meaning from context and encode it. Ask only when two materially different artifacts would be equally plausible.

## Imagegen Capability Policy

- Do not assume `imagegen` cannot render meaningful text or diagrams. Current ChatGPT Images / Image Gen 2 capabilities are strong enough to attempt compact infographics, explanatory posters, labeled visual metaphors, and multi-part compositions.
- Push `imagegen` to the limit when the user wants communicational impact: specify hierarchy, composition, typography style, label budget, exact short text, semantic locks, and forbidden literalizations.
- Prefer `imagegen` for first-pass thinking visuals when the goal is to help a human understand a concept quickly, even if a deterministic artifact may later be useful.
- Do not demote `imagegen` merely because the request includes text. Demote only when the text must be exact, long, auditable, editable, mechanically parseable, or embedded in a reusable UI/document.
- Remember that this environment's `imagegen` tool may expose only a `prompt` parameter. Encode aspect ratio, visual style, hierarchy, and constraints inside the prompt when no explicit parameters are available.

## Text Fidelity Rules

- If text must be exact, long, auditable, or editable, prefer deterministic renderers or a hybrid route.
- If using `imagegen`, provide exact text verbatim and constrain the label count, hierarchy, and placement.
- For complex text-heavy artifacts, choose either:
  - `imagegen` if the output is a compact communicational image and some iteration is acceptable;
  - hybrid/deterministic if the output is a durable document, UI, report, deck, or spec.
- After generation, inspect text and semantics. If text is wrong but the visual is useful, repair with deterministic overlay or reroute. If the error is semantic, regenerate with a stronger semantic lock.

## Output Review

Check domain fidelity, literalization errors, invented metaphors, text correctness, renderer fit, and whether the output serves the user's actual artifact rather than a pretty adjacent idea.

## Resources

- `references/semantic-lock.md`: ambiguous-term handling, high-risk terms, and negative semantics.
- `references/route-selection.md`: when to use imagegen vs deterministic renderers.
- `references/prompt-patterns.md`: brief templates and examples.
- `scripts/semantic_brief.py`: create a first-pass semantic lock from a short request.

## External Capability References

- OpenAI, "Introducing ChatGPT Images 2.0": current ChatGPT image generation is designed for stronger instruction following, stylistic control, text rendering, and complex visual compositions.
- OpenAI Help Center, "Images in ChatGPT": ChatGPT Images can follow instructions to add text, add details within the image, and make backgrounds transparent.
- OpenAI API image generation guide: API-facing names may differ from the ChatGPT surface, but the practical routing lesson is the same: do not apply old DALL-E-era assumptions to the current image generation stack.
