---
name: kicad-netlist
description: Parse KiCad `.net` netlist exports (S-expressions) to list components, list nets, show a net's nodes, or trace which net each pin of a part connects to. Use when investigating board connectivity, power/ground topology, or which components share a net, given a KiCad `.net` file.
---

# KiCad netlist parser

`parse_net.py` parses a KiCad netlist export (`*.net`, S-expression) with
`sexpdata` and answers connectivity questions. Regex does **not** work on these
files — the nested parens defeat it — so always use this, not `grep`.

Dependencies are inline (PEP 723), so run it with `uv` — nothing to install:

```bash
DIR=.claude/skills/kicad-netlist
uv run $DIR/parse_net.py FILE.net components      # ref, value, footprint
uv run $DIR/parse_net.py FILE.net nets --min 2    # nets with >= 2 nodes (skip no-connects)
uv run $DIR/parse_net.py FILE.net net "+3V3"      # every pin on one net
uv run $DIR/parse_net.py FILE.net pins U1         # each pin of U1 -> the net it's on
```

## What each subcommand answers

- **`pins REF`** — power/pinout topology of one part: which rail each power pin
  sits on, where each signal goes. The fastest way to see, e.g., whether an
  MCU's USB-VBUS pin and an external supply land on the same net.
- **`net NAME`** — everything electrically tied together on that net (all
  `ref.pin` nodes). Use for a rail (`GND`, `+5V`) or any signal.
- **`nets --min 2`** — skim the real nets; `--min 2` drops single-node
  no-connects so the list is readable.
- **`components`** — the BOM-ish list (ref, value, footprint).

## Notes

- The input is a KiCad **netlist export** (Schematic Editor → File → Export →
  Netlist → KiCad, or `kicad-cli sch export netlist FILE.kicad_sch`), *not* the
  `.kicad_sch` itself.
- Net names come from schematic labels; unlabelled nets get auto names like
  `Net-(U1-Pad12)`.
