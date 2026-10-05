---
name: voiced-caption-video
description: Create complete short videos or animation videos with planned visuals, natural Mandarin voiceover, burned-in Chinese subtitles/captions, music/effects when appropriate, and final MP4 validation. Use when the user asks to make, improve, or automate a 视频, 动画视频, 教育视频, 宣传片, 图片视频, 剪影视频, HyperFrames video, or any video that needs 配音 and 字幕.
---

# Voiced Caption Video

## Core Goal

Produce a finished MP4, not just a concept. The minimum complete delivery is:

- Visual composition or generated video/animation.
- Natural Mandarin narration or other requested voice.
- Burned-in captions/subtitles that are readable on every scene.
- Timing that matches narration and avoids empty/black gaps.
- Verification with render checks, stream checks, and frame review.

Use the best available route for the task. Photos are only one mode, not a requirement.

## Route Selection

- Use **HyperFrames HTML animation** when the video needs designed pages, kinetic text, data cards, photo layouts, training explainers, or reliable caption placement.
- Use **photo/story montage** when the user provides real photos and wants a documentary, 宣传, 纪实, or 剪影-like video.
- Use **AI video generation tools/plugins** when the user wants moving scenes that are hard to build from HTML alone. Still add voice/subtitles and QA after generation.
- Use **hybrid production** when quality matters: generated stills or photos as visual base, HyperFrames for layout/motion/captions, and ffmpeg for final assembly.

When in doubt, choose the most controllable route first: storyboard -> assets -> HyperFrames composition -> TTS -> subtitles -> render -> QA.

## Workflow

1. Restate the target in one line: topic, audience, style, length, output path, and must-have elements.
2. Create a clean project under a user-approved project folder, unless the user gives an exact destination. Prefer the bundled scaffold helper for standard folders and starter files.
3. For safety education or rule-based training, audit the source content before storyboarding. Keep the rule meaning intact, do not blindly copy long clauses, and do not invent domain terms.
4. Draft a simple storyboard before building: 5-8 scenes for 30-60 seconds, each with one visual purpose and one narration beat. If the material is too long, split it into multiple videos and finish the first one well before starting the second.
5. Prepare assets from user photos, generated images, Iconfont SVG icons, simple SVG/HTML shapes, or video clips depending on the route.
6. Write or polish narration into short spoken Chinese. Avoid long paragraph dumps on screen.
7. Generate TTS audio when possible and record exact duration with `ffprobe`.
8. Build captions as visible HTML text or burned-in subtitles. Do not rely only on sidecar subtitle files.
9. Compose and render with HyperFrames/ffmpeg or the selected video tool.
10. Run validation: layout inspect, MP4 stream check, and extracted frame review. If the user reports blocking, clutter, wrong labels, ugly icons, blank starts, or any specific visual issue, extract the relevant frames and inspect them one by one before calling the repair done.
11. Final response should include the absolute MP4 path and mention any limitations honestly.

## Safety Education Animation Requirements

- Content accuracy comes before visual polish. For railway, safety, medical, legal, financial, or other rule-heavy topics, first map each video to the exact source clauses it covers and what it leaves out.
- Do not alter the meaning of a safety rule to make a scene easier to draw. Avoid made-up workplace terms; use domain terms only when they match the user's source or confirmed context.
- If the user says the content is wrong, too simple, or too crude, stop and re-audit the script before adding more effects. Do not hide content errors under busier animation.
- Safety education should show warning value, not only slogans. Include plausible consequence chains where appropriate, such as injury, work interruption, investigation, accountability, or operational disruption. Avoid gore or sensational accident imagery.
- Risk-chain scenes must land on the safety consequence that teaches the lesson. Do not make administrative after-effects the final emphasis unless the user's source explicitly says so.
- Prohibition or risk pages need an explicit teaching motion tied to the rule, such as flashing red crosses, risk bars lighting in sequence, gauge needles moving, dotted paths flowing, breakpoints blinking, or conclusion highlights.
- Page-specific labels and UI chips must belong to the current rule only. Do not carry unrelated labels across scenes.
- Every safety education delivery must pass checks for content accuracy, correct terminology, visual clarity, asset-selection records, animation relevance, readable captions, and audio/visual sync.

## Visual Standards

- Start with content immediately. No initial black screen, no empty first seconds. At 0 seconds, or within 0.2 seconds of any scene start, there must already be a clear subject, title, or core image.
- Use strong readable caption containers. Avoid white text directly over bright or busy backgrounds.
- Keep motion purposeful: slow push-in, parallax, card entrance, spotlight, scene wipes. Avoid random bouncing, spinning, or gimmicks unless the user asks.
- For HTML/HyperFrames animation, first decide which scene elements would benefit from SVG assets, then search Iconfont broadly for matching visual metaphors. Do not limit the search to a fixed icon list, and do not accept the first result blindly.
- Treat Iconfont results as design candidates: download several options for several keywords, preview them side by side, choose the best-looking and most style-consistent SVG, and skip SVGs that look crude, generic, or mismatched.
- Recolor Iconfont SVGs to fit the scene palette before final render. Avoid raw black, dirty gray, or abrupt colors that fight the layout.
- Keep `ASSET_SELECTION.md` in the project whenever Iconfont assets are used. Record searched categories/keywords, shortlisted SVGs, rejected rough options, chosen files, and why each chosen asset fits the scene.
- For safety/training videos, keep the tone serious enough: clear consequences, realistic visual cues, and readable instructional text.
- For promo/documentary videos, make the visuals warm and polished but not childish.
- For animation, characters and objects should be recognizable. If Q-style makes things too abstract, use semi-cartoon or clean illustrated realism.
- Educational animation should be visually rich and concrete. Use multiple scene objects, diagrams, warning markers, comparison panels, and consequence chains rather than empty cards with one icon.
- Leave deliberate composition space for people, cards, lines, panels, and titles. Characters must not cover text, cards must not crush the subject, diagrams need readable clearance, and titles need safe margins from screen edges and moving elements.

