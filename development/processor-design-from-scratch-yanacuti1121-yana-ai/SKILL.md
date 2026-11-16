---
name: processor-design-from-scratch
description: "Use when designing and simulating a simple CPU/processor from first principles — instruction set design, fetch-decode-execute cycle, a minimal assembler. Not for general low-level programming or existing CPU architecture study. Triggers on: 'design a CPU from scratch', 'build a simple processor', 'implement an instruction set', 'fetch decode execute cycle', 'write a toy CPU simulator', 'build my own assembler'. Covers ISA design, the FDE cycle, register/ALU design, and software-simulated vs HDL implementation."
origin: yana-ai — synthesized from classic computer-architecture pedagogy (Nand2Tetris-style toy CPU design, RISC-V's minimal-ISA philosophy) and community from-scratch tutorials indexed in codecrafters-io/build-your-own-x
license: Apache-2.0
version: 1.0.0
compatibility: yana-ai >= 0.43.2
---

# /processor-design-from-scratch

## When to Use

- Designing a minimal instruction set architecture (ISA) and simulating a CPU for it in software, for teaching or a toy VM project.
- Understanding the fetch-decode-execute cycle well enough to implement it, not just describe it.
- Deciding between a software CPU simulator and an HDL (Verilog/VHDL) implementation targeting real or emulated silicon (FPGA).

## Do NOT use for

- Studying/using an existing real ISA (x86, ARM, RISC-V) for systems programming — that's reading a manual, not designing one; see OS/kernel-level skills for working with real hardware ISAs.
- General emulator development for an *existing* console/computer's exact CPU — that's a different task (matching a spec precisely, cycle-accurate timing) from designing your own ISA from scratch.
- Bytecode VM design for a programming language (stack machine for a language interpreter) — related in spirit but a different design space; a language VM optimizes for the language's semantics, not for real-hardware constraints like registers and memory addressing.

---

## Software Simulator vs HDL — Decide First

```
Goal is to understand CPU concepts, build a working simulator quickly?
  → Software simulation (Steps 1-4 below) — a program that interprets your ISA,
    running on your actual computer's real CPU underneath

Goal is to actually synthesize real digital logic (FPGA or ASIC)?
  → HDL (Verilog/VHDL) — you're describing hardware circuits, not writing a program;
    a fundamentally different skill (digital logic design), out of scope here —
    Nand2Tetris is the standard learning path for that direction
```

This skill covers the software-simulation path — it's the right starting point even if HDL is the eventual goal, since ISA design decisions transfer directly.

## Step 1: Design the Instruction Set (ISA)

Keep it minimal — a working toy CPU needs surprisingly few instruction categories:

```
Arithmetic/Logic:  ADD, SUB, AND, OR, XOR, NOT
Data movement:     LOAD (memory → register), STORE (register → memory), MOV (register → register)
Control flow:      JMP (unconditional), JZ/JNZ (jump if zero/not-zero), CALL, RET
Immediate:         LOADI (load a literal constant into a register)
HALT
```

Decide **instruction format** (fixed-width is far simpler to decode than variable-width): e.g. a 16-bit instruction as `[4-bit opcode][4-bit dest reg][4-bit src reg][4-bit operand/unused]`. Fixed-width means decode is always "read N bits, mask out each field" — no need to first determine instruction length before knowing how to parse it (the added complexity real ISAs like x86 accept for code-density reasons, not worth it for a first design).

Decide **register count** (4-16 is plenty for a toy design) and whether you have a dedicated accumulator (all ALU ops implicitly use one fixed register) vs general-purpose registers (any register can be an ALU operand) — accumulator designs are simpler to implement, general-purpose designs are closer to what real ISAs do.

## Step 2: The Fetch-Decode-Execute Cycle

This is the actual CPU "loop" — everything else is supporting infrastructure around it:

```
loop:
  1. FETCH:   instruction = memory[program_counter]
  2. DECODE:  opcode, operands = parse(instruction)
  3. EXECUTE: perform the operation (ALU op, memory access, or PC jump)
  4. ADVANCE: program_counter += instruction_width   (unless EXECUTE already jumped it)
```

Implementation is a big switch/dispatch on opcode:

```python
def step(cpu):
    instr = cpu.memory[cpu.pc]
    opcode, dst, src, imm = decode(instr)
    if opcode == ADD:   cpu.regs[dst] += cpu.regs[src]
    elif opcode == LOAD: cpu.regs[dst] = cpu.memory[cpu.regs[src]]
    elif opcode == JZ:  cpu.pc = imm if cpu.regs[dst] == 0 else cpu.pc + 1; return
    # ... etc
    cpu.pc += 1
```

The critical detail: **jump instructions must set `pc` directly and skip the normal auto-increment** (the `return` above) — a common toy-CPU bug is incrementing `pc` after a jump instruction already set it, landing one instruction past the intended jump target.

## Step 3: Registers, ALU, and Flags

- **Registers**: just an array (`regs[0..N]`) — fast, fixed-size storage the ALU and data-movement instructions read/write directly, distinct from main memory (which is addressed, larger, and slower to access in real hardware — the distinction matters conceptually even in a software simulator with no real speed difference).
- **ALU**: the functions implementing ADD/SUB/AND/OR/etc. — in a software simulator these are just your host language's own arithmetic operators, called from the EXECUTE step.
- **Flags** (zero, carry, negative, overflow): a small status register set after arithmetic ops, used by conditional jumps (`JZ` checks the zero flag rather than re-comparing values). Deciding to have explicit flags vs. conditional instructions that re-evaluate a condition directly (RISC-V's approach) is itself an ISA design choice — flags are simpler to bolt onto a first design.

## Step 4: A Minimal Assembler

Once the ISA exists, hand-writing raw instruction words is painful — build a two-pass assembler:

```
Pass 1: scan the source, record every LABEL's line number as an address
        (needed because a jump can reference a label defined LATER in the file —
        you can't resolve it until you've seen the whole program)
Pass 2: re-scan, emit actual instruction words, substituting each label
        reference with its now-known address from pass 1's table
```

```asm
        LOADI r0, 10
loop:   SUB   r0, r0, 1
        JNZ   r0, loop      ; label resolved in pass 2 using pass 1's table
        HALT
```

## What NOT to Do

- Don't design a variable-width instruction format for a first ISA — the decode complexity isn't worth it until you have a concrete code-density reason to need it.
- Don't forget to skip the auto-increment on jump instructions — see Step 2; this is the most common toy-CPU bug and it's silent (the program runs, just wrong).
- Don't conflate "register" and "memory" access cost/semantics even in a simulator with no real performance difference — keeping the conceptual distinction is what makes the design transferable to understanding real hardware.
- Don't try to support self-modifying code, interrupts, or virtual memory in a first design — these are real and important CPU features, but they're extensions to a working fetch-decode-execute loop, not part of getting one working.
