---
name: jett-social-media
description: Create brand-specific 12-post Instagram campaigns and topic-led editorial feed previews, with generated backgrounds, deterministic typography, visual review, and delivery-ready assets. Use for coordinated social media grids, branded feed series, launch campaigns, or one combined 12-tile concept preview.
---

# Jett Social Media

Build one coherent 12-post campaign without leaking identity from any other client. Generate text-free backgrounds first, add exact copy and an optional logo with the deterministic renderer, and inspect the complete 3x4 feed before delivery.

## Art direction and delivery mode

For every invocation, first read [references/topic-led-art-direction.md](references/topic-led-art-direction.md). Derive a fresh visual direction from the current subject and brand. Aim for distinctive, relevant work; do not reuse a previous campaign's palette, props or scene arrangement as a universal template.

- **Combined preview:** when the user wants one concept feed, follow the combined-preview workflow in that reference. One text-free composite and deterministic overlays are supported. Let the model compose the scene vocabulary unless exact order is required.
- **Separate production posts:** follow the production workflow below after establishing the visual direction. Existing renderer and manifest contracts remain in force.

## Non-negotiable rules

- Use only the current user's brand inputs and explicitly approved references.
- Never invent metrics, customers, results, guarantees, testimonials, certifications, prices, or proof.
- For separate production posts, generate one background per post, without collages. For a requested combined preview, a single 3×4 composite is allowed.
- Background generation must contain no text, letters, numbers, logos, watermarks, UI, or signatures.
- Add exact copy and the optional supplied logo only through the renderer.
- Production posts use the fixed `balanced-orderly` anchor matrix. Combined previews use the actual quiet areas and package-label bounds; do not impose a headline or logo on every cell.
- Treat visual QA as `UNVERIFIED` until a person or vision-capable agent inspects the final composition and enlarged text/product areas; also inspect representative full-size posts for production delivery.
- Report technical rendering, visual review, browser/runtime, and publication readiness separately.

## Required intake

Read [references/intake-contract.md](references/intake-contract.md). Obtain or propose the brand name, sector, offer, target audience, campaign goal, language, colors, typography, voice, CTA, logo policy, and visual references. Mark proposed identity choices as proposed; do not silently treat them as approved brand facts.

## Runtime setup

Before scaffolding, read [references/runtime-setup.md](references/runtime-setup.md) and verify Python 3.12+, Node.js 20+, and npm. If a runtime is missing, show the relevant installation command or official download link and wait for the user to approve system-level installation. Use `python` on Windows or `python3` on macOS/Linux in the commands below.

## Production workflow

1. Inspect all supplied files. Label each as a brand reference, visual reference, logo asset, or proof asset. Never infer that a mood image is the brand itself.
2. Scaffold a campaign:

   ```bash
   <python-command> scripts/init_campaign.py \
     --dest /absolute/path/to/campaign \
     --brand-name "Your Brand" \
     --campaign-slug your-brand-campaign \
     --language tr
   ```

3. Write `brand/brand.json` and `content/posts.json`. Follow [references/content-architecture.md](references/content-architecture.md), keep claims source-safe, and validate:

   ```bash
   <python-command> scripts/validate_manifest.py --campaign /absolute/path/to/campaign
   ```

4. Read [references/image-generation.md](references/image-generation.md). Use the built-in image generation tool once per post. Generate a 4:5 text-free scene with negative space matching that post's anchor. Save it as `assets/backgrounds/NN-slug.png`.
5. Render deterministic overlays from the campaign directory:

   ```bash
   npm install
   npx playwright install chromium
   npm run build
   ```

6. Read [references/qa-and-delivery.md](references/qa-and-delivery.md). Inspect `outputs/preview/contact-sheet.png` plus at least four representative full-size posts. Record the result, then rerun verification:

   ```bash
   node scripts/record-visual-review.mjs --status pass --notes "Reviewed the contact sheet and posts 01, 04, 08, and 12."
   npm run verify
   ```

7. Package the final delivery:

   ```bash
   <python-command> scripts/package_delivery.py \
     --campaign /absolute/path/to/campaign \
     --desktop-dir /absolute/path/to/delivery
   ```

## Evidence contract

- `PASS`: directly checked in the current run.
- `FAIL`: directly checked and a defect was found.
- `UNVERIFIED`: not directly exercised or visually inspected.
- A successful manifest check does not prove visual quality.
- A successful render does not prove publication, scheduling, or platform upload.

## Bundled resources

- `scripts/init_campaign.py`: copy the reusable campaign engine.
- `scripts/validate_manifest.py`: enforce identity, layout, content, and proof rules.
- `scripts/package_delivery.py`: produce a clean desktop delivery and ZIP.
- `scripts/test_skill.py`: run the skill's regression tests.
- `assets/campaign-template/`: deterministic HTML/Playwright/Sharp rendering project.
