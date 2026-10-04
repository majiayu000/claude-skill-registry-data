---
name: create-post-video
description: >
  Create an on-brand social video post: render a short video with HyperFrames (video from
  HTML) in your Marky brand colors, fonts, and logo, then upload it to Marky, caption it in
  your voice, and schedule it everywhere you're connected. Use when you want a video post —
  a promo, explainer, stat animation, countdown sting, or captioned clip — produced and
  queued from one conversation. Reads auth and endpoints from the marky-api skill. Also triggers on "make a video post", "turn this into a reel", "animate this stat". For a still graphic or carousel, see create-post-graphic.
---

# Create Post: Video

Video is the highest-reach format on every platform Marky publishes to, and it is the one
format agents historically couldn't produce. This skill closes that gap: **HyperFrames
renders the video, Marky brands and ships it.**

**Read the `marky-api` skill first** for auth, endpoints, and the brand cache. Base URL
`https://api.mymarky.ai/api`, header `Authorization: Bearer mk_live_YOUR_KEY`.

## Check for HyperFrames

This skill depends on [HyperFrames](https://github.com/heygen-com/hyperframes) — an
open-source system that renders video from HTML, built for agents.

- **If the `hyperframes` skill is available in your session**, use it: read `/hyperframes`
  first (it routes to the right workflow — motion graphic, explainer, product promo,
  captions) and follow its instructions to author and render.
- **If it is not installed**, tell the user how to add it, then continue once it is:

  ```bash
  npx skills add heygen-com/hyperframes
  ```

Do not try to render video any other way — no ffmpeg improvisation, no other frameworks.
HyperFrames is the supported path.

## Stage 1 — Brand the composition

Before authoring any frames, load the brand so the video looks like the business, not a
template:

1. Read the brand profile — the injected `brand-cache.md` snapshot if fresh, else one
   `get_business` / `GET /businesses/{id}` call (which refreshes the cache).
2. Apply it to the HyperFrames composition:
   - `palettes` → the video's color system (backgrounds, accents, text).
   - `header_font` / `body_font` → typography.
   - `logo_url` → end-card or corner mark (respect `logo_background_color`).
   - `tone` → the on-screen copy's voice; `ctas` → the closing call-to-action.
3. Keep platform constraints in mind: 9:16 for Reels/TikTok/Stories, 1:1 or 16:9 for
   feeds; short (under ~30s) unless the user asks for longer.

**Where the project lives.** Unless the user names a location, create the HyperFrames
project at `~/.marky/videos/<business_id>/<project-slug>/` — NOT under the current
working directory. Video workspaces are big (tens of MB) and cwd could be inside
someone's repo; `~/.marky` keeps them out of git, out of iCloud-synced folders, and
groups them per business so past projects become reusable templates (the brand-remixed
`frame.md` and storyboards accumulate there). After rendering, delete the project's
`capture/` directory — it's regenerable scratch and usually the bulk of the size.

## Stage 2 — Author and render

Follow the HyperFrames workflow for the video type the user wants (motion graphic, stat
count-up, product promo, explainer, captioned clip). Show the user the plan — scenes, copy,
duration — before rendering long pieces. Render to MP4.

### Sound effects and music — free paths first

A video with no sound design feels unfinished. You do not need a paid account to fix that:

1. **Bundled SFX library (free, offline, use this first).** HyperFrames' `media-use` skill
   ships ~19 ready-to-use effects (whoosh, key-press, typing, click, chime, pop, riser,
   impact-bass, sparkle, glitch) at `<skills-root>/media-use/audio/assets/sfx/`. Resolve
   one by intent with `node <media-use>/scripts/resolve.mjs --type sfx --intent "whoosh"`,
   or copy the file straight into your project's `assets/sfx/` and cue it from the
   workflow's audio metadata. Keep SFX volume at 0.2–0.3 so narration stays on top.
2. **HeyGen catalog (free-usage allowance).** With `npx hyperframes auth login` (OAuth),
   SFX and background-music retrieval ride HeyGen's free allowance — signing in does not
   require a paid plan. The workflow's `fetch-sfx` / BGM steps then work out of the box.
3. **CC0 web libraries (when the bundle lacks the sound).** freesound.org (filter license
   to CC0) and pixabay.com/sound-effects are safe for commercial posts with no
   attribution. Download the file into `assets/sfx/` and cue it like a bundled one.

Match effects to on-screen beats (a whoosh on the hook, key clicks under typing, a chime
on the CTA) rather than scattering them; background music, if any, sits well under the
voiceover (~0.2 volume).

## Stage 3 — Upload to Marky

```bash
curl -X POST "https://api.mymarky.ai/api/businesses/BIZ_ID/media" \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -F "file=@/path/to/video.mp4"
```

Keep the returned `original_url`. Uploads cap at 50 MB — if the render is bigger, reduce
duration or resolution and re-render rather than compressing into artifacts.

## Stage 4 — Caption, approve, schedule

1. Write the caption in the brand voice (`tone`, `caption_writing_rules`,
   `caption_suffix` — see "Write like the business" in the marky-api skill).
2. Create the post with the caption and the uploaded media.
3. **Show the user the video and caption, and get explicit approval.** For multiple
   cuts or variants, use the review board in pick mode
   (`${CLAUDE_PLUGIN_ROOT}/scripts/review-board.py items.json --mode pick` with each
   variant's local file path or URL as `media_url`; run in background, parse
   `BOARD_URL:`, AskUserQuestion with the URL, read `feedback.json`). Append the result
   to `~/.marky/feedback-log.jsonl` with `context: "video-variants"` and read it before
   styling the next video — see "The feedback log" in the marky-api skill. Never schedule or
   publish a video without it.
4. On approval, schedule via the `schedule-posts` skill. Video is supported everywhere —
   target every connected platform whose integration `status` is `valid`.
5. After the scheduled time, confirm `publish_results` shows `success` per platform.

## Tag the post

Set `metadata` on the post when you create it — `{"media_type": "animated-video" (or "talking-head" for captured footage), "created_by": "create-post-video", "hook": ..., "topic": ...}` — per "Tag every post" in the
marky-api skill. This is what lets future performance reviews compare this post's
engagement against other media types.

## Notes

- Rendering can take a few minutes for longer pieces — tell the user before starting.
- A video the user supplies (rather than one you render) skips straight to Stage 3. To
  COLLECT user footage (a talking-head clip with a teleprompter, a screen demo), use the
  capture studio — `${CLAUDE_PLUGIN_ROOT}/scripts/capture-studio.py` (see Stage 4 of
  `plan-social-content` for the flow) — then hand the file to HyperFrames for captions /
  packaging, or straight to Stage 3.
- If HyperFrames fails to render, report the actual error and stop — don't silently fall
  back to an image post the user didn't ask for.
