---
name: forge-text-audio
description: "Generate, redraw, inpaint, continue, validate, and deliver explicitly requested game sound effects and ambience with a locally installed Stable Audio 3 Small-SFX model and Unity AudioClip integration. Use only when the user explicitly asks for non-speech game audio; do not trigger for visual-only work, dialogue, voice-over, songs, or complete musical scores."
---

# Forge Text Audio

Use this Skill only when the user explicitly requests a game sound effect, UI sound, action sound, ambience, or non-verbal creature sound. Do not add audio as a side effect of map, sprite, or video work. Reject dialogue, speech, voice-over, songs, and complete musical scores instead of silently selecting another provider.

## Workflow

1. Group intake questions into sound, mode/source, and delivery. Ask for one consolidated request confirmation. Support exactly `text-to-audio`, `redraw`, `inpaint`, and `continue`.
2. Preserve the user's original request and create an English Stable Audio prompt package. Use three candidates for text generation and redraw, and one candidate for inpainting and continuation unless the confirmed request overrides the count.
3. Run the local-only provider preflight. The user must install the official `stable-audio-3` runtime in an isolated, user-selected directory, accept the Stability AI and Gemma model terms personally, make `stabilityai/stable-audio-3-small-sfx` available in the local Hugging Face cache, and install FFmpeg/FFprobe. If the runtime is missing, return `needs_user_action` with the installation request from the repository README. Never install, download, accept licenses, or call a hosted API during ordinary Skill use.
4. Run the provider through `scripts/providers/stable_audio.py` using the shared binary UTF-8 JSON protocol and the repository-local `game-visual-forge.local.json` runtime configuration. UTF-8 is mandatory for every subprocess even when the generated prompt is English because paths, original requests, logs, and Unity names may be non-ASCII.
5. Decode provider latents without the official API's destructive output clamp. Before writing a raw candidate, record the decoded peak and overrange count and apply only enough global attenuation to keep the peak at or below -1.0 dBFS; never boost quiet audio. Keep written raw candidates and source audio immutable. Process into a separate staging directory, validate 44,100 Hz, 16-bit signed PCM WAV delivery, and record SHA-256 hashes, waveform, spectrum, loop evidence, and protected-region evidence.
6. Present playable candidates and require the user's final listening approval. Record exactly these checks: prompt/action match; transient/impact clarity; noise/generation artifacts; unwanted speech/music; spatial/channel suitability; loop/tail quality. Do not publish with a failed or missing check.
7. If Unity delivery is requested, import the approved `unity-audio-manifest.json` with the independent UPM package at `integrations/unity/com.game-visual-forge.audio`. The package imports `AudioClip` assets and does not create or modify scene objects.
8. Only when the user explicitly requests scene placement, use Unity MCP to create or reuse an `AudioSource`, bind the imported clip, apply playback and spatial settings, save the target scene, and verify that unrelated scene roots are unchanged.

## Required safeguards

- Never retry a failed or `generation_unknown` attempt automatically.
- Reject generated one-shots with continuous dense energy and no credible transient-to-tail decay as `dense-noise`; do not present them for listening approval.
- Never treat a local WAV as proof that Unity import or scene placement succeeded.
- Publish WAV only: 44,100 Hz, 16-bit signed PCM, mono or stereo as confirmed. Do not publish MP3, OGG, FLAC, AIFF, or an upsampled 48 kHz copy.
- Use the repository command surface through `scripts/run.py`; do not duplicate business logic in this Skill launcher.

Read [stable-audio-workflow.md](references/stable-audio-workflow.md) for the provider protocol and [processing-and-quality.md](references/processing-and-quality.md) for deterministic processing and review gates.
