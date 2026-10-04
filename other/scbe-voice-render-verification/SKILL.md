---
name: scbe-voice-render-verification
description: Govern and verify SCBE voice rendering work that maps Langues weighting into breath, phase, and Layer 14 audio-axis packets. Use when implementing or reviewing `scripts/voice_gen_hf.py`, emitting sidecar voice packets, validating canonical tongue ordering, tuning breath planning or phase timing, or keeping voice docs and code aligned with `docs/LANGUES_WEIGHTING_SYSTEM.md` and `docs/specs/SCBE_VOICE_EMOTIONAL_TIMBRE_SYSTEM.md`.
---

# SCBE Voice Render Verification

Use this skill when the task is to make SCBE voice work checkable, reproducible, and canon-aligned.

## Core Rules

1. Keep canonical tongue order `KO, AV, RU, CA, UM, DR`.
2. Preserve layer mapping `L3 -> tongue mixture`, `L6 -> breath`, `L7 -> phase`, `L14 -> audio realization`.
3. Emit or validate a sidecar packet whenever voice behavior is changed.
4. Prefer verifiable outputs: patched file, sample packet, validator result, targeted command output.
5. Do not claim breath realism from punctuation-only pauses.

## Read Order

When this skill triggers:

1. Read `references/source-map.md`.
2. Read `references/verification-checklist.md`.
3. Read only the repo files touched by the request.

Do not bulk-load unrelated audio, story, or emulator material.

## Workflow

1. Lock the task mode.
- Choose one: `docs`, `packet-schema`, `renderer-integration`, `qa`, or `review`.

2. Load canon.
- Read `C:\Users\issda\SCBE-AETHERMOORE\docs\LANGUES_WEIGHTING_SYSTEM.md`.
- Read `C:\Users\issda\SCBE-AETHERMOORE\docs\specs\SCBE_VOICE_EMOTIONAL_TIMBRE_SYSTEM.md`.
- Read `C:\Users\issda\SCBE-AETHERMOORE\scripts\voice_gen_hf.py` if code is touched.

3. Build or patch.
- For docs, keep the canonical layer mapping and fallback rules explicit.
- For code, emit `voice_packet` or `line.wav.json` sidecars instead of burying control state in prose.
- Preserve `speaker_baseline` separately from runtime timbre controls.

4. Verify.
- Run `scripts/validate_voice_packet.py` on a sample or generated packet.
- Run targeted syntax checks when code changes:
  - `python -m py_compile C:\Users\issda\SCBE-AETHERMOORE\scripts\voice_gen_hf.py`
- State whether the packet is `minimal` or `layer14`.

5. Report.
- Return changed files.
- Return validator status.
- Return what remains unimplemented in the renderer.

## Packet Contract

Use one of two modes.

### Minimal Packet

Use for preprocessing or planning before synthesis.

Required fields:
- `speaker`
- `text`
- `profile`
- `scene_intensity`
- `tongue_logits`
- `speaker_baseline`

### Layer 14 Packet

Use for governed render output.

Required fields:
- `speaker`
- `text`
- `tongue_mix`
- `timbre`
- `breath_plan`
- `phase`
- `render`

Use `assets/voice-packet.example.json` as the baseline sample.

## Verification

Default validator command:

```powershell
python C:\Users\issda\.codex\skills\scbe-voice-render-verification\scripts\validate_voice_packet.py `
  C:\Users\issda\.codex\skills\scbe-voice-render-verification\assets\voice-packet.example.json
```

Validation should prove:

- canonical tongue keys are present
- tongue values are numeric
- `tongue_mix` sums to `1.0` within tolerance
- breath entries use allowed kinds
- timbre keys are complete

## Resources

- `references/source-map.md`
- `references/verification-checklist.md`
- `scripts/validate_voice_packet.py`
- `assets/voice-packet.example.json`
