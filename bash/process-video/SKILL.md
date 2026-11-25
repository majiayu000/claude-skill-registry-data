---
name: process-video
description: Process a local video file with ffmpeg — extract a poster frame for <video poster>, re-encode to WebM/VP9 or AV1 for smaller web delivery, compress an oversized clip, trim to the segment that matters, strip an unwanted audio track, make a looping clip wrap without a visible jump, export a frame sequence for scroll- or cursor-driven animation, reverse or ping-pong a clip, join clips, inspect duration/codec/size, or check a clip with a contact sheet and a motion timeline. Runs entirely offline, no fal.ai credit spent. Use whenever the user wants to convert, compress, shrink, trim, cut, mute, or get info about a video they already have — including making a generated generate-video clip actually shippable on a web page, fixing a loop that jumps or stutters where it repeats, and preparing a clip for a page that plays it by scroll position or cursor ("scroll animation from this video", "Apple-style scroll sequence").
compatibility: Claude Code with Bun 1.4 or later and ffmpeg/ffprobe on PATH. Offline; no API key.
---

# process-video

Wraps ffmpeg behind one CLI: `${CLAUDE_SKILL_DIR}/scripts/process-video.ts`.
Purely local — no network, no API key. Requires `ffmpeg` (and `ffprobe`, which ships with it) on
PATH; if it's missing the script exits with per-OS install instructions — relay them to the user
instead of hunting for a workaround.

```
bun ${CLAUDE_SKILL_DIR}/scripts/process-video.ts <command> ...
```

If the shell says `bun` isn't found, Bun isn't installed. Stop and ask the user to install it from
https://bun.com/docs/installation and restart Claude Code. Don't replace the script with other tools or
code of your own: the checks it runs before a paid call and on the result would be lost.

This is the post-production half of the video pipeline: `generate-video` generates a clip, `process-video`
makes it shippable. A generated MP4 dropped straight into a page is usually 2–4x larger than the
same clip re-encoded, has no poster frame, and may carry an audio track nobody asked for.

Every command renders to a temporary file and only replaces `--output` once the result is checked
to contain video frames — a poster time or trim range past the end of the clip fails with the
source duration in the message instead of reporting an empty file as saved. Missing output
directories are created.

## info — inspect before deciding

```
process-video.ts info --source <path>
```

Prints container, duration, video codec/resolution/fps, audio codec (or `none`), and file size.
Run it first when you don't know what you're holding — e.g. before picking a `--crf` or checking
whether there's an audio track to strip.

## poster — extract a frame for `<video poster="…">`

```
process-video.ts poster --source <video> --output <path>.jpg|.png|.webp [--time <seconds>]
```

Grabs one frame (default: the first). A background video without a poster shows a blank box until
the first frame decodes — always pair a hero/background video with a poster image. Pick `--time`
past any initial fade-in (`0.5`–`1` is usually enough); fractional seconds are fine.

## encode — re-encode for web delivery

```
process-video.ts encode --source <video> --output <path>.webm|.mp4
  [--codec vp9|av1|h264] [--crf N] [--width N] [--fps N] [--keyframe-interval N] [--no-audio]
```

The codec defaults from the output extension: `.webm` → VP9, `.mp4` → H.264. VP9 in `.webm` is
the go-to for background videos — typically 30–50% smaller than the delivered MP4 at the same
visual quality, supported by every current browser. AV1 is smaller still but encodes slowly and
needs `--codec av1` explicitly.

`--crf` is quality (lower = better/larger; sensible defaults per codec are built in: VP9 32,
AV1 35, H.264 23). `--width` downscales keeping aspect ratio (never upscales; odd values are rounded down to even, which the codecs require) — a 1080p-wide background rarely needs
more than `--width 1280`. `--no-audio` drops the audio track during the same pass, so don't chain
a separate `strip-audio` call.

For a hero background, the usual full treatment is one `encode --no-audio` to WebM plus one
`poster`, then wire both into `<video poster loop muted autoplay playsinline>`.

For a video the page scrubs by setting `currentTime` (scroll- or cursor-driven), add
`--keyframe-interval N`. A browser can only show a frame by decoding forward from the keyframe before
it, and a normal encode has one keyframe every few seconds, so scrubbing stutters. Every frame a
keyframe (`1`) seeks most smoothly but makes the file several times larger; `5`–`10` is the usual
compromise. Use `.mp4` (H.264) for scrubbing: it seeks more reliably across browsers than WebM.

## trim — cut to a time range

```
process-video.ts trim --source <video> --output <path> --start <sec> (--duration <sec> | --end <sec>) [--copy]
```

Default is a frame-accurate re-encode (codec from the output extension, same defaults as `encode`).
`--copy` is instant and lossless but can only cut on keyframes — the actual start may land up to a
couple of seconds off, so don't use it when trimming a loop to the exact frames that repeat cleanly.

## strip-audio — drop the audio track, keep everything else

