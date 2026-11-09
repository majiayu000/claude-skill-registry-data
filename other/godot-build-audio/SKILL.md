---
name: godot-build-audio
description: Implement Godot audio players and buses with bounded voices, explicit clocks, and safe scene interruption.
engines: [GODOT]
---

# Godot Build Audio

## When to use

Implement Godot audio players and buses with bounded voices, explicit clocks, and safe scene interruption. Apply this feature only to Godot-owned code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh godot-build-audio` before edits or tool launches. Continue only when the effective engine is `GODOT` and the skill is eligible. Skill selection never selects the engine. Honor validated task override evidence and its permitted isolated output scope.

Record Godot version, project language, target outputs, AudioServer bus layout, imported streams, voice/memory budgets and pause policy. Selected plugins and specialized codecs remain explicit dependencies.

## Workflow

1. Choose AudioStreamPlayer, AudioStreamPlayer2D or AudioStreamPlayer3D by spatial requirements. Map validated gameplay events to owned playback requests and route them to existing named buses.
2. Configure import formats, looping, compression and streaming for actual use. Preserve audio rights/provenance and keep dialogue/subtitle timing and localization variants explicit.
3. Bound concurrent voices with priorities, coalescing and stealing rules. Use the selected version's supported polyphony strategy; pooled players must reset stream, pitch, bus, spatial and callback state.
4. Define listener and attenuation behavior for 2D/3D scenes and local-player viewports. Audio position must follow its chosen owner without retaining a freed actor.
5. Separate simulation time, SceneTree pause/process mode and audio-mix time. For precise sequencing, use the installed version's supported playback/mix timing rather than relying on a render-frame timer.
6. Own bus effects, volume preferences and ducking restorations. Validate bus identity after layout changes and ensure one effect cannot restore over another active mix owner.
7. Handle stop, natural completion, cancellation, scene exit, device suspension and missing streams distinctly. Gameplay must progress safely when playback fails; provide subtitles or visible equivalents for required information.

## Verification

- Listen for clipping, spatial placement, transition gaps and subtitle alignment on representative outputs.
- Test voice saturation, pooled reuse, cancelled loops, scene changes, paused trees and suspend/resume; stopped playback must not require a natural-finished callback.
- Record real Godot audio profiling, voices and memory. API call success and headless Dummy audio runs do not prove listening quality.

## Output

Audio stream/import and bus changes, voice/player ownership, clock/cancellation rules, listening review and target audio budgets. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not install middleware or assume web audio activation matches native behavior. Adapters follow the project's selected GDScript or C# language. Independent services and tools retain their architecture contracts.

## References

- [Godot audio buses](https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html). Select the documentation matching the project release.
- [Godot AudioStreamPlayer](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html). Select the documentation matching the project release.

