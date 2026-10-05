---
type: Skill
name: design-video-creation
description: Create and process videos using AI generation (Runway, Pika, Replicate, Sora, Veo) and FFmpeg processing. MCP bridge provides frame extraction (extract_video_frames); the Design Stack media worker handles full FFmpeg processing (resize, trim, compress, GIF, format conversion). Covers social-media-optimized video output. Use when generating AI videos, extracting frames/thumbnails, transcoding videos, creating GIFs from clips, or preparing video for social platforms.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Video Creation & Processing

Use this skill when generating AI videos or processing existing video files for web, social media, or marketing use.

## MCP Tool Discovery

The plugin provides video tools that may be agent-prefixed or bare. Check your
tool list for the correct names:

```
Pattern: nv_oos_{AGENT_NAME}_agent_extract_video_frames
         extract_video_frames  (bare — may not be registered)
```

| Video Task | Tool Name Pattern |
|---|---|
| Extract frames/thumbnails | `extract_video_frames` or `nv_oos_*_agent_extract_video_frames` |
| Cross-site video ops | `remote_wp_connection` — list spoke sites |

For full video processing (compression, resizing, trimming, format conversion,
GIF creation), use the **media worker fallback** (`http://localhost:3100/api/video/process`)
with FFmpeg.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for video workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai health` | Verify video processing tools and providers |
| `wp mcp-ai bulk` | Batch process video assets |
| `wp mcp-ai log` | Check video processing success/failure logs |

## When to use this skill

Trigger when ANY of the following is true:

- The task asks to "create a video", "generate a clip", or "animate".
- Video files need resizing, compression, format conversion, or trimming.
- Creating GIFs from video clips.
- Preparing video for social media (stories, reels, feed posts).
- Extracting metadata or thumbnails from video files.

## Extracting video frames via MCP (Primary)

Use `extract_video_frames` to pull frames from videos in your Media Library or from a URL:

```
Parameters:
  video_url      — URL of the video file
  url            — Alternative URL parameter
  attachment_id  — WordPress attachment ID of the video
  file_id        — Provider file identifier (OpenAI/Gemini)
  timestamps     — Specific timestamps in seconds: [5.5, 10, 15.25]
  interval       — Extract at regular intervals in seconds (e.g., 5)
  frame_count    — Number of evenly-distributed frames (1–20, default 10)
  save_to_media  — Save extracted frames to Media Library (default: false)
  quality        — JPEG quality 1–31, lower is better (default: 2)
```

**Examples:**
- Get 5 evenly-distributed thumbnails: `frame_count: 5`
- Extract at 10s intervals: `interval: 10`
- Get specific moments: `timestamps: [3.5, 8.0, 15.2]`
- Save poster image: `timestamps: [0.5], save_to_media: true`

## AI video generation providers (media worker / external)

| Provider | Model | Best For | Access |
|---|---|---|---|
| **Higgsfield** | Cinema Studio 4.0 | Cinematic text/image-to-video, native audio, granular camera controls | API (`generate_higgsfield_video` MCP tool) |
| **Runway** | Gen-3 Alpha | Cinematic, high-quality clips | Web + API |
| **Pika** | Pika 1.0 | Short creative clips, animations | Web |
| **Replicate** | Stable Video Diffusion | Open-source, self-hostable | API |
| **Haiper** | Haiper v1 | Text-to-video, image-to-video | Web |
| **Kling** | Kling 1.5 | Ultra-realistic, long clips | Web (China) |

> AI video generation requires external API keys and is handled through the media worker or direct provider APIs.

### Higgsfield via MCP (built-in tools)

Higgsfield (https://docs.higgsfield.ai) is integrated as a first-class
provider with four tools sharing one two-part credential:

| Tool | Purpose |
|---|---|
| `generate_higgsfield_video` | Text/reference-to-video across 5 verified models (below) |
| `generate_higgsfield_image` | Styled stills via SOUL workflows (`soul-2`, `soul-cinema`) |
| `check_higgsfield_request` | Poll any `request_id` (queued/in_progress/completed/failed/nsfw/canceled) |
| `cancel_higgsfield_request` | Cancel queued work that has not started |

**Video models** (`model` param on `generate_higgsfield_video`):
`cinema-studio-4.0` (default — camera/genre/era controls), `seedance-2.5`
(4-30s), `seedance-2.0` (4-15s, up to 4k), `wan-3.0` (2-30s, 1080p,
adaptive aspect, seed), `kling-3.0` (3-15s, multi-shot, no refs).

- **Auth:** two-part credential — Key ID + Secret → `Authorization: Key {ID}:{SECRET}`.
  Configure via **NV oOS → Providers → Higgsfield** or the
  `HIGGSFIELD_API_KEY_ID` / `HIGGSFIELD_API_KEY_SECRET` env vars (a combined
  `HIGGSFIELD_API_KEY` with `ID:SECRET` also works).
- **Lifecycle:** async — submit returns a `request_id` + `status_url`; the
  shared client polls with backoff (2s → 10s) until `completed`, `failed`,
  `nsfw`, or `canceled`, then downloads and saves to the Media Library.
  On timeout the `request_id` is returned — poll it with
  `check_higgsfield_request`.
- **Params (video):** `prompt`, `model`, `duration`, `resolution`,
  `aspect_ratio`, `generate_audio`, `camera_movement`, `genre`, `era`,
  `seed`, `reference_image_id` / `reference_image_url` /
  `reference_video_url` / `reference_audio_url` (public URLs),
  `save_to_media`, `async`, `timeout`. Values are clamped per model.
- **Params (image):** `prompt`, `model`, `aspect_ratio`, `resolution`,
  `enhance_prompt`, `seed` (1-1000000), `batch_size` (1|4), `style_id`
  (soul-2 only), `save_to_media`, `async`, `timeout`.
- **Retention:** Higgsfield keeps outputs ≥7 days — the tools download
  immediately so nothing is lost.
- **Cost:** billed per second of video / per image from a prepaid balance;
  the tools report `cost` with `is_estimated` when local pricing is
  unavailable.
- **Status:** poll async jobs with `check_video_status` (supports `async_*` job IDs).

## Social media video specs

| Platform | Feed | Stories/Reels | Max Duration |
|---|---|---|---|
| **Instagram** | 1080×1080 (1:1) / 1080×1350 (4:5) | 1080×1920 (9:16) | 60s feed / 90s reels |
| **TikTok** | 1080×1920 (9:16) | Same | 10 min |
| **YouTube Shorts** | 1080×1920 (9:16) | Same | 60s |
| **Facebook** | 1280×720 (16:9) | 1080×1920 | 240 min |
| **LinkedIn** | 1280×720 (16:9) | — | 10 min |
| **Twitter/X** | 1280×720 (16:9) | — | 140s |

**Recommended:** H.264 MP4, 30fps, 4–8 Mbps for 1080p.

## Media worker fallback (FFmpeg processing)

For full video processing, use the media worker API at `http://localhost:3100`:

