---
name: hdl-module-design
description: Use when writing, refactoring, or deciding how to test an HDL module, component, or IP block (ROHD, Chisel, SpinalHDL, Verilog, VHDL) and you need it parameterized, validated, and covered by exhaustive tests rather than a one-off
---

# HDL Module Design

## Overview

A hardware module is an interface plus an implementation. Get the interface and its configuration right and the implementation stays swappable, testable, and reusable across an FPGA and an ASIC.

**Core principle:** A module should declare exactly what it needs as typed configuration, validate it at build time, and be exhaustively testable in isolation. If you can't construct and test it without the rest of the SoC, the boundary is wrong.

## When to Use

- Writing a new peripheral, datapath, control block, or reusable IP
- A module takes a pile of bare `int`/`String`/`bool` constructor args
- Configuration is validated late (at elaboration or simulation) instead of at construction
- Domain logic is leaking into the CLI/generator wrapper instead of the library
- Tests only exercise the top level, not the component

Skip for throwaway testbench glue or a one-line wire rename.

## Design The Configuration First

Hardware bugs are expensive, so push errors as early as possible: ideally a type error, otherwise a build-time assertion, never a silent miscompile.

1. **One config object per module.** Group the parameters into an immutable config type with named, typed fields. The module takes the config, not a long positional arg list.
2. **Types, not strings.** Use enums for modes, kinds, and identifiers. `BusKind.axi4` not `"axi4"`. A typo becomes a compile error instead of a wrong build.
3. **Validate at construction.** Width relationships, power-of-two requirements, address-range overlaps, legal mode combinations: assert them when the config is built, with a message that names the offending field and value. Do not defer to simulation.
4. **Derive, don't duplicate.** If `addrWidth` is a function of `depth`, compute it. Don't make the caller pass both and hope they agree.

```dart
// ROHD-flavored, but the shape is language-neutral.
class FifoConfig {
  final int depth;
  final int width;
  const FifoConfig({required this.depth, required this.width});

  // build-time validation, names the bad field
  void validate() {
    if (depth <= 0 || (depth & (depth - 1)) != 0) {
      throw ArgumentError('FifoConfig.depth must be a power of two, got $depth');
    }
    if (width <= 0) {
      throw ArgumentError('FifoConfig.width must be positive, got $width');
    }
  }

  int get addrWidth => depth.bitLength - 1; // derived, not passed in
}
```

## Keep Logic In The Library

The module and its elaboration logic live in the library. The CLI, build script, or generator is a thin wrapper that parses args and calls library methods. This keeps the module usable by other code (other generators, tests, third parties) and keeps the surface testable without spawning a process.

If you find yourself reaching into a module's internals from the CLI, lift that into a library method.

## Test Every Component, Exhaustively

This is going to silicon. A miss is a respin.

- **Mirror the source layout in tests.** `lib/components/fifo.dart` -> `test/components/fifo_test.dart`, `lib/config/...` -> `test/config/...`. Anyone can find the test for a unit.
- **Test each component on its own**, not only through the top level. Small units with clean boundaries are why this is possible.
- **Cover the config validation**: assert the bad inputs actually throw.
- **Sweep the parameter space** for parameterized modules: a representative set of widths/depths/modes, plus the boundaries (width 1, max depth, every enum value).
- **Use non-default, non-zero operands.** Test data at the reset default or offset 0 masks a whole bug class. A store suite where every offset is 0 never exercises sign-extension, so a broken sign-extend passes. A vector op run only at the default element width hides a scalar laid out at a fixed width. Drive non-default values on purpose, and exercise every access width and beat position so a narrow access does not leave the wide word untested.
- A failing check must fail. Never add an `ignore`/`skip`/`ERROR_ON_X=false` knob to make a violating design pass. Fix the design. See [[failures-should-fail]] in the silicon-grade-discipline skill.

## Red Flags

| Smell | Do instead |
|-------|------------|
| 8 positional `int` args | One typed config object |
| `mode == "fast"` | `mode == Mode.fast` (enum) |
| Width mismatch caught in sim | Assert it at config construction |
| Logic in the CLI command | Library method, CLI calls it |
| Only top-level tests | One test file per component, mirrored layout |
| `skipDrc = true` to get a pass | Fix the design |

## Midstall House Style

- ROHD/Dart: config classes use `const` constructors with `final` fields.
- ISA-extension capabilities derive from the microcode/ISA description; privilege modes stay constructor flags. Derive, don't restate.
- Build a reusable unit standalone with a golden test before wiring it in; it de-risks correctness and locks the interface.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes in code, comments, or docs. No emoji.
- For ROHD/rohd_bridge/rohd_hcl sim and emission pitfalls see `rohd-rtl-gotchas`. See `silicon-grade-discipline` for the failures-should-fail and no-over-engineering rules this leans on.
- See `usb-fs-softphy-dfu-silicon-bugs.md` in this directory: a worked catalogue of the silicon-grade bugs in a full-speed USB soft-PHY + EP0/DFU engine + SPI-NOR write engine (clock-recovery sample point, consecutive-SE0 EOP, async-FIFO data-storage and back-pressure, SET_ADDRESS/ZLP/toggle/SETUP-catch, flash erase/program arbitration), each one a happy-path-passing trap caught only by adversarial review.
