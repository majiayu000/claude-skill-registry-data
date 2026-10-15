---
name: content-os-tools
description: Use local media tools for short-form and long-form content production, including B-roll search, licensed downloads, ffmpeg edits, contact sheets, and asset ledgers.
---

# Content OS Tools

Use these tools when creating TikTok, YouTube Shorts, YouTube videos, or content-production drafts.

## Tool Directory

Prefer `CONTENT_OS_TOOLS_DIR` when set. Otherwise use:

```bash
$HOME/content-os
```

On a local Mac test install, the path may be:

```bash
$HOME/Downloads/content-os
```

## Rules

- Do not use random YouTube videos as B-roll unless the user owns the video, has explicit permission, or the license allows reuse.
- Prefer downloadable licensed media from Pexels and Pixabay for B-roll.
- For Content OS video production, B-roll is not optional unless the user explicitly asks for a lightweight text-only test. A real draft must feel like edited video, not generated stills stitched together: include actual moving video clips where possible (licensed Pexels/Pixabay footage, screen recordings, product demos, animated UI captures, motion graphics, or generated video), with purposeful cuts, speed ramps, push-ins, match cuts, overlays, transitions, SFX, and pacing matched to the voiceover. Generated stills may be used only as supporting shots unless animated internally with meaningful subject motion, parallax, camera moves, and foreground/background movement.
- Use YouTube search for trend research, metadata, links, and transcript-driven inspiration by default.
- Always track downloaded/generated assets in `asset-ledger`, including source URL, license/permission status, crop/trim path, and which storyboard beat uses the asset.
- Always produce a contact sheet for generated video drafts before claiming the draft is ready. If contact-sheet review shows captions cut off, reduce font size, wrap long lines, add safe margins, and re-render before delivery. If generated stills are animated with FFmpeg crop/pan/overscale, verify the motion itself did not clip typography; prefer full-frame renders or internal-element motion when text is already in the still.
- For generated shorts, QA captions for complete phrases. Auto VTT/word-cue grouping can truncate contact-sheet text; use concise hand-authored caption chunks when readability matters.
- Treat voice as an asset, not an afterthought: for Content OS shorts, avoid bland default TTS voices; use an energetic creator-style voice and generate a short sample before full render.
- When contact-sheet tiles sample past the video duration, blank cells are a QA artifact. Prefer explicit timestamp/frame selection for the sheet and then inspect with vision/manual review.

## Short-form hook database

When designing Instagram/TikTok/Shorts openings, treat the first 2–5 seconds as modular Lego bricks: combine **one visual hook** with **one spoken hook**, plus matching audio/SFX when possible.

Canonical source: Kallaway / Content Game FigJam board, "Short Form Lego Bricks / Visual + Spoken Hooks": `https://www.figma.com/board/xDzw2Ix07R7xDUcKluhT11/Short-Form-Lego-Bricks?node-id=3037-1734&utm_source=www.content.game&utm_medium=newsletter&utm_campaign=here-is-your-short-form-visual-spoken-hooks-database`

Important: choose the hook bricks from this FigJam-derived hook database **before** designing/generated asset cards. Do not reverse-engineer the hook from the PNG/SVG asset pack. In `hook-recommendation.md` or user-facing recommendations, explicitly name the selected FigJam visual brick(s), selected spoken brick, opening shot, first spoken line, SFX/audio cue, and why that exact combo fits the topic.

If the user asks for the "actual video from FigJam" or a hook they can "edit into the video," they mean a playable embedded reference clip, not the text taxonomy. Try extraction honestly, disclose limitations, and if generating a replacement, label it as an original FigJam-style insert. See `references/figjam-video-hook-extraction.md`.

Visual hook categories learned from Kallaway's "Short Form Lego Bricks / Visual + Spoken Hooks" FigJam board:

- **Subject motion:** point to visual, move in frame, camera whip, jump in, snap/pop reveal, clone/body double, anticipated disaster, object catch, setting down phone, holding prop, many-of-same-prop, framebreaker, jump switch, crash zoom, fridge POV, write on screen, mirror, yap cold open.
- **Graphic/text overlays:** A-vs-B comparison graphic, text slide-in, interactive title, text arrow pointer, small image drop overlay, screen recording with motion, image overlay motion, countdown.
- **Visual selection:** high-motion base B-roll, unusual first image/scene, silent reaction PIP, visual mistake.
- **Pattern interrupt / visual switching:** viral stitch reaction, match cut, visual switch, beat-match visual switch, viral stitch motion match, unlinked/unexpected switch.
- **Effects/transitions:** speed ramp, zoom in, look-up/top-down camera, sudden danger first-person POV, fisheye, frame collage, crazy transition, experimental interactive effect, color switch.

Spoken hook categories:

- **Educational:** secret reveal, case study, problem, contrarian, negative/warning, direct education, list, scenario/hypothetical, comparison, question, ranking/rating.
- **Storytelling:** authority/proof, personal experience.

Practical rule: never open with static setup if a hook can start with movement, surprise, visual contradiction, comparison, warning, secret, question, or credibility. Example combinations: Camera Whip + Contrarian; Holding Prop + Problem; Unusual First Image + Secret Reveal; Screen Recording w/ Motion + Case Study; Frame Collage + Ranking/Rating.

## Instagram carousel/static image packs

