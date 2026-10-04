---
name: cortex-r5-debug
description: Use when debugging Cortex-R5 or Cortex-R firmware — TCM, MPU, caches, DFSR/DFAR aborts, exceptions, GIC/VIC interrupts, lockstep or split mode, ECC, or JTAG bring-up
---

# Cortex-R5 Debug

## Overview

Use this skill to debug Cortex-R5 (ARMv7-R, PMSA) systems by separating core mode, boot source, memory map, exception vectors, TCM, MPU/cache policy, interrupt controller, and safety configuration. Cortex-R5 uses an `MPU` (not an MMU) and CP15-based control; failures usually come from memory attributes, ECC/TCM setup, or lockstep configuration rather than C code.

## When To Use

Use this skill when:

- The user is bringing up or debugging Cortex-R5/R5F, Cortex-R4, or Cortex-R7 firmware (Xilinx Zynq UltraScale+ RPU, TI Hercules/Sitara, and similar).
- The issue involves early boot, Undefined/Prefetch Abort/Data Abort exceptions, IRQ/FIQ, ATCM/BTCM, MPU regions, caches, ECC/parity, lockstep, split mode, or JTAG attach.
- The platform is an SoC with real-time cores, safety islands, motor/control firmware, storage controllers, or heterogeneous Linux + R5 systems.

Do not use this skill for Cortex-M microcontrollers. Use `cortex-m-debug` when the target has `NVIC`, `VTOR`, and M-profile exception behavior instead of CP15/CPSR.

## First Questions

Ask for:

- SoC/board, exact core, boot owner, toolchain, debugger, and whether the R5 runs bare metal or an RTOS.
- Core mode: single core, split (performance) mode, or lock-step (`DCLS`); which core the debugger is attached to.
- Memory map: boot ROM, flash, DDR, OCM/SRAM, `ATCM`/`BTCM` base and size, stacks, heaps, and linker script.
- MPU/cache policy, TCM enable state (`INITRAMA`/`INITRAMB` reset straps), ECC init, and DMA/coherency paths.
- Exception symptom plus a dump of `CPSR`/`SPSR`, `DFSR`/`DFAR` (data abort) or `IFSR`/`IFAR` (prefetch abort), `LR`, and disassembly around `PC`/`LR`.

## Debug Workflow

1. Prove debugger attach and reset control.
   Confirm JTAG target and core selection, reset type, and halt behavior. Read `MIDR` and `MPIDR` to confirm you are on the expected R5 core, and check whether the sibling R5 or an A-core changes state.

1. Verify boot entry.
   Check the reset vector and vector base. Vectors sit at `0x00000000` or at `0xFFFF0000` when `SCTLR.V` (bit 13) is set. Verify per-mode banked stacks are set for `SVC`, `IRQ`, `FIQ`, `ABT`, `UND`, and `SYS` before C runtime init.

1. Stabilize memory first.
   Enable and scrub `ATCM`/`BTCM` before use — set the base+enable in the ATCM/BTCM Region Registers (`MRC/MCR p15, 0, Rt, c9, c1, 0` for ATCM, `c9, c1, 1` for BTCM; bit 0 is Enable). Initialize ECC-protected RAM (write to establish valid ECC) before any read. Init BSS/data and stacks before touching DDR or cached regions.

1. Configure MPU/cache deliberately.
   Read `MPUIR` (`MRC p15, 0, Rt, c0, c0, 4`) for region count. Per region: select with `RGNR` (`c6, c2, 0`), set `DRBAR` (`c6, c1, 0`), `DRSR` (`c6, c1, 2`, size+enable), and `DRACR` (`c6, c1, 4`, AP/TEX/S/C/B/XN). Mark peripherals as Device/Strongly-ordered with `XN`, TCM/SRAM/DDR as Normal. Enable via `SCTLR.M` (bit 0); enable caches with `SCTLR.C` (bit 2) and `SCTLR.I` (bit 12). Use `DSB`/`ISB` after CP15 writes.

