---
name: eric-intro-motion-skill
description: Create editable product and personal introduction videos, GIF demos, and animated GitHub README showcases. Reuse existing assets and render caches, with scene-by-scene native layouts for 1:1, 3:4 and 9:16 and independent Chinese/English typography.
---

# eric-intro-motion-skill

Turn an idea into a small visual story: objects should gather, travel, connect, or change in a way that explains the idea. Deliver the editable content alongside the animation.

For a product introduction, read [intro production](references/intro-production.md): verify the real workflow, choose meaningful shots, plan each language/ratio, and retain source and asset licenses. Duration follows the story and reading time; the examples are not a fixed length requirement.

For motion in a GitHub repository introduction, read [GitHub README presentation](references/github-readme.md). Put a supported looping preview, clear value statement, factual badges and install entry in the README itself. Preserve the requested primary language; a separate Pages gallery does not fulfill an inline README showcase.

## Reuse first; keep context small

Inspect existing media and manifests before creating anything. Reuse artwork, fonts and suitable components. Read the source needed for the requested changes; a whole-film ratio adaptation may require editing every scene. Keep resumable manifests and caches instead of repeatedly loading unchanged material.

When richer artwork or a polished product UI already exists, read [illustrated introductions](references/illustrated-intro.md). The finished Tidekeeper case combines scenes, characters, evolving objects and real UI states in six native bilingual films. Prefer the best completed case for the gallery and README; keep basic diagram studies below it. Do not reduce a mature visual system to generic cards just because a small template is available.

Choose the least expensive path that actually achieves the requested result:

1. Same finished animation: copy its GIF or transcode to MP4. No new artwork.
2. Reorder/cut footage: `scripts/assemble-media.mjs` keeps existing pixels and audio. Read [reuse recipes](references/reuse.md).
3. Change copy, modules, or ratio: `scripts/compose.mjs`. Run `--list` once for the 12-module catalog; inspect only selected labels in `assets/modules.json` if changing them. Nine profile scenes and three motion studies can be sequenced freely.
4. A new visual idea: extend just the missing component, then reuse it through the same recipe.

For a capture → categorize → save → return workflow, start from the new [native intro template](references/native-intro.md). Its four shots are optional and reorderable. Use `scripts/native-intro.mjs --stills` for all scene/language/ratio layouts before encoding. Keep a custom source renderer when the product needs richer UI or existing artwork; do not replace it with generic cards just to use this template.

A request to change the whole video's aspect ratio requires independent layer re-layout, including every scene and transition. An inset landscape video with a new background is a different treatment. For existing source films, follow sibling [social-motion's native recomposition workflow](../social-motion/references/native-recomposition.md); the small bundled module renderer is not a universal converter. Quality and fidelity take priority over token savings when the user requests that tradeoff.

```sh
node scripts/compose.mjs --input assets/examples/profile-remix.json --out output/remix --cache output/cache --preset moments
```

Start with `--formats png` for layout review. Clip hashes reuse unchanged renders across recipes; exact output hits skip encoding too. Keep the cache between runs. Rendering calls no model or image API; planning and editing still consume tokens. Do not invent a savings percentage.

Only the v3 native intro renderer uses resumable PNG frame caches. Its visual key covers recipe, scripts, font, dependency lock, language, ratio and frame rate; the output key also covers audio and encoder. For custom renderers, include every referenced visual asset and runtime input in the key. Audio-only changes can use `scripts/replace-audio.mjs --video old.mp4 --audio music.wav --out new.mp4`; it verifies that the H.264 stream is unchanged. See [cache and audio details](references/native-intro.md#cache-and-audio).

## Choose the story

Use the user's own subject and tone. Pick a concrete action to show, then write the minimum copy needed to understand it. The bundled examples are starting points, not a prescribed personal brand or a requirement to use three points for every story.

Read [the content schema](references/story-format.md) when using the renderer. Its starter motifs each support three cards:

- `flow`: a note moves through a process.
- `orbit`: information travels between a central agent and supporting nodes.
- `stack`: references are collected and organized.

For a substantially different story, extend the renderer or create a custom composition using [the motion language](references/motion-language.md). Preserve source-based ratio adaptation. Do not squeeze arbitrary content into three cards or replace requested content merely to fit a template.

## Render locally

Paths below are relative to this skill directory. Require Node.js 22+ and `ffmpeg` / `ffprobe` on PATH. Install dependencies once:

```sh
npm ci
node scripts/cli.mjs --input assets/examples/idea-to-post.json --out output/demo
```

Copy the JSON example into the user's workspace before editing it. Use an output directory there rather than modifying the installed examples.

The default is a 1920×1080, 30 fps MP4 plus a 720 px wide, 20 fps GIF, a full-size PNG poster, source SVG and JSON, a safe-area preview, and a validation report. MP4 is H.264 / yuv420p / square pixels / faststart with a silent AAC track. The GIF loops indefinitely. The PNG is the static alternative for reduced motion.

```sh
node scripts/cli.mjs --input story.json --out output/square --width 1080 --height 1080
```

Useful options: `--formats png` for a fast layout pass, `--gif-width 600` for a smaller GIF, `--fps 20`, and `--force` to replace that output deliberately. A poster and review files are always included.

## Review the result

- Inspect the poster and safe-area preview at the size people will actually see. Review moving frames too: a passing text-bounds check does not prove a useful or appealing story.
- Keep the content intact when changing ratios. The renderer measures outlined glyphs, wraps text, and fails on overflow or missing characters instead of clipping. Shorten copy with the user's intent in mind, or enlarge/rearrange the composition.
- Measure text inside its UI container as well as inside the canvas. Inspect embedded artwork labels, occlusion, reading time, entrance/motion/hold frames and both sides of every cut. Compare matching frames from the same source revision in every ratio. Each scene needs independent re-layout evidence; one changed shot does not establish a whole-film adaptation.
- Verify the final encoded files by full decoding and playback, not just source stills. If a closing QR code is used, decode it from the compressed video and verify the target. Review every delivered language separately.
- Check the report for geometry, duration, frame count, sampled motion, and file sizes. A GIF above the suggested 5 MB budget needs optimization if the destination requires it; this budget is not a universal platform limit.
- Include the JSON and poster with final GIF/MP4 links. State any remaining display uncertainty.

For LinkedIn, X, Moments, or a pack of multiple ratios, use the sibling `social-motion` skill when installed. Creating an asset does not authorize publishing it or changing profiles.

The former `motion-story` entry forwards to this skill. [Migration notes](references/migration.md) explain old commands, backups and installation. [Case findings](references/case-findings.md) distinguish existing public examples from locally verified production material.
