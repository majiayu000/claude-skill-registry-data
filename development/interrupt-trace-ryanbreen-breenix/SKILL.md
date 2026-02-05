---
name: interrupt-trace
description: Use when analyzing low-level interrupt behavior - debugging interrupt handler issues, investigating crashes or triple faults, verifying privilege level transitions, analyzing register corruption between interrupts, or understanding interrupt sequencing and timing issues.
---

# breenix-interrupt-trace

## When to Use This Skill

Use this skill when you need to analyze low-level interrupt behavior in Breenix:
- Debugging interrupt handler issues (timer, syscalls, exceptions)
- Investigating unexpected crashes or triple faults
- Verifying privilege level transitions (Ring 0 <-> Ring 3)
- Analyzing register corruption between interrupts
- Understanding interrupt sequencing and timing issues

## Overview

This skill captures QEMU's interrupt trace logs and provides systematic analysis of:
1. Interrupt vector sequences (what interrupts fired and when)
2. CPU register state at each interrupt
3. Privilege level transitions
4. Anomalies (unexpected exceptions, register corruption, etc.)

## Step-by-Step Instructions

### Phase 1: Capture Interrupt Trace

1. **Set up environment variables:**
   ```bash
   export BREENIX_QEMU_LOG_PATH=/tmp/breenix-int-trace.log
   export BREENIX_QEMU_DEBUG_FLAGS="int,cpu_reset,guest_errors"
   ```

2. **Run QEMU with trace enabled:**
   ```bash
   cargo run --release --bin qemu-uefi -- -serial stdio -display none
   ```

3. **Wait for completion or crash** (typically 5-10 seconds for boot stages test)

4. **Verify trace was captured:**
   ```bash
   ls -lh /tmp/breenix-int-trace.log
   ```

### Phase 2: Parse Interrupt Sequence

Extract the interrupt vector sequence:

```bash
grep "v=" /tmp/breenix-int-trace.log | head -100
```

**What to look for:**
- `v=20` (0x20 = 32): Timer interrupt - should fire regularly
- `v=80` (0x80 = 128): Syscall interrupt - indicates userspace is making syscalls
- `v=0d` (13): General Protection Fault - privilege violation or invalid operation
- `v=0e` (14): Page Fault - memory access issue
- `v=08` (8): Double Fault - critical error handling another exception
- `v=06` (6): Invalid Opcode - executing bad instruction

### Phase 3: Analyze Privilege Transitions

Check for Ring 0 <-> Ring 3 transitions:

```bash
grep "CPL=" /tmp/breenix-int-trace.log | head -50
```

**Expected patterns:**
- `CPL=0`: Kernel mode (Ring 0)
- `CPL=3`: User mode (Ring 3)
- Syscalls should transition: `CPL=3` -> interrupt -> `CPL=0`
- Return from interrupt should transition: `CPL=0` -> iret -> `CPL=3`

### Phase 4: Examine Register State

For critical interrupts, examine full register dumps:

```bash
# Look at the last 200 lines before a crash
tail -200 /tmp/breenix-int-trace.log

# Or search for specific interrupt vectors
grep -A 10 "v=0d" /tmp/breenix-int-trace.log | head -50
```

**Key registers:**
- `RIP`: Instruction pointer - where the interrupt occurred
- `RSP`: Stack pointer - check for stack corruption
- `CR3`: Page table base - verify process context
- `RFL`: Flags register - check interrupt enable flag (IF)

### Phase 5: Identify Anomalies

**Common patterns indicating problems:**

1. **Unexpected exception cascade:**
   ```
   v=0e (Page Fault)
   v=0d (GPF)
   v=08 (Double Fault)
   v=02 (Triple Fault) -> CPU reset
   ```

2. **Stack pointer corruption:**
   - RSP outside valid range
   - RSP not aligned
   - RSP pointing to unmapped memory

3. **Missing timer interrupts:**
   - Long gaps between `v=20` events
   - Could indicate interrupts disabled too long

4. **Privilege level confusion:**
   - CPL=3 code accessing kernel memory
   - CPL=0 code with user stack pointer

### Phase 6: Generate Summary Report

Provide a report with:

1. **Interrupt Statistics:**
   - Total interrupts captured
   - Breakdown by vector (timer, syscall, exceptions)
   - Frequency of each type

2. **Privilege Transitions:**
   - Number of Ring 3 -> Ring 0 transitions
   - Number of Ring 0 -> Ring 3 transitions
   - Any stuck in one ring?

3. **Anomalies Found:**
   - List of unexpected exceptions
   - Register corruption patterns
   - Timing issues

4. **Crash Analysis (if applicable):**
   - Last 10 interrupts before crash
   - Register state at crash
   - Likely root cause

## Example Commands

### Quick Interrupt Summary
```bash
echo "=== Interrupt Vector Summary ==="
grep "v=" /tmp/breenix-int-trace.log | awk -F'v=' '{print $2}' | awk '{print $1}' | sort | uniq -c | sort -rn

echo "=== Privilege Level Transitions ==="
grep "CPL=" /tmp/breenix-int-trace.log | awk -F'CPL=' '{print $2}' | awk '{print $1}' | uniq -c

echo "=== Exception Events ==="
grep -E "v=0[0-9a-f]" /tmp/breenix-int-trace.log | grep -v "v=20" | head -20
```

### Detailed Syscall Analysis
```bash
# Find all syscall interrupts and show register state
grep -B 2 -A 5 "v=80" /tmp/breenix-int-trace.log | less
```

### Crash Investigation
```bash
# Show last 50 interrupts before end of log
grep "v=" /tmp/breenix-int-trace.log | tail -50
```

## Interpreting Results

### Healthy Boot Sequence

A normal Breenix boot should show:
```
v=20 (timer) - repeated regularly
v=80 (syscall) - when userspace runs
CPL=0 -> CPL=3 transitions when entering userspace
CPL=3 -> CPL=0 transitions on syscalls/interrupts
```

### Problematic Patterns

1. **No syscalls (v=80):**
   - Userspace never started
   - Process creation failed
   - Check for earlier exceptions

2. **No CPL=3:**
   - Never entered userspace
   - Privilege transition failed
   - Check interrupt return path

3. **Exception storm:**
   - Same exception repeating rapidly
   - Handler not fixing root cause
   - Infinite loop in exception handling

4. **CPU reset events:**
   - Triple fault occurred
   - Unrecoverable state
   - Check for double faults before reset

## Common Debug Flags

Other useful QEMU debug flag combinations:

```bash
# Just interrupts
export BREENIX_QEMU_DEBUG_FLAGS="int"

# Interrupts + MMU/page tables
export BREENIX_QEMU_DEBUG_FLAGS="int,mmu"

# Interrupts + all exceptions
export BREENIX_QEMU_DEBUG_FLAGS="int,cpu_reset,guest_errors,exception"

# Everything (very verbose)
export BREENIX_QEMU_DEBUG_FLAGS="int,cpu_reset,guest_errors,mmu,exception"
```

## Notes

- The trace log can be **very large** (10MB+ for full boot)
- Focus on specific time windows or interrupt types
- Use `head`/`tail` to avoid overwhelming output
- Correlate with Breenix's own serial output logs for context
- Timer interrupt (v=20) is the most common - filter it out to see other events
