---
name: generate-video
description: Generate video via fal.ai — MiniMax H3 Max, Kling 4 and Seedance 2.5 (text-to-video, image-to-video, start+end frame transitions, multi-keyframe clips, seamless loops) and Veo 3.1 (extending an existing clip). Use whenever the user asks for a video background, a looping/seamless hero animation, a transition or morph between images, or media for a scroll- or cursor-driven page (scroll sequence, exploded product view, a character whose head or eyes follow the cursor, a camera journey through scenes), or to extend an existing clip — even if they don't name a model, and also when they do ("with Kling", "Seedance").
compatibility: Claude Code with Bun 1.4 or later and a fal.ai API key in FAL_KEY.
---

# generate-video

Wraps fal.ai video models behind one CLI: `${CLAUDE_SKILL_DIR}/scripts/generate-video.ts`.
Requires a fal.ai key in `FAL_KEY` (same key as the `generate-image` skill) — if it's missing the
script exits with a clear error; ask the user to export it in their shell, never to paste the key into the chat.

```
bun ${CLAUDE_SKILL_DIR}/scripts/generate-video.ts loop --prompt "..." --source ./hero.png --output ./out.mp4
```

If the shell says `bun` isn't found, Bun isn't installed. Stop and ask the user to install it from
https://bun.com/docs/installation and restart Claude Code. Don't replace the script with other tools or
code of your own: the checks it runs before a paid call and on the result would be lost.

The script prints the final path and file size plus a temporary `Result URL`, which is exactly what
`extend --source` needs. Unknown models, durations, resolutions and aspect ratios fail before anything
is sent. A clip takes about 30 s–3 min, longer when the queue is busy; the call blocks until done
and prints a line when the job starts generating. That outlasts Bash's default 2-minute timeout, so
run the command in the background or with a 10-minute timeout. If it is cut off anyway, use the
printed `resume` command — rerunning the original pays for the clip again.

`--source`/`--from`/`--to` accept a local file path or a public URL; local images are inlined as a
data URI. With `--model kling-4`, frames must be at least 300×300 px with an aspect ratio between 2:5
and 5:2 — checked before the paid call for local files, not for URLs.

**A paid result is never lost.** As soon as fal.ai accepts a job the script prints its request ID and a ready `resume --model … --request-id … --output …` command on stderr. If the download fails or the run is interrupted, run that command — it fetches the already-paid result. Don't rerun the original command: that generates (and bills) again.

## Model choice

**If the user names a model, use it.** Otherwise:

| Model | Cost | Pick it for |
|---|---|---|
| `h3-max` (default) | 1080p ~\$0.16/s · 768p ~\$0.08/s · 480p ~\$0.05/s | hero backgrounds, loops, product motion, transitions. Top-ranked image-to-video model (no-audio category). Always adds a quiet generated soundtrack (no switch to turn it off), so drop it for the page with `process-video` (`encode --no-audio`, `loop-seam` or `strip-audio`) |
| `kling-4` | 1080p ~\$0.24/s · 720p ~\$0.16/s | `keyframes` (the only model here that takes frames between the first and last), clips longer than 15 s (up to 30 s), or when the user asks for Kling. Silent |
| `seedance-2.5` | 1080p ~\$1.16/s · 720p ~\$0.47/s · 480p ~\$0.22/s | long continuous camera moves through several spaces without a cut (4–30 s), or when the user asks for Seedance. Ranked first for image-to-video with audio, but 3–7× the price of the others: say the estimate before using it. Sent with its soundtrack turned off |
| Veo 3.1 (`extend` only) | ~\$0.10–0.20/s | continuing an existing clip |

`--resolution` defaults to `1080p` (`720p` for Seedance). Draft at `480p`/`768p`/`720p` while the
motion is still being worked out, then render the chosen prompt at full resolution: that is a new
generation, not an upscale of the draft, so check it again. The WebM delivered on the page is usually
downscaled anyway.

## Writing motion prompts

The model already sees the image — describe **motion**, not the scene. For every thing that should
move, say what it is, where the motion comes from, how much and when ("from 2 s to 3 s"). Make only
the camera static ("Static shot, locked-off camera"): models move as little as the prompt allows, and
"subtle", "slowly" or "everything else stays still" bring back a nearly frozen clip. Describe an
effect in plain terms instead of one loaded word — "flicker" tends to mean switching off and on, no
matter what qualifier sits next to it. For loops, choose motion that can return to its start.

