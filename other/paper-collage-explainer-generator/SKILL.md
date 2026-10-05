---
name: paper-collage-explainer-generator
description: "Plan and produce one editorial paper-collage explainer from a concept, narration line, or story beats: approve visual metaphors and final stills before generating tactile stop-motion collage clips and optional assembly. Use for halftone cut-paper explainers and social B-roll; unlike make-explainer-video (relationship 0.78), choose this when paper material, still approval, and stop-motion assembly own the deliverable; unlike generate-video (0.59), choose this when the shot is part of a coherent collage plan. Do not use for presenter ads, editable-layer delivery, exact readable typography, generic B-roll, or unrequested voiceover, music, and subtitles."
---
# Paper Collage Explainer Generator

## Catalog

- Display name: Paper Collage Explainer Generator
- Categories: Video
- Status: Ready
- Route label: Approved cut-paper visual-metaphor production
- Tone: orange
- Short description: Turn an idea into an approved halftone paper-collage plan, tactile clips, and optional assembly.
## What this skill does

- Converts each idea or beat into an object-led visual metaphor rather than relying on on-screen text.
- Locks a coherent material system—halftone cut-outs, color fields, cream keylines, paper grain, torn edges, and soft shadows—before generation.
- Uses approved final stills as the end-state anchor for readable stop-motion paper assembly.

## How to use

Provide the concept, source line or story beats, audience/context, ratio, duration, number of segments, and any explicitly requested narration, music, subtitles, or supplied assets.

#### Example

```text
把“城市树木会降低街道热岛效应”做成三个 16:9 的纸艺拼贴解释镜头。先给我隐喻和静帧方案；不要旁白、音乐或字幕，保留自然的纸张滑动和按压音。
```

## Workflow

1. Lock the message, audience, ratio, duration, beat count, factual source expectations, and supplied assets. Do not request or verify copyright rights. If factual claims matter, keep a source/fact note; do not imply research that was not performed.
2. Create a production plan before media: for each beat, identify core meaning, emotion, visual metaphor, three-to-six object groups, palette, composition, assembly order, and optional sound treatment. Default to 16:9 and tactile paper SFX only when the selected video route natively supports it; do not add music, voiceover, narration, or subtitles without an explicit request and a supported route.
3. Continue without a client-side confirmation. Generate one final still per approved beat using GPT Image 2 Medium/2K through the native WeShop route. The still must visibly use a bold color field, black-and-white halftone cut-outs, restrained color-card accents, warm cream keylines, soft paper shadows, subtle fibers, torn edges, layered depth, and no accidental text or logos.
4. Inspect the stills and continue without a client-side confirmation. If any beat is too literal, busy, brown/distressed, flat, or typographic, revise its still before video generation.
5. For each accepted still, hand off one atomic shot to `$generate-video`: start on a matching color field; slide, pop, lightly bounce, press flat, pause, and lock distinct paper groups into the approved final composition. Keep camera motion restrained, preserve ratio, and forbid scene cuts, smooth digital layer motion, morphing, new objects, readable copy, and unwanted speech/music.
6. Persist one durable `operationKey` for each still or clip before submission; poll its receipt and surface the API outcome as returned. Use `$combine-videos` only if the user requests an ordered multi-clip delivery from accepted clips.
7. Review every final frame against the approved still and inspect the complete sequence for metaphor clarity, material continuity, object readability, palette, unwanted text/audio, ratio, duration, and clip order. Repair the originating still, shot, or assembly step only.


## User-facing output

- Media type: One approved production plan, one still per approved beat, and requested MP4 clips or assembly
- Default quantity: One to three beats unless the user specifies another count
- Content per artifact: Visual metaphor, approved end-state, cut-paper motion contract, and QA result
- Default layout: 16:9; user-requested ratio overrides
- Model policy: GPT Image 2 Medium/2K for stills; current catalog-selected video route for clips; no standalone audio claim
- Downstream use: Editorial explainers, social B-roll, and approved multi-clip assembly
