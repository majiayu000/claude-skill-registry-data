---
name: phaserjs-build-audio
description: Integrate Phaser SoundManager playback with browser activation, bounded voices, scene ownership and explicit backend limitations.
engines: [PHASERJS]
---

# Build Phaser Audio

## When to use

Add Phaser runtime music, effects, positional sounds or scene audio transitions.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh phaserjs-build-audio`; require compatibility and honor task override scope. Inspect the locked Phaser revision, selected audio configuration, browser codec support and event/bus budgets. Use rights-cleared local audio; generation is a separate workflow governed by `MEDIA.md` when selected. Do not install audio middleware or adopt remote assets implicitly.

## Workflow

1. Queue audio through the Scene loader with declared keys and supported formats; distinguish loading, decoding, activation and playback failure. Respect the selected Web Audio, HTML5 audio or disabled configuration and its capability differences.
2. The SoundManager belongs to the game. Define scene-owned effects versus persistent music explicitly; scene shutdown does not by itself guarantee a looping sound stops. Cache/texture-style global lifetime assumptions must not leak into sound ownership.
3. Create reusable sound instances through `this.sound.add` or bounded one-shot calls. Declare concurrency, priority/stealing, volume/mute settings and channel categories. Drop expired feedback while locked rather than replaying stale bursts after activation.
4. Handle `locked`/unlock behavior from valid browser interaction. Pause/resume and visibility policies must preserve user settings and distinguish gameplay clocks from audio scheduling. Unsupported spatial or mixing features require an explicit limitation report, not a silent claim of parity.
5. For supported positional audio, define listener/camera and emitter updates in consistent units; detach or stop emitters at actor despawn. Cancelling an event cancels owned fades, delayed plays and loops.
6. Remove listeners and stop/destroy scene-owned sounds at shutdown. Preserve persistent music only under a surviving service owner; destroy the service when the game ends. Audio errors never determine gameplay outcomes.

## Output and verification

Deliver voice/channel ownership, activation/error paths and runtime evidence. Check locked startup, codec failure, overlap limits, repeated scene restarts, mute persistence, visibility changes and stopped loops. Audibility/spatial quality requires playback on target hardware; mocked calls establish routing only. Consult the [Phaser audio guide](https://docs.phaser.io/phaser/concepts/audio) for backend and lifecycle behavior.