Models like to cut, ease and reframe. When the clip must be one take, say so up front ("one continuous
shot, no cuts, no montage, no camera reset"). When the page will scrub it by scroll or cursor, ask for
constant speed with no easing, otherwise most of the change lands in the middle frames. Time-code the
beats of anything longer than a few seconds ("0–3 s: …, 3–6 s: …"), and give each moving part its
path, not just its destination. When the page picks frames by position, anything incidental the
model adds (a blink, a twitch of the tail, a light change) lands at a fixed spot on the screen, so
rule it out by name ("eyes stay open, no blinking").

**When the user asks to change a detail** of a clip ("the steam should come out of the pipe, and
less of it", "the light should tremble, not blink"): keep the previous prompt, rewrite only the lines
about that detail, and regenerate. If the detail needs something the source image doesn't show (a
part that should move but isn't drawn), add it to the image first with `generate-image edit` —
otherwise the model invents it mid-clip.

**Check the clip before showing it** — two or three frames are not enough. Use the process-video
skill: `sheet` puts evenly spaced frames in one image (`--crop` to the area the user cares about),
and `motion` prints how much each frame changes, second by second. That timeline shows a frozen clip,
where the motion bunches up instead of running evenly, and single-frame spikes such as cuts. Rewrite
the prompt with bigger, named motion if it barely moves. Tell the user what you checked and what
still doesn't match.

Keep the raw clip as fal.ai returned it (it is paid for: re-encoding it later costs nothing,
generating it again does), along with sheets and draft cuts, in the project's work folder:
`media-generation/` inside the project's own scratch folder if it has one (`.scratch/`, `tmp/`),
otherwise `.media-generation/` holding a `.gitignore` that contains `*`, so git never sees it. Never
`/tmp` or a folder next to the project. Only the files the user asked for go in the project itself;
tell the user where the raw originals are.

## Scroll- and cursor-driven effects

Pages where the scroll position or the cursor drives the picture (a product that comes apart as you
scroll, a camera that travels through rooms, a head or eyes that follow the cursor) play an ordinary
clip frame by frame. Plan the media backwards from the page:

1. **Stills first.** Make every state the clip must pass through as an image: the first with
   `generate-image`, the others as `generate-image edit` of it, listing what must not change (framing,
   light, background, everything but the moving part). Consistent stills are what make the video
   join up; an edit asked only "look left" may turn a face into a profile.
2. **One command per number of states.** One still plus described motion: `animate`. Two: `transition`.
   Three or more in order (left / centre / right for a head that follows the cursor; assembled /
   halfway / exploded for a product): `keyframes`. A journey through several scenes: one `transition`
   per leg, each starting on the previous leg's last still, then `process-video concat --chained`.
3. **Prompt for scrubbing:** static camera unless the camera move is the effect, one continuous shot,
   constant speed, no incidental actions. Check the result with `process-video motion`: an even
   timeline means even scrubbing.
4. **Prepare for the page with `process-video`:** `frames` exports the image sequence a `<canvas>`
   draws by scroll or cursor position (the usual approach), `encode --keyframe-interval` makes a
   scrubbed `<video>` seek smoothly, and `reverse --pingpong` turns a one-way move into an idle loop.

## generate — text to video

```
generate-video.ts generate --prompt "<description>" --output <path>.mp4
  [--model h3-max|kling-4|seedance-2.5] [--duration N] [--resolution …] [--aspect-ratio 16:9|9:16|1:1|21:9|…]
```

Pure text, no starting image. Prefer `animate` when a source image exists or can be generated first
with `generate-image` — the subject and composition stay steadier. Aspect ratios: H3 Max and
Seedance 2.5 `21:9 16:9 4:3 1:1 3:4 9:16`, Kling 4 `16:9 9:16 1:1 21:9`.

## animate — image to video (single start frame)

```
generate-video.ts animate --prompt "<motion>" --source <path-or-url> --output <path>.mp4
  [--model h3-max|kling-4|seedance-2.5] [--duration N] [--resolution …]
```

The general "turn this hero image into a video background" command.

## transition — morph between two different images

```
generate-video.ts transition --prompt "<how it transforms>" --from <path-or-url> --to <path-or-url> --output <path>.mp4
  [--model h3-max|kling-4|seedance-2.5] [--duration N] [--resolution …]
```

`--from` anchors the first frame and `--to` the last. For scene changes, before/after reveals and
section-to-section scroll transitions.

## keyframes — pass through three or more stills in order

```
generate-video.ts keyframes --prompt "<how it moves between them>" --frame <first> --frame <middle> [--frame …] --frame <last>
  --output <path>.mp4 [--model kling-4] [--duration N] [--resolution 720p|1080p]
```

Up to 10 frames with Kling 4, spread evenly over the clip. The clip passes through each still, which
keeps a long or multi-stage move on track where a single `transition` would improvise the middle.

## loop — seamless start=end animation

```
generate-video.ts loop --prompt "<continuous motion>" --source <path-or-url> --output <path>.mp4
  [--model h3-max|kling-4|seedance-2.5] [--duration N] [--resolution …]
```

The same image is both the first and the last frame, so the clip comes back close to where it
started. Close isn't seamless: run the result through `process-video loop-seam`, which blends the tail
into the head so `<video loop>` wraps without a jump. This is the command for hero backgrounds;
follow the prompt rules above and check the result.

Durations: H3 Max 1–15 s, Kling 4 3–30 s, Seedance 2.5 4–30 s (default 5).

## extend — continue an existing clip

```
generate-video.ts extend --prompt "<what happens next>" --source <public-video-url> --output <path>.mp4
  [--duration 7] [--resolution 720p] [--audio]
```

Veo 3.1 extend only offers a 7-second continuation at 720p; other values are rejected locally.
`--source` must be a public `https://` URL (Veo fetches it server-side) — the `Result URL` printed by
another `generate-video` command works. The input must be 720p or 1080p, 16:9 or 9:16, 3–10 s long.

## After the download — make it shippable

The MP4 is the *master*, not the deliverable. Run it through the `process-video` skill: a poster
frame for `<video poster>`, a WebM/VP9 re-encode (usually 30–50% smaller), downscaled to the display
width. All local and free — don't re-generate a clip just to fix its file size.

## Cost awareness

Video is priced per second of output: a 10 s clip costs twice a 5 s one. Before a batch (more than one
clip, or anything above ~\$1), state the estimate (`seconds × price per second` from the table) to the
user. Default to the shortest duration that shows the motion (5 s).

## Error handling

| Error | Cause | Resolution |
|-------|-------|-----------|
| `FAL_KEY is not set` | Not configured | Ask the user to export it in their shell |
| `extend requires --source to be a public https URL` | Local file passed to `extend` | Pass the `Result URL` a previous command printed, or upload the clip somewhere public |
| `Failed to download …` | CDN hiccup after a successful generation | Run the printed `resume` command — never regenerate |
| The clip barely moves | Prompt allowed stillness | Rewrite with named, sized, timed motion (see above) and check with `process-video motion` |
