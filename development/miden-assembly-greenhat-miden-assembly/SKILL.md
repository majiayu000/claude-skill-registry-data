---
name: miden-assembly
description: |
  Guide for understanding and writing Miden VM assembly (MASM) code. Use when:
  (1) Reading, analyzing, or explaining MASM code
  (2) Writing new MASM procedures or programs
  (3) Debugging MASM execution or stack state
  (4) Optimizing MASM code for cycle count
  (5) Working with Miden VM stack machine concepts
  Covers instructions, code organization, core library, and common patterns.
---

# Miden Assembly (MASM)

Miden assembly is a low-level language for Miden VM, a stack-based zero-knowledge virtual machine.

## Key Concepts

### Stack Machine
- Operand stack holds field elements (prime field p = 2^64 - 2^32 + 1)
- Top 16 elements directly accessible
- A *word* = 4 field elements
- Stack grows upward; `push` adds to top, operations consume from top

### Stack Notation
- `[a, b, ...]` means `a` is on top, `b` below
- Operations consume inputs and push outputs
- Example: `add` with `[3, 5, ...]` produces `[8, ...]`

## Quick Reference

### Basic Operations

```masm
# Arithmetic (field elements)
push.5 push.3 add    # [8, ...]
push.10 push.2 sub   # [8, ...]
push.4 push.3 mul    # [12, ...]

# Stack manipulation
dup.0                # Duplicate top
swap                 # Swap top two
drop                 # Remove top
movup.2              # Move 3rd item to top

# Memory
push.42 mem_store.100        # mem[100] = 42
push.100 mem_load            # push mem[100]

# Control flow
push.1
if.true
    push.10
else
    push.20
end

push.5
dup.0 neq.0
while.true
    push.1 sub
    dup.0 neq.0
end
drop
```

### Program Structure

```masm
# Import from core library
use miden::core::math::u64

# Constants
const ADDR = 100
const LIMIT = 1000

# Private procedure with locals
@locals(4)
proc helper
    loc_store.0    # Store to local
    loc_load.0     # Load from local
end

# Public procedure (exported)
pub proc api_function
    exec.helper
end

# Program entry point
begin
    push.42
    exec.api_function
end
```

## Reference Files

Load these as needed for detailed information:

- **[instruction_reference.md](references/instruction_reference.md)**: Complete instruction set with stack effects and cycle counts
- **[code_organization.md](references/code_organization.md)**: Procedures, modules, constants, types, execution contexts
- **[core_library.md](references/core_library.md)**: Standard library modules (u64, hashes, memory, etc.)

## Common Patterns

### U32 Operations

```masm
# u32 values must be < 2^32
push.100 push.50 u32wrapping_add   # 150
push.100 push.50 u32lt             # 0 (100 < 50 is false)
push.0xFF push.0x0F u32and         # 0x0F
```

### U64 Operations (via core library)

```masm
use miden::core::math::u64

# u64 = [hi, lo] on stack, with lo deeper (push lo first, then hi)
push.100.0 push.50.0    # Two u64s: 100, 50
exec.u64::wrapping_add  # Result: [0, 150]
```

### Conditional Selection

```masm
# cdrop: select based on condition
push.10 push.20 push.1 cdrop   # [20, ...] (cond=1 selects b)
push.10 push.20 push.0 cdrop   # [10, ...] (cond=0 selects a)
```

### Loop with Counter

```masm
# repeat.N - compile-time unrolled
repeat.5
    push.1 add
end

# while.true - runtime condition
push.1
while.true
    # loop body
    # must push 0 or 1 for next iteration check
    push.0   # exit after one iteration
end
```

### Memory Words

```masm
# Store/load 4 elements as word
padw                        # [0, 0, 0, 0, ...]
push.1.2.3.4               # [4, 3, 2, 1, 0, 0, 0, 0, ...]
push.100 mem_storew_be     # Store word at addr 100
dropw padw                 # Clear and prepare
push.100 mem_loadw_be      # Load word from addr 100
```

### Procedure Locals

```masm
@locals(8)
proc with_locals
    push.42 loc_store.0     # Store to local[0]
    loc_load.0              # Load from local[0]

    # Word loads (loc_loadw_*) require indices divisible by 4
    padw loc_storew_be.4    # Store word at local[4..7]
end
```

### Hashing

```masm
# Single word hash
push.1.2.3.4 hash          # [digest_word, ...]

# Merge two words
push.1.2.3.4 push.5.6.7.8 hmerge  # [digest_word, ...]
```

## Debugging

```masm
# Only active in debug mode
debug.stack        # Print entire stack
debug.stack.8      # Print top 8 items
debug.mem.100      # Print memory at address 100
debug.local        # Print procedure locals

# Tracing (requires -t flag)
trace.1            # Emit trace event
```

## Best Practices

1. **Validate inputs**: Use `u32assert`, `assert` before operations with preconditions
2. **Track stack state**: Comment stack layout at key points
3. **Minimize cycles**: Check cycle counts for hot paths
4. **Use locals sparingly**: They have overhead vs. stack manipulation
5. **Word-align memory**: Load/store words at addresses divisible by 4
6. **Return correctly**: `call`/`dyncall`/`syscall` require stack depth = 16 on return

## Error Patterns

```masm
# Division by zero
push.10 push.0 div      # FAILS

# Boolean required
push.2
if.true                 # FAILS: 2 is not boolean
end

# u32 range check
push.0x100000000 u32assert  # FAILS: value >= 2^32
```
