---
name: camera-audio-ai
description: Implement camera, photo, live vision, audio, voice, and AI-assisted pipelines for Meta AI glasses while respecting SDK capabilities, latency, privacy, and mobile resource constraints.
---

# Camera, Audio and AI Pipelines

Use this skill for POV capture, live analysis, visual assistance, streaming, voice flows, or multimodal AI.

## Camera

Distinguish three workloads:

1. **Photo capture** — best when one high-quality still is enough.
2. **Preview/live stream** — best for on-phone viewfinders and low-latency visual feedback.
3. **AI sampling** — process selected frames, not necessarily the entire stream.

For AI sampling, default to a backpressure-safe design:

```text
DAT camera stream
  -> frame sampler
  -> image normalization/compression
  -> at most N in-flight inference requests
  -> result state
  -> phone UI / audio response / display output
```

Do not buffer an unbounded stream of images.

## Cloud vision

When sending images to a cloud model:

- Never hardcode privileged API keys in the mobile client.
- Prefer a backend token exchange/proxy when secrets are required.
- Reduce resolution/quality to the minimum useful level.
- Make upload behavior explicit in UX and privacy documentation.
- Do not retain frames by default.
- Add cancellation and timeout handling.

## On-device vision

Prefer on-device inference when it satisfies quality/latency requirements and reduces privacy/network cost. Separate the vision adapter from DAT so models can be swapped independently.

## Audio

Audio support is version/device/platform-sensitive. Do **not** assume there is a DAT audio package with a particular class name.

Before implementing audio or voice:

1. Query current DAT docs.
2. Identify whether the path is a DAT capability, normal Bluetooth audio profile, OS audio session API, or a combination.
3. Confirm microphone route, speaker route, permissions, background behavior and interruption handling.
4. Implement using the OS-native audio stack plus only the documented DAT pieces.

## UX

Wearable experiences should remain usable without staring at the phone. Prefer short status cues, clear error recovery, and hands-free progression when the supported APIs make that possible.
