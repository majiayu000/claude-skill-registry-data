---
name: whats-the-difference-short
description: Create viral-style stickman "What's the Difference?" YouTube Shorts from one or two pairs of similar words or concepts, using bold example images, a consistent expressive stick-figure presenter of any requested gender, white meme-style 9:16 layouts, fast pacing, energetic Kokoro narration, and data-driven Remotion sequencing. Use when Codex should research an accurate distinction, build the signature "This is X. This is Y. What's the difference?" five-scene format, organize a complete topic folder, preview or render the Short, and prepare publishing metadata and sources.
---

# What's the Difference Short

Build a complete 1080x1920 comparison Short in the signature viral stick-figure format. Keep Remotion limited to sequencing finished scene images, voiceover, timing, subtle motion, optional captions, and rendering.

## Accept the brief

- Accept one or two comparison pairs.
- Default to 30 FPS, 1080x1920, 15-40 seconds, American English, and Kokoro `af_bella` at speed `1.08`.
- Treat requested language, voice, character gender, duration, caption, or visual-source choices as authoritative.
- Preserve the signature format unless the user explicitly requests a variation: white meme-style canvas, bold black headline, large example imagery, and one consistent expressive stick-figure presenter.
- Ask one concise question only when a missing choice materially changes the result. Otherwise proceed.

## Inspect or initialize the project

1. Inspect the current directory for a compatible Remotion project.
2. If no project exists, run:

   ```bash
   python <skill-dir>/scripts/bootstrap_project.py --target .
   npm install
   ```

3. Run `python scripts/doctor.py --project .` and resolve required failures.
4. Preserve existing user changes when adapting a project.

Read [remotion-architecture.md](references/remotion-architecture.md) before changing the renderer or data model.

## Research and write

1. Verify each distinction with reliable sources. Browse when the term is current, niche, medical, legal, psychological, or otherwise accuracy-sensitive.
2. For each pair, use this sequence without an introductory filler line:
   - `This is X.`
   - `This is Y.`
   - `What's the difference?`
   - Explain X plainly.
   - Explain Y plainly and make the contrast explicit.
3. Keep the narration energetic, natural, concise, and understandable without the images.
4. Avoid diagnosing real people or presenting fictional characters as literal clinical or legal examples. Label them as analogies when needed.

Read [script-and-storyboard.md](references/script-and-storyboard.md) for scene patterns and wording rules. Read [production-workflow.md](references/production-workflow.md) for the complete artifact checklist.

## Create the topic package

Run the scaffold once the pairs are known:

```bash
python scripts/scaffold_video.py --project . --pair "Equality|Equity"
```

For two pairs, repeat `--pair`:

```bash
python scripts/scaffold_video.py --project . \
  --pair "Strategy|Tactics" \
  --pair "Correlation|Causation"
```

Keep all topic-specific files under `public/videos/<video-id>/`. Do not scatter narration, sources, downloaded assets, or publishing copy elsewhere.

## Produce complete scene images

- Treat every scene image as a finished video frame.
- Do not draw stick figures, comparison cards, icons, layouts, backgrounds, or illustrations in React/Remotion.
- Prefer an available image-generation tool for original scene art. If the user requests web or supplied assets, follow that choice.
- Keep important text and faces inside the Shorts safe area: at least 80 px from the sides, 100 px from the top, and roughly 320 px above the bottom.
- Use "stickman" as the general format name regardless of character gender.
- Maintain the same stickman design, face, proportions, line weight, and footwear across every scene. Match the requested gender; default to a female-presenting character when using the default female Kokoro voice.
- Use the recurring pointing-left, pointing-right, teaching, and question-mark poses defined in the visual guidelines.
- Treat the presenter and meme-style layout as required parts of the format, not optional decoration.
- Save final PNG, JPG, JPEG, or WebP files as `images/scene-01.*`, `scene-02.*`, and so on.
- Record web sources and license or usage notes in `sources/SOURCES.md`.

Read [visual-guidelines.md](references/visual-guidelines.md) before generating scenes. Read [asset-sourcing.md](references/asset-sourcing.md) before downloading third-party media.

## Generate and synchronize narration

1. Put one narration chunk per scene on its own line in `narration.txt`.
2. Set up Kokoro using [kokoro-setup.md](references/kokoro-setup.md).
3. Generate audio:

   ```bash
   .venv/bin/python scripts/generate_voiceover.py \
     --input public/videos/<video-id>/narration.txt \
     --output public/videos/<video-id>/audio/voiceover.wav \
     --voice af_bella --lang a --speed 1.08 --pause-ms 90
   ```

   On Windows use `.venv\\Scripts\\python.exe`.

4. Synchronize scene durations and JSON captions from Kokoro timing metadata:

   ```bash
   python scripts/sync_timeline.py --project . --video-id <video-id>
   ```

5. Keep captions optional. If enabled, store them in Remotion `Caption` JSON shape.

## Validate, preview, and render

Run:

```bash
python scripts/sync_registry.py --project .
python scripts/validate_video.py --project . --video-id <video-id>
npm run lint
npm run dev
```

Render only when the user requests a final render:

```bash
npx remotion render <video-id> public/videos/<video-id>/output/<video-id>.mp4
```

Use hard cuts by default. Use only fast fade, crossfade, slide, zoom-in, or pop transitions when they improve comprehension. Drive all motion from the Remotion frame, never CSS animation or browser time.

## Prepare publishing copy

Write `publishing.md` with:

- A concise searchable title ending with or implying "What's the Difference?"
- A short description that states both distinctions accurately.
- Three to eight relevant hashtags, including `#WhatsTheDifference` and `#Shorts` when appropriate.
- Any educational, medical, psychological, or legal caveat the topic needs.

Read [publishing-metadata.md](references/publishing-metadata.md) for the format.

## Completion checklist

- Confirm every scene is a complete 1080x1920 image.
- Confirm narration starts directly with `This is ...` and contains no filler introduction.
- Confirm the voice sounds energetic and clear.
- Confirm no scene audio overlaps unexpectedly.
- Confirm scene durations follow the generated voice timing.
- Confirm essential content avoids Shorts UI collision zones.
- Confirm the topic folder contains content, narration, configuration, sources, images, audio, and publishing copy.
- Confirm config validation and TypeScript lint pass.
- Confirm a preview or still was inspected before handing off a render.
