---
name: ableton-live-m4l-codex
description: Operate Ableton + Max for Live production workflow with a stateful, evidence-based practice, including 30/60/90 minute studio blocks, Codex-assisted generation, and weekly consistency controls. Use when the user wants to run, refine, or operationalize a production session with this workflow.
---

# Ableton Live + Max for Live (Codex Studio Pro)

## Skill locations

Canonical skill manifest: `~/.agents/skills/ableton-live-m4l-codex/SKILL.md`
Bundled Transit 2 references: `references/transit-2/`
External Ableton toolbox: `$ABLETON_CODEX_TOOLBOX` when installed locally

## What this skill does

It applies the Ableton M4L Skill protocol built in this repo for:

- planning sessions by 30/60/90-minute blocks,
- creating structured session artifacts,
- running a fast preflight check,
- and tracking weekly evidence/recovery decisions.

## Scope

- Trigger on any request to plan/execute a music production session with Ableton Live + Max for Live and Codex.
- Trigger on requests for script-driven session setup and session indexing.
- Trigger for defining block boundaries, blocked-state recovery, or weekly review cadence for Ableton sessions.

## Required files

- Reference skill manifest: `~/.agents/skills/ableton-live-m4l-codex/SKILL.md`
- UI adapter skill: `~/.agents/skills/ableton-computer-use-daw-adapter/SKILL.md`
- Transit 2 references: `references/transit-2/README.md`
- External toolbox root: `$ABLETON_CODEX_TOOLBOX`
- Reference implementation guide: `$ABLETON_CODEX_TOOLBOX/skills/ableton-live-m4l-codex-skill.md`
- Quick start command: `$ABLETON_CODEX_TOOLBOX/scripts/quick_start_ableton_studio.sh`
- Device parameter exposure tool: `$ABLETON_CODEX_TOOLBOX/scripts/device_parameter_exposure.py`
- AbletonOSC queue wrapper: `$ABLETON_CODEX_TOOLBOX/scripts/ableton_osc_queue.py`
- Ableton Computer Use app target resolver: `$ABLETON_CODEX_TOOLBOX/scripts/ableton_app_target.py`
- Musical automation mapping resolver: `$ABLETON_CODEX_TOOLBOX/scripts/musical_automation_mapping.py`
- Ableton awareness snapshot CLI: `$ABLETON_CODEX_TOOLBOX/scripts/ableton_awareness_snapshot.py`
- Ableton awareness hook doc: `$ABLETON_CODEX_TOOLBOX/docs/ableton-awareness-hooks.md`

## One-line start

```bash
"$ABLETON_CODEX_TOOLBOX/scripts/quick_start_ableton_studio.sh" "<tema>" 30 "house" 124 "A minor" outputs/ableton-sessions pass "sesion pro"
```

## Workflow

1. Read the reference skill doc and confirm objective, tempo, key, and block length.
2. Run the one-line start command.
3. Execute creative steps for the selected block (30/60/90).
4. On blocked state, run a mandatory 3–5 minute recovery action, then re-evaluate.
5. For block closure, write/update the corresponding artifacts and weekly index entry.

## Notes

- Keep the skill conversational and concrete: avoid open-ended creativity claims without artifact evidence.
- Prefer state-closure over fixed time.
- In creative emergencies, allow one weekly "creative mode" bypass pass if declared explicitly.
- Before automating plug-in controls, verify that Live exposes the target control as a `DeviceParameter` with `scripts/device_parameter_exposure.py`; use MIDI CC mapping only as a lower-observability fallback when host exposure is unavailable.
- Before writing Musical Automation Mapping automation, resolve `docs/musical-automation-mappings.manifest.json` with `scripts/musical_automation_mapping.py`; writer modes should require `mapping_state = write_ready` by default.
- Before writer-like Ableton commands, refresh `scripts/ableton_awareness_snapshot.py snapshot --diff --json` or rely on the project `PreToolUse` hook; do not treat stale track/device/parameter indexes as current runtime truth.
- When running multiple AbletonOSC-facing commands in one agent turn, wrap them with `scripts/ableton_osc_queue.py exec` so UDP reply-port use stays single-flight.
- When a required Ableton or plug-in action is UI-only, load `ableton-computer-use-daw-adapter` and treat Computer Use as observe-act-verify UI control, not blind clicking. Use `app="/Applications/Ableton Live 12 Suite.app"` for Computer Use on this machine; never use the ambiguous name `Live`, and avoid `com.ableton.live` when installer volumes are mounted because the bundle id can be ambiguous.
- For transport-sensitive scripts, use `scripts/ableton_osc_queue.py exec -- ...`; the queue auto-selects `--command-timeout 0` for `automation_lane_recorder.py record` so the child script can run its own transport cleanup, and auto-sizes finite timeouts for `ableton_play_segment.py` / `ableton_play_session_scene.py` from the requested playback duration plus cleanup margin. If a finite recording timeout is necessary for a supervised failure-mode test, pass the explicit opt-in flag and verify `record_mode=false` plus `is_playing=false` before continuing.
