---
name: IT Format (Impulse Tracker)
description: |
  Use this skill for IT file generation - the more powerful of the two tracker formats. Provides Python library for programmatic IT creation with advanced features.

  **Trigger phrases:** "generate IT", "write IT file", "Impulse Tracker", "procedural IT", "NNA", "pitch envelope", "IT effects"

  **Load references when:**
  - Effect command details → `references/it-effects.md`
  - NNA, envelopes, filters → `references/workflow-guide.md`
  - Binary format details → `references/it-format-spec.md`

  **Use IT when:**
  - Need >32 channels (IT: 64)
  - Need NNA polyphony (notes fade/continue)
  - Need pitch envelopes
  - Need resonant filters

  **Use XM instead when:** Simpler songs, smaller file size, features sufficient.

  For composition philosophy, use `tracker-fundamentals`.
  For music theory, use `sound-design:music-composition`.
version: 1.1.0
---

# IT Format (Impulse Tracker)

## Overview

IT is the more advanced format with features beyond XM.

**Key advantages:**
- Up to 64 channels (vs 32)
- 10 octaves (vs 8)
- NNA (New Note Actions) for polyphony
- Pitch envelopes
- Resonant filters

## Quick Start

```python
from it_writer import ItModule, ItPattern, ItNote, ItInstrument, ItSample, write_it

pattern = ItPattern.empty(64, num_channels=4)
pattern.set_note(0, 0, ItNote.play("C-4", instrument=1, volume=64))

module = ItModule(
    name="My Song",
    num_channels=4,
    default_speed=6,
    default_bpm=125,
    order_table=[0],
    patterns=[pattern],
    instruments=[ItInstrument(name="kick")],
    samples=[ItSample(name="kick", c5_speed=22050, default_volume=64)],
    sample_data=[kick_bytes]
)

write_it(module, "output.it")
```

## Core API

### ItNote

```python
ItNote.play("C-4", instrument=1, volume=64)   # Note on
ItNote.play_note(60, 1, 64)                    # MIDI number
ItNote.off()                                    # Note off (^^^)
ItNote.cut()                                    # Note cut (===)
ItNote.fade()                                   # Note fade

# Chainable:
note = ItNote.play("C-4", 1, 64).with_effect(7, 0x10)  # G10
```

### ItPattern / ItInstrument / ItSample / ItModule

Same pattern as XM - see `references/workflow-guide.md` for full examples.

## Common Effects

IT uses letter-based effects (A=1, B=2, ...):

| Effect | Letter | Code | Usage |
|--------|--------|------|-------|
| Set Speed | A | 1 | `.with_effect(1, 6)` |
| Vol Slide | D | 4 | `.with_effect(4, 0x0F)` |
| Porta Down | E | 5 | `.with_effect(5, 0x10)` |
| Porta Up | F | 6 | `.with_effect(6, 0x10)` |
| Tone Porta | G | 7 | `.with_effect(7, 0x10)` |
| Vibrato | H | 8 | `.with_effect(8, 0x34)` |
| Arpeggio | J | 10 | `.with_effect(10, 0x37)` |
| Set Tempo | T | 20 | `.with_effect(20, 125)` |

See `references/it-effects.md` for complete list.

## NNA (New Note Actions)

NNA controls polyphonic behavior - what happens to previous notes when new ones play.

```python
from it_writer import NNA_CUT, NNA_FADE, NNA_CONTINUE, DCT_NOTE, DCA_FADE

# Polyphonic piano - previous notes fade when new ones play
piano = ItInstrument(
    name="Piano",
    nna=NNA_FADE,         # Fade previous note
    dct=DCT_NOTE,         # Check for duplicate notes
    dca=DCA_FADE,         # Fade duplicates
    fadeout=512,          # Fade speed (0-1024)
)
```

| NNA Mode | Behavior | Use For |
|----------|----------|---------|
| NNA_CUT | Cut previous note | Leads, bass (default) |
| NNA_FADE | Fade previous | Piano, pads, strings |
| NNA_CONTINUE | Continue previous | Drones, ambient |

## Envelopes

### Volume Envelope (ADSR)

```python
from it_writer import ItEnvelope, ENV_ENABLED, ENV_SUSTAIN_LOOP

env = ItEnvelope()
env.points = [(0, 0), (10, 64), (30, 48), (100, 48), (130, 0)]
env.sustain_begin = 2
env.sustain_end = 3
env.flags = ENV_ENABLED | ENV_SUSTAIN_LOOP

instr = ItInstrument(name="Pad", volume_envelope=env)
```

### Pitch Envelope (IT-only)

```python
# Kick drum with pitch drop
pitch_env = ItEnvelope()
pitch_env.points = [(0, 24), (15, 0)]  # Start +24 semitones, drop to normal
pitch_env.flags = ENV_ENABLED

kick = ItInstrument(name="Kick", pitch_envelope=pitch_env)
```

See `references/workflow-guide.md` for more envelope examples.

## Filters (IT-only)

```python
bass = ItInstrument(
    name="Filtered Bass",
    filter_cutoff=64,      # 0-127
    filter_resonance=32,   # 0-127
)
```

## Validation

```python
from it_writer import validate_it
validate_it("output.it")
```

## Parser Location

The IT writer is part of the unified `.studio/` infrastructure.

**Source:** `ai_studio_core/templates/project/studio/parsers/`
- `it_writer.py` - IT file writing
- `it_types.py` - IT data structures

**Setup:** Run `/init-procgen` to install the `.studio/` scaffold (generator + parsers).

## Project Structure

```
project/
├── .studio/parsers/
│   ├── it_writer.py     # Downloaded via /init-procgen
│   └── it_types.py
├── .studio/specs/music/
│   └── song_name.spec.py
└── generated/music/
    └── song_name.it     # Output (gitignored)
```

## XM vs IT Decision

| Feature | XM | IT |
|---------|----|----|
| Channels | 32 | 64 |
| Polyphony | Note-off only | NNA |
| Pitch envelope | No | Yes |
| Resonant filter | No | Yes |
| File size | Smaller | Larger |

**Choose IT when:** Polyphonic instruments, pitch effects, filters, or >32 channels needed.

## API Reference Files

- **`.studio/parsers/it_types.py`** - API surface (~280 lines, READ THIS)
- **`.studio/parsers/it_writer.py`** - Binary packing (just import)
- **`references/it-effects.md`** - Complete effect reference
- **`references/workflow-guide.md`** - NNA, envelopes, filters, examples
- **`references/it-format-spec.md`** - Binary format specification
