---
name: fpga-bringup
description: Use when loading a bitstream onto a physical FPGA and driving or observing it over JTAG or GPIO, especially bit-banged JTAG from a host like a Raspberry Pi, or when configuration silently fails
---

# FPGA Bring-Up

## Overview

Bringing up an FPGA on the bench means three things: get the bitstream in over a real transport, drive the design's inputs, and observe its outputs. Most early failures are transport and pin-mapping problems, not logic problems.

**Core principle:** Bring the transport up first and prove it independently, before you trust anything the design does. A bitstream that "loaded" but didn't is the most expensive hour on the bench.

## When to Use

- Loading a bitstream onto a board over JTAG, SPI, or a custom config chain
- Bit-banging JTAG from GPIO (Pi-as-host, no FTDI/FT2232)
- Driving test vectors into pins and reading results back
- Configuration "succeeds" but the design doesn't run

## Bring Up The Transport First

Before any design-level work, prove the link end to end:

1. **Read the IDCODE.** Shift the JTAG IDCODE instruction and confirm the value matches the part. If IDCODE is wrong or all-ones/all-zeros, you have a wiring, voltage, or clock problem. Stop here and fix it. Nothing downstream matters yet.
2. **Confirm the IR width.** The instruction register width is part-specific and must match the design's TAP. A wrong IR width shifts every instruction into garbage and configuration silently no-ops. Make the IR width a parameter, not a magic constant baked in one place.
3. **Confirm clock and levels.** TCK speed, signal voltage, pull directions. Bit-banged GPIO has no buffering; mind the levels and keep TCK slow until the link is proven.

## Load The Bitstream

- Use the part's documented configuration instruction (for example a JTAG `CONFIG` opcode) to enter config mode, then shift the bitstream.
- After load, read back a status or DONE indication. Do not assume success from "the shift completed." A clocked-but-ignored shift looks identical to a real one.
- If load fails intermittently, suspect TCK too fast, marginal levels, or a shared bus contending during config.

## Generate The Bitstream At A Safe Clock

Before you blame the bench, confirm the bitstream's configured clock is at or below the design's real Fmax. The PLL output, UART baud divisor, and timer timebase all derive from it. A bitstream configured for 48 MHz on logic that only times at 29 MHz fails with setup violations AND a wrong baud rate, which looks exactly like a wiring or transport fault. Regenerate at a clean integer PLL divide below Fmax. See `fpga-synthesis-fit`.

## The PLL Must Actually Lock

A dead-silent board with a clean configuration load is very often a PLL that never locked, not a logic or wiring fault. When the design gates reset on `~LOCK` (the common `sysReset = porReset | ~LOCK`), a PLL that never locks holds the core in reset forever and every output stays dead.

Check the VCO math from the emitted PLL parameters BEFORE you flash:

- The ECP5 VCO must land in the legal band (roughly 400 to 800 MHz). `fVCO = fIN / CLKI_DIV * CLKFB_DIV`. A hardcoded `CLKI_DIV = 1` that cannot divide a 48 MHz oscillator down to a 24 MHz system clock drives `fVCO` to 1584 MHz, out of band, no lock. Realize the ratio as a reduced fraction (`CLKFB_DIV : CLKI_DIV` by gcd) so the divider is honest.
- The constraint file's input-frequency line (`FREQUENCY PORT "clk"` in the `.lpf`) must carry the OSCILLATOR frequency on the pin, not the system frequency. Constrain it to the system freq and the tool derives the VCO from the wrong input (24/2*25 = 300 MHz, out of band) and writes analog and loop settings the silicon never runs, even though the gateware is correct.
- Loop-filter attributes (ICP_CURRENT, LPF_RESISTOR, MFG_*) are a red herring here. They are not even valid yosys EHXPLLL parameters; chasing them wastes hours. The fix is the divider math and the input-frequency constraint.

A second PLL whose LOCK is unconnected (a DDR PHY PLL that does not gate core reset) can carry the same divider bug silently until you bring that block up.

## Partition The Design In Sim Before Blaming The Bench

Before bench guessing, partition logic from analog in simulation. Generate the design with NO target (sim-passthrough clock, external reset, flop memories, no PLL or block-RAM blackboxes), dump the SystemVerilog, and run it under a fast compiled simulator (Verilator). If the design streams its output here, the LOGIC is correct and the suspect is the PLL or a primitive the flop sim does not model. An interpreted RTL sim is usually too slow for a full boot (tens of thousands of cycles to first output); a compiled sim does it in a fraction of a second after a one-time compile. Lower the clock or UART divisor to shrink the run.