1. Decode exceptions.
   Data Abort: read `DFSR` (`c5, c0, 0`) and `DFAR` (`c6, c0, 0`). Prefetch Abort: read `IFSR` (`c5, c0, 1`) and `IFAR` (`c6, c0, 2`). ECC/parity events also surface in `ADFSR`/`AIFSR` (`c5, c1, 0` / `c5, c1, 1`). Decode the DFSR status field (short-descriptor `FS` = bit 10 + bits [3:0]): `0b00001` alignment, `0b00000` background (no MPU region), `0b01101` permission, `0b01000` synchronous external abort, `0b10110` asynchronous external abort, `0b11001`/`0b11000` synchronous/asynchronous parity/ECC. Check `WnR` (bit 11) for write vs read.

1. Bring up interrupts separately.
   Validate routing before load. For a GIC: `GICD_CTLR`, `GICD_ISENABLERn`, `GICD_IPRIORITYRn`, `GICD_ITARGETSRn`, then CPU interface `GICC_CTLR`, `GICC_PMR`, and the `GICC_IAR`/`GICC_EOIR` acknowledge/EOI pair. For a PL192-style VIC or TI VIM, validate the vector table and enable/priority registers. Confirm the FIQ/IRQ mode has its own stack and that `CPSR.I`/`CPSR.F`/`CPSR.A` masks are cleared as intended.

1. Add multicore/safety features last.
   Prove single-core execution before enabling lock-step comparison, split-mode messaging, watchdogs, or safety monitors. Note lock-step vs split is a hardware/reset configuration (e.g., `DCLS`, `INITRAM*` straps), not a runtime software toggle.

## Common Failures

- Linker script places vectors, stacks, or `.data` in `ATCM`/`BTCM` or DDR not yet enabled/initialized by the boot stage.
- `ATCM`/`BTCM` assumed enabled: the region Enable bit (`c9, c1, x` bit 0) is clear, or `INITRAMA`/`INITRAMB` reset base does not match the linker map.
- ECC-protected RAM read before being written, producing a synchronous parity/ECC Data Abort (`DFSR` = `0b11001`) with the address in `DFAR`.
- Peripheral registers left in a Normal/cacheable MPU region instead of Device with `XN`, causing reordering or speculative-access aborts.
- DMA buffers cached without `DCCMVAC`/`DCIMVAC`/`DCCIMVAC` maintenance plus `DSB` around ownership handoff.
- Missing banked `IRQ`/`FIQ` stack, so the first interrupt corrupts memory once `CPSR.I`/`CPSR.F` is cleared.
- MPU enabled (`SCTLR.M`) with no `DRSR`-enabled region and background region off (`SCTLR.BR`, bit 17), so every access takes a background fault (`DFSR` = `0b00000`).
- Debugger attached to the wrong core, or expecting two cores while the group is in lock-step (only one core is visible).

## Verification

Before claiming Cortex-R5 firmware works:

- State SoC, core, mode (single/split/lock-step), boot chain, memory map, and debugger path.
- Confirm reset-to-main with vectors (`SCTLR.V`/base), per-mode stacks, TCM enabled, and C runtime initialized.
- Confirm MPU regions (`DRBAR`/`DRSR`/`DRACR`) and cache state (`SCTLR.M`/`.C`/`.I`) for code, data, Device/peripheral, DMA, and shared memory.
- Confirm at least one timer/interrupt path (GIC/VIC ack + EOI) and one exception dump path (`DFSR`/`DFAR` or `IFSR`/`IFAR`).
- Confirm watchdog, lock-step/split, and inter-core communication behavior if used.

## Example

User:

```text
Cortex-R5 一开 D-cache 就随机 data abort。
```

Agent:

1. Reads `DFSR`/`DFAR` at the abort to classify the fault, e.g. via OpenOCD after `halt`:

   ```text
   arm mrc 15 0 5 0 0   ;# DFSR  (p15, op1=0, CRn=c5, CRm=c0, op2=0)
   arm mrc 15 0 6 0 0   ;# DFAR  (p15, op1=0, CRn=c6, CRm=c0, op2=0)
   ```

   (Xilinx XSDB equivalent: select the RPU core with `targets`, then `rrd` for `CPSR`/banked regs and `mrd` for the faulting address.)

1. Checks whether the faulting `DFAR` lands in a peripheral or shared buffer marked Normal/cacheable, and whether the status is permission (`0b01101`), external (`0b01000`), or parity/ECC (`0b11001`).

1. Fixes the MPU attributes (`DRACR`: Device + `XN` for peripherals) and adds `DCCIMVAC`/`DSB` cache maintenance around DMA/shared memory before changing application logic.
