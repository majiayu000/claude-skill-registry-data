---
name: assembly-programming
description: Assembly programming and low-level debugging skill for reading, writing, explaining, optimizing, and reviewing assembly across x86, x86-64, ARM, AArch64, RISC-V, calling conventions, ABI boundaries, inline assembly, disassembly, stack frames, registers, and binary-level behavior. Use for .s/.asm files, compiler output, reverse-engineering snippets, low-level performance, and crash analysis.
---

# Assembly Programming

## Operating Rules

- Identify architecture, bitness, syntax, ABI, OS, compiler, and optimization level before interpreting code.
- Track register meaning, stack layout, flags, memory aliases, and call clobbers explicitly.
- Prefer correctness and ABI compliance before micro-optimization.
- For security-sensitive code, call out memory safety, control-flow integrity, and undefined behavior risks.

## Workflow

1. Establish target platform and syntax: Intel vs AT&T, GNU as vs NASM/MASM, ARM vs AArch64, etc.
2. Map inputs, outputs, preserved registers, stack alignment, and external calls.
3. Translate blocks into pseudocode before proposing edits.
4. For edits, preserve calling convention, unwind expectations, and toolchain constraints.
5. Recommend verification with assembler, unit tests, debugger traces, or compiler-generated comparison.

## Review Checklist

- Stack alignment is correct at calls.
- Caller-saved and callee-saved registers are handled correctly.
- Memory widths, sign extension, and endian assumptions are explicit.
- Branch conditions match the intended signed or unsigned comparison.
- Inline assembly constraints describe all inputs, outputs, clobbers, and memory effects.