```
process-video.ts strip-audio --source <video> --output <path>
```

Stream copy — no re-encode, no quality loss, runs in under a second. Use when the video is
otherwise already right; if you're re-encoding anyway, use `encode --no-audio` instead.

## loop-seam — make a loop wrap without a jump

```
process-video.ts loop-seam --source <video> --output <path>.webm|.mp4 [--fade <seconds>] [--crf N]
```

Run it on every `generate-video loop` result. Even with the same image as first and last frame,
models end a little off: the last frame typically scores ~0.98 SSIM against the first, while
neighbouring frames score ~0.996, and that difference shows as a jump on every repeat. `loop-seam`
blends the last `--fade` seconds (default 0.5) into the first ones. The result starts on source frame
k and ends exactly on frame k-1, so the wrap joins two consecutive frames of the original. The clip
gets shorter by the fade; audio is dropped, since it could not loop anyway.

Don't try to make the first and last frames identical instead: the player would then show that frame
twice on every pass, a visible hitch.

Write the WebM straight from it (`--output hero.webm`) to avoid a second lossy pass. If the clip
also needs `--width`, write an `.mp4` master with `--crf 12`, then `encode` that.

## frames — export an image sequence for scroll- or cursor-driven animation

```
process-video.ts frames --source <video> --output-dir <dir> [--fps N | --count N]
  [--start <sec>] [--end <sec>] [--width N] [--format webp|jpg] [--quality 1-100] [--prefix frame] [--even]
```

Writes `frame_0001.webp`, `frame_0002.webp`, … and a `frames.json` manifest (count, width, height,
fps, file names, total bytes). It refuses a directory that already holds frames with the same prefix,
since leftovers from a longer run would silently extend the sequence.

This is how most "the video follows the scroll" and "the character follows the cursor" pages work:
the page preloads the sequence and draws frame `i` on a `<canvas>`, where `i` comes from the scroll
progress or the cursor position. It seeks instantly in every browser, which a scrubbed `<video>`
doesn't. Budget the sequence for the page:

- 60–150 frames are usually enough. Use `--count` to hit a number regardless of clip length,
  `--start`/`--end` to drop a dead intro or outro.
- `--width 1280` (or the largest size the element is shown at) with WebP `--quality 70–80` keeps a
  frame around 30–80 KB. Check the reported total: several MB of frames needs a loading state.
- Phones: export a second, smaller set (`--width 720 --count` about half) and pick it by viewport.
- `--even` (with `--count`): generated clips ease in and out even when asked not to, so frames taken
  at equal times put most of the change in the middle of the scroll. `--even` picks frames at equal
  steps of measured change instead, so every scroll step moves the picture by about the same amount;
  `frames.json` then lists the source frame numbers it used. Use it for scroll-driven sequences.
- Write the frame count and name pattern into the page's script rather than fetching `frames.json`:
  a `fetch` fails when the page is opened straight from disk (`file://`), and people often try a
  demo page that way.

The alternative is one `<video>` whose `currentTime` follows the scroll: smaller to download, but it
only seeks smoothly when encoded with `encode --keyframe-interval`.

## reverse — play backwards, or forward-then-back

```
process-video.ts reverse --source <video> --output <path> [--pingpong] [--crf N]
```

Without flags the clip plays backwards. `--pingpong` plays it forward and then back, without showing
either end frame twice, so `<video loop>` turns around smoothly; it's the easy way to loop a
movement that can't loop on its own (a head turning left to right, a product rotating half a turn).
Audio is dropped. The whole clip is held in memory, which is fine for generated clips.

## concat — join clips into one

```
process-video.ts concat --source <a> --source <b> [--source <c> …] --output <path> [--chained] [--crf N]
```

Joins clips in order. Every clip is fitted to the first one's size and frame rate. Use `--chained`
when each clip was generated to start on the previous clip's last frame (a journey built from
several `transition` calls): it drops that shared frame so the join doesn't hold. Audio is dropped.

## sheet — see the whole clip in one image

```
process-video.ts sheet --source <video> --output <path>.png|.jpg|.webp [--count 12] [--columns 4]
  [--width 320] [--start <sec>] [--end <sec>] [--crop w:h:x:y]
```

Evenly spaced frames in a grid, with a printed legend of which frame and time each tile is. Use it
to look at a generated clip before showing it; `--crop` zooms in on the part that matters (a face, a
product), `--start`/`--end` on a moment.

## motion — measure how the clip moves

```
process-video.ts motion --source <video> [--crop w:h:x:y]
```

Prints, one row per second, how much each frame differs from the previous one (1 − SSIM × 1000), the
frames that spike against their neighbours (cuts, blinks, glitches) and how far the clip gets from its
first frame. Values under ~10 throughout mean the clip barely moves; a row of high numbers between
rows of zeros means the motion bunches up instead of running at an even speed, which is what makes a
scrubbed clip feel jerky. `--crop` measures one area only.
