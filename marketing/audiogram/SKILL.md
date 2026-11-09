---
name: audiogram
description: This skill should be used when the user asks to "make an audiogram", "turn a podcast into a video", "create a waveform video", "make a podcast clip video", "convert audio to video", "animate a waveform/audio bars", "add a moving waveform to my voiceover", or "make a square/vertical clip for a podcast quote". Covers amplitude-driven waveforms, frequency bars, synced captions, cover-art layout, a progress bar, and 1:1 / 9:16 social framing.
version: 0.1.0
---

# Audiogram

Turn an audio clip — a podcast highlight, a voiceover, a quote — into a short, captioned video that stops the scroll in a muted feed. The moving element (a waveform or equalizer bars) signals "there is sound here," the captions carry the message for the 80% who watch on mute, and cover art + title + a progress bar give it a finished, branded frame.

## When to use

- A podcast soundbite or quote clip for Reels / TikTok / Shorts / feed posts.
- A voiceover or narration that needs a visual so it can post as video.
- Music or any audio where a reactive waveform/bars is the hero.

## The one rule that prevents 90% of bugs

**Drive every bar height from the current frame, never from a real-time analyser loop.** Live `AnalyserNode` + `requestAnimationFrame` reads "what is playing right now" — but a video renderer paints frames out of order and faster/slower than real time, so the wave desyncs or freezes. Instead, decode the whole file to amplitude samples once, then compute the displayed value as a pure function of the frame. In Remotion this is `useAudioData()` + `visualizeAudio()`; in plain canvas it is `decodeAudioData()` into a sample array you index by frame.

```tsx
import { useAudioData, visualizeAudio } from "@remotion/media-utils";
import { useCurrentFrame, useVideoConfig } from "remotion";

const audioData = useAudioData(staticFile("episode.mp3"));
if (!audioData) return null; // still loading
const { fps } = useVideoConfig();
const bars = visualizeAudio({
  audioData,
  frame: useCurrentFrame(),
  fps,
  numberOfSamples: 32, // MUST be a power of two
}); // → Float array, length 32, each 0–1, low freq → high freq
```

## Two ways to render the wave

| Look | Data | API | Best for |
|---|---|---|---|
| Equalizer **bars** | frequency spectrum, values 0–1 | `visualizeAudio()` | music, energy, "feed the bars" |
| Smooth **oscilloscope wave** | time-domain amplitude, −1…1 | `visualizeAudioWaveform()` | voice, podcasts, a calm minimal look |

`visualizeAudio` returns lows on the left, highs on the right. For a centered equalizer, take the first N bars and **mirror** them around the middle so the bass sits in the center. `numberOfSamples` must be a power of two (16/32/64); use 16–32 for a chunky branded look, 64+ for a detailed spectrum. See `references/waveform-render.md` for full bars and oscilloscope components.

## Long files: don't load the whole episode

`useAudioData()` reads the entire file into memory — fine for a 30–90s clip, slow and memory-heavy for a full episode. For anything long, trim first or use `useWindowedAudioData()`, which fetches only the audio around the current frame via HTTP range requests.

```tsx
import { useWindowedAudioData } from "@remotion/media-utils";
const { audioData } = useWindowedAudioData(
  staticFile("full-episode.mp3"),
  fps,
  /* windowInSeconds */ 10,
);
```

Best practice: **trim to the soundbite** (≤90s) before rendering. A tight clip is a better social asset and a lighter render.

## The layout

A finished audiogram is five stacked layers. Keep them in fixed zones so one composition crops cleanly to every aspect.

| Layer | Job | Notes |
|---|---|---|
| Background | brand color / subtle gradient / blurred cover | never busy enough to fight captions |
| Cover art + title | who/what this is | small square cover + episode/show title, top zone |
| Waveform / bars | the motion that signals audio | center band, the hero element |
| Captions | the message, for muted viewers | high contrast, one short phrase at a time |
| Progress bar | how far through the clip | thin bar driven by `frame / durationInFrames` |

```tsx
// progress bar — a pure function of frame, no audio needed
const { durationInFrames } = useVideoConfig();
const progress = useCurrentFrame() / durationInFrames; // 0 → 1
<div style={{ width: `${progress * 100}%`, height: 6, background: "#fff" }} />
```

## Captions synced to speech

Captions are not optional — most feed video plays muted, and subtitled video holds attention far longer. Generate word/phrase timings with a transcription step (Whisper / `@remotion/captions` `parseSrt`), then show one short phrase at a time, switching on its start frame. The mechanics of word-by-word reveal, active-word highlighting, and SRT/JSON timing belong to the **caption-animation** skill — use it for the caption layer rather than duplicating it here. This skill's job is to place that caption track inside the audiogram layout and keep it synced to the same audio clock the waveform uses.