To sim the REAL netlist instead of the flop stand-in, supply functional models for the vendor blackboxes. The yosys `ecp5/cells_sim.v` DP16KD is a pure stub: it declares the INITVAL params but has no read or write logic, so a real-netlist sim reads every block-RAM ROM as zero and the core hangs at instruction zero. That hang is a SIM ARTIFACT, not a hardware bug. Write a functional primitive model (unpack INITVAL per `fpga-synthesis-fit`'s `dp16kd-initval-packing.md`, clocked read and write) plus a behavioral PLL and config stub, and the real netlist runs, isolating the remaining failure to the analog PLL the stub cannot model.

## When Sim Says OK But The Chip Is Silent: Probe One Layer At A Time

When every simulation passes but the assembled design is dead on the board and you cannot observe internals, do NOT keep theorizing. Build a ladder of tiny bitstreams, each bit-banging ONE diagnostic byte out the UART pin, each isolating a single layer, from the rawest signal upward:

1. Raw-oscillator streamer (a fixed byte clocked straight off the input pin): proves the oscillator, FPGA configuration, the pin, and the host adapter.
2. PLL-lock probe (emit one letter if LOCK else another, bit-banged from the raw clock): proves the PLL locks.
3. PLL-output probe (clock the streamer FROM the PLL output): proves CLKOP is a clean frequency.
4. Reset-path probe (replicate POR plus LOCK plus reset-sync, emit the stage letter): proves reset releases.
5. Real-primitive probes (instantiate the actual SRAM, block RAM, or regfile, write a known value, read it back, stream it): prove each memory primitive on silicon, with INITVAL reads and runtime writes as separate probes.
6. Core-liveness heartbeat (rewire the UART to bit-bang the core's own PC or bus address as a letter: stuck, moved, or never-fetched): localizes a stuck core.

Each probe builds in about two minutes and routes in seconds. When every block passes in isolation, the conclusion is forced: it is the assembled, timing-loaded design, not any one block. Prefer a NON-latching live indicator (a heartbeat reflecting the current state) over a latching one; "it got a bit further when I slowed the clock" can be a latching-probe artifact or routing variation, not real progress, on a marginal high-utilization design.

## Map The Pins Explicitly

Keep a pad map in config (a file, not scattered constants): logical signal name -> device pad -> host GPIO line. Every drive and observe goes through this map.

- Open the GPIO lines on `prepare`, close them on `release`. Own the lifecycle so a crashed run doesn't leave lines claimed.
- Drive inputs, settle, then sample outputs. Respect setup/hold; don't sample combinationally before the design has propagated.
- A `RunVector` is: set inputs per the pad map, pulse/settle, read outputs per the pad map, compare to expected.

## Host Setup (Pi-as-host)

- Use the Linux character-device GPIO interface (gpiod / cdev), not the deprecated sysfs path.
- The host user needs the right group to access GPIO; a diagnostics step that checks group membership, tool presence, and line availability saves a lot of confusion.
- Bit-banged JTAG works without an FTDI adapter, which is the point: fewer parts on the bench.

## Red Flags

| Smell | Do instead |
|-------|------------|
| Assuming load worked because the shift finished | Read back DONE/status |
| IR width hardcoded in one spot | Parameterize it; confirm against the part |
| Pin numbers scattered through code | One pad map, name -> pad -> GPIO line |
| Sampling outputs immediately | Settle for propagation first |
| sysfs GPIO | character-device GPIO (cdev/gpiod) |
| Skipping IDCODE | Always read IDCODE before trusting the link |
| Dead UART, chasing loop-filter attrs | Check the VCO band and the `.lpf` input freq first |
| Theorizing about why the chip is silent | Probe one layer at a time out the UART pin |
| Trusting a real-netlist sim that hangs at instr 0 | yosys DP16KD is a stub; supply a functional model |
| 0-byte UART capture read as a boot hang | Confirm the flash command actually ran; zsh no-op |
| OpenOCD reads garbage dtmcontrol, blaming the RTL | Reload the bitstream and retry; it is often transient |
| Early boot prints missing | UART drops the first seconds after reconfig; re-print late |
| Building a DQS-strobed read capture on the open flow | Capture on CK plus calibration; DQS pins are not clock-capable |
| Running DDR3 at 200 MHz CK to "de-risk" | Below the DLL's slowest rated bin; drive 400 MHz plus or gate on DQS |
| A lane reads exactly 0x00, chasing the eye | Exact 0x00 is a whole-strobe framing failure, not tight timing |
| Tuning writes before proving the read path | Read the DDR3 MPR to prove the lane and read path first |

## Midstall House Style

- Aegis over bit-banged JTAG from a Pi host is the reference setup; the IR width is parameterized and the loader uses the documented JTAG CONFIG opcode.
- The pad map lives in config (heimdall.toml style), resolved at startup. GPIO transports open on prepare and close on release.
- The `creek` core's first OrangeCrab 25F bring-up needed five stacked fixes (two PLL/VCO bugs, a regfile write-mode quirk, and two logic bugs), each isolated by the probe ladder and the partition sim above.
- See `onchip-microprobe-ladder.md` in this directory: the bit-bang-one-byte-per-layer diagnostic ladder for a silent chip, the silicon-only DP16KD x18-runtime-write gotcha, and the faithful-primitive partition sim.
- See `ddr3-read-capture-open-flow.md` in this directory: the DDR3 read-path bring-up on Spartan-7 with openXC7 (capture on CK plus calibration not a DQS strobe, DQS pins are not clock-capable, do not underclock below the DLL bin, IDELAYCTRL for absolute taps, exact-0x00 is a strobe framing fault, MPR proves a lane read-perfect, CL+1 shifts capture by a whole memory clock).
- See `bench-and-capture-gotchas.md` in this directory: the silent no-ops that look like hangs (a multi-word command that zsh does not word-split, UART dropping the first seconds after reconfig, stale UART readers splitting the stream, transient garbage JTAG state), and widening a marginal capture eye by slowing the clock with its analog-spec floor.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji. Pairs with `differential-verification` for comparing observed outputs against a golden model, and `fpga-synthesis-fit` for the clock and block-RAM details.
