---
name: qwen-image-prompting
description: Load for local Qwen-Image / Qwen-Image-2512 image-generation work — prompt writing, lane and settings selection, negative-prompt routing, multi-seed attempts and QA, ComfyUI workflows, PPT/poster/infographic/chart/textbook figures, UI thumbnails and minimalist UI-shape prompts, and text-heavy academic visuals. Use Kosta's RTX/GamingPC full Qwen+CacheDiT lane; Lightning is draft-only.
metadata:
  targets:
    - claude
    - codex
    - hermes-default
    - hermes-gpt
    - claude-hermes
    - cursor
    - gemini
    - droid
---

# Qwen-Image Prompting

Use this for Qwen-Image and Qwen-Image-2512 on Kosta's RTX/GamingPC ComfyUI setup: school, study, paper, poster, PDF, slide, chart, infographic, textbook visuals, and local UI/shape thumbnail work. The same rules apply if the local lane is later swapped to another diffusion model, except for Qwen-specific defaults flagged below.

## Local model coverage and default lane

Current RTX local inventory includes **Qwen-Image-2512 FP8**, matching Qwen 2.5-VL text encoder, Qwen VAE, **Qwen Lightning 4-step LoRA**, and a separate **Ideogram 4 NVFP4 mixed** ComfyUI lane at `http://100.93.10.54:8190`. A 2026-05-22 live ComfyUI API/object_info audit found Qwen installed and FLUX.2-dev **not installed yet**; keep **FLUX.2-dev FP8** as the planned secondary RTX workflow for polished presentation imagery/reference-driven visuals. Default routing: Qwen remains primary for textbook/PPT figures, exact-ish charts, scientific diagrams, and local production visuals; Ideogram is the first local lane for typography/design-heavy posters, signs, labels, packaging, menus, and infographic-style layout experiments **only when prompted with structured JSON captions**. Do not declare RTX models present or absent from shallow directory listings; use ComfyUI `/models/<category>`, `/object_info`, and targeted known model directories. Mac Studio has other image models, but RTX is Kosta's primary image-generation machine; do not default to Mac fallbacks unless asked.

Use **full Qwen-Image-2512 FP8 + CacheDiT** for any image intended to ship. Use **Lightning 4-step LoRA only for draft candidates**, because local stress-test QA showed valid composition but garbled dense titles/legends. If using Ideogram, load `media/ideogram4-prompting`; never send plain prose as the final Ideogram prompt for text/layout work, because Ideogram 4's documented training format is structured JSON captions and non-JSON prompts caused safety-placeholder false positives in local testing.

Known GamingPC files:

- ComfyUI root: `C:\Users\kosta\AIProjects\ComfyUI`
- Health script: `scripts\health-comfyui.ps1`
- Stress script: `scripts\stress-qwen-comfyui.ps1`
- Diffusion: `models\diffusion_models\qwen_image_2512_fp8_e4m3fn.safetensors`
- Text encoder: `models\text_encoders\qwen_2.5_vl_7b_fp8_scaled.safetensors`
- VAE: `models\vae\qwen_image_vae.safetensors`
- Draft LoRA: `models\loras\Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors`
- Style/speed LoRA catalog: `references/gamingpc-qwen-lora-catalog-2026-05-23.md`
- CacheDiT node: `CacheDiT_Model_Optimizer`; use model type `Qwen-Image`, warmup `5`, skip interval `3` for 50-step jobs.

## Prompt as a layout spec, not a vibe

For text-heavy images, write the prompt like a design brief with exact quoted text:

```text
Create a [16:9 PowerPoint slide / academic poster / textbook figure / infographic / chart] in [style].
Canvas/layout: [grid, columns, rows, hierarchy, margins].
Title text: "[exact title]"; location: [top center/etc.]; style: [bold sans-serif/etc.].
Section 1: [visual object], label "[exact label]", caption "[exact caption]".
Arrows/flow: [direction, labels, colors].
Legend: [exact legend entries].
Axes/chart labels: x-axis "[exact]", y-axis "[exact]", tick labels "[...]", units "[...]".
Use clean spacing, high contrast, readable typography, aligned margins.
No additional text beyond the quoted text.
```

Every visible word should be quoted exactly. Avoid “some labels,” “a legend,” “a list,” or “a chart” without giving the exact labels/numbers.

## Strong defaults for academic visuals

Use these phrases when appropriate:

- `clean textbook figure`, `PowerPoint lecture slide`, `white background`, `vector-like flat colors`, `thin consistent strokes`, `crisp readable labels`, `high contrast`, `generous margins`, `no extra text`
- For diagrams: specify panels, object positions, arrow direction, callout labels, legend entries, and what each color means.
- For charts: specify chart type, axes, units, tick labels, legend, colors, and whether values must be schematic or data-accurate.
- For posters/PDFs: split dense content into multiple figures/slides; do not ask one image to hold a full page of tiny text.

