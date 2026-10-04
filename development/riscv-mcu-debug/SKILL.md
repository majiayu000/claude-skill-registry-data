---
name: riscv-mcu-debug
description: Use when debugging RISC-V microcontrollers, bare-metal firmware, RTOS bring-up, OpenOCD or GDB sessions, traps, CSRs, startup code, or flashing failures
---

# RISC-V MCU Debug

## Overview

Use this skill to debug RISC-V MCU firmware systematically. Identify the exact core, SoC, debug module, toolchain, memory map, and trap state before changing startup code, linker scripts, flash settings, or machine-mode configuration.

## When To Use

Use this skill when:

- The target is a RISC-V MCU or bare-metal RISC-V SoC.
- The user mentions OpenOCD, GDB, JTAG, RISC-V debug module, `mstatus`, `mcause`, `mepc`, `mtvec`, trap handlers, startup code, or linker scripts.
- Firmware cannot flash, stops before `main`, traps, hangs, or has no UART/log output.

Do not use this skill for Cortex-M, 8051, embedded Linux application debugging, or general C code review without target evidence.

## First Questions

Ask for:

- Exact chip, board, and core if known, such as RV32IMAC, RV32E, RV64, F/D extension, or vendor core name.
- Toolchain: GCC, LLVM, vendor IDE, Zephyr, RT-Thread, or bare metal.
- Debug path: OpenOCD, vendor GDB server, J-Link, WCH-Link, onboard probe, or UART bootloader.
- Current symptom: cannot connect, cannot flash, no boot, trap, hang, no log, or peripheral failure.
- Available artifacts: ELF, MAP, linker script, startup file, OpenOCD config, UART log, trap dump, or GDB transcript.

## Workflow

1. Confirm the target profile.
   RISC-V MCU behavior depends on XLEN, extensions, privilege mode, vendor CSRs, debug module, and memory map.

1. Classify the failure phase.
   Use connect, flash, reset/startup, trap, runtime hang, peripheral bring-up, or RTOS scheduling.

1. Establish a non-destructive debug session.
   Prefer halt/reset-halt and symbol loading before flash erase or startup rewrites.

1. Collect trap and reset evidence.
   Record `pc`, `sp`, `mstatus`, `mcause`, `mepc`, `mtval`, `mtvec`, and key memory addresses.

1. Check linker and startup alignment.
   Confirm reset address, vector/trap base, RAM origin, stack top, `.data` copy, `.bss` zeroing, and `main` call path.

1. Ask before risky operations.
   Mass erase, option bytes, boot mode, security locks, and vendor flash config changes require explicit approval.

## OpenOCD And GDB Checks

Useful patterns:

```bash
openocd -f interface/<probe>.cfg -f target/<target>.cfg
riscv64-unknown-elf-gdb build/firmware.elf
riscv-none-elf-gdb build/firmware.elf
```

GDB baseline:

```gdb
target extended-remote :3333
monitor reset halt
info registers
p/x $pc
p/x $sp
p/x $mcause
p/x $mepc
p/x $mtval
p/x $mtvec
bt
```

Check:

- `pc` points to a valid executable region.
- `sp` points inside RAM and is aligned.
- `mtvec` points to the intended trap handler.
- `mepc` maps to source or disassembly.
- OpenOCD target config matches the exact chip or debug module.

## Trap Debugging

When a trap occurs:

1. Preserve state before reset.
1. Read `mcause`, `mepc`, `mtval`, `mstatus`, and `mtvec`.
1. Decode whether the cause is interrupt or exception.
1. Map `mepc` to a symbol and instruction.
1. Check whether `mtval` contains a bad address or instruction.

Common causes:

- Illegal instruction due to wrong ISA flags, such as compiling for `rv32imac` but running on a core without compressed instructions.
- Misaligned access or unsupported unaligned loads/stores.
- Executing from erased flash or wrong boot address.
- Stack pointer outside RAM.
- Trap vector not initialized or not aligned as required.
- Accessing peripheral addresses before clocks or bus bridges are ready.
- M-mode interrupt enable or PLIC/CLIC setup mismatch.

## Startup And Linker Checks

If firmware fails before `main()`:

- Confirm linker script flash/RAM origins match the exact SoC.
- Confirm reset entry address agrees with boot ROM or flash mapping.
- Confirm stack top is valid and aligned.
- Confirm global pointer `gp` and small data sections are initialized if used.
- Confirm `.data` and `.bss` initialization.
- Confirm trap handler is installed before enabling interrupts.
- Confirm compiler ABI, ISA string, and startup assembly agree.

## Flashing Checks

If flashing fails:

- Separate connect, erase, program, and verify failures.
- Check probe wiring, target voltage, reset, and JTAG/SWD-equivalent pin mux.
- Lower adapter speed.
- Confirm flash algorithm and target config match the chip.
- Ask before mass erase or security unlock.

## Verification

Before claiming progress:

- State chip/core, XLEN, ISA string if known, probe, debug server, and toolchain.
- Confirm whether GDB can halt and read registers.
- Report `pc`, `sp`, `mcause`, `mepc`, `mtval`, and `mtvec` when trap-related.
- Confirm flash erase/program/verify status separately if flashing was attempted.
- List destructive actions skipped or awaiting approval.

## Common Failures

- Using the wrong `-march` or `-mabi` for the actual core.
- Assuming all RISC-V MCUs have the same interrupt controller.
- Resetting before reading trap CSRs.
- Debugging C code before confirming startup assembly and linker origins.
- Using a near-match OpenOCD target config without checking memory map and flash algorithm.

## Example

User:

```text
RISC-V 小板下载后进 trap，串口没有日志。
```

Agent:

1. Asks for chip, core/ISA, probe, OpenOCD config, ELF, and trap register dump.
1. Connects halt-first and reads `pc`, `sp`, `mcause`, `mepc`, `mtval`, and `mtvec`.
1. Maps `mepc` to source or disassembly.
1. Checks ISA flags, stack range, trap vector, and linker origins before editing code.
