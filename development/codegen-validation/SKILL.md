---
name: codegen-validation
description: Use when building or debugging a compiler backend, codegen, or assembler and you need to prove the generated machine code is correct by executing it on a real CPU or a fast emulator, not just inspecting the output
---

# Codegen Validation

## Overview

A codegen backend is correct when the code it emits computes the right answer on a real machine. Reading the assembly proves nothing; a plausible-looking instruction sequence with a wrong ABI detail or a clobbered callee-saved register passes every eyeball review and fails on hardware.

**Core principle:** Execution-validate. Compile a known program, run the output on a real CPU or a fast emulator, and assert the observed result. If you didn't run it, you don't know it works.

## When to Use

- Bringing up a new codegen target or instruction selection
- Implementing calling conventions, stack frames, register spilling, relocations
- Debugging "the assembly looks right but the answer is wrong"
- Adding an optimization pass and needing to prove it preserves behavior

## The Validation Loop

```
known program (expected result known)
   -> codegen -> machine code
   -> run on real CPU / fast emulator
   -> assert observed result == expected
```

- **Pick programs with known answers.** Start tiny: return a constant, add two args, a call to a leaf function, a loop that sums. Each isolates one capability (literals, ABI, calls, control flow).
- **Run on something real and fast.** A native emulator for your target CPU closes the loop in milliseconds, so it can run on every build. The point is real execution semantics, not a model of what you think the instruction does.
- **Assert the observed value**, not "it didn't crash." Read the result register or memory and compare to the expected answer.

## This Catches Bugs Review Misses

Execution validation reliably catches the codegen bugs that look fine on paper:

- A `select`/conditional-move lowering that picks the wrong operand.
- Critical-edge splitting that drops or duplicates a value.
- A prologue/epilogue that fails to save/restore a callee-saved register (return-address corruption shows up only when something actually calls).
- ABI mistakes: argument in the wrong register, stack misaligned, return value in the wrong place.
- Relocations that resolve to the wrong address.

These are exactly the bugs that turn into silicon respins or weeks of "intermittent" debugging if they escape. A handful of executed tests finds them in seconds.

## Build It Up By Capability

Order tests so each new one depends only on capabilities already validated:

1. Return a constant (codegen + run harness works at all).
2. Arithmetic on arguments (ABI in, result out).
3. Stack frame (alloca, alignment, prologue/epilogue).
4. Calls (the full ABI, callee-saved save/restore, return address).
5. Control flow (branches, loops, phi/select).
6. Spilling (more live values than registers).

When a higher test fails and the lower ones pass, the bug is in the new capability. That ordering is the debugger.

## Red Flags

| Smell | Do instead |
|-------|------------|
| "The disassembly looks correct" | Execute it and assert the result |
| Test asserts "no crash" | Assert the actual computed value |
| Slow full-system sim per test | Fast target emulator, run every build |
| One big program as the only test | Capability-ordered tests, smallest first |
| Skipping ABI/spill tests | Those are exactly where the bugs hide |

## Midstall House Style

- Vulcan is the reference: a reusable codegen system whose RISC-V output is execution-validated on Midstall's River CPU via a fast `river-emulator`. That harness caught real codegen bugs (select lowering, critical-edge splitting, return-address save) that passed inspection.
- Targets nest under `vulcan-target/<arch>`; validation is a first-class part of bring-up, not an afterthought.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji. The compare-against-truth loop is the same shape as `differential-verification`.
