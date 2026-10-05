---
name: generate-video
description: Generate one coherent video from a text or multimodal shot brief using a deliberately selected current model and one observable action. Use for new cinematic footage when no narrower video Atom owns the outcome; do not use for animating one supplied still, editing supplied footage, talking portraits, intros, or multi-clip assembly.
---
# Generate Video

## Catalog

- Display name: Generate Video
- Categories: Video
- Status: Ready
- Route label: Guide-routed cataloged video model
- Tone: purple
- Short description: Generate one coherent video from a shot brief using a deliberately selected current model and one observable action.

## What this skill does

- Turns text into one shot with explicit subject, action, environment, camera, duration and sound.
- Selects a current model from capabilities, not from the phrase text-to-video.

## How to use

Provide subject, one action, setting, camera, duration, ratio, style and audio preference.

#### Example

```text
Generate a 5-second 16:9 video of a paper boat drifting through a rain puddle; slow low tracking shot; natural rain audio.
```

## Workflow

1. Compile one atomic shot with subject, action, setting, camera, light, duration, ratio and audio. When the request is underspecified, choose one visible change from A to B with a clear emotional or visual payoff; avoid a merely drifting camera over a static subject.
2. When references are supplied, label each role as identity/content, first or last frame, motion, style, or audio timing. Reject a camera move that fights the source composition—for example, revealing space outside a tightly cropped reference—unless an upstream expansion step is approved.
3. Select exactly one cataloged model before submission: MiniMax H3 for large-amplitude/natural human motion or H3 multimodal and first/last-frame modes; Kling V3 Omni for several named image roles or one motion-reference video; Kling 3.0 for precise one/two-frame, product, or ordinary image animation; Seedance 2.5 for long multimodal, audio-visual, artistic, or talking-performance work; Veo 3.1 for one-source-image premium synchronous dialogue/SFX at 16:9 or 9:16; Seedance 2.0 for routine image-led video. Do not trial models in sequence. After selection, apply the matching multi-step orchestration model prompt guide when installed, while using only the selected Agent's live fields.
4. Start one WeShop run, poll to terminal success and download MP4.
5. Inspect first, middle and last frames, motion continuity, reference-role fidelity, camera/source compatibility, visible change, duration, ratio and audio.


## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: One coherent generated shot
- Default layout: User-requested delivery format
- Model policy: H3 large/natural motion; Kling Omni complex/motion references; Kling 3 precise frames/products; Seedance 2.5 long audiovisual/artistic/performance; Veo source-image premium synchronous audio; Seedance 2.0 routine
- Downstream use: General video generation
