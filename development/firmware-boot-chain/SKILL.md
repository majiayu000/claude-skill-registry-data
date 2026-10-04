---
name: firmware-boot-chain
description: Use when building or debugging a firmware and boot chain (RISC-V SBI, UEFI, ACPI, a bootloader handoff like Limine to an OS) or adding measured boot with a TPM, and a stage fails to hand off to the next
---

# Firmware Boot Chain

## Overview

A boot chain is a relay of stages, each responsible for setting up just enough state to hand control to the next: ROM to firmware (SBI/UEFI), firmware to bootloader, bootloader to OS. Every handoff has a contract: where the next stage lives, what registers/tables it expects, and what memory is already set up.

**Core principle:** Each stage owns a contract with the next. Most boot failures are a broken contract at exactly one handoff, so isolate which handoff fails before theorizing about the stage itself.

## When to Use

- Writing or porting firmware (RISC-V SBI, UEFI services, ACPI table provision)
- Chaining a bootloader (Limine, GRUB, U-Boot) into an OS kernel
- A stage loads but the next never starts, or starts and immediately faults
- Adding measured boot / TPM PCR extension to the chain
- Discovering peripherals from a device tree or ACPI at firmware time

## Map The Handoffs First

Write down the relay before debugging:

```
ROM -> firmware (SBI/UEFI) -> bootloader -> OS kernel
        provides: SBI calls,    loads:        expects: a0=hartid,
        memory map, ACPI/DTB     kernel+initrd  a1=DTB/ACPI ptr, MMU off
```

For each arrow, name: the entry address, the register/pointer contract, and the memory/translation state. The failing arrow is your bug location.

## Firmware Responsibilities

- **Provide the platform description.** Hand the next stage a device tree (DTB) or ACPI tables describing memory, CPUs, and peripherals. Probe peripherals from this description rather than hardcoding addresses, so one firmware serves multiple board memory maps.
- **Set the entry contract precisely.** RISC-V convention passes hartid and a pointer to the platform description in fixed registers; get them exactly right. The next stage trusts them blindly.
- **Build-time configure the memory base.** RAM base and the firmware's own load address differ per board (for example external DRAM at a high base on one board, on-chip SRAM on another). Make these build-time parameters, not constants buried in one file.

## Bootloader Handoff Gotchas

These bite when chaining a general loader (for example Limine) into an OS:

- **Filesystem format constraints.** The loader may require a specific boot filesystem (FAT16, not FAT32) and a specific layout. Get this wrong and the loader silently finds nothing.
- **Timeout and entry config.** A nonzero menu timeout can stall an automated boot; a missing or misnamed entry just drops to a prompt.
- **Ramdisk/module placement.** The loader places initrd/modules in memory; make sure that placement doesn't collide with where the kernel expects to run or with the stack (see `bare-metal-bringup`).

## Measured Boot (TPM)

If the chain is measured:

- Drive the TPM over its real interface (TIS for TPM 2.0) and gate the whole probe on the platform description actually advertising a TPM. Don't assume presence.
- **Measure before you transfer control.** Each stage extends a PCR with a hash of the next stage (and relevant config) before jumping to it. Measuring after handoff measures nothing useful.
- Use the standard protocol surface (for example `EFI_TCG2_PROTOCOL`) and emit a TCG2 event log so the measurements are verifiable later.
- Test against a software TPM (swtpm) on the bench before trusting real silicon.

## Red Flags

| Smell | Do instead |
|-------|------------|
| Hardcoded peripheral addresses | Probe from DTB/ACPI |
| RAM base as a constant | Build-time parameter per board |
| "It doesn't boot" with no stage isolated | Identify the failing handoff first |
| TPM probe with no presence gate | Gate on the platform description |
| Extending a PCR after the jump | Measure-then-transfer |
| A rebuild that has no effect | Confirm the flashed slot is the one the ROM jumps to |
| Silent boot from a quad-read flash | Fall back to standard 0x03 to isolate flash config |
| Writing optional CSRs unconditionally | Probe each under a temp trap handler, skip absent ones |

## Midstall House Style

- Weir is the reference: pure-Zig RISC-V firmware (SBI/UEFI/ACPI), Limine to NixOS, measured boot with a TPM 2.0 TIS driver and TCG2 event log. Peripherals are discovered from the DTB; RAM base is build-time.
- See `boot-handoff-traps.md` in this directory: the first-stage failures that boot silent or run a stale image (reset-into-flash XIP needs a BRAM maskrom, a stale image at the real boot slot, a quad/QE flash mismatch, FSBL scratch colliding with the copy destination, a device-tree cell-size parser mismatch, and probing optional CSRs).
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji. Pairs with `bare-metal-bringup` for the early-output and translation rungs.
