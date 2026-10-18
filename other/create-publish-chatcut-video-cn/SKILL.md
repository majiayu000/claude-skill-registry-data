---
name: create-publish-chatcut-video-cn
description: Create or continue editable Chinese short-form videos in ChatCut, completing script shaping, natural TTS voiceover, Motion Graphics, timeline assembly, subtitles, music, visual/audio QA, export, local delivery, and authorized publishing to Douyin and Xiaohongshu. Use when the user asks to 做视频, 继续现有 ChatCut 项目, 把口播做成 9:16 课件式 MG 视频, 导出成片, or 做完后发到抖音和小红书.
---

# Create and publish a ChatCut video

Deliver up to three linked results, according to the current request:

1. An editable ChatCut project and timeline.
2. A verified local MP4.
3. Authorized Douyin and Xiaohongshu posts with confirmed status.

Treat video production as the main job. Treat publishing as a separately authorized final delivery phase.

## Load the applicable operating skills

Read and follow the current installed skill for each phase instead of copying stale tool parameters:

- Always load `chatcut:chatcut-plugin-basics` for project and timeline work.
- Load `chatcut:create-motion-graphics` for hand-authored course-style MG scenes.
- Load `chatcut:voice` before generating or replacing narration.
- Load `chatcut:transcription` for captions and transcript readiness.
- Load `chatcut:verification` before claiming the edit is correct.
- Load `chatcut:export` for rendering and local delivery.
- Load `chrome:control-chrome` before publishing through logged-in web sessions.
- Load `chatcut:known-errors` if a ChatCut tool fails or returns an unexpected shape.

Use the current MCP and browser schemas as the runtime contract. Do not guess hidden IDs, routes, or UI selectors.

## Decide the starting point

1. If the user names an existing project or supplies an editor URL, target that exact project. Do not create another project.
2. Read both project assets and the current timeline before spending credits or editing.
3. Reuse ready assets, completed MG scenes, approved scripts, transcripts, voiceovers, music, and exports when they match the request.
4. Treat pending generation as work in progress. Track it before submitting a duplicate job.
5. If only a finished MP4 and publishing are requested, skip ChatCut editing.
6. If the user explicitly asks for end-to-end execution or says not to reconfirm, proceed through reversible production choices using the saved defaults. Ask only when a missing choice materially changes content, cost, account, or external state.

Read [references/production-defaults.md](references/production-defaults.md) before writing the script, choosing a voice, or designing the timeline.

## Produce the video

### 1. Lock the spoken structure

- Start from the user's approved script or the latest clearly approved project script.
- Compress to the requested duration before generating voice or batch MG scenes.
- Prefer one idea per sentence and one visual job per scene.
- Map the script into a hook, diagnosis, explanation, method, practical example or tool, action step, and ending card. Adapt the scene count to the content.
- Do not imply approval of a rewritten script when the user only asked for analysis or review.

### 2. Build or reuse the narration

- Use the saved concrete voice preference in `production-defaults.md` unless the current request overrides it.
- Search the project assets before generating. Never use an old voice asset merely because its duration fits.
- Generate only after the script is final enough to avoid credit waste.
- Place narration on A1 and treat it as the timing spine for all visuals, captions, and music.
- Keep speech conversational and restrained; avoid announcer delivery.

### 3. Create the visual system

- Use one coherent visual language across the video.
- If the user has not chosen a direction and has not waived alignment, follow the representative-MG gate in `chatcut:create-motion-graphics` before batching.
- When the user has explicitly asked to proceed directly, use the saved course-style MG direction and verify representative settled frames early.
- Make each scene explain something visually through diagrams, comparisons, funnels, tables, checklists, or conversation examples. Do not turn every page into text inside a card.
- Keep all content editable as ChatCut MG assets and timeline items. Do not flatten the edit locally.

### 4. Assemble the timeline

- Create or use a 9:16 timeline with the requested resolution and fps.
- Place scenes in spoken semantic order and cover the full narration without black gaps.
- Put narration on A1 and background music on A2. Keep music clearly below speech and fade it out over the final second.
- Generate sentence-level Chinese captions after narration timing is stable.
- Keep captions in the bottom safe zone and check they do not collide with MG content.

## Verify before export

Use both structural and visual evidence:

1. Re-read the latest timeline and assets.
2. Inspect composed frames at the opening, each major scene, text-dense states, transitions, and the ending card.
3. Check for black frames, uncovered narration, gaps, overlaps, clipped text, broken wrapping, overflow, subtitle obstruction, inconsistent styles, and premature scene endings.
4. Confirm the required narration asset is on A1 and rejected or superseded narration is not used.
5. Audition the voice when the host supports playback. Do not claim that it sounds natural from metadata alone.
6. Check the mix: speech remains intelligible throughout, music is subordinate, and the ending fades cleanly.

Fix failures in the editable project, then re-verify. A successful mutation response is not proof of a correct video.

## Export and deliver locally

1. Use ChatCut's export workflow, then track the durable render to completion.
2. Reuse a fresh matching completed download instead of downloading twice. Never treat an old same-named file as the current render.
3. Copy or move the completed MP4 to the user-requested destination without overwriting an existing unrelated file. If no destination was given, use a descriptive filename in `~/Downloads`.
4. Run the bundled preflight before publishing:

```bash
python3 scripts/check_video.py "/absolute/path/to/video.mp4"
```

Override duration or dimensions only when the current request requires another format. Read the script output and fix any failure before publishing.

## Publish only after the video passes

Read [references/platform-publishing.md](references/platform-publishing.md) before opening either publishing page.

1. Publish only when the current user request explicitly includes publishing or invokes the full create-and-publish workflow.
2. Confirm the visible platform account before upload. If the user named an expected account, require an exact match.
3. Search the platform's work or note manager for the exact title or a distinctive title phrase before uploading. Stop if the same post already exists unless the user explicitly wants a duplicate.
4. Adapt the title and body per platform; do not paste a long Douyin title into Xiaohongshu unchanged.
5. Default to public and immediate publishing only when publishing was explicitly authorized. Do not enable cross-posting, product linking, events, groups, location, or commercial declarations unless requested or required by the content.
6. If login is missing, leave a handoff page and ask the user to sign in. If a CAPTCHA appears, ask the user to handle it.
7. Verify Douyin in works management and verify Xiaohongshu from the success page or note management. Preserve the final result page as the browser deliverable.

## Completion contract

Report completion only when all requested stages have evidence:

- ChatCut project and timeline are editable and verified.
- The MP4 exists at the requested path and passes preflight.
- Each requested platform reports success or a precise review or pending state.
- The final summary names the output path, duration, resolution, visible accounts, titles, and platform statuses.

If a stage is blocked, report the exact blocked stage and preserve completed upstream work. Do not restart generation, re-export, or re-upload merely because a downstream site is unavailable.
