---
name: reference-driven-rohd
description: Use when implementing a hardware block, protocol, peripheral, or ISA feature in ROHD and you should ground it in the authoritative spec, existing reference implementations, and reusable libraries you fetch first, instead of writing it from memory
---

# Reference-Driven ROHD

## Overview

Writing a protocol or peripheral from memory is how you ship a design that is subtly wrong: a reserved bit in the wrong place, a handshake that almost matches the spec, an edge case the standard calls out that you never saw. The fix is cheap and boring: get the real sources first, then implement against them.

**Core principle:** Before writing custom ROHD, fetch the authoritative spec, the existing reference implementations, and any reusable library that already solves part of the problem. Implement from primary sources, not from recall. The spec is the oracle, the references show the behavior, the library saves the parts you should not rewrite.

## When to Use

- Implementing a standardized block (a bus, a UART, an SPI controller, a CRC, an ECC, a CSR file, an ISA extension)
- Building something that must interoperate with hardware or software you do not control
- You are about to write RTL from your own memory of how the protocol works
- A datasheet, RFC, ISA manual, or vendor spec exists for what you are building

Skip for genuinely novel internal logic that has no external spec and no prior art.

## Fetch The Sources First

Do this before writing a line of RTL. Three buckets, in order:

1. **The authoritative spec.** The actual standard, datasheet, or ISA manual, not a blog summary. RISC-V unprivileged/privileged manuals, the Wishbone B4 spec, a part's datasheet PDF, the protocol's RFC. Use WebFetch/WebSearch to pull it, and note the exact version and section numbers. A spec you cite by section is a spec you can be held to.
2. **Existing reference implementations.** Other HDL (Verilog/Chisel/SpinalHDL/migen), a C model, a vendor reference, an emulator. Clone or fetch them to read the behavior, especially the corner cases and reset values. These show you what the spec leaves ambiguous and how real implementations resolved it.
3. **Reusable libraries.** Check `rohd_hcl` and existing Midstall ROHD (River, Harbor) before writing anything new. A FIFO, ECC, ready/valid handshake, rotator, or arbiter is probably already there, tested. Compose it; do not reinvent it.

If you cannot find a source for something the block needs, that gap is the first thing to resolve, not to guess past.

## Build A Spec-To-RTL Map

Turn the fetched spec into a checklist before implementing:

- List every field, register, state, and transition the spec defines, each tagged with its spec section.
- Note reset values, reserved bits, and the must/should/may distinctions explicitly. Reserved is not "do whatever"; the spec usually says read-zero or preserve.
- Mark the edge cases the spec calls out (wrap, overflow, back-pressure, error responses). These are the ones memory drops.
- Each item becomes something the implementation handles and a test asserts. A spec line with no corresponding test is a line you are trusting to luck.

## Reference Implementations Inform, They Do Not Get Pasted

You read references to understand behavior, then write your own clean ROHD.

- **Provenance matters for silicon.** Do not paste code whose license is incompatible with the project into a clean design. Read it, understand the behavior, reimplement it in ROHD. Reimplementation from understanding is clean; copy-paste carries the license with it.
- A reference shows you the timing and the corner cases. Your job is to express that behavior in idiomatic ROHD with build-time-validated config, per `hdl-module-design`.
- When references disagree with each other, the spec breaks the tie. When a reference disagrees with the spec, the reference may be buggy or may know something the spec implies; dig until you know which.

## Turn The Reference Into A Golden Test

The reference implementation or C model you fetched is not just documentation, it is a verification oracle.

- Run your ROHD DUT and the reference against the same stimulus and compare, the differential-verification pattern. The reference becomes the golden model.
- If the reference is a C model or emulator, drive both with the same vectors and diff the outputs cycle-relevant signals.
- Cover every item from the spec-to-RTL map, including the reserved-bit and error-response cases the reference exercises.

## Red Flags

| Smell | Do instead |
|-------|------------|
| "I know how SPI works, I'll just write it" | Fetch the datasheet and an existing controller first |
| Implementing a CRC/ECC/FIFO from scratch | Check `rohd_hcl` and existing ROHD first |
| Citing the protocol from memory | Cite the spec by version and section number |
| Pasting GPL/incompatible RTL into a clean design | Read it, reimplement the behavior cleanly in ROHD |
| Reserved bits left to "whatever the tools do" | Implement read-zero/preserve as the spec states |
| No golden model when a reference exists | Diff the DUT against the reference as the oracle |

## Midstall House Style

- River and Harbor are pure ROHD/Dart; new blocks compose `rohd_hcl` and existing modules before adding custom RTL.
- Heimdall's verification leans on golden models (Spike for the ISA, SPICE for analog); a fetched reference implementation plays the same role for a new block.
- Record the spec version and section numbers you implemented against, in the conversation or a comment, so the next person can check the design against the same source.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji, no slang. Pairs with `hdl-module-design` for the module shape, `rohd-rtl-gotchas` for the ROHD pitfalls, and `differential-verification` for the golden-model harness.