## Social framing

Design once inside the center safe zone, then reframe — don't letterbox.

| Aspect | Use | Resolution | Layout |
|---|---|---|---|
| 1:1 | feed posts | 1080×1080 | cover+title top, wave center, captions lower third |
| 9:16 | Reels / TikTok / Shorts | 1080×1920 | more vertical breathing room; keep captions clear of bottom 18% (UI) |
| 16:9 | YouTube, landing embed | 1920×1080 | wave wide and low, captions centered |

Make the clip **playable on mute and on sound**: the waveform + captions must tell the whole story silently, while the actual audio track plays for anyone who taps. Always include the real audio with `<Audio src={...} />` so the export carries sound.

## Output checklist

- Bar/wave height is a pure function of `useCurrentFrame()` — no live analyser loop.
- `numberOfSamples` is a power of two; centered bars are mirrored around the middle.
- Clip trimmed to ≤90s, or `useWindowedAudioData()` for long source.
- Captions present, high-contrast, synced to the same audio clock (via caption-animation).
- Cover art + title + progress bar render; progress = `frame / durationInFrames`.
- Real audio muxed in (`<Audio>`); story still reads with sound off.
- 1:1 + 9:16 (and 16:9 if needed) from one composition, key content in the safe zone.

## Deliver & verify (rendered stills → MP4)

> **Packaged helper** (`scripts/`): tile your stills with `scripts/contact-sheet.sh sheet.png f-hook.png f-mid.png f-end.png`, then assert the encode with `scripts/probe-mp4.sh out.mp4 [WxH] [fps]`. See `scripts/README.md`.

This is HEAVY tier: the deliverable is a real **MP4** (audio muxed in), and the waveform must be *data-driven* — its shape at any frame must match the audio at that time. Verify a few frames as stills before paying for the full encode.

**Output contract:**
- A Remotion project with the audiogram registered (`<Composition>` + zod `schema` + `defaultProps`), all motion frame-driven — no `Date.now()` / `Math.random()` / timers, and **no realtime analyser**.
- Bake the amplitude/waveform samples into props (or decode once via `useAudioData`) **offline** — never analyse audio at render time; headless render has no realtime audio clock.
- Deliverable = the rendered `out/*.mp4` (audio muxed via `<Audio src={staticFile()}>`) plus the project, so the user can re-render with new audio/captions.

**Verify loop — render stills → inspect → encode.**

```bash
# 1. Frame-exact stills at start / mid / end, WITH SHIPPED PROPS (not just defaultProps)
npx remotion still Audiogram out/f-start.png --frame=0   --props=./props.json
npx remotion still Audiogram out/f-mid.png   --frame=N   --props=./props.json
npx remotion still Audiogram out/f-end.png   --frame=N-1 --props=./props.json   # last = durationInFrames-1

# 2. Inspect each PNG — fidelity (waveform/bar heights match the audio's amplitude at
#    that exact time; the right caption phrase is on screen and synced) AND artifacts
#    (missing cover art, caption off-canvas / under the bottom UI band, bar overflow).

# 3. Only once the stills check out, encode the full video (audio muxed):
npx remotion render Audiogram out/audiogram.mp4 --props=./props.json
```

- The waveform is **data-driven** — verify amplitude + caption sync at a few frames *before* the full render, so a desync is caught once, not after a long encode.
- Use `npx remotion compositions` to read `durationInFrames`/`fps` and pick the end frame.
- README demo: `npx remotion render Audiogram out/demo.gif --codec=gif` (silent, but proves the motion).

**Before you finish:**
1. `npx remotion still` renders cleanly at frame 0, mid, and last — no errors, no missing cover/audio assets.
2. Bar/wave height at each checked frame matches the audio's amplitude there; the correct caption phrase is on screen and synced.
3. Frame-driven only — no realtime analyser / `Date.now()` / `Math.random()` / timers; samples baked offline.
4. Captions stay inside the safe zone (clear of the bottom ~18% UI band) at every checked frame; cover art + title + progress bar present.
5. Full MP4 encoded with real audio muxed in and plays; (optional) GIF rendered for the README.

## Reference files

- `references/waveform-render.md` — complete runnable components for both looks: a mirrored frequency-bar equalizer and a smooth oscilloscope wave (`visualizeAudio` / `visualizeAudioWaveform`), the full five-layer audiogram composition with cover art, title, progress bar and audio mux, a power-of-two/smoothing cheat sheet, and a dependency-free Web Audio + canvas variant that decodes to a per-frame sample array. Ends with build/attribution notes.
