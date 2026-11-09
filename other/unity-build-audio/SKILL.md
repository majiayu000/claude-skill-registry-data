---
name: unity-build-audio
description: Build Unity runtime audio with mixer routing, spatial ownership, bounded voices, and interruption-safe playback.
engines: [UNITY]
---

# Unity Build Audio

## When to use

Build Unity runtime audio with mixer routing, spatial ownership, bounded voices, and interruption-safe playback. Use this feature only for Unity-owned project code and assets.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-build-audio` before edits or tool launches. Continue only when the effective engine is `UNITY` and this skill is eligible. A requested skill never selects its engine. Honor the resolved task override evidence and permitted output scope when an isolated prototype is selected.

Identify Unity version, audio output targets, AudioMixer layout, imported clip settings, voice and memory budgets, pause policy, loudness targets and accessibility equivalents. Record any selected audio middleware separately.

## Workflow

1. Map gameplay events to AudioSource playback requests and explicit AudioMixer groups. Distinguish music, ambience, dialogue and transient effects; prevent direct sound calls from becoming authoritative gameplay transitions.
2. Choose clip load type, compression, sample rate and preload behavior from duration, concurrency and target memory. Verify asset rights and language variants before runtime integration.
3. Create a bounded voice manager with priority, stealing and coalescing rules. Track ownership and completion; pooled AudioSources must reset clip, pitch, spatial settings, mixer assignment and callbacks before reuse.
4. Configure spatialBlend, attenuation, rolloff, doppler and listener ownership. Local split-screen or multiple listeners require a deliberate supported mixing strategy rather than accidentally activating duplicate listeners.
5. Use AudioSettings.dspTime and scheduled playback when sample-aligned transitions are required. Explicitly bridge simulation, unscaled time and audio time; pause or slow motion must not corrupt music scheduling.
6. Implement mixer snapshots, volume settings and ducking with reversible ownership. Scene teardown, focus changes and cancellation must stop or transfer owned loops without abruptly restoring another system's mix.
7. Handle missing clips, output device changes and platform suspension without blocking gameplay. Supply subtitles, visual cues or alternative channels when sound communicates required information.

Read [import, mixer and measurement decisions](references/audio-production.md) for load types, stereo/spatial choices, resource teardown and evidence limits.

## Verification

- Test voice saturation, loops across scene changes, cancelled requests, pooled reuse and settings persistence.
- Listen on representative devices for clipping, spatial placement, transition seams, pause/resume and suspension recovery; inspect native mixer and audio profiler data.
- Record peak voices, DSP/CPU cost and memory against declared budgets. A successful AudioSource call is not a listening review.

## Output

Clip import and mixer configuration, playback/voice ownership code, clock and cancellation contract, listening review and target audio measurements. Record environment, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not install middleware or assume every audio backend behaves identically. Browser web-build audio activation and native audio suspension require separate testing. Engine guidance applies to engine-owned code; independent services retain their architecture contracts.

## References

- [Unity audio overview](https://docs.unity3d.com/6000.0/Documentation/Manual/Audio.html). Use the documentation matching the installed project version.
- [Scheduled AudioSource playback](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/AudioSource.PlayScheduled.html). Use the documentation matching the installed project version.