## Repair And Versioning Rules

- Protect versions during repair. Copy `vN` to `vN+1` before substantial changes, keep already reviewed or discussed versions intact, and never overwrite a version that the user may need to compare.
- Keep final output and QA frame folders obvious. Use clear paths such as `renders/v4/final.mp4` and `renders/v4/qa_frames/`, or an equivalent project convention, and report those exact paths at handoff.
- A successful export is not enough after visual criticism. When the user names a blocked, cluttered, ugly, or wrong frame, extract frames around that timecode plus scene starts and inspect them visually.
- During repair, validate the original complaint directly. Confirm that the offending icon, label, overlap, blank start, or composition issue is gone in the new frames before doing broader stream checks.

## Audio And Subtitle Standards

- Prefer natural Mandarin neural voices when available.
- Choose voice by tone: serious safety/training content needs a steadier voice; promo/documentary content can be warmer; explainers can be lighter and more conversational.
- Good Mandarin defaults include `zh-CN-YunyangNeural` for formal narration, `zh-CN-YunjianNeural` for serious safety/training content, `zh-CN-XiaoxiaoNeural` for warm promo/documentary content, and `zh-CN-YunxiNeural` for relaxed explainers.
- Avoid zombie-like narration by rewriting formal source text into short spoken lines before TTS.
- Add pauses through punctuation and line breaks, and keep the speech rate modest unless the user wants faster pacing.
- Include voiceover on the opening page if there is an opening page.
- Match subtitle timing to narration beats; keep each caption short.
- Burn subtitles/captions into the rendered picture unless the user explicitly wants external subtitles.
- If background music is added, keep it low enough that narration remains clear.

## HyperFrames Notes

Use the HyperFrames workflow when available. A safe pattern:

- Keep HTML as source of truth.
- Set `data-composition-id`, `data-duration`, `data-width="1920"`, and `data-height="1080"`.
- Use a deterministic Chinese-capable font stack such as `"Noto Sans SC", sans-serif`.
- Mark intentionally oversized blurred/decorative elements with `data-layout-allow-overflow`.
- Keep `#root` as the main clipping boundary. If scene clipping creates false layout errors, use `.scene { overflow: visible; }`.
- Avoid dynamic selector template literals in timeline code. Prefer simple ID/class lookups.

For detailed commands and pitfalls, read `references/workflow.md` when present.

## Bundled Helpers

Use the scaffold helper to start repeatable projects:

```powershell
python "skills/voiced-caption-video/scripts/scaffold_project.py" "project-name" --root "<PROJECTS_ROOT>" --title "Video Title"
```

It creates `assets/original`, `assets/processed`, `audio`, `renders`, starter `DESIGN.md`, starter `narration.txt`, and a HyperFrames `index.html` template.

Use the Iconfont SVG search helper when the video needs clean icon assets. If a site requires a session token or cookie, pass it through a local environment variable or command-line argument and never commit it:

```powershell
python "skills/voiced-caption-video/scripts/search_iconfont_svg.py" "keyword" --out "<PROJECT_FOLDER>/assets/iconfont" --all
```

Review downloaded SVGs before use. Never use an ugly result just because it downloaded successfully.

## Validation Checklist

- For safety education, verify the script against the source rules: no missing core point, no invented rule, no softened prohibition, and no domain term used incorrectly.
- Check whether the video has enough concrete visual teaching material: recognizable people, scene objects, risk cues, wrong/correct contrasts, and consequence displays.
- Confirm `ASSET_SELECTION.md` exists when Iconfont was used, and that it records multi-keyword search, candidate comparison, final picks, and rejection of crude/mismatched icons.
- Review whether animation improves understanding: scene changes, highlights, risk chains, and consequence reveals should align with narration beats.
- Check audio/visual sync after final TTS, especially when using segmented narration. Rebuild scene timing from actual audio durations instead of relying on old fixed timings.
- `hyperframes inspect` passes when using HyperFrames.
- `ffprobe` confirms a video stream and an audio stream.
- Frames near the beginning, middle, and end were extracted and inspected.
- Each scene's first frame, or a frame within the first 0.2 seconds, was checked for a clear subject, title, or core image.
- If repairing a user-reported problem, QA frames for the exact problem area were reviewed directly.
- There is no black screen, blank early gap, sideways media, unreadable captions, or missing opening narration.
- Captions are burned into the video unless external subtitles were explicitly requested.
- Source files, narration text, audio, subtitles, renders, and preview frames are saved in the project folder.
