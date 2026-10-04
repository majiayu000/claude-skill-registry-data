---
name: bare-metal-bringup
description: Use when bringing up bare-metal or kernel code on a new architecture, SoC, or board (RISC-V, ARM, x86, ESP32) and it won't boot, hangs after boot, or faults early; covers trap vectors, MMU/PMP, syscall ABI, and boot ordering
---

# Bare-Metal Bring-Up

## Overview

Bringing up code on new silicon or a new architecture is a sequence of "does the most basic thing work yet" checkpoints. Each layer has a small number of mistakes that produce total silence or a single cryptic fault, and they are almost always init ordering, trap setup, address translation, or ABI mismatches.

**Core principle:** Get one character out the door first, then build up one checkpoint at a time. Until you have output, you are debugging blind, so the first job is always a working console, not the feature you wanted.

## When to Use

- First boot on a new arch/board, or a port to a new target
- "Boots but hangs," silent boot, or a fault before main
- Traps/interrupts not firing, or firing into garbage
- Syscalls returning wrong values or corrupting registers across the boundary
- A driver works under one emulator/accelerator but not another (TCG vs KVM)

## The Checkpoint Ladder

Climb in order. Don't debug a higher rung until the one below it is solid.

1. **Earliest output.** Poke the UART directly (no driver, no allocator). One known byte. If you can't get a byte, nothing else is debuggable.
2. **Stack and BSS.** A valid, correctly-placed stack and a zeroed BSS before any C/Zig/Rust runs. On some boots the stack must live inside a specific LOAD segment or the loader drops your initrd on top of it.
3. **Trap/exception vectors.** Install the vector table, prove it by taking a deliberate trap and returning. Get this working before timers or interrupts.
4. **Timer.** Architectural timer init MUST run before any kernel timer that divides by its frequency, or you divide by zero and panic with no output.
5. **Address translation.** MMU/PMP/page tables. Identity-map what you need, then enable. Wrong here means a fault the instant translation turns on.
6. **Interrupts.** Controller (PLIC/GIC/APIC), enable bits, the right per-IRQ vs global mask model for the part.
7. **Userspace / syscalls.** Drop to user mode, take a syscall, return cleanly without clobbering caller-saved-by-the-ABI registers.

See `bringup-gotchas.md` in this skill directory for the concrete, hard-won failures at each rung.

## Trap And Syscall Discipline

- **Save and restore exactly what the ABI promises.** The single most common syscall bug is the entry stub clobbering a register the user-side ABI expects preserved (often the arg/temp registers, or the user stack pointer saved to a per-CPU slot that a sibling thread overwrites). Build the return frame from a safe location, not from a register you're about to reuse.
- **Vector alignment is part-specific.** Some cores require the trap base aligned to 256 bytes and force vectored mode; some need relaxation/compression disabled so each slot stays the expected width. Read the manual, don't assume 4-byte slots.
- **64-bit values across a 32-bit syscall boundary** split across two registers and sentinel checks must use pointer-width max, not `u64` max, or they fall through to a null deref.

## Emulator vs Accelerator

A bug that only appears under KVM (and not plain TCG) is usually a real hardware-ordering or state-save bug that TCG's looser model hides: FP/SIMD state not saved on the trap path, per-CPU pointer not set before the first IRQ, a sleeper list reusing a runqueue link. Treat "works in TCG, dies in KVM" as a genuine bug in your save/restore or ordering, not an emulator quirk.

## Debugging When It's Silent

1. Bisect by checkpoint: which rung's "hello" still prints?
2. Add a raw byte at the suspect transition (before/after enabling translation, before/after the first trap).
3. Suspect ordering first (init A before B), then ABI (who clobbered what), then translation (what's mapped).
4. Fix the root cause. Do not add a retry loop or a save-on-failure hatch to paper over a corruption; find what corrupts. See `silicon-grade-discipline`.

## Midstall House Style

- Ferrite is the reference: multi-arch RT microkernel (aarch64/riscv64/i386/x86_64) plus ESP32-C6. The gotcha file distills its bring-up bugs.
- No design docs; keep the bring-up reasoning in-conversation and go straight to the fix.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji.
