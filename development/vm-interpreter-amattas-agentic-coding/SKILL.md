---
name: vm-interpreter
description: Exploiting custom interpreters and virtual machines
---

# VM/Interpreter Exploitation

**Concept:** Turn VM semantics into arbitrary read/write primitives.

---

## Recognition

**Signals:**
- Custom interpreter for small language
- Brainfuck-like instructions (`>`, `<`, `+`, `-`, `.`, `,`)
- Bytecode VM with opcodes manipulating memory
- Memory tape/array with movable pointer

---

## Goal

Convert VM operations into:
- **Arbitrary read:** Leak addresses, secrets
- **Arbitrary write:** Modify GOT, return addresses, pointers

---

## Analysis Steps

**1. Map memory layout:**
```
Where does VM memory live?
- Stack (near return addresses)
- Heap (near malloc metadata)
- BSS/data (near GOT, globals)
```

**2. Find neighbors:**
```
What's adjacent to VM memory?
- GOT entries
- Function pointers
- Stack frames
- Global variables
```

**3. Calculate distances:**
```
distance = target_addr - vm_memory_base
moves = distance / pointer_step_size
```

---

## Common VM Types

**Brainfuck-style:**
| Op | Effect |
|----|--------|
| `>` | Move pointer right |
| `<` | Move pointer left |
| `+` | Increment byte |
| `-` | Decrement byte |
| `.` | Output byte |
| `,` | Input byte |

**Bytecode style:**
- LOAD, STORE - Memory access
- ADD, SUB - Arithmetic
- JMP, JZ - Control flow
- PUSH, POP - Stack operations

---

## Exploitation Patterns

**Pattern A - Leak via output:**
```
1. Calculate distance from VM memory to target
2. Move pointer to target location
3. Output bytes at pointer
4. Reconstruct leaked address
```

**Pattern B - GOT/pointer overwrite:**
```
1. Move pointer to writable target
2. Set bytes to desired value
3. Trigger overwritten function
```

**Pattern C - Return address overwrite:**
```
(Only if VM memory is on stack)
1. Find offset to saved return address
2. Navigate and overwrite
```

---

## Pitfalls

| Issue | Solution |
|-------|----------|
| Off-by-one navigation | Verify with known values first |
| Endianness | x86 is little-endian |
| Character restrictions | Use loops for encoding |
| Instruction limits | Optimize, use loops |
| Null bytes in target | Write in pieces |
