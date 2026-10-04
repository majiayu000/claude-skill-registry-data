---
name: multimedia
description: Dojo Multimedia — workflow for media inspection (ffprobe), conversion/remux (ffmpeg), preview, local transcription, Spotter visual search, thumbnails, and frame extraction.
version: 1.1.0
category: media
tags: media, video, audio, image, preview, transcription, spotter, ffmpeg, ffprobe, probe, remux, mp4, mkv, subtitles
---

# Dojo Multimedia

Use this skill for **video, audio, images, media inspection, conversion, previews, transcription, thumbnails, frame extraction, Spotter visual search, or FFmpeg/FFprobe-backed processing**.

Core rule: use Dojo native media tools first. Do not reach first for shell `ffmpeg`, `ffprobe`, Python, or `mediainfo` when a native media tool can do the job. Native tools use the bundled engines, show proper tool UI, respect cancellation/timeouts, integrate with Preview/Spotter, honor path and permission guards, and avoid cross-platform shell quoting problems.

## Pick the right tool

- **`media_probe` inspects (read-only).** `type=engine` reads metadata, streams, codecs, frames, packets, chapters, and bitrate with bundled **ffprobe**. `type=preflight` estimates local transcription cost.
- **`media_process` transforms.** `type=engine` runs bundled **ffmpeg** to convert, remux, extract, or thumbnail. `type=transcribe` runs local speech-to-text.
- **`preview`** opens the in-app lightbox. **`media_spotter`** does LLM-powered visual search in video.

Rule of thumb: if you only need to _look at_ a file, use `media_probe`. If you need to _change_ a file, use `media_process`.

## Bundled engines and permissions

- `ffmpeg` and `ffprobe` are bundled **together** as one versioned tool pair, so they never drift. You never need a system/Homebrew install.
- All media tools enforce the same path and permission guards as `read`/`write`: kernel/device paths are always blocked, network/external paths follow the access tier, and out-of-scope paths trigger a permission prompt.
- In **Normal** mode, a media operation prompts before it runs (allow once or allow all). In **YOLO** and higher it proceeds without a prompt. Remote inputs (`http://`, `rtsp://`, `pipe:`, `lavfi`, …) are passed straight to the engine and are not treated as local files.

## `media_probe` — full-power ffprobe + transcription preflight

```text
MediaProbe(type=engine, path=<audio-or-video>)
MediaProbe(type=preflight, path=<audio-or-video>)
```

`type=engine` is **full-power ffprobe** — it behaves exactly as if you ran `ffprobe` yourself. With no `args` it returns a JSON dump of streams and format for `path`. Pass **any** ffprobe arguments via `args` (no whitelist, no forced flags) to read frames, packets, chapters, side data, bitrate, or anything else:

```text
MediaProbe(type=engine, path=<file>)
MediaProbe(type=engine, path=<file>, args=["-show_format", "-show_streams", "-print_format", "json"])
MediaProbe(type=engine, path=<file>, args=["-show_frames", "-select_streams", "v:0", "-read_intervals", "%+#5"])
MediaProbe(type=engine, path=<file>, args=["-show_chapters", "-print_format", "json"])
MediaProbe(type=engine, path=<file>, args=["-show_entries", "format=duration:stream=codec_name,width,height", "-of", "csv"])
MediaProbe(type=engine, path=<file>, args=["-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "default=nokey=1:noprint_wrappers=1"])
```

Notes:

- `path` is appended automatically unless it already appears in `args`, so you may supply the input either way.
- When you pass custom `args`, output is returned untouched (use `-print_format json|csv|xml` / `-of` to shape it). With no `args`, output is pretty-printed JSON.
- Use `within=<ms>` to set an ffprobe timeout for slow/large inputs (default 30s).

`type=preflight` requires a local file. It probes duration and estimates transcription speed; use its recommended `within` value when calling transcription.

## `media_process` — ffmpeg engine + local transcription

Common parameters:

- `type=engine` — raw ffmpeg operation; `args=[...]` are FFmpeg-style arguments.
- `type=transcribe` — local English-mode speech-to-text.
- `path=<file>` — media path for transcription.
- `format=markdown|summary` — transcription output shape.
- `outputPath=<path>` — optional transcription output path.
- `within=<ms>` — time budget; use the preflight recommendation for transcription.

For metadata, prefer `MediaProbe(type=engine)` (bundled ffprobe). Use `MediaProcess(type=engine)` to actually transform media — convert, remux, extract, thumbnail.

## `preview` — in-app lightbox

Use to open the Preview lightbox for images, video, audio, markdown, text, and files.

Common parameters:

- `path=<file>` — artifact or local file to open.
- `seek` / `time` — video timestamp in seconds or `HH:MM:SS`/`MM:SS` style.
- `muted=true` / `sound=off` — start silent.
- `autoplay=true` — start playback automatically when possible.
- `zoom=<number>` — initial image zoom, e.g. `0.90`.
- `label=<text>` — friendly title.

