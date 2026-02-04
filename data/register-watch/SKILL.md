---
name: register-watch
description: Use when debugging register corruption issues - registers have unexpected values after context switches, userspace processes crash with corrupted state, stack pointer corruption, syscall return values corrupted, or timer interrupt handlers corrupting register state.
---

# Breenix Register Watch - Debug Register Corruption

## When to Use This Skill

Use this skill when debugging register corruption issues in the Breenix kernel, specifically:

- Registers (RSP, RBP, RIP, etc.) have unexpected values after context switches
- Userspace processes crash with corrupted register state
- Stack pointer corruption causing kernel panics
- General-purpose registers (RAX, RBX, RCX, RDX, etc.) not preserved across operations
- Syscall return values corrupted
- Timer interrupt handlers corrupting register state

## Overview

This skill provides a systematic approach to tracking register corruption using GDB:

1. Set up QEMU with GDB debugging enabled
2. Configure watchpoints and breakpoints at critical boundaries
3. Create register snapshot and comparison utilities
4. Identify the exact instruction where corruption occurs
5. Analyze the root cause and validate the fix

## Phase 1: Set Up GDB Environment

### Start QEMU with GDB Server

```bash
# Start kernel in debug mode (paused, waiting for GDB)
BREENIX_GDB=1 cargo run --release --bin qemu-uefi
```

### Connect GDB

In a separate terminal:

```bash
# Connect to QEMU's GDB server
gdb -ex "target remote :1234" \
    -ex "symbol-file target/x86_64-breenix/release/kernel" \
    -ex "set architecture i386:x86-64"
```

## Phase 2: Configure Breakpoints at Critical Boundaries

### Context Switch Boundaries

Break at points where registers MUST be preserved:

```gdb
# Main context switch entry point
break check_need_resched_and_switch

# Context restore to userspace
break restore_userspace_thread_context

# Context save from userspace
break kernel::interrupts::context_switch::save_context

# Timer interrupt handler
break timer_handler

# Syscall entry/exit
break syscall_handler
break kernel::syscall::handler::return_to_userspace
```

### Interrupt Boundaries

```gdb
# All interrupt handlers that touch user context
break handle_page_fault
break handle_general_protection_fault
break handle_divide_error
```

## Phase 3: Register Snapshot and Comparison

### Define GDB Snapshot Commands

Add these to your GDB session or save in `~/.gdbinit`:

```gdb
# Capture complete register state
define snap-regs
    set $snap_rax = $rax
    set $snap_rbx = $rbx
    set $snap_rcx = $rcx
    set $snap_rdx = $rdx
    set $snap_rsi = $rsi
    set $snap_rdi = $rdi
    set $snap_rbp = $rbp
    set $snap_rsp = $rsp
    set $snap_r8  = $r8
    set $snap_r9  = $r9
    set $snap_r10 = $r10
    set $snap_r11 = $r11
    set $snap_r12 = $r12
    set $snap_r13 = $r13
    set $snap_r14 = $r14
    set $snap_r15 = $r15
    set $snap_rip = $rip
    set $snap_rflags = $eflags
    printf "Register snapshot captured at RIP=0x%lx\n", $rip
end

# Compare current state against snapshot
define diff-regs
    printf "\n=== Register Differences ===\n"
    if $snap_rax != $rax
        printf "RAX: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_rax, $rax, $rax - $snap_rax
    end
    if $snap_rbx != $rbx
        printf "RBX: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_rbx, $rbx, $rbx - $snap_rbx
    end
    if $snap_rcx != $rcx
        printf "RCX: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_rcx, $rcx, $rcx - $snap_rcx
    end
    if $snap_rdx != $rdx
        printf "RDX: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_rdx, $rdx, $rdx - $snap_rdx
    end
    if $snap_rsi != $rsi
        printf "RSI: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_rsi, $rsi, $rsi - $snap_rsi
    end
    if $snap_rdi != $rdi
        printf "RDI: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_rdi, $rdi, $rdi - $snap_rdi
    end
    if $snap_rbp != $rbp
        printf "RBP: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_rbp, $rbp, $rbp - $snap_rbp
    end
    if $snap_rsp != $rsp
        printf "RSP: 0x%016lx -> 0x%016lx (diff: 0x%lx) STACK POINTER\n", $snap_rsp, $rsp, $rsp - $snap_rsp
    end
    if $snap_r8 != $r8
        printf "R8:  0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_r8, $r8, $r8 - $snap_r8
    end
    if $snap_r9 != $r9
        printf "R9:  0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_r9, $r9, $r9 - $snap_r9
    end
    if $snap_r10 != $r10
        printf "R10: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_r10, $r10, $r10 - $snap_r10
    end
    if $snap_r11 != $r11
        printf "R11: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_r11, $r11, $r11 - $snap_r11
    end
    if $snap_r12 != $r12
        printf "R12: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_r12, $r12, $r12 - $snap_r12
    end
    if $snap_r13 != $r13
        printf "R13: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_r13, $r13, $r13 - $snap_r13
    end
    if $snap_r14 != $r14
        printf "R14: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_r14, $r14, $r14 - $snap_r14
    end
    if $snap_r15 != $r15
        printf "R15: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_r15, $r15, $r15 - $snap_r15
    end
    if $snap_rip != $rip
        printf "RIP: 0x%016lx -> 0x%016lx (diff: 0x%lx)\n", $snap_rip, $rip, $rip - $snap_rip
    end
    if $snap_rflags != $eflags
        printf "RFLAGS: 0x%08x -> 0x%08x\n", $snap_rflags, $eflags
    end
    printf "=============================\n\n"
end

# Show all general-purpose registers
define show-regs
    printf "\n=== Current Register State ===\n"
    printf "RAX: 0x%016lx  RBX: 0x%016lx  RCX: 0x%016lx  RDX: 0x%016lx\n", $rax, $rbx, $rcx, $rdx
    printf "RSI: 0x%016lx  RDI: 0x%016lx  RBP: 0x%016lx  RSP: 0x%016lx\n", $rsi, $rdi, $rbp, $rsp
    printf "R8:  0x%016lx  R9:  0x%016lx  R10: 0x%016lx  R11: 0x%016lx\n", $r8, $r9, $r10, $r11
    printf "R12: 0x%016lx  R13: 0x%016lx  R14: 0x%016lx  R15: 0x%016lx\n", $r12, $r13, $r14, $r15
    printf "RIP: 0x%016lx  RFLAGS: 0x%08x\n", $rip, $eflags
    printf "==============================\n\n"
end
```

