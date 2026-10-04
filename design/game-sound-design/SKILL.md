---
name: game-sound-design
description: Design, generate, implement, debug, and review game sound effects and interactive audio. Use when Codex is asked about SFX, Foley, ambience, UI sounds, combat sounds, creature sounds, weapon audio, footsteps, spatial audio, procedural audio, audio events, middleware integration, mix behavior, sound libraries, generated sound assets, Unity audio, Unreal MetaSounds, FMOD, Wwise, or game audio implementation.
license: MIT
---

# Game Sound Design

## Core Workflow

1. Identify the game genre, art style, camera perspective, platform, player fantasy, accessibility needs, middleware/engine, and target mix style.
2. Define the sound's gameplay job before designing texture: confirm, warn, reward, locate, sell impact, communicate state, create atmosphere, guide attention, or support UI flow.
3. Build a sound palette: acoustic vs synthetic, dry vs processed, realistic vs stylized, clean vs noisy, tonal vs percussive, close vs distant, and diegetic vs non-diegetic.
4. Design in layers. Separate transient, body, texture, tail, sweetener, movement, and environmental response so timing and mix can be tuned independently.
5. Add variation and rules: random pitch/volume, round-robin takes, surface/material switches, distance attenuation, obstruction/occlusion, cooldowns, priority, and voice limits.
6. Implement with explicit event names, parameters, busses, snapshots/states, and debug hooks.
7. Verify in context, not solo. Test at gameplay speed, repeated playback, dense scenes, quiet scenes, different output devices, and with music/dialogue active.

## Creative Priorities

- Readability: each sound should tell the player what happened, where it happened, and how important it is.
- Hierarchy: reserve the loudest, brightest, widest, or most detailed sounds for critical player-facing events.
- Identity: establish recurring materials, motifs, instruments, synths, processing, or acoustic signatures for factions, abilities, UI families, and environments.
- Feedback timing: align attack, impact, release, and tail timing to animation and gameplay frames.
- Repetition resistance: use variation, layering, randomization, procedural elements, and silence to avoid fatigue.
- Accessibility: do not make audio the only carrier for critical information unless the game is intentionally audio-first and provides appropriate support.

## Implementation Priorities

- Route sounds through meaningful busses such as master, music, SFX, ambience, UI, dialogue, voice, reverb, and accessibility cues.
- Use parameters for speed, intensity, health, surface, material, distance, size, charge, weather, room, threat, and state.
- Define priorities and voice limits for spam-prone sounds such as footsteps, bullets, impacts, UI ticks, particles, and crowds.
- Use spatialization, attenuation, occlusion, reverb sends, and environmental zones deliberately.
- Keep source quality high enough for processing, then compress and stream/load according to platform and memory constraints.
- Track licensing and provenance for library sounds, recordings, generated audio, and third-party assets.

## Freshness Rule

Verify current engine and middleware docs before giving version-sensitive implementation advice about Unity audio, Unreal audio/MetaSounds, FMOD, Wwise, platform audio compression, licensing, or generated-audio commercial-use terms.

## Engine Mapping

- Unity: use AudioSources, AudioClips, AudioMixer groups, snapshots, exposed parameters, spatial blend, profiler, and middleware integrations when needed.
- Unreal: use Audio Components, Sound Waves, Sound Cues where present, MetaSounds for procedural/parameterized sources, Submixes, attenuation, concurrency, and Sound Classes.
- FMOD: use events, parameters, snapshots, banks, VCAs/busses, random/multi instruments, live update, profiler, and engine integration hooks.
- Wwise: use Events, Switches, States, RTPCs/Game Parameters, Blend/Random/Switch Containers, SoundBanks, busses, profiling, and game sync monitoring.

## Deliverable Shape

For sound design work, provide:

- Gameplay function and priority
- Creative palette and references
- Layering or generation direction
- Variation, parameter, and event rules
- Middleware/engine implementation notes
- Mix, accessibility, and performance considerations
- Rights/provenance and verification steps

## References

- Read `references/sound-design-checklist.md` when designing, implementing, or reviewing game sound effects, ambience, UI audio, or generated SFX.
