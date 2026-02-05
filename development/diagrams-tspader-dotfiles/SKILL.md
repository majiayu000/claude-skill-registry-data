---
name: diagrams
description: Use when generating any diagrams using ASCII and Unicode characters.
---

# Diagrams
## Quick Reference
**Box drawing (single):**
```
┌───┬───┐
│   │   │
├───┼───┤
│   │   │
└───┴───┘
```

**Box drawing (double):**
```
╔═══╦═══╗
║   ║   ║
╠═══╬═══╣
║   ║   ║
╚═══╩═══╝
```

**Tree characters:** `├── └── │`

**Arrows:** `→ ← ↑ ↓ ↔ ↕ ⟶ ⟵`

**Blocks:** `█ ▀ ▄ ▌ ▐ ░ ▒ ▓`

## Diagram Types

| Type | Use Case | Reference |
|------|----------|-----------|
| Memory layouts | Struct fields, memory regions, pointers | [memory-layouts.md](references/memory-layouts.md) |
| Bit layouts | Register bits, flags, binary formats | [bit-layouts.md](references/bit-layouts.md) |
| Boxes/frames/tables | Bordered text, headers, data tables | [boxes-frames.md](references/boxes-frames.md) |
| Banners | Large text logos, titles | [banners.md](references/banners.md) |
| Flowcharts | Process flows, decisions | [flowcharts.md](references/flowcharts.md) |
| Trees | Directory structure, hierarchies | [trees.md](references/trees.md) |
| Sequences | Message flows, timelines | [sequences.md](references/sequences.md) |

Full character reference: [characters.md](references/characters.md)

## Guidelines

- **Width**: Keep under 80 chars for code comments, 120 for documentation
- **Alignment**: All box characters assume monospace font
- **ASCII fallback**: Use `+`, `-`, `|` when Unicode unavailable
- **Consistency**: Pick single or double line style, don't mix within a diagram
