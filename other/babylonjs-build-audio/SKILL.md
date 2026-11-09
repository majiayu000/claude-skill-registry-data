---
name: babylonjs-build-audio
description: Integrate Babylon.js audio playback, buses and spatial ownership using the explicitly selected audio API generation.
engines: [BABYLONJS]
---

# Build Babylon.js Audio

## When to use

Implement runtime music, effects, spatial emitters or scene audio lifecycle in Babylon.js.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh babylonjs-build-audio`; require compatibility and honor task override scope. Inspect the locked Babylon revision and explicitly select its audio API generation. AudioEngineV2 and legacy `Sound`/`AudioEngine` have different construction/lifetime contracts; do not mix examples or migrate implicitly. Use rights-cleared project audio and codecs. Read `MEDIA.md` only when media generation or media validation is in scope.

## Workflow

1. For a compatible V2 project, initialize through `CreateAudioEngineAsync` and create sounds through supported V2 factories such as `CreateSoundAsync`; await initialization and browser activation. Existing legacy projects keep their declared adapter until a migration is selected.
2. Give the application one owning audio service and define scene-owned versus persistent music/emitter lifetimes. Explicitly route buses, gain/mute settings and pause behavior. Device output and audio-context failures must not block simulation.
3. Set listener/camera ownership, spatial position/attachment, attenuation and distance units. Validate detachment when an actor despawns; do not leave an emitter following a disposed node.
4. Bound simultaneous voices, loops and queued activation requests. Drop expired feedback rather than replaying a burst after unlock/resume. Interruption cancels scheduled effects; user volume/mute settings survive transitions. Audio clocks and game clocks need an explicit synchronization policy.
5. Treat audio as presentation of gameplay events. Provide required visual/text alternatives and independent channel settings. Stop owned sounds, remove observers and release buffers/buses/engine only at their owning boundary.

## Output and verification

Deliver the selected API/version contract, bus/voice policy and runtime adapter. Exercise locked startup, rejected decode/load, rapid event overlap, pause, reconnect, scene exit and repeated playback. Record audible behavior on supported target devices; mocked play calls prove routing only. Check [Babylon audio generation guidance](https://doc.babylonjs.com/features/featuresDeepDive/audio/) and the [V2 playback API](https://doc.babylonjs.com/features/featuresDeepDive/audio/playingSoundsMusic) for the installed version.