When creating Instagram carousels from Content OS scripts, do not default to flat HTML/PPT-style cards. The user prefers aesthetic, premium-looking images; if a generated carousel looks like HTML components, basic web cards, or a slide deck, treat that as a miss and redo/refine it. First resolve the exact source: if the user asks in a thread reply to make a carousel “out of this,” use the referenced parent/thread concept and saved script, not a rejected-ideas/digest variant unless explicitly requested. When the user explicitly asks to use Codex, or when a more designed static image set is needed, use Codex to generate/refine a deterministic Pillow-based `generate_carousel.py`, 1080x1350 PNG slides, a contact sheet, and caption/README files, then QA with vision and run a targeted Codex refinement pass for readability/design issues before delivery. Deliver ordered individual slide images first; zip files are optional backup only. See `references/codex-aesthetic-carousel-generation.md` and the `instagram-carousel` skill.

## Talking-head asset packs

When the user is filming themselves and only needs supporting insert visuals, do not default to full-video production. Create an editor-friendly asset pack instead:

- Read the latest script and its asset/B-roll brief.
- Generate 5–10 supporting visuals: headline cards, diagrams, workflow maps, comparison cards, checklists, mock UI screens, quote cards, or abstract tech/editorial cutaways.
- Prefer 1080x1920 SVG/PNG cards or transparent overlays that can be dropped into an Instagram edit.
- Save `README.md`, `asset-ledger.jsonl`, and `broll-suggestions.md` alongside the assets.
- Suggest licensed B-roll using Pexels/Pixabay search URLs or source-page screenshot/screen-recording ideas; do not suggest random YouTube footage without clear reuse permission.

## Humor inserts and background removal for Reels

When the user asks for humorous memes/GIFs from a voiceover/script, extract concrete humor beats from the script first, query each source, and deliver a contact sheet rather than a raw list of links. For fast Reels, prefer **animated reaction GIFs/MP4s with no or minimal text** over static long-caption memes; viewers will not read long meme text during a 0.5-1.5s insert. Prefer MP4 GIF variants when available because they edit and compress better than raw GIFs. Prefer a curated local AI/dev/founder/operator meme+GIF corpus with semantic search for production use; treat public meme indexes as proof-of-concept/discovery only.

For talking-head background removal comparisons, test the same short representative clip across tools, normalize outputs to the same background, and deliver a comparison video/contact sheet before recommending the default. After a short clip succeeds, validate the chosen tool on the **full talking-head duration** using a CPU-friendly proxy first (for example 360x640 at 15fps), then create a side-by-side QA video and contact sheet sampled across the whole clip to catch temporal drift/flicker. Default to RVM-style matting for normal talking-head clips, keep rembg/video-background-remover as a simple fallback, and ask for an empty-background plate when trying BackgroundMattingV2-style workflows. See `references/humor-inserts-and-bg-removal-eval.md` and `references/rvm-long-and-reaction-gif-eval.md`.

## Local generated-video fallback

When Remotion/TTS integrations are unavailable or too heavy, a fully local path is acceptable for drafts: generate VO with `edge-tts` or the configured content-OS `text_to_speech` tool, draw 9:16 scenes with Python/Pillow when available or pure FFmpeg `drawbox`/`drawtext` filters when Python imaging libraries are missing, encode with FFmpeg, then mux the VO with a quiet generated bed (`sine`/`anoisesrc`) if needed. This avoids third-party B-roll/licensing, but still requires the normal ledger, decode check, black-frame check, and contact-sheet review. If using FFmpeg text overlays, wrap long captions into safe line lengths before rendering; contact-sheet QA should catch and trigger fixes for right-edge clipping.

For a reusable video-first local motion-graphics workflow, including FFmpeg QA commands and the `afade=d=0.7` duration gotcha, see `references/local-motion-graphics-fallback.md`.
For procedural Python/Pillow + FFmpeg rendering details—NumPy background performance, 15fps draft targets, silent-render reuse, generated-local ledgers, and slide-in text contact-sheet pitfalls—see `references/procedural-motion-graphics-rendering-notes.md`.
For OpenNolan fast draft production when cloud TTS fails or Remotion is too slow, including Piper/local voice fallback, FFmpeg muxing, contact-sheet fixes, and delivery-channel language, see `references/opennolan-ffmpeg-draft-render.md`.
For approval-gate / vertical-AI shorts, including contact-sheet fixes for blank stamps, final CTA safe areas, washed-out cards, and lower-third overlap, see `references/approval-gate-short-qa.md`.

## Commands

Search:

```bash
node bin/media-search.mjs --provider pexels --query "office reaction" --limit 5
node bin/media-search.mjs --provider pixabay --query "startup founder laptop" --limit 5
node bin/media-search.mjs --provider youtube --query "creator economy trend" --limit 5
```

Plan B-roll from a script:

```bash
node bin/broll-plan.mjs --script scripts/idea-1.md --out assets/broll-plan.json
```

Download after license confirmation:

```bash
node bin/media-download.mjs --url "https://..." --license-confirmed --out assets/clip.mp4
```

Edit:

```bash
node bin/video-edit.mjs trim --input assets/clip.mp4 --start 0 --duration 5 --out assets/clip-trimmed.mp4
node bin/video-edit.mjs crop --input assets/clip-trimmed.mp4 --ratio 9:16 --out assets/clip-vertical.mp4
node bin/video-edit.mjs contact-sheet --input renders/final.mp4 --out qa/contact-sheet.jpg
```

Ledger:

```bash
node bin/asset-ledger.mjs add --ledger assets/ledger.jsonl --path assets/clip.mp4 --source-url "https://..." --license "pexels-review-confirmed"
```

