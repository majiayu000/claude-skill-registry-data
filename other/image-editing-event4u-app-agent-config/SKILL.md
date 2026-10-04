---
model_tier: inherit
name: image-editing
description: "Edit an existing image — inpaint, background swap, variation — via providers that support it. Use when editing/modifying/inpainting an image or making variations."
domain: product
personas: []
workspaces:
  - small-business
packs:
  - ai-image
trust:
  level: experimental
install:
  removable: true
scope:
  write: []
  verification_reason: "execution declares no handler, so this skill runs nothing of its own — every write is the calling agent's, under the rules that govern it. No command can prove a scope the skill never executes."
execution:
  type: manual
---

# image-editing

Edit or vary an existing image: inpaint masked regions, swap backgrounds, produce
variations from a seed, or upscale — routed to providers that support the edit API,
with governance applied before delivery. All adapters are scaffold-tier (dry-run) until promoted to `stable`.

## When to use

- User asks to edit, modify, inpaint, or make a variation of an existing image.
- Background removal or swap on a provided asset.
- Upscaling or restyling an existing render from a prior generation run.
- Any task that starts from an image rather than a blank brief.

## Procedure

1. **Identify the edit type** — classify the request: `inpaint` (replace a masked
   region), `background` (remove or swap), `variation` (alternate version of the
   same subject), or `upscale` (resolution increase).
2. **Confirm provider support** — not all providers support image editing. GPT Image 2
   and `gemini-image` both expose an edit/inpaint endpoint. Flux and Recraft support
   variation via seed/ref-image only; Ideogram is largely generate-only. Check
   the provider's capability before proceeding.
3. **Route the provider** via [`image-provider-routing`](../image-provider-routing/SKILL.md) —
   route to a provider whose adapter exposes an edit endpoint for the required edit
   type. Selecting a generate-only provider for an inpaint task will fail silently.
4. **Author the edit instruction** via [`prompt-engineering-image`](../prompt-engineering-image/SKILL.md) —
   write the edit prompt in the target provider's grammar. For inpaint, describe what
   fills the masked region. For variation, carry the original seed/ref-image path forward.
5. **Invoke the adapter (dry-run today)** — run
   `node_modules/@event4u/agent-config/src/scripts/ai-image/adapters/<provider>.sh` with the assembled params including
   the source image path and, for inpaint, the mask path. Validate the returned
   artifact path or dry-run confirmation. All adapters are `experimental`
   (scaffold-tier); no live editing occurs until a maintainer promotes the adapter
   via `provider-lifecycle-discipline`.
6. **Apply rights and disclosure governance** — run the rights check
   (`image-likeness-and-rights`) when the source image or edit instruction involves
   a real person's likeness, a brand mark, or a named living artist's style. Attach
   the AI-disclosure footer per `media-governance-routing` before delivering output.

## Output format

1. **Edit plan** — edit type, chosen provider, routing rationale, and prompt string
   ready to copy.
2. **Provider + params** — adapter file reference, source image path, mask path (if
   inpaint), key params (aspect ratio, strength, seed/ref-image for variation).
3. **Artifact path / dry-run note** — the path returned by the adapter, or an
   explicit note: "adapter is experimental (scaffold-tier) — dry-run plan only; no
   edited asset until promotion per `provider-lifecycle-discipline`."

## Gotcha

- **Scaffold-tier adapters produce plans, not pixels** — adapters for GPT Image 2,
  `gemini-image`, Flux, and Recraft are **scaffold-tier** (dry-run only). This skill
  produces the edit blueprint + dry-run confirmation; actual edits require a
  maintainer to capture a smoke trace and promote the adapter to `stable`. Claiming
  an edited asset exists when no adapter is stable misleads the caller.
- **Not all providers support editing** — Ideogram and Recraft are primarily
  generate-only; they do not expose a mask-based inpaint endpoint. Routing an
  inpaint task to them silently falls back to generation from scratch, discarding the
  source image entirely.
- **Variation needs the original seed or ref-image** — requesting a variation without
  carrying the seed value or ref-image path from the original generation will produce
  a stylistically unrelated result. The seed/ref-image is the only reliable
  continuity lever for variation workflows.

## Do NOT

- Do NOT assume every provider supports image editing — check provider capability
  before routing; a generate-only provider will discard the source image.
- Do NOT skip `image-likeness-and-rights` when the source image or edit prompt
  involves a real person's face, a brand mark, or a named living artist's style.
- Do NOT claim a live edit is produced while adapters are scaffold-tier — surface
  the dry-run caveat explicitly every time.
- Do NOT use this skill for generating a new image from scratch — route that to
  [`image-generation`](../image-generation/SKILL.md) instead.

## See also

- [`image-generation`](../image-generation/SKILL.md) — generate a new image from a brief (not editing an existing one).
- [`image-provider-routing`](../image-provider-routing/SKILL.md) — select the right provider before writing the prompt.
- [`prompt-engineering-image`](../prompt-engineering-image/SKILL.md) — translate the edit brief into provider-specific prompt grammar.
- [`image-likeness-and-rights`](../../rules/image-likeness-and-rights.md) — rights check before editing real-person likenesses or brand marks.
- [`screenshot-hygiene`](../screenshot-hygiene/SKILL.md) — for redacting a documentation screenshot, use a deterministic opaque box/blur (never the lossy inpaint here).
