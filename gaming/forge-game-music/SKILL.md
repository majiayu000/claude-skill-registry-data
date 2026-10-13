---
name: forge-game-music
description: "Create, process, review, and deliver game background music, light music, and strict instrumental tracks with local MiniMax Music 3 plus explicitly selected Stable Audio 3 or discovery-gated Suno fallback."
---

# Forge Game Music

Use this Skill for game BGM, light music, menu or exploration tracks, combat beds, looping music, and standalone instrumental music. Keep dialogue, voice-over, sound effects, and ambience-only requests in their dedicated workflows.

## Provider routing

- Use the local Comfy Desktop `audio_minimax_music_3` workflow by default. Inspect the live workflow and models before running it.
- Use Stable Audio 3 only when the user explicitly selects it and a current credential, rights confirmation, and dated capability snapshot are available.
- Keep Suno disabled with `needs_user_action` until the official account exposes its API schema and API-specific commercial game terms. Never copy fields from an unofficial client.
- A local failure never silently triggers a paid provider. A cloud submission with an unknown response is recorded and recovered by task ID only; never resubmit automatically.

## Vocal policy

Background music defaults to instrumental. Allow singing or humming only when the user explicitly requests vocals. `standalone-instrumental` always uses `Instrumental, no vocals` and `[instrumental]`, and review rejects audible voice-like content.

## Workflow

1. Ask only for missing scene, instruments or style, duration, loop intent, vocal policy, provider, and delivery details. Preserve the original brief and every explicit exclusion.
2. Read only the relevant reference: [prompt-guide.md](references/prompt-guide.md), [game-music-templates.md](references/game-music-templates.md), [comfyui-music3.md](references/comfyui-music3.md), [stable-audio-api.md](references/stable-audio-api.md), or [suno-api.md](references/suno-api.md).
3. Run `audio music plan` and `audio music route` before generation. These commands are offline and never spend credits.
4. Save native candidates immutably, then decode a separate staging copy to 44,100 Hz, 16-bit PCM stereo. The current Comfy Music 3 template saves MP3/FLAC/Opus; record the native codec before conversion. Use the music processor and loop evidence; do not use the SFX transient or dense-noise gate.
5. For a continuous BGM request, keep the complete groove from beat one through the final bar. Reject an intro, low-energy middle, sudden high or loud accent, voice-like tail, or fade-out unless the user explicitly asks for it; if the seam is weak, deliver a clean instrumental ending instead.
6. Present candidates for listening. Record exactly six music checks: scene and mood, vocal policy, instrumentation and structure, mix and generation artefacts, loop or ending quality, and gameplay listening suitability.
7. Publish only after the quality report and listening review pass. Generate the optional `music` Unity manifest only when requested; it imports an AudioClip and does not place an AudioSource.

## Boundaries

Do not install models or nodes, download weights, accept licenses, modify user environment variables, print credentials, call hidden web endpoints, or make a paid submission without explicit authorization and a valid one-time confirmation. Do not claim a loop, vocal absence, or API capability from file existence alone.

See [processing-and-quality.md](references/processing-and-quality.md) for processing, loop evidence, and publication gates.
