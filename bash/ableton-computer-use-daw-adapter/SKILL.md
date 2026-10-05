---
name: ableton-computer-use-daw-adapter
description: Use Computer Use as a verified UI adapter for Ableton Live production workflows, especially when Live API, AbletonOSC, scripts, or Max for Live cannot expose an action directly. Use when operating Ableton/plugin UI, exposing device parameters, reconciling UI state with RuntimeState, loading presets, or recovering from bridge gaps without relying on blind clicks.
---

# Ableton Computer Use DAW Adapter

## Purpose

Use Computer Use as the UI layer of the Agentic DAW Bridge, not as ad hoc
clicking. Computer Use may observe and operate visible Ableton or plugin UI,
but every important action should be bounded by structured state checks before
and after.

## Core Rule

Prefer structured tools first:

```text
AbletonOSC / scripts / jq / Max for Live bridge -> Computer Use -> structured verification
```

Computer Use is appropriate when the target is visible in the UI but not exposed
as a reliable API action, such as plugin Configure, floating plugin windows,
drag/drop loading, preset browsers, modal dialogs, or visual reconciliation.

## Ableton App Target

Use the absolute app path, not the generic app name:

```text
app="/Applications/Ableton Live 12 Suite.app"
```

Do not call Computer Use with `app="Live"`; it is ambiguous and has failed in
this workflow. Avoid `app="com.ableton.live"` when Ableton installer volumes are
mounted, because multiple apps can share the same bundle identifier. Resolve the
current target first:

```bash
uv run python scripts/ableton_app_target.py --json
```

The resolver should return `/Applications/Ableton Live 12 Suite.app` on this
machine when the installed app is present.

## Primitive Map

- `get_app_state`: visual `RuntimeState` observation. Use before every UI action sequence.
- `click`, `set_value`, `type_text`, `scroll`, `drag`, keypresses: UI `DAW Materialization`.
- screenshots/app state: `Evidence Policy` support, not proof by themselves.
- repeated observe-act-verify sequences: `Runtime Reconciliation`.
- failed or ambiguous UI readings: `Unknown State`, requiring fallback or user clarification.

## Workflow

1. Load the related domain skill first, usually `ableton-live-m4l-codex`.
2. Use shell/OSC scripts to inspect current state and write snapshots when possible.
3. Call Computer Use only for the missing UI affordance.
4. Immediately verify with structured tools, not just visual confidence.
5. Emit or store a compact evidence packet: intent, UI action, before/after state, diff, risk notes.

## Ableton Parameter Exposure Pattern

Use this for plugin controls such as Transit 2 Macro:

```bash
uv run python scripts/device_parameter_exposure.py inspect <track> <device> --out before.json --json
```

Then use Computer Use to select the device, enable Configure, and touch the
desired plugin controls. Finish with:

```bash
uv run python scripts/device_parameter_exposure.py inspect <track> <device> --out after.json --json
uv run python scripts/device_parameter_exposure.py compare before.json after.json --format summary --json
```

## Safety Policy

Follow the upstream Computer Use confirmation policy. For Ableton work, ask
before destructive UI actions such as deleting tracks/clips/devices, overwriting
files, installing software, uploading exports, or changing system settings.

## Capability-Bias Pair

Capability: reaches UI-only affordances that structured bridges cannot yet
control.

Bias: can over-trust layout, focus, coordinates, and visual appearance. Counter
this with `get_app_state`, snapshots, jq-friendly diffs, and OSC/CLI readback.

## Completion Criteria

The task is complete only when one of these is true:

- the UI action is verified by structured RuntimeState,
- the UI action is documented as visual-only evidence with explicit uncertainty,
- or the system reports an `Unknown State` and proposes a safe next action.

## References

- UI adapter workflows: [references/workflows.md](references/workflows.md)
