---
name: beatflow-skill
description: Compose, revise, validate, compare, inspect, and export original multi-track music as Standard MIDI with BeatFlow's compact, style-neutral Python DSL. Use for turning a musical brief into a deterministic Composition, testing explicit phrase/counterpoint/theme contracts, or inspecting MIDI.
license: GPL-3.0-only
---

# BeatFlow

Use Codex for musical decisions and BeatFlow for exact timing, functional pitch
realization, validation, diagnostics, MIDI rendering, and inspection.

Run `python "<skill-root>/scripts/run.py" <command> ...`. Write scripts and
outputs in the user's workspace, never inside `<skill-root>`.

## Workflow

1. Extract duration, tempo, meter, tonal center, form, instrumentation, energy
   path, priorities, and exclusions. Make reversible assumptions when needed.
2. Read [composition-format.md](references/composition-format.md) before
   authoring. Read [diagnostics.md](references/diagnostics.md) only when adding
   explicit contracts, comparing candidates, or revising findings. Read
   [architecture.md](references/architecture.md) only for runtime maintenance.
3. Plan the shared clock, harmony, bass, role entries, rests, foreground,
   arrivals, and development before adding decoration.
4. Author a trusted Python file whose `build()` returns `Composition`. Prefer
   `SongBuilder` and exact `beat()` values. Style belongs in authored material,
   not compiler branches.
5. Keep identity-bearing material recognizable before transforming it. Declare
   phrases, interactions, counterpoint, themes, or silence only when the brief
   makes them testable.
6. Render and inspect:

```text
python "<skill-root>/scripts/run.py" compose song.py --midi song.mid --composition song.composition.json --report song.report.json
```

7. Treat validation errors as hard failures. Treat diagnostics as evidence
   against declared intent, never as a universal taste score. Listen before
   making the final musical judgment.

## Constraints

- Keep timing quantized unless the user explicitly requests timing variation.
- Count the perceptual tactus; do not assume every quarter note is one felt beat.
- Preserve essential instruments; repair writing or balance before dropping them.
- Give foreground a clear rhythmic identity, internal contrast, and arrival.
- Coordinate roles without forcing identical attacks.
- Use `top_target` when a chord's top voice carries the line.
- Keep all realized onsets and durations explicit.
- Create original music; do not copy a reference melody or imitate a living artist.
- Treat General MIDI as a preview, not final production timbre.

## Commands

- `compose SCRIPT --midi MIDI [--composition JSON] [--report JSON]`
- `analyze COMPOSITION [--output REPORT]`
- `compare COMPOSITION... [--revision] [--output REPORT]`
- `inspect [MIDI|COMPOSITION] [--schema] [--output REPORT]`
- `self-check`

## Interruptions

The Python source is the durable checkpoint. `--composition` is written
atomically before MIDI rendering, and MIDI/report outputs are also atomic.
After interruption, rerun the same command; deterministic realization restarts
cheaply without requiring an internal project cache.