## Negative prompt routing

Never write `Exclude X`, `no X`, or `avoid X` clauses at the end of the positive prompt. Qwen frequently parses those as concepts to render (benchmark evidence: `Exclude folded paper stack` produced a paper stack on intent 01; `no device frame` produced a tablet bezel on intent 05). Put every exclusion in the dedicated negative prompt slot — `CLIPTextEncodeNegative` in ComfyUI, or the equivalent slot in any other UI.

Pick the preset that matches the job, then append intent-specific tokens (e.g. `human face` for avatar placeholders, `hinges` for drawers).

**Text-heavy academic / slide / poster / textbook / chart:**

```text
low resolution, low quality, blurry text, distorted text, misspelled text, extra text, duplicated labels, unreadable small print, broken legends, incorrect axes, misaligned layout, cluttered spacing, cropped labels, random symbols, incorrect arrows, inconsistent legend colors, decorative filler text, watermark, noisy background
```

For charts/figures also add: `fake data, incorrect tick labels, mismatched legend colors, overlapping labels, cropped axis title`.

**UI essence / minimalist shapes / non-text thumbnails:**

```text
text, labels, caption, heading, annotation, callout, gibberish text, fake UI text, device frame, phone bezel, tablet bezel, laptop, keyboard, monitor frame, product mockup, paper stack, folded paper, book pages, oval, lens, lozenge, blob, perspective tilt, folded card, tilted card, card standing on edge, hinged door, swinging door, glass door, door hinges, photo-realistic face, stock photo, portrait, watermark, low resolution, blurry
```

## Prompt-build checklist

Before returning a prompt, output these six items on one line each, marked addressed or `n/a`. Do not silently skip. The benchmark showed rewriters apply some rules and quietly drop others; the explicit list is the audit.

1. **Geometry, count, spatial layout** pinned (shape, orientation, camera angle, exact count tied to `side by side` / `stacked` / `top-left` etc.).
2. **Colors** named concretely when color matters (no bare `colorful` / `vibrant`).
3. **Composition language** instead of motion verbs (`pinned to the left edge`, not `sliding in`; `larger version on the right`, not `scaling into`).
4. **Positive prompt is clean** — no `exclude`, `no`, `avoid`, or `without` clauses.
5. **Negatives routed** to the negative-prompt slot, with the correct preset plus intent-specific tokens.
6. **Trigger-word scan** done: no `label / callout / caption / annotation / heading / before-after / study / diagram / explanation / how it works`, and no `mockup / product / studio / professional photography / on a desk` unless the subject genuinely is a physical mockup or device.

## Settings

Pick the lane by acceptance bar, not by speed:

| Use case | Lane | Steps | CFG | CacheDiT |
| --- | --- | ---: | ---: | --- |
| Anything intended to ship (text-heavy or UI/shape) | Full Qwen-Image-2512 FP8 | `50` | `4.0` | warmup `5`, skip `3` |
| Fast exploratory draft / candidate | Qwen Lightning 4-step LoRA or Wuli Turbo LoRA | `4` | `1.0` | off |
| Obsidian/editorial card A/B | Full Qwen + one style LoRA from LoRA catalog | `30-50` | `3.5-4.0` | optional |
| Benchmark / stress / one-off experiment | record in manifest | record | record | record |

Aspect-ratio sizes (Qwen-Image-2512 native): 16:9 slides `1664x928`; 4:3 figures `1472x1104`; square `1328x1328`; 3:2 `1584x1056`; 2:3 `1056x1584`.

If a final-quality request runs at fewer than `30` full-Qwen steps, warn that output is below the skill's normal ship lane and treat it as draft/benchmark until QA proves otherwise. Lightning at `4` steps is fine because it is explicitly a draft lane.

For benchmark or A/B runs, always record `steps / CFG / sampler / scheduler / size / LoRA / CacheDiT / seed` in a manifest. Single-seed comparisons are directional, not conclusive — the current generalization benchmark is n=1 per intent, so its rule-by-rule conclusions should be treated as signals to refine, not proofs.

## Batch catalog thumbnails

For second-brain/catalog thumbnails, do not prompt from the title alone. Read the entry content/code summary and name the concrete UI pattern, components, and interaction. A batch of 94 technically successful files can still be a bad result if every image is a generic phone mockup.

LoRA routing for this work lives in `references/gamingpc-qwen-lora-catalog-2026-05-23.md`. Do not turn a LoRA on globally just because it exists: run the 5-note smoke test first, use at most one style LoRA at a time, and route by domain when a LoRA only helps one class of note. Good defaults: `illustration-1.0` for general editorial Obsidian cards, `Isometric Redmond` for systems/architecture/tooling notes, `Stickers Redmond` for single icon/motif covers, `Pixel Art` only for intentionally retro/playful covers. Keep speed LoRAs as draft lanes unless QA proves final quality.

