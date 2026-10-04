---
name: assembly-systems
description: Read, write, debug, and review x86-64, AArch64, and RISC-V assembly at C, C++, and Rust boundaries. Use for compiler output, disassembly, calling conventions, inline assembly, SIMD, atomics, ABI bugs, or low-level performance work; use a reverse-engineering workflow instead for whole-binary investigation.
---

# Assembly systems

Start by identifying the target ISA and bitness, operating system, object format, ABI, compiler, syntax, and optimization level. Do not infer the ABI from the instruction set alone. In particular, keep Windows x64 separate from System V AMD64 and Windows ARM64 separate from generic AAPCS64.

Read only the matching reference:

- x86-64 or x64: [references/x86-64.md](references/x86-64.md)
- AArch64 or ARM64: [references/aarch64.md](references/aarch64.md)
- RISC-V: [references/riscv.md](references/riscv.md)

For whole binaries, symbol recovery, malware, firmware, or cross-version comparison, use `reverse-skill-router`. Use `idapython` when the task requires IDA database automation.

## Working method

1. Preserve the exact source, compiler, target triple, flags, and relevant disassembly bytes.
2. Mark function boundaries, inputs, outputs, stack state, preserved registers, control flow, and memory accesses before translating the logic.
3. Separate observed facts from inferred types, names, invariants, and intent.
4. Check instruction semantics in the vendor manual when flags, exceptions, privilege, memory ordering, or encoding matter.
5. Verify the interpretation with the smallest useful experiment: compile a probe, disassemble it, single-step it, or run a focused test on the intended target.

## Engineering rules

- Prefer portable C, C++, Rust, or compiler intrinsics until measured evidence justifies assembly.
- At every call boundary, verify argument classification, stack alignment, return registers, preserved registers, unwind metadata, and platform-specific stack areas.
- For inline assembly, declare every input, output, clobber, and memory effect. Never use `volatile` as a substitute for a correct compiler contract.
- Preserve position independence and relocation behavior. Do not replace symbolic addressing with hard-coded addresses.
- Treat signedness, operand width, partial-register writes, extension, overflow flags, endianness, alignment, and aliasing as explicit facts.
- For atomics, state the language memory order and the ISA ordering guarantee separately. A compiler barrier is not a hardware barrier.
- For optimization, measure the real workload. Instruction count alone does not establish latency, throughput, cache behavior, or branch behavior.
- Do not execute an unknown binary on the host merely to understand it. Use static inspection first and an isolated environment for authorized dynamic analysis.

## Language boundaries

- C and C++: confirm name mangling, exception/unwind rules, object layout, and the active compiler ABI. Use `extern "C"` only when a C linkage boundary is intended.
- Rust: confirm the target triple, `repr(C)` or another required representation, FFI unwind behavior, and every `asm!` operand and option. Inspect monomorphized code rather than assuming the source-level generic shape survives.
- Mixed-language code: write a small ABI probe and inspect both sides of the boundary before changing production code.

Report the target assumptions, the evidence used, the recovered behavior, and any remaining uncertainty.

## Loading in Oh My Pi

Relative paths in this skill (`references/…`, `scripts/…`) resolve against the skill's own directory. Read them with `skill://assembly-systems/<relative-path>`. When a shell command needs a real filesystem path, that directory is `<OMP_HOME>/skills/assembly-systems/` — `~/.omp/agent/skills/assembly-systems/` by default. Invoking `/skill:assembly-systems` also prints the resolved location.