### Video processing
```javascript
const form = new FormData();
form.append('file', videoBlob, 'input.mp4');
form.append('operation', 'compress'); // resize | trim | convert | compress | gif
form.append('format', 'mp4');
form.append('width', '1080');

const response = await fetch('http://localhost:3100/api/video/process', {
  method: 'POST',
  body: form,
});
```

### Video metadata extraction
```javascript
const form = new FormData();
form.append('file', videoBlob);

const response = await fetch('http://localhost:3100/api/video/info', {
  method: 'POST',
  body: form,
});

const { video, audio, duration, format, size } = await response.json();
// video.codec, video.width, video.height, video.fps
```

## FFmpeg recipes (media worker)

### Resize to social media dimensions

```bash
# Instagram feed (1:1)
ffmpeg -i input.mp4 -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -crf 23 output.mp4

# Instagram story (9:16)
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -crf 23 output.mp4

# Twitter (16:9)
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:v libx264 -crf 23 -c:a aac -b:a 128k output.mp4
```

### Create GIF from video

```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1:flags=lanczos" -c:v gif -loop 0 output.gif
```

### Trim and compress

```bash
# Trim first 5 seconds, starting at 00:02
ffmpeg -i input.mp4 -ss 00:00:02 -t 5 -c:v libx264 -crf 28 -preset fast output.mp4
```

### Add text overlay

```bash
ffmpeg -i input.mp4 -vf "drawtext=text='Your Brand':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h-th-20" output.mp4
```

## WordPress video best practices

1. **Never upload videos directly to WordPress** — use YouTube/Vimeo for hosting, embed via oEmbed.
2. **For short clips (<10s, no audio)**: auto-play muted HTML5 video with `<video autoplay muted loop playsinline>`.
3. **Poster images**: always include a `poster` attribute — use `extract_video_frames` with `save_to_media: true` to generate one.
4. **Transcoding**: offload to the media worker for format standardization.

```html
<video autoplay muted loop playsinline poster="hero-poster.webp"
       width="1200" height="675">
  <source src="hero-bg.webm" type="video/webm" />
  <source src="hero-bg.mp4" type="video/mp4" />
</video>
```

## What This Skill Does NOT Cover

- AI video generation API key management and provider setup → `mcp-ai-wpoos-plugin`
- Social media publishing of finished videos → `design-social-publishing`
- Video analytics, engagement tracking, or performance reporting
- Live streaming setup and RTMP configuration
- Audio production, sound design, or podcast editing
- 3D animation, motion graphics design, or compositing (After Effects)
- Video hosting infrastructure (YouTube/Vimeo channel management)

## Critical rules

- **MCP first for frames** — use `extract_video_frames` for thumbnails, posters, and scene previews.
- **Media worker for processing** — compression, resizing, trimming, and GIF creation go through the FFmpeg-powered media worker.
- **Compress before upload** — raw screen recordings can be 50MB+ for 10s; compress to 2–5MB.
- **Use H.264 for compatibility** — it plays everywhere; AV1 is smaller but not universal yet.
- **Mute autoplay videos** — browsers block unmuted autoplay; add captions if audio is essential.
- **Test on mobile** — vertical (9:16) for stories, square (1:1) for feed, landscape (16:9) for YouTube.
- **Generate thumbnails** — use `extract_video_frames` to get a poster image, then `resize_image` to optimize it.

## Common mistakes

```html
<!-- WRONG — unmuted autoplay (blocked by browser) -->
<video autoplay src="promo.mp4"></video>

<!-- WRONG — 200MB raw video file served directly -->
<video src="screen-recording.mov"></video>

<!-- RIGHT — compressed, muted, with poster -->
<video autoplay muted loop playsinline
       poster="promo-poster.webp"
       width="1080" height="1080">
  <source src="promo-compressed.mp4" type="video/mp4" />
</video>
```

## Cross-references

- Run **`design-image-optimization`** for video poster/thumbnail images — use `resize_image` (MCP).
- Run **`design-social-publishing`** to attach videos to social posts.
- Run **`design-media-workflow`** for end-to-end pipeline automation including cross-site video workflows.
- Run **`mcp-ai-wpoos-plugin`** for `remote_wp_connection` — pull video content from spoke sites.

## References

- FFmpeg documentation: <https://ffmpeg.org/documentation.html>
- Runway API: <https://runwayml.com>
- Replicate video models: <https://replicate.com/collections/video-generation>
- HTML5 video best practices: <https://web.dev/video-best-practices/>