Useful visible form:

```text
Preview(type=image, zoom=0.90)
Preview(type=video, time=154s, sound=off)
Preview(type=md)
Preview(type=txt)
```

Default to safe audio. When opening video/audio automatically, start muted or low volume unless the user asked for sound. The volume slider should match the actual mute state: volume zero means muted; moving above zero unmutes.

Preview can seek an already-open video **without reloading** if the same media path is used. During Spotter/visual search, keep the preview moving: call `preview` repeatedly with the same video path and new timestamps so the user can watch candidate scrubbing live.

## WebView playback and MP4 remuxing

The Preview lightbox uses native WebView playback. It is fast for compatible MP4/WebM, but containers like `.mkv`, `.avi`, `.flv`, `.wmv`, `.ts`, `.m2ts`, or `.mov` with unsupported codecs may show a black frame, `0:00`, no sound, or no seeking.

Do not fight the browser. Create a previewable MP4 copy.

Prefer **fast remux** first when streams are MP4-compatible, such as H.264 video and AAC audio:

```text
MediaProcess(type=engine, args=["-i", "<input>", "-c", "copy", "-movflags", "+faststart", "<output>.mp4"])
```

If carrying SRT subtitles into MP4, convert subtitles to `mov_text`:

```text
MediaProcess(type=engine, args=["-i", "<input>", "-map", "0", "-c", "copy", "-c:s", "mov_text", "-movflags", "+faststart", "<output>.mp4"])
```

Only transcode when stream-copy fails because codecs are not MP4-compatible:

```text
MediaProcess(type=engine, args=["-i", "<input>", "-c:v", "libx264", "-c:a", "aac", "-movflags", "+faststart", "<output>.mp4"])
```

Codec note: the bundled builds are LGPL-safe. Do not assume GPL/nonfree encoders like `libx264`, `libx265`, or `libfdk-aac` are always present; if a transcode fails because an encoder is missing, prefer stream-copy remux or a widely available encoder.

Converted-copy policy:

1. Write the converted copy next to the original file.
2. Keep the same base name and use the new extension, usually `.mp4`.
3. Never modify or delete the original.
4. Use and reference the converted copy from that point on.
5. Tell the user where the copy was created.

Example:

```text
/path/to/show.mkv
/path/to/show.mp4
```

## Local transcription

`MediaProcess(type=transcribe)` is local and currently English-mode only.

Workflow:

1. Call `MediaProbe(type=preflight, path=<file>)`.
2. Tell the user transcription will be treated as English (`lang=en`).
3. Call `MediaProcess(type=transcribe, path=<file>, format=markdown, within=<recommended>)`.
4. Report the markdown timeline path.
5. Say: "Please check accuracy before relying on it."
6. Open the markdown timeline with Preview: `Preview(type=md)`.

Markdown transcript previews should preserve timestamps and timeline structure.

## Spotter visual search

Use `media_spotter` when the user asks to find a person, object, logo, scene, or reference image inside video.

Spotter is **LLM-powered**. Do not describe it as local face recognition. Local media processing prepares candidates; the active vision model decides semantic matches such as "Rachel," "this woman," or "the first time this object appears."

Good Spotter behavior:

- Start with a bounded candidate set.
- Preview the source video at each promising timestamp.
- Keep seeking the already-open Preview as candidates change.
- Leave Preview at the best match.
- Report exact timestamp plus evidence path/frame when available.
- Be honest about uncertainty and one-second offsets.

## 3×3 contact-sheet workflow

When visual matching is expensive or ambiguous, use a human-assisted loop:

1. Generate or collect candidate frames.
2. Pick the 9 closest or most representative candidates.
3. Build a 3×3 contact sheet/sprite with large labels and timestamps, e.g. `A1 00:02:13`.
4. Open it with `Preview(type=image, zoom=...)`.
5. Ask the user to choose the closest tile.
6. Jump Preview to that tile's source timestamp and refine nearby.

This is ideal when many frames look similar, model confidence is low, or the user can identify the target faster than more model calls.

## Thumbnails and frame extraction

For thumbnails, stills, or evidence frames, use `MediaProcess(type=engine)` with FFmpeg args. Prefer concise JPEG/PNG outputs in an artifact directory or next to the source when the user needs a persistent result.

Examples:

```text
MediaProcess(type=engine, args=["-ss", "00:02:13", "-i", "<video>", "-frames:v", "1", "<frame>.jpg"])
MediaProcess(type=engine, args=["-i", "<video>", "-vf", "fps=1", "<frames-dir>/frame-%06d.jpg"])
```

Preview extracted frames with `Preview(type=image)`.

## Reporting

Always tell the user:

- what was created,
- where it was written,
- whether it was remuxed or transcoded,
- whether quality was preserved,
- the timestamp(s) found,
- and when transcription accuracy must be checked.

Prefer showing evidence through Preview over dumping long paths or raw media-engine output.