Kosta specifically prefers creative renderings of the code output / visual essence over literal phone-screen app mockups. Avoid the reflexive `SwiftUI → iPhone screen → polished app UI` chain. For effects and components, make the effect/component the subject: geometry, material, masks, layers, motion state, shadows, spacing, and the rendered composition. Only include a phone/device frame when the source code truly depends on the device surface; otherwise crop to the component or use an abstract render.

Before a large batch, generate 3-5 samples from different categories and visually inspect them. If the user criticized a previous batch, delete or quarantine the old assets before regenerating so stale low-quality images do not remain linked. Use Lightning only for drafts; use the full Qwen/CacheDiT lane or another quality lane for final replacement batches.

For iterative repair, keep prompts short and run an adversarial review loop: score each image 0-5 against the intended visual essence, name the single dominant failure, revise only the failing prompts, and stop when two reviewers agree the remaining issues have plateaued. When Kosta asks for self-evolution/self-improvement, do not treat 2-3 passes as enough: run at least 10 loops, at most 30 loops, or stop only after 4 consecutive plateau loops. Track loop number, score, dominant failure, prompt delta, image path, elapsed time, token/call estimate if available, and plateau count. Use a persistent Claude Code reviewer/worker (`claude -p -c`) for caching benefits; give it concise intended descriptions and image paths, not long prompt essays. When GPT prompt-architect guidance is requested, simplify rather than expand: one short intent line, 1-2 visible constraints, explicit scope boundaries/exclusions, and a manifest of score/failure/fix.

If a correction arrives embedded in tool output or background-process output, treat it as an active user correction before continuing. Do not let a “process completed” notification hide user feedback like “delete these images” or “send representative samples.”

For any UI-essence prompt — thumbnail, motion study, component render, shape composition — avoid words that invite Qwen to fabricate explanatory text: `label`, `callout`, `annotation`, `caption`, `heading`, `before/after`, `study`, `diagram`, `explanation`, `how it works`. Even with `no text` in the negative prompt, these words tend to produce garbled pseudo-labels (benchmark intent 04: `UI motion study` produced fake labels under both tiles). Prefer icon-only rows, placeholder bars, arrows, panels, ghosted duplicate shapes, and cropped UI states.

Avoid product-photo framing unless the subject is genuinely a physical object: `mockup`, `product mockup`, `product render`, `studio shot`, `professional photography`, `on a desk`, `on a surface`, `laying on a table`. These pull Qwen toward physical-object realism (benchmark intent 01: `Minimal product mockup` framing turned a flat card into a stack of paper sheets, scoring −2.0 versus the plain baseline). For flat UI/shape work, use `flat 2D UI graphic`, `minimal vector composition`, `orthographic view`, or `viewed from directly above`.

Use this compact schema for code-pattern/catalog thumbnails:

```text
High-quality visual-essence thumbnail for a SwiftUI code pattern. Pattern: "<specific pattern>". Rendered subject: <the component/effect itself — geometry, material, masks, layers, shadows, spacing, motion state>. Surface: <component crop / abstract render / macOS window / device frame only if the code depends on it>. Focus on what the rendered code output could look like, not a hypothetical app screen using it. No code, no watermark, no logos, no labels, no callout text, no random readable text, no gibberish labels.
```

Bad default: “SwiftUI catalog thumbnail as a flat 2D UI storyboard / app interface / iPhone screen.” That still tends to produce plausible phone mockups. Prefer “rendered component/effect as the subject.”

### UI-essence failure modes to pin in the prompt

Six failures recur even with the schema above; all need explicit in-prompt language, not just negatives:

- **Literal device backdrops creep in.** Saying “floating macOS desktop window” or “app screen” pulls Qwen toward rendering a literal MacBook keyboard, phone bezel, or monitor frame *behind* the subject — even when the rest of the prompt is abstract. Add an explicit positive negative: `no laptop, no keyboard, no device frame` (or `no phone, no bezel` for mobile). For the backdrop, name the abstract thing you want (`soft abstract pastel desktop wallpaper gradient`, `clean off-white studio`) instead of relying on words like “desktop” or “workspace.”
- **Edge-anchored panels flip orientation.** “Side drawer,” “bottom sheet,” “snackbar,” and similar edge-anchored overlays often render with the wrong aspect or wrong edge. Pin three things together: aspect (`tall vertical, taller than wide` or `wide horizontal, wider than tall`), edge (`attached to the left edge` / `pinned to the bottom edge`), and an explicit negative for the wrong orientation (`no horizontal drawer`). Describe the scene as a layered composition (`darkened dimmed background rectangle filling the frame, partially covered on the left half by …`) rather than a motion verb (`sliding in from the side`) — Qwen interprets composition more reliably than implied motion.
- **Edge-anchored drawers render as physical glass doors.** Even with "no horizontal drawer" pinned, Qwen still produces a hinged glass-door composition when the prompt mentions "drawer" or "overlay." You need an explicit "flat 2D UI surface, no hinges" in the positive prompt plus negatives `hinged door, swinging door, glass door, door hinges`. The orientation rule alone is not enough — it fixes the aspect but not the affordance.
- **Glass-tile geometry drifts to oval/lens.** When the subject is "a translucent glass tile" or "rounded glass shape," Qwen frequently renders an oval or circular lens. Pin geometry explicitly (`rounded rectangle, gentle corner radius`, or `rounded square`) and negate the failure modes (`no oval, no circular tile, no lens`). Same pattern applies to any rounded-rectangle UI element described loosely.
- **Avatar placeholders default to photo-realistic faces.** "Small circular avatar" in a UI prompt almost always produces a stock-photo human face. Pin the placeholder explicitly: `small solid filled gray circle, abstract placeholder, no face, no photo` and negate `human face, photograph, portrait, person, woman, man, eyes, hair, realistic skin`. Same risk applies to "profile picture," "user icon," "contact photo."
- **"Flat card" doesn't pin orientation.** When a card or sticker should lie flat on a surface, the word "flat" alone tends to produce a tilted or folded card. Pin the camera angle (`lying flat on a surface, viewed from slightly above`) and negate the failure modes (`folded card, tilted card, card standing on edge, leaning card`). For peel/curl compositions, also specify which corner peels.
- **Element counts drift unless tied to spatial hints.** "Two pill buttons" can render as one; "three pill bars" can become four. Pair the count with a spatial layout (`exactly two small pill buttons side by side`, `three short horizontal pill bars stacked vertically`) and negate the common drift (`single pill, only one button`). Spatial-hint anchoring beats bare count words.
- **Single-corner instructions need two anchors.** `top-right corner curl` can flip to bottom-right. Pin the target twice: `upper-right corner, near the top edge and right edge`, and add the opposite corner to negatives if needed. Single corner names are weak.
- **Named colors need zones.** If you name four colors without assigning positions, Qwen may render only three. Either cap to three colors or map each color to a zone (`red triangle left`, `blue square top-right`, `yellow circle center`).
- **Abstract shape phrases collapse to bands.** `sharp geometric shapes` can become color stripes. Name the shape category: `crisp triangles, circles, and squares`, then place them behind/around the subject.
- **Ghost trails become separate cards.** `ghosted motion trail` often renders as discrete stacked cards. For smoother morphs, describe `one faint elongated overlapping silhouette fading from small to large` instead of several ghost copies.

## QA before accepting an image

For any image where intent matters, do not accept a sample-of-1. Generate at least **3 seeds** for the first prompt. Score each candidate `0-5` against the original intent; pick the highest; on ties, pick the one with the fewest negative-prompt violations. If the best is below `4` for normal use or below `5` for exact-text deliverables, revise the prompt and run **3 more seeds**. Stop after two prompt revisions with no material score gain — unless the user asked for the deeper self-evolution loop, which is governed by the batch section below.

Run a vision reviewer before shipping. On Kosta's setup that means calling `vision_analyze` from Hermes, `mcp__zai-vision__analyze_image` where available, or — when Claude is the agent — reading the candidate image with the `Read` tool. Give the reviewer the original intent line (not the full prompt essay) and ask for `score 0-5`, `dominant failure`, and `ship / revise`. Reject below `3`; revise below the user's acceptance bar.

Inspect visually at 100–200% zoom yourself before declaring ship. Check:

- All quoted text appears exactly, with correct spelling, capitalization, punctuation, and units.
- No extra/unrequested text appears.
- Title, headings, labels, captions, legend, axes, and arrows match the prompt.
- Text is large enough at final slide/PDF size.
- Legend colors match chart/diagram elements.
- Arrows point to the right targets.
- No cropped labels, overlapping text, fake watermarks, pseudo-gibberish, or decorative filler.
- Scientific content is conceptually correct.

If exact text is critical, prefer generating a clean visual without dense text, then place final labels as editable PowerPoint/SVG/vector text.

## Sources checked

- Qwen-Image-2512 model card: `https://huggingface.co/Qwen/Qwen-Image-2512`
- Qwen-Image official repo and prompt-enhancement guidance: `https://github.com/QwenLM/Qwen-Image`
- ComfyUI Qwen-Image-2512 docs: `https://docs.comfy.org/tutorials/image/qwen/qwen-image-2512`
- ComfyUI Qwen-Image docs: `https://docs.comfy.org/tutorials/image/qwen/qwen-image`
- LightX2V Qwen-Image-Lightning settings: `https://github.com/ModelTC/LightX2V-Qwen-Image-Lightning`
