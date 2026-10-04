---
name: create-post-clips
description: >
  Turn an existing long-form video (a YouTube link, a local file, or one from your Marky
  library — webinar, podcast episode, talk, sermon) into 2-5 short vertical clips: find the
  strongest 30-60 second moments, cut them, crop to 9:16, add captions, upload to Marky,
  caption each in your brand voice, and schedule them across the week after your approval.
  Use when you already have the footage and want it repurposed. Also triggers on "turn my
  YouTube video into clips", "cut this webinar into shorts", "repurpose my podcast", "make
  reels from this video". To author a new video from scratch, see create-post-video;
  caption STYLE questions are about copy — the humanize skill covers copy, not subtitles.
---

# Create Post: Clips

Most businesses already have hours of long-form video doing nothing — webinars, podcast
episodes, talks. The short-form versions are the highest-reach posts they never make.
This skill mines a long video for its best moments and ships them as scheduled posts.

Pipeline shape and hard-won ffmpeg/Whisper details adapted from
[ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills) (MIT).

**Read the `marky-api` skill first** for auth, endpoints, and the brand cache. Base URL
`https://api.mymarky.ai/api`, header `Authorization: Bearer mk_live_YOUR_KEY`.

## Prerequisites

```bash
command -v yt-dlp ffmpeg whisper
```

- `yt-dlp` and `ffmpeg` are required. If missing, ask the user before installing, then
  offer: `brew install yt-dlp ffmpeg` (macOS) or their package manager's equivalent.
