---
name: unreal-build-cinematics
description: Build Unreal Sequencer playback and cinematic integration with real bindings, explicit clocks, interruption and state restoration.
engines: [UNREAL]
---

# Unreal Build Cinematics

## When to use

Author or integrate Unreal Level Sequences, runtime sequence playback, bindings, cinematic camera handoffs or selected movie-render workflows. Gameplay camera behavior belongs to the camera capability.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-cinematics` before writes or tool launches. Require effective engine `UNREAL` and `compatible: true`; revalidate task override evidence for every output scope. The skill never selects an engine.

Record actual Unreal version, LevelSequence/MovieScene modules, map/sequence assets, actor bindings, player ownership, clock, target platform and shot budgets. Movie Render Queue, Control Rig, template sequences and other plugins are explicit selections.

## Workflow

1. Author real sequence and map assets through native tools. Define possessable/spawnable lifetime, binding identity, hierarchy, playback range and frame rates; verify bindings in the intended world and cooked content.
2. Choose one playback owner per sequence request and retain its player/actor and generation. Use the [Sequencer integration reference](references/sequencer-integration.md) for runtime APIs and version-specific restore semantics.
3. Coordinate camera claims, input/HUD restrictions and pause with current owners. Configure completion/restore policy explicitly; avoid global unpause, focus reset or restoring an obsolete camera after replacement.
4. Define skip, seek, reverse, interruption, travel and actor-loss outcomes. Separate Stop from natural completion and handle queued callbacks safely. Critical gameplay outcomes require authoritative, idempotent rules independent of sampled event tracks.
5. Select the sequence clock and dilation policy. Record display/tick resolution and evaluation assumptions; explicit seeks, timecode/audio synchronization and real-time playback have different behavior.
6. For selected rendering workflows, stage outputs with exact shot/sequence, settings, dependencies and rights. Preserve editable sources and keep rendering approval and runtime asset promotion separate.

## Verification

Exercise real bound-property changes, pause, stop/restore, natural completion, replacement, skip and invalid binding. Verify player camera/input/HUD restoration and map/cook dependencies in a native target build. Record actual shot captures, audio sync and performance separately from structural/headless tests; NullRHI cannot certify a cinematic image or soundtrack.

## Output

Native sequence/map assets, binding and playback contract, clock/restore/cancel ownership, native tests and representative shot findings. Record environment, expected/observed results and blocked/not-run checks under the active `.hephaera/.cache/tasks/` task.

## Boundaries

Do not synthesize binary assets, enable optional rendering plugins, generate media, accept licenses or promote outputs implicitly. Existing art/media/provenance and human review gates still apply.

## References

- [Sequencer integration](references/sequencer-integration.md): bindings, completion modes, authority and native evidence.
