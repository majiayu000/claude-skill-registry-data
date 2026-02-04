---
name: gdb-attach
description: Use when debugging the Breenix kernel at assembly or C-level using GDB - investigating CPU exceptions, page faults, triple faults, examining register state during interrupt handling, stepping through boot sequence, analyzing syscall entry/exit paths, debugging context switches, or inspecting memory layout and page tables.
---

# Breenix GDB Debugging

## When to Use This Skill

Use this skill when you need to debug the Breenix kernel at the assembly or C-level using GDB. Common scenarios:

- Investigating CPU exceptions, page faults, or triple faults
- Examining register state during interrupt handling
- Stepping through boot sequence or early initialization
- Analyzing syscall entry/exit paths
- Debugging context switches and process state transitions
- Inspecting memory layout and page tables
- Understanding TSC/APIC timer behavior

## Quick Start

### 1. Launch QEMU in GDB Mode

```bash
# Set the GDB flag and run the kernel
BREENIX_GDB=1 cargo run --release --bin qemu-uefi
```

This will:
- Start QEMU with `-s -S` (GDB server on localhost:1234, paused)
- Wait for GDB to connect before executing any code
- Print connection instructions

### 2. Connect GDB (in another terminal)

```bash
# Connect to the running QEMU instance
gdb target/x86_64-breenix/release/kernel -ex 'target remote localhost:1234'
```

Or use the helper command from `.gdbinit`:

```bash
gdb target/x86_64-breenix/release/kernel
(gdb) breenix-connect
```

## Essential GDB Commands for Kernel Debugging

### Navigation & Execution

```gdb
# Continue execution
c

# Step one instruction (into calls)
si

# Step one instruction (over calls)
ni

# Step one source line
s

# Step over source line
n

# Finish current function
finish
```

### Breakpoints

```gdb
# Hardware breakpoint (works before paging is set up)
hbreak kernel_main

# Software breakpoint (requires memory to be mapped)
break rust_syscall_handler
break timer_interrupt_handler
break process::manager::spawn_process

# Conditional breakpoint
break syscall_handler if $rax == 0x1  # Only break on specific syscall

# List breakpoints
info breakpoints

# Delete breakpoint
delete 1
```

### Registers & State

```gdb
# Show all general-purpose registers
info registers

# Show specific register
print $rip
print/x $rsp
print/x $cr3

# Show segment registers
info registers cs ds ss fs gs

# Custom helper to show segments nicely
show-segments
```

### Memory Inspection

```gdb
# Examine memory (format: x/nfu addr)
# n=count, f=format (x=hex, d=decimal, s=string), u=unit (b=byte, h=halfword, w=word, g=giant/8-bytes)

x/16xg $rsp              # Show 16 8-byte values at stack pointer
x/32xb 0xffff800000000000  # Show 32 bytes at kernel base
x/s 0xsomeaddr           # Show null-terminated string
x/i $rip                 # Show instruction at program counter

# Display memory continuously as you step
display/16xg $rsp
```

### Backtraces & Frames

```gdb
# Show call stack
backtrace
bt

# Show detailed backtrace with local variables
backtrace full

# Move between stack frames
frame 0
frame 1

# Show local variables in current frame
info locals

# Show function arguments
info args
```

### Symbols & Source

```gdb
# List source code around current location
list

# Show disassembly around current instruction
disassemble

# Show disassembly of specific function
disassemble kernel_main
disassemble rust_syscall_handler

# Show type information
ptype some_variable
```

## Common Debugging Scenarios

### Scenario 1: Boot Debugging

Set breakpoint at kernel entry and step through initialization:

```gdb
(gdb) hbreak kernel_main
(gdb) c
(gdb) layout asm     # Show assembly view
(gdb) si            # Step through boot sequence
(gdb) info registers
```

### Scenario 2: Syscall Debugging

Debug a specific syscall (e.g., clock_gettime):

```gdb
(gdb) break rust_syscall_handler
(gdb) c
# When syscall hits:
(gdb) print/x $rax   # Syscall number
(gdb) print/x $rdi   # First argument
(gdb) print/x $rsi   # Second argument
(gdb) s              # Step into handler
```

### Scenario 3: Page Fault Investigation

Examine CPU state on page fault:

```gdb
(gdb) break page_fault_handler
(gdb) c
# When fault occurs:
(gdb) print/x $cr2   # Faulting address
(gdb) print/x $rip   # Instruction that faulted
(gdb) x/i $rip       # Show the faulting instruction
(gdb) print error_code  # Error code (if captured)
(gdb) backtrace
```

### Scenario 4: Timer Interrupt Debugging

Trace timer interrupt flow:

```gdb
(gdb) break timer_interrupt_handler
(gdb) c
# First timer interrupt hits:
(gdb) print ticks    # Check tick counter
(gdb) s              # Step into APIC EOI
(gdb) finish         # Return from handler
(gdb) c              # Continue to next tick
```

### Scenario 5: Context Switch Analysis

Debug process switching:

```gdb
(gdb) break context_switch::switch_to
(gdb) c
# When switching:
(gdb) print from_process
(gdb) print to_process
(gdb) print/x $cr3   # Current page table
(gdb) s              # Step through switch
(gdb) print/x $cr3   # New page table
```

## Breenix-Specific Helpers

The `.gdbinit` file provides custom commands:

```gdb
# Connect to QEMU
breenix-connect

# Show segment registers nicely
show-segments

# Set common kernel breakpoints
breenix-breaks
```

## Advanced Techniques

### Watchpoints (Memory Access Breakpoints)

```gdb
# Break when memory location is written
watch *0xffff800000010000

# Break when memory location is read
rwatch some_global_variable

# Break on read or write
awatch some_global_variable
```

### Examining Page Tables

```gdb
# Get CR3 (page table root)
print/x $cr3

# Walk page table manually (requires understanding x86_64 paging)
x/4xg ($cr3 & ~0xfff)  # PML4 entries
```

### TSC Debugging

```gdb
# Read TSC register value
print $ia32_tsc  # May not be directly accessible
# Instead, examine TSC handling code:
break tsc::read_tsc
```

## Tips & Gotchas

1. **Use hardware breakpoints early**: Before paging is fully set up, use `hbreak` instead of `break`
2. **Serial output interference**: GDB traffic and serial logs both compete for terminal output
3. **Optimization can confuse stepping**: Release builds may inline or reorder code
4. **No symbols for assembly**: Some early boot code won't have Rust symbols
5. **Context switches reset state**: Watch out for process switching changing $cr3, $rsp, etc.

## Exiting GDB

```gdb
# Quit GDB (QEMU will also stop)
quit

# Detach but leave QEMU running
detach
```

## Integration with Existing Workflow

This GDB debugging flow complements the existing log-based debugging:

- **Use logs for**: High-level flow, timing issues, multi-test scenarios
- **Use GDB for**: Precise state inspection, assembly-level debugging, crash analysis

You can combine both: run with logs first to narrow down the issue, then use GDB to investigate the exact instruction or register state.