- `whisper` (OpenAI's CLI, `pip install -U openai-whisper`) gives word-level timestamps
  for tight caption sync. It is optional for YouTube sources — auto-captions work as a
  transcript fallback — but burned-in captions look best with it. Offer the install; if
  the user declines, continue with the fallback and say captions will be line-level.

**Workspace:** put everything in `~/.marky/clips/<business_id>/<slug>/` — not the current
working directory. Video work is big and cwd may be inside someone's repo. Delete the
source download when the run is done.

## Stage 1 — Get the source video

- **YouTube link** (also grabs auto-captions as the transcript fallback):

  ```bash
  yt-dlp \
    --write-auto-sub --sub-lang en --convert-subs vtt \
    -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
    --merge-output-format mp4 \
    -o "source/%(title)s.%(ext)s" \
    "https://www.youtube.com/watch?v=VIDEO_ID"
  ```

- **Local file**: copy or symlink it into the workspace.
- **Marky library**: `search_media_library` (or `GET /businesses/BIZ_ID/media`) to find it,
  then download the returned URL.

Check the duration with `ffprobe`. Under ~10 minutes there may only be 1-2 good clips;
tell the user and lower the target instead of forcing five.

## Stage 2 — Transcribe with timestamps

Preferred — Whisper on the source (word timestamps power everything downstream):

```bash
whisper source/video.mp4 --model small --language en \
  --word_timestamps True --output_format json --output_dir transcript/
```

Fallback — parse the downloaded `.vtt` auto-captions into `[MM:SS] line` entries.
Dedupe repeated lines (YouTube VTTs overlap heavily).

## Stage 3 — Find the best moments (you are the segmenter)

Read the timestamped transcript and pick the **2-5 strongest 30-60s segments**. Criteria:

- **Hook in the first 3 seconds** — the opening line must grab: surprising stat, bold
  claim, counterintuitive take, or a story that starts mid-action. Score each candidate's
  hook 1-10; only keep clips scoring **7 or higher**. The clip must OPEN on the hook
  line — never on setup.
- **One complete idea** — one framework, one stat, one story. Not a summary.
- **Emotional punch** — surprise, humor, a strong opinion, or data that shocks.
- **Ends on a takeaway or cliffhanger.**
- Ideal 30-45s, hard max 60s. Skip anything under 30s.
- Avoid: segments starting mid-sentence, meandering setup, references to earlier content
  ("as I mentioned..."), multiple unrelated ideas.

For each clip record: `start_time`, `end_time`, `title`, `hook_sentence` (exact first
line), `payoff_sentence`, `hook` pattern (stat / contrarian / story / question / bold
claim — see plan-social-content's hook palette), and a `layout` guess: `talking_head`
(one presenter), `screen_share` (slides/screen with a webcam bubble), or `side_by_side`.

## Stage 4 — Verify every cut (do not skip)

Second pass, one clip at a time: re-read the transcript **±10 seconds around each
proposed end time** and ask: does the thought actually complete there? A clip must end
on a complete thought or reaction — never mid-sentence, never mid-idea. If it runs on,
move `end_time` to where the thought resolves. This pass catches the single most common
failure (a clip that cuts off the punchline) and is cheap. If a corrected clip now
exceeds 90s, trim the end back to about 75s at the nearest sentence boundary instead.

Show the user the clip list (timestamps, titles, hooks) before cutting — a 10-second
sanity check here beats re-rendering later.

## Stage 5 — Cut and crop to 9:16

Cut each clip (re-encode; stream-copy lands on the wrong keyframe):

```bash
ffmpeg -y -ss START_SECONDS -i source/video.mp4 -t DURATION_SECONDS \
  -c:v libx264 -c:a aac -avoid_negative_ts make_zero clips/clip-1.mp4
```

**Look before you crop.** Extract a frame and view it to confirm the layout guess and
where the speaker sits:

```bash
ffmpeg -y -ss 2 -i clips/clip-1.mp4 -frames:v 1 clips/clip-1-frame.png
```

- **Talking head** — center crop to 9:16, then scale. Crop BEFORE scaling. If the
  speaker is off-center, shift the crop x-offset toward them (read the frame you
  extracted):

  ```bash
  ffmpeg -y -i clips/clip-1.mp4 \
    -vf "crop=ih*9/16:ih,scale=1080:1920" \
    -c:v libx264 -preset medium -crf 20 -c:a copy clips/clip-1-v.mp4
  ```

- **Screen share / side by side** — do not center-crop (you lose the content). Stack:
  screen region on top, speaker region below. Take the two regions from the frame you
  extracted and adjust the crop coordinates to match:

  ```bash
  ffmpeg -y -i clips/clip-1.mp4 -filter_complex \
    "[0:v]crop=iw:ih*3/4:0:0,scale=1080:1150[top];\
     [0:v]crop=ih*3/4:ih*3/4:iw-ih*3/4:ih/4,scale=1080:770[face];\
     [top][face]vstack=inputs=2[v]" \
    -map "[v]" -map 0:a -c:v libx264 -crf 20 -c:a copy clips/clip-1-v.mp4
  ```

- **Anything unclear** — safe fallback is letterbox: full frame scaled onto a 1080x1920
  canvas with black bars:

  ```bash
  ffmpeg -y -i clips/clip-1.mp4 \
    -vf "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
    -c:v libx264 -c:a copy clips/clip-1-v.mp4
  ```

Verify each output is 1080x1920 before moving on:

```bash
ffprobe -v error -show_entries stream=width,height -of csv=p=0 clips/clip-1-v.mp4
```

## Stage 6 — Burn in captions

Silent-scroll viewers are most of the audience; clips without captions underperform.
**Re-run Whisper on each CUT clip** — never reuse source-video timestamps, the offsets
drift and captions desync:

```bash
whisper clips/clip-1-v.mp4 --model small --language en \
  --word_timestamps True --output_format srt --output_dir clips/
```

Two burn-in paths:

- **Path A — HyperFrames.** If the `hyperframes` skill (and its `embedded-captions`
  workflow) is available in your session, use it — it produces the word-highlight style
  natively and handles brand fonts/colors. Hand it the cut vertical clip.
- **Path B — ffmpeg + ASS.** First confirm the local ffmpeg was built with libass
  (some minimal builds are not):

  ```bash
  ffmpeg -hide_banner -filters 2>/dev/null | grep subtitles
  ```

  Then write an `.ass` file from the SRT (3-4 words per Dialogue
  line, timed from the word timestamps) with this style block, and burn:

  ```text
  [Script Info]
  PlayResX: 1080
  PlayResY: 1920
  WrapStyle: 0

  [V4+ Styles]
  Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
  Style: Default,Arial Black,64,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,0,2,40,40,270,1

  [Events]
  Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
  Dialogue: 0,0:00:00.00,0:00:01.20,Default,,0,0,0,,THE HOOK WORDS
  ```

  ```bash
  ffmpeg -y -i clips/clip-1-v.mp4 -vf "subtitles=clips/clip-1.ass" \
    -c:v libx264 -crf 20 -c:a copy clips/clip-1-final.mp4
  ```

Colors: ASS uses `&HAABBGGRR` (blue-green-red, not RGB). Swap the highlight color for a
brand accent from the brand cache if it stays readable on video.

## Stage 7 — Upload and draft one post per clip

For each final clip:

1. Upload:

   ```bash
   curl -X POST "https://api.mymarky.ai/api/businesses/BIZ_ID/media" \
     -H "Authorization: Bearer mk_live_YOUR_KEY" \
     -F "file=@clips/clip-1-final.mp4"
   ```

   Keep the returned URL. Uploads cap at 50 MB; if over, raise `-crf` to 23 and re-encode.
2. **Write the caption in the brand voice.** Start from the clip's `hook_sentence` — it
  already earned its place — then rewrite per the brand profile (`tone`,
  `caption_writing_rules`, `caption_suffix`; see "Write like the business" in the
  marky-api skill). Run every caption through the **humanize** skill's pattern check
  (score 90+, fix silently) before showing the user.
3. Create the post as a draft with `metadata`:
   `{"media_type": "video", "format": "clip", "hook": "<pattern>", "topic": "...", "created_by": "create-post-clips"}`
   — per "Tag every post" in the marky-api skill.

## Stage 8 — Approve, then schedule (hard gate)

1. Present all clips on the **review board in approve mode** — exactly the
   plan-social-content Stage 6 flow: write `items.json` (one item per clip, `media_url`
   pointing at the local final file or uploaded URL, `meta` like "Clip 2 - 0:42 -
   stat hook"), run `${CLAUDE_PLUGIN_ROOT}/scripts/review-board.py items.json` in the
   background, parse `BOARD_URL:`, AskUserQuestion with the URL, then read
   `feedback.json`. Apply edits verbatim; append the feedback to
   `~/.marky/feedback-log.jsonl` with `context: "clips"`.
2. **Nothing is scheduled until the user approves.** Rejected clips are dropped; edited
   captions use the user's wording.
3. Schedule approved clips via the `schedule-posts` skill, **spaced across the week**
   (for example Tue/Thu/Sat at the same hour) — never all on one day. Video is supported
   everywhere: target every connected platform whose integration `status` is `valid`.
4. After the scheduled times pass, check `publish_results` per post shows `success`.

## Troubleshooting

- **FFmpeg filter_complex error:** don't use `-c:v copy` with `-filter_complex`. Only
  `-c:a copy` is safe.
- **Wrong output resolution:** always crop before scaling. Verify with
  `ffprobe -show_entries stream=width,height`.
- **Caption sync issues:** run Whisper on the cut clip, not the source episode.
- **TikTok upload fails:** ensure H.264 + AAC encoding. Add `-c:v libx264 -c:a aac`.
- **Clip too long:** segmentation sometimes overshoots. Auto-trim anything over 90s
  back to ~75s at a sentence boundary.
- **"Unknown filter 'subtitles'":** that ffmpeg was built without libass. Use Path A
  (HyperFrames) for the caption burn, or install a full ffmpeg build.
- **No auto-captions on the YouTube video:** Whisper becomes required; install it or stop.

**Marky wants your feedback.** If anything breaks or is confusing while you run this
skill — and again once the clips are scheduled — send Marky a quick note with the
`submit_feedback` MCP tool. See "Marky wants your feedback" in the `marky-api` skill.
