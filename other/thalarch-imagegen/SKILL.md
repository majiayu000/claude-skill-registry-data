---
name: thalarch-imagegen
description: >
  Creates and edits project images through the strongest image-generation/editing capability
  actually available on the current host. Uses disciplined visual briefs, reference-role
  labeling, light art-direction guidance, invariants, deliberate iteration, exact-text handling,
  brand consistency, design-reference grounding, and post-generation review. Use for raster
  artwork, photography, mockups, marketing assets, textures, concept visuals, compositing, and
  semantic image edits.
---

# Thalarch Imagegen

Use a real host-provided image-generation/editing tool when raster generation or semantic image
editing is the correct medium. Antigravity may expose `generate_image`; other hosts may expose a
different image tool or none at all.

**Never invent a tool call because another host supports it.** If no compatible image capability is
available, keep generation/editing `UNVERIFIED`/unperformed and use a deterministic alternative only
when it genuinely satisfies the request.

The goal is not to write the longest prompt. The goal is to make visual intent unambiguous while
leaving the image model enough room to use its strengths.

## 1. Confirm capability and artifact path

Before generation/editing:

- confirm the current host exposes a compatible image tool;
- confirm whether it accepts text-only generation, image references, editing, masks, aspect ratio,
  transparency, or other requested controls;
- use the tool's **actual current schema**, not remembered parameters from another host;
- preserve source/reference images unless replacement is explicitly requested.

If the host only supports text generation but not precise edits, do not claim edit invariants can be
preserved with the same confidence.

## 2. Build the generation brief

Normalize the request into this order:

1. **Use case / destination**
2. **Asset type**
3. **Primary request**
4. **Canvas / aspect ratio / framing**
5. **Subject and key details**
6. **Composition / focal point**, when it materially helps
7. **Style / medium**
8. **Lighting / mood**
9. **Palette / brand constraints**
10. **Text (verbatim), if any**
11. **Input image roles**
12. **Invariants**
13. **Forbidden elements**
14. **Output intent**

Do not over-specify details that the user did not request. Prefer a clear creative direction over
micromanaging every visual property.

For professional or presentation-critical work, add only the few art-direction details that can
materially improve the result: focal hierarchy, framing, visual balance, destination crop, or one
brand-specific cue.

## 2.5 Design-reference assist

For visually consequential or open-ended generation, use the
`../thalarch-design-system/references/awesome-design-md.md` protocol when external research is
available.

`VoltAgent/awesome-design-md` is a high-value reference atlas of structured `DESIGN.md` analyses.
Use it to help Gemini/image generation with **design reasoning**, not to force another brand's look.

Default behavior:

- user/project references and the current brand always come first;
- if direction is still under-specified, choose **one** well-matched DESIGN.md reference;
- allow a second only when it contributes a clearly different named quality;
- extract a compact capsule: atmosphere, hierarchy, palette roles, type character,
  composition/framing, material/lighting, imagery treatment, and relevant guardrails;
- translate that capsule into light image-generation guidance;
- keep proprietary marks/fonts/layout identity out unless explicitly supplied/authorized;
- never claim a DESIGN.md was consulted unless it was actually read.

Do not perform this lookup for every tiny image edit. A precise edit with strong supplied references
should stay focused on those references. The atlas is fundamental **support for art direction**, not
mandatory context bloat.

## 3. Generation vs editing

### New generation

Use the current host's actual image-generation capability with a concise structured brief and a
semantic asset name when naming is supported.

If the first result is already strong, do not regenerate merely to satisfy a process. Iterate only
when a visible problem or a meaningful improvement opportunity is present.

### Edit

Pass the real source image through the host's supported reference/edit mechanism.

State the mutation first:

`Change only <X>.`

Then restate invariants:

`Keep <Y, Z, composition, subject identity, lighting...> unchanged.`

Repeat critical invariants on every edit iteration. Do not rely on conversational memory to preserve
them.

## 4. Multi-reference control

When multiple inputs are supported, label them explicitly:

- `Image 1 — edit target`
- `Image 2 — style reference`
- `Image 3 — brand/logo reference`

Describe exactly how they interact. For compositing specify scale, placement, perspective, lighting,
and which image owns the base framing.

If the host cannot distinguish reference roles reliably, reduce the number of references or use a
more deterministic production path.

## 5. Preserve identity and structure

For identity-sensitive edits, explicitly lock attributes that must survive:

- facial/character identity;
- body proportions;
- pose;
- hairstyle;
- clothing;
- object geometry;
- camera framing;
- perspective;
- brand marks;
- lighting direction.

Do not claim preservation until the rendered output is inspected.

## 6. Text inside images

When text must be generated inside a raster image:

- author final copy first;
- place literal text in quotes;
- require verbatim rendering;
- specify location, hierarchy, alignment, and typographic character;
- prohibit extra text;
- inspect final image and read every visible word back.

If exact typography, legal copy, dense tables, or perfect spelling is mission-critical, prefer
deterministic text/vector composition over generative raster text.

## 7. Brand consistency

For brand work derive a compact brand lock:

- approved mark/logo;
- palette;
- shape language;
- typography character;
- spacing/density;
- photography/illustration treatment;
- elements that must never change.

Use real reference assets when available. Do not invent a new brand system when the project already
has one.

## 8. Exploration and convergence

### Exploration

When direction is genuinely undecided, create a small number of materially different concepts. Each
concept explores a real design axis, not trivial color swaps.

### Convergence

Once a direction is chosen:

- keep the strongest accepted output as anchor;
- change one meaningful axis per iteration;
- restate invariants;
- compare against previous accepted anchor;
- stop when acceptance contract is met.

Avoid endless generation loops. Preserve a strong first result instead of forcing unnecessary
variations.

## 9. Transparency and cutouts

If transparency is required, request it only when the current image tool supports that property and
verify the actual alpha channel afterward.

If output is opaque, do not call it transparent because the prompt asked for transparency.

For exact cutouts, use deterministic post-processing when available and inspect edge halos,
semi-transparent regions, shadows, glass, hair/fur, and despill artifacts.

## 10. Logos, icons, diagrams, and UI

Do not use raster generation by default for:

- exact SVG logos;
- simple icons;
- architecture diagrams with exact labels;
- charts driven by real data;
- production UI layout.

Use vector/code-native construction when determinism, editability, or exact text matters more than
organic imagery.

Generated mockups are appropriate for visual exploration, not proof that implemented UI matches.

## 11. Immediate post-generation check

Every generated or edited image must be viewed before acceptance when the host can expose the final
artifact. If the final pixels cannot be inspected, visual acceptance remains `UNVERIFIED`.

Check:

- composition and focal clarity;
- subject correctness;
- unwanted additions;
- anatomy/geometry where relevant;
- text accuracy;
- reference fidelity;
- crop/safe zones;
- transparency;
- edge artifacts;
- logos/watermarks;
- requested dimensions/export requirements;
- obvious visual imbalance or unnecessary clutter when the user requested a polished result.

If a critical property fails, make a targeted edit rather than rewriting the whole creative brief.
Do not reject a strong image merely because it uses common effects such as gradients, glow,
symmetry, bokeh, or stylized lighting when those choices work visually.
