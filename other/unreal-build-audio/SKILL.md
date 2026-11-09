---
name: unreal-build-audio
description: Implement Unreal runtime audio using explicit assets, spatial routing, concurrency, and interruption-safe component ownership.
engines: [UNREAL]
---

# Unreal Build Audio

## When to use

Implement Unreal runtime audio using explicit assets, spatial routing, concurrency, and interruption-safe component ownership. Use this feature for Unreal-owned game code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-audio` before edits or tool launches. Continue only when the effective engine is `UNREAL` and `compatible: true`. Skill selection never selects the engine. Honor any validated task override and its permitted isolated output scope.

Identify Unreal version, supported audio backend/targets, selected SoundWave/SoundCue or MetaSound approach, submix/sound-class layout, source rights, voice/memory budgets and pause policy. Middleware and optional plugins remain explicit selections.

## Workflow

1. Map validated gameplay events to playback requests with ownership and semantic categories. Select the appropriate authored sound asset rather than coupling simulation state to audio component completion.
2. Configure import compression, streaming, looping and platform quality for actual clip duration and use. Preserve subtitle/localization metadata and validate licensing/provenance before integration.
3. Use owned AudioComponents or bounded transient playback deliberately. Track handles for loops and cancellable effects; pooling must reset parameters, attachments, mix routing and completion bindings.
4. Set attenuation, spatialization, occlusion and listener behavior for the target experience. Optional spatialization plugins require explicit support and hardware verification rather than an assumed platform feature.
5. Apply Sound Concurrency rules, priority, virtualization and voice limits. Overlapping impacts should coalesce or steal predictably without cutting essential dialogue or leaving suppressed gameplay cues.
6. Separate game-thread events from audio-render timing. Use supported scheduling such as the selected Quartz workflow when precise musical timing is required; pause, dilation and travel need explicit bridge behavior.
7. Manage submix/sound-class settings and reversible ducking under clear owners. Stop or transfer scene-owned audio on teardown, recover from output/suspension changes and provide subtitles or visual equivalents.
8. Read the [runtime audio reference](references/runtime-audio.md) for component/delegate lifetime, MetaSound parameter contracts, Quartz scheduling and failure-aware verification. Generating or changing source media still follows the existing media contract and approval boundaries.

## Verification

- Listen on target hardware for clipping, attenuation, occlusion, transition timing and subtitle alignment.
- Stress concurrency, virtualized loops, cancellation, actor destruction, world travel and suspended/resumed playback.
- Record native audio CPU, active voices, streaming/memory and timing evidence. Mock playback calls do not replace a listening review.

## Output

Native audio assets, component and concurrency ownership rules, routing/clock map, listening review and target performance measurements. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not install middleware or assume MetaSounds/Quartz integration is already selected. Sound output failures must not change authoritative gameplay outcomes. Independent tools and services retain their own architecture contracts.

## References

- [Unreal audio](https://dev.epicgames.com/documentation/en-us/unreal-engine/audio-in-unreal-engine). Match the documentation version to the project.
- [Sound concurrency](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-concurrency-reference-guide). Match the documentation version to the project.
- [Runtime audio](references/runtime-audio.md): playback handles, clocks, selected systems and native listening evidence.

