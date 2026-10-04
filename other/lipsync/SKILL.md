---
name: lipsync
displayName: "Animate Face With Audio"
description: >
  Drive a face's mouth from a separate audio track, built into Genspark
  — no API key, no external account. Two native lip-sync routes on the
  Genspark sandbox: animate a portrait still into a talking head from an
  audio file (OmniHuman), or mouth-swap a voiceover onto an existing
  video while preserving the rest of the frame (Sync Labs sync v2). Turn
  a headshot + a voiceover into a virtual presenter, dub a brand video
  into another language, or build a UGC ad from one photo. Runs via the
  `gsk video_generation` CLI. Triggers on "lip sync video", "lipsync",
  "make this video speak", "match audio to mouth", "dub a video", "drive
  avatar from audio", "sync lips to voice", "talking head from photo",
  "voiceover sync", or any explicit ask to drive a face's mouth from an
  audio track.
allowed-tools: Bash(gsk *)
homepage: https://www.genspark.ai
license: MIT
---

# Animate Face With Audio

Drive a face's mouth from a separate audio track — turn a portrait into
a talking head, or mouth-swap a voiceover onto existing footage. Lip-sync
runs **natively inside the Genspark sandbox** through the `gsk` CLI: no
install, no `runcomfy login`, no API key, no external account. The
sandbox already has `gsk` on the PATH.

There are two routes. Pick by the shape of the user's input:

| User has… | Route | Model |
|---|---|---|
| A **portrait / headshot** + an audio file | **Talking head** | `fal-ai/bytedance/omnihuman/v1.5` |
| An **existing video** + an audio file | **Mouth-swap** | `fal-ai/sync-lipsync/v2` |

## Route 1 — Portrait still + audio → talking head (OmniHuman)

The default for "make this photo speak." One portrait image + one audio
track → a video where the subject speaks and gestures naturally.

```bash
gsk video_generation "talking head" \
  --model fal-ai/bytedance/omnihuman/v1.5 \
  --image_urls "https://your-cdn.example/portrait.jpg" \
  --audio_url "https://your-cdn.example/voiceover.mp3" \
  --output-file ./out/talking-head.mp4
```

- `--image_urls <url>` — the portrait. Head-and-shoulders or upper body
  works best. **Required.**
- `--audio_url <url>` — the voiceover the face should speak. WAV or MP3,
  a web URL or an AI Drive path. **Required** — OmniHuman is
  audio-driven.
- The quoted `value` is a short label only — OmniHuman derives motion
  from the image + audio, **not** from a prompt. Don't try to direct it
  with prose.
- Output is 16:9; duration tracks the audio length (up to ~30 s).
- `--output-file <path>` downloads the finished `.mp4`. Omit it and the
  JSON response still carries the generated video URL.

## Route 2 — Source video + audio → mouth-swap (Sync Labs sync v2)

For "lip-sync this voiceover onto an existing video." Sync Labs swaps the
mouth motion to match the new audio and leaves the rest of the frame —
camera, lighting, background, body pose — untouched.

```bash
gsk video_generation "lip sync" \
  --model fal-ai/sync-lipsync/v2 \
  --video_url "https://your-cdn.example/source-video.mp4" \
  --audio_url "https://your-cdn.example/voiceover.mp3" \
  --output-file ./out/dubbed.mp4
```

- `--video_url <url>` — the source video containing the face to re-sync.
  **Required.**
- `--audio_url <url>` — the new voiceover to sync the mouth to.
  **Required.**
- The quoted `value` is a short label only; this route is driven by the
  two media inputs, not a prompt.
- `--output-file <path>` downloads the finished `.mp4`.

Both routes POST the job, poll until the render is done, and (with
`--output-file`) download the video for you.

## When to use which route

- **Portrait → talking head (Route 1, OmniHuman)** — you have a *still
  image* and want the person in it to speak. Virtual presenter, UGC ad
  from one headshot, dubbed product demo from a single photo, animated
  spokesperson.
- **Video → mouth-swap (Route 2, Sync Labs)** — you have *existing
  footage* and want to change what the on-screen person is saying.
  Foreign-language dubbing of a brand video, fixing a flubbed line,
  re-voicing a talking-head clip while keeping the original motion.

If the user just wants a video with *its own generated speech* (no
specific audio track to lock to — "make a clip of someone saying X"),
that's general video generation with native audio, not lip-sync — use
`gsk video_generation --model fal-ai/bytedance/seedance-2.0` and put the
line in the prompt. Seedance generates its own voice; it does **not**
sync a face to a pre-recorded MP3.

## Where the audio comes from

You need an audio track for both routes. If the user only has a script,
generate the voiceover first, then feed it in:

```bash
# 1. Generate the voiceover
gsk audio_generation "Welcome to our spring launch — three new colors, one bold look." \
  --model fal-ai/elevenlabs/tts/multilingual-v2 \
  --requirements "Warm, confident female voice, moderate pace" \
  --output-file ./out/voiceover.mp3

# 2. Drive the portrait with it (upload the mp3 to a URL the sandbox can
#    reach, then pass that URL)
gsk video_generation "talking head" \
  --model fal-ai/bytedance/omnihuman/v1.5 \
  --image_urls "https://your-cdn.example/portrait.jpg" \
  --audio_url "https://your-cdn.example/voiceover.mp3" \
  --output-file ./out/talking-head.mp4
```

For Chinese / Japanese / Korean voiceovers, prefer
`--model fal-ai/minimax/speech-2.8-hd`. To match a *specific* person's
voice, clone it first with `gsk voice_cloning`, then synthesize the line.

## Prompting / input tips

Lip-sync quality is driven by the **media you feed in**, not by prose:

- **Clean audio = clean sync.** A dry voiceover (no music bed, no
  reverb) produces sharper mouth motion. Isolate the voice stem if the
  source has background music.
- **Match audio length to the clip.** For mouth-swap, a large
  audio/video duration mismatch causes drift — trim the audio or extend
  the video so they line up.
- **Portrait framing (Route 1).** Head-and-shoulders, face clearly
  visible, neutral starting expression. Avoid extreme angles or heavy
  occlusion (hands over mouth, sunglasses).
- **One face per clip.** Both routes target a single primary face. For a
  multi-person scene, sync each speaker's shot separately.
- **Front-lit, sharp source.** Motion blur, low light, or a tiny face in
  the frame all degrade the result.

## Common patterns

### Foreign-language dub of an existing brand video
Route 2 (Sync Labs) with the original video + a translated voiceover MP3.
Generate the translated voiceover with `gsk audio_generation` first.

### Virtual presenter / UGC ad from one headshot
Route 1 (OmniHuman) with the creator's portrait + a product-pitch
voiceover.

### Multi-language launch (same identity, many languages)
Route 1 with one portrait + N different audio files — one call per
language. The same identity holds across every dub.

### Fix a flubbed line in finished footage
Route 2 with the existing clip + a clean re-recording of the corrected
line.

## Limitations

- **You must supply the audio.** Both routes lip-sync to an audio track
  you provide — they do not write a script or generate speech. Make the
  voiceover with `gsk audio_generation` first if you only have text.
- **One face per render.** No multi-speaker mouth-sync in a single call.
- **Route 1 is 16:9, ~30 s max**, audio-length-bound. For longer pieces,
  generate sections and stitch them.
- **Route 1 ignores prompts** — OmniHuman derives everything from the
  image + audio. You can't direct camera or background with text.
- **Cost + time scale with length.** Each render takes a few minutes and
  bills to the Genspark account that owns the sandbox.
- **Not "generate a talking clip from scratch."** For a video that
  speaks its own generated voice, use
  `gsk video_generation --model fal-ai/bytedance/seedance-2.0` instead.

## How it works

The skill classifies intent — portrait still + audio, or source video +
audio — picks the matching model, and runs `gsk video_generation` inside
the Genspark sandbox. `gsk` submits the job to Genspark's media backend
(OmniHuman v1.5 or Sync Labs sync v2), polls until the video is rendered,
and (with `--output-file`) downloads the finished clip. Credits are
billed to the Genspark account that owns the sandbox — there is no
separate provider key to manage.

## Security & Privacy

- **Consent / dual-use.** Driving a real person's face from a separate
  audio track is dual-use. Refuse requests that target real public
  figures without consent, or that aim at defamatory or sexually
  explicit synthetic media. The skill does not gate inputs — that
  responsibility rests with the operator.
- **Voice provenance.** Confirm the speaker in the audio has consented to
  having their voice paired with the target face. Both the face rights
  and the voice rights must be in hand. The skill does not check.
- **No keys, no external setup.** The skill only calls `gsk`, which is
  pre-authenticated inside the sandbox. There is no API key to ask the
  user for, store, or leak.
- **Input boundary.** The label, model, and asset URLs are passed as
  discrete arguments to `gsk`; they are sent to the media backend over
  HTTPS, not shell-expanded as commands. No shell-injection surface.
- **Untrusted reference assets.** The portrait, source video, and audio
  are untrusted input. Ingest only assets the user explicitly provided
  for this lip-sync. If the output diverges (wrong identity, broken
  sync), suspect the reference asset.
- **Output.** Generated video is written only to the `--output-file`
  path you choose inside the sandbox workspace.

## See also

- `gsk audio_generation` — generate the voiceover (TTS) the face speaks
- `gsk voice_cloning` — clone a specific person's voice, then synthesize
  the line and lip-sync to it
- `gsk video_generation --model fal-ai/bytedance/seedance-2.0` — generate
  a video with its own native speech (when there's no audio track to
  lock to)