## Phase 4: Watchpoints for Specific Registers

### Watch Stack Pointer (Most Common Corruption)

```gdb
# Watch for any write to RSP
watch -l $rsp

# Or watch a memory location where RSP is saved
watch *(uint64_t*)0xYOUR_CONTEXT_ADDRESS

# Continue and wait for watchpoint trigger
continue
```

### Conditional Watchpoints

```gdb
# Only break if RSP becomes invalid (not in kernel stack range)
watch -l $rsp
condition 1 $rsp < 0xffff800000000000 || $rsp > 0xfffffffffffff000
```

## Phase 5: Debugging Workflow

### Step-by-Step Investigation

```gdb
# 1. Break before suspect operation
break check_need_resched_and_switch

# 2. Run to breakpoint
continue

# 3. Capture register state BEFORE
snap-regs
show-regs

# 4. Step through (or continue to next boundary)
# Use 'stepi' for instruction-level or 'next' for source-level
stepi
# or
break restore_userspace_thread_context
continue

# 5. Compare register state AFTER
diff-regs
show-regs
```

### Automated Breakpoint Actions

Run snapshot/diff automatically at each breakpoint:

```gdb
# Capture state on entry to context switch
break check_need_resched_and_switch
commands
    snap-regs
    continue
end

# Check state on exit
break restore_userspace_thread_context
commands
    diff-regs
    continue
end

# Start running
continue
```

## Phase 6: Common Corruption Patterns

### Pattern 1: Context Not Saved Before Switch

**Symptom:** Registers change between syscall entry and return to userspace

**Debug:**
```gdb
break syscall_handler
commands
    snap-regs
    print "Entering syscall"
    continue
end

break kernel::syscall::handler::return_to_userspace
commands
    diff-regs
    print "Exiting syscall"
    continue
end
```

**Root Cause:** Context not properly saved before context switch, or saved to wrong location.

### Pattern 2: Stack Pointer Corruption During Interrupt

**Symptom:** RSP has invalid value after timer interrupt

**Debug:**
```gdb
break timer_handler
commands
    printf "Timer: RSP=0x%lx RIP=0x%lx\n", $rsp, $rip
    snap-regs
    continue
end
```

**Root Cause:** Timer interrupt handler not preserving RSP, or stack frame setup incorrect.

### Pattern 3: General-Purpose Register Clobbering

**Symptom:** RAX, RDI, RSI (syscall argument registers) corrupted

**Root Cause:** Inline assembly clobbering registers, or incorrect clobber list in `asm!()`.

### Pattern 4: Userspace Register Corruption on Context Restore

**Symptom:** Userspace process receives wrong register values after being scheduled back in

**Root Cause:** Context restore logic copying from wrong memory location, or context structure layout mismatch.

## Phase 7: Validate the Fix

After identifying and fixing the corruption:

1. **Remove all breakpoints:** `delete`
2. **Re-run the scenario:** `run`
3. **Verify registers remain consistent:**
   - Set breakpoints only at entry/exit of the fixed function
   - Verify `diff-regs` shows no unexpected changes
4. **Run full test suite:** Exit GDB, run `cargo test`

## Key Breenix Kernel Functions

These are the critical functions where register state MUST be preserved:

- `kernel::interrupts::context_switch::save_context` - Saves all GPRs to InterruptContext
- `kernel::interrupts::context_switch::restore_userspace_thread_context` - Restores context before returning to userspace
- `kernel::interrupts::context_switch::check_need_resched_and_switch` - Orchestrates context switch
- `kernel::syscall::handler::syscall_handler` - Entry point for all syscalls
- `kernel::interrupts::timer::timer_handler` - Timer interrupt handler
- `kernel::interrupts::InterruptContext` - The structure holding saved register state

## Expected Register Preservation Invariants

1. **Callee-saved registers (RBX, RBP, R12-R15):** Must be preserved across function calls
2. **Stack pointer (RSP):** Must always point to valid kernel or user stack
3. **Instruction pointer (RIP):** Must point to executable code
4. **Syscall arguments (RDI, RSI, RDX, R10, R8, R9):** Must be preserved from userspace entry until syscall handler reads them
5. **Return value (RAX):** Must be preserved from syscall handler return until userspace receives it

## Success Criteria

You have successfully debugged the register corruption when:

1. You can identify the EXACT instruction where corruption occurs
2. You understand WHY the corruption happens (missing save, wrong offset, clobber, etc.)
3. Your fix preserves all required registers across the suspect operation
4. `diff-regs` shows no unexpected changes after the fix
5. All tests pass, especially `clock_gettime_test` and context switch tests
