---
name: boot-analysis
description: This skill should be used when analyzing the Breenix kernel boot sequence, verifying initialization order, timing boot stages, identifying boot failures, optimizing boot time, or understanding the boot process from bootloader handoff to kernel ready state.
---

# Boot Sequence Analysis for Breenix

Analyze and optimize the kernel boot process from bootloader to kernel ready.

## Purpose

Understanding the boot sequence is critical for debugging initialization issues, optimizing boot time, and ensuring proper subsystem ordering. This skill provides tools for analyzing boot logs, verifying checkpoint progression, and identifying boot failures.

## When to Use

- **Boot failures**: Kernel hangs or crashes during initialization
- **Initialization order issues**: Subsystems initialized in wrong order
- **Boot time optimization**: Reducing time from bootloader to ready
- **Checkpoint verification**: Confirming all subsystems initialize correctly
- **Boot regression analysis**: New code breaks boot sequence
- **Understanding boot flow**: Learning how kernel initialization works

## Breenix Boot Sequence

### Phase 1: Bootloader Handoff

**What happens**:
- Bootloader (bootloader crate) loads kernel
- Sets up initial page tables
- Provides memory map
- Transfers control to kernel entry point

**Entry point**: `kernel/src/main.rs` `kernel_main()`

**Initial state**:
```rust
// CPU in Long Mode (64-bit)
// Interrupts disabled
// Paging enabled (bootloader setup)
// Stack ready
// Physical memory mapped at offset
```

**Typical log output**:
```
[Bootloader messages]
Loading kernel...
Jumping to kernel entry point...
```

### Phase 2: Early Initialization

**Subsystems initialized** (in order):

**1. Logger**
```
[ INFO] Breenix OS starting...
```
- Serial output configured
- Framebuffer initialized
- Log level set

**2. GDT (Global Descriptor Table)**
```
[ INFO] GDT initialized
```
- Kernel/user code segments
- Kernel/user data segments
- TSS (Task State Segment)

**3. IDT (Interrupt Descriptor Table)**
```
[ INFO] IDT initialized
```
- Exception handlers (divide by zero, page fault, etc.)
- Interrupt handlers (timer, keyboard)
- Double fault handler with IST stack

**4. PIC (Programmable Interrupt Controller)**
```
[ INFO] PIC initialized
```
- Remapped to avoid conflicts
- All interrupts masked initially

### Phase 3: Memory Subsystem

**5. Frame Allocator**
```
[ INFO] Physical memory: 94 MiB usable
[DEBUG] Frame allocator initialized
```
- Reads bootloader memory map
- Identifies usable regions
- Initializes frame tracking

**6. Heap Allocator**
```
[ INFO] Heap: 1024 KiB
```
- Sets up kernel heap
- Enables dynamic allocation
- #[global_allocator] now functional

**7. Virtual Memory**
```
[DEBUG] Page table initialized
```
- Kernel page table setup
- Higher-half kernel mapping
- Recursive mapping if used

**8. Kernel Stacks**
```
[DEBUG] Kernel stack allocator initialized
```
- Stack bitmap allocator
- Guard pages configured
- IST stacks for exceptions

### Phase 4: Device Drivers

**9. Timer (PIT)**
```
[ INFO] Timer initialized at 100 Hz
```
- Configures Programmable Interval Timer
- Sets interrupt frequency
- Starts tick counting

**10. RTC (Real-Time Clock)**
```
[ INFO] RTC initialized: 2025-10-23 12:34:56 UTC
```
- Reads hardware clock
- Caches boot time
- Enables wall-clock time APIs

**11. Serial Input**
```
[ INFO] Serial input interrupts enabled
```
- UART receive interrupts
- Input buffer ready
- Command processing available

**12. Keyboard**
```
[ INFO] Keyboard initialized
```
- PS/2 keyboard driver
- Scancode processing
- Key event generation

### Phase 5: System Infrastructure

**13. Interrupts Enabled**
```
[ INFO] Enabling interrupts...
```
- Unmasks timer interrupt
- Unmasks keyboard interrupt
- System becomes responsive

**14. System Calls**
```
[ INFO] System call infrastructure initialized
```
- INT 0x80 handler registered
- Syscall dispatcher ready
- SWAPGS configured

**15. Threading**
```
[ INFO] Threading subsystem initialized
```
- Scheduler initialized
- Idle thread created
- Context switch infrastructure ready

**16. Process Management**
```
[ INFO] Process management initialized
```
- Process manager ready
- PID allocation working
- Fork/exec infrastructure initialized

### Phase 6: Testing (if enabled)

**17. POST (Power-On Self Test)**
```
[ INFO] Running POST tests...
=== Memory Test ===
✅ MEMORY TEST COMPLETE
...
🎯 KERNEL_POST_TESTS_COMPLETE 🎯
```
- Validates subsystems
- Runs self-checks
- Confirms kernel health

**18. Userspace Tests (if configured)**
```
RING3_SMOKE: creating hello_time userspace process
[ INFO] Process created: PID 1
USERSPACE OUTPUT: Hello from userspace!
```
- Creates test processes
- Verifies userspace execution
- Tests system calls

### Phase 7: Kernel Ready

**Final state**:
```
[ INFO] Kernel initialization complete
[ INFO] System ready
```
- All subsystems operational
- Ready for interactive use or more tests
- Idle loop or wait for input

## Boot Analysis Techniques

### Technique 1: Extract Boot Timeline

**Using log-analysis skill:**

```bash
# Get all initialization messages in order
grep "initialized\|INITIALIZED\|Initializing" logs/breenix_20251023_*.log

# Or more comprehensive
grep -E "INFO|WARN|ERROR" logs/latest.log | less
```

**Expected sequence**:
1. GDT initialized
2. IDT initialized
3. PIC initialized
4. Physical memory info
5. Timer initialized
6. RTC initialized
7. Interrupts enabled
8. Threading initialized
9. Process management initialized

### Technique 2: Find Boot Checkpoint Failures

**Identify last successful checkpoint:**

```bash
# Find last "initialized" message
grep "initialized" logs/breenix_*.log | tail -10

# Or find last successful operation
grep "SUCCESS\|✅\|complete" logs/breenix_*.log | tail -10
```

**If boot hangs**:
- Last checkpoint shows how far boot progressed
- Next subsystem is where hang occurs
- Focus debugging on that subsystem

### Technique 3: Compare Boot Sequences

**Working vs broken boot:**

```bash
# Extract initialization sequence
grep "initialized\|Initializing" working.log > working_boot.txt
grep "initialized\|Initializing" broken.log > broken_boot.txt

# Compare
diff -u working_boot.txt broken_boot.txt
```

**Look for**:
- Missing initialization steps
- Different initialization order
- New error messages
- Stops at different point

### Technique 4: Time Boot Stages

**Add timing checkpoints:**

```rust
let start = kernel::time::get_monotonic_ms();

// Initialize subsystem
gdt::init();

let elapsed = kernel::time::get_monotonic_ms() - start;
log::info!("GDT initialization took {}ms", elapsed);
```

**Analyze timing:**
- Which stages are slow?
- Where can we optimize?
- Any unexpected delays?

### Technique 5: Verify Subsystem Dependencies

**Check initialization order:**

```rust
// Memory must be initialized before heap
assert!(frame_allocator.is_initialized());
heap::init(); // Safe now

// GDT must be before IDT
gdt::init();
idt::init(); // Can reference GDT segments

// Interrupts must be off during sensitive operations
assert!(!are_enabled());
```

## Common Boot Issues

### Issue 1: Boot Hang

**Symptoms**:
- Kernel boots partway then stops
- No error message, just hangs
- Some subsystems initialized, others not

**Diagnosis**:
```bash
# Find last successful operation
grep "initialized\|complete" logs/latest.log | tail -1

# Check if interrupts were enabled prematurely
grep "Enabling interrupts" logs/latest.log

# Look for infinite loops
grep "WARN\|ERROR" logs/latest.log
```

**Common causes**:
1. **Interrupts enabled too early**
   - Timer interrupt fires before handler ready
   - Solution: Ensure all handlers registered before enabling

2. **Deadlock during initialization**
   - Lock acquired, never released
   - Solution: Check lock usage during boot

3. **Infinite loop in subsystem init**
   - Waiting for condition that never happens
   - Solution: Add timeouts or debug why condition fails

**Fix patterns**:
```rust
// Add checkpoint logging
log::info!("About to initialize subsystem X");
subsystem_x::init();
log::info!("Subsystem X initialized successfully");

// If hangs between checkpoints, focus on subsystem_x::init()
```

### Issue 2: Boot Panic

**Symptoms**:
```
PANIC: [message]
Stack trace: ...
```

**Diagnosis**:
```bash
# Get panic message
grep "PANIC" logs/latest.log

# Get context
grep -B20 "PANIC" logs/latest.log
```

**Common causes**:
1. **Assertion failure**
   ```rust
   assert!(condition); // Failed during boot
   ```
   Check if assertion is correct or if precondition not met

2. **Unwrap on None/Err**
   ```rust
   let value = option.unwrap(); // Panic if None
   ```
   Use proper error handling during boot

3. **Out of memory**
   ```
   allocation error: Layout { ... }
   ```
   Increase heap size or defer allocation

### Issue 3: Wrong Initialization Order

**Symptoms**:
- Later subsystem fails
- "Not initialized" error
- Double fault or page fault

**Example**:
```rust
// BAD - heap used before initialization
use alloc::vec::Vec;
let v = Vec::new(); // Panic! Heap not initialized yet
heap::init();

// GOOD
heap::init();
use alloc::vec::Vec;
let v = Vec::new(); // OK
```

**Diagnosis**:
- Check dependency chain
- Verify order matches requirements
- Look for use-before-init patterns

### Issue 4: Boot Regression

**Symptoms**:
- Kernel booted before, now doesn't
- Recent change broke boot
- Used to reach checkpoint X, now stops at Y

**Diagnosis**:
```bash
# Find which commit broke it
git bisect start
git bisect bad HEAD
git bisect good last_working_commit

# Test each commit
kernel-debug-loop/scripts/quick_debug.py \
  --signal "KERNEL READY" \
  --timeout 15
```

**Fix**:
- Identify the breaking commit
- Understand what it changed
- Fix or revert

## Boot Optimization

### Current Boot Time

**Measure with kernel-debug-loop:**

```bash
# Time to specific checkpoint
kernel-debug-loop/scripts/quick_debug.py \
  --signal "Kernel initialization complete" \
  --timeout 30
```

**Typical times** (approximate):
- Early init (GDT, IDT, PIC): ~10ms
- Memory subsystem: ~50ms
- Drivers (timer, keyboard): ~20ms
- Threading/processes: ~10ms
- POST tests: ~100ms (if enabled)
- Total boot: ~200-500ms to ready state

### Optimization Strategies

**1. Defer non-critical initialization**
```rust
// Don't initialize during boot if not needed
// keyboard::init(); // Defer until first use

// Or lazy initialization
pub fn get_keyboard() -> &'static Keyboard {
    static INIT: Once = Once::new();
    INIT.call_once(|| {
        keyboard::init();
    });
    &KEYBOARD
}
```

**2. Parallelize independent operations**
```rust
// Currently serial:
timer::init();
rtc::init();
keyboard::init();

// Could be parallel (if truly independent):
// Note: Difficult in kernel without threading during boot
```

**3. Reduce logging verbosity**
```rust
// Debug builds: verbose
#[cfg(debug_assertions)]
log::debug!("Detailed info");

// Release builds: minimal
#[cfg(not(debug_assertions))]
log::info!("Essential info only");
```

**4. Optimize expensive operations**
```rust
// Identify slow operations with timing
let start = time::get_monotonic_ms();
expensive_operation();
let elapsed = time::get_monotonic_ms() - start;
if elapsed > 10 {
    log::warn!("Slow operation: {}ms", elapsed);
}
```

## Integration with Other Skills

### With kernel-debug-loop
```bash
# Fast iteration on boot fixes
kernel-debug-loop/scripts/quick_debug.py \
  --signal "BOOT_CHECKPOINT" \
  --timeout 10
```

### With log-analysis
```bash
# Extract boot sequence
echo '"initialized"' > /tmp/log-query.txt
./scripts/find-in-logs

# Find boot failures
echo '"PANIC|FAULT|ERROR"' > /tmp/log-query.txt
./scripts/find-in-logs
```

### With systematic-debugging
Document boot issues:
```markdown
# Problem
Kernel hangs after "Enabling interrupts"

# Root Cause
Timer interrupt handler called before scheduler ready

# Solution
Initialize scheduler before enabling interrupts

# Evidence
Before: Hang
After: Boot completes successfully
```

## Boot Checkpoints Reference

Essential checkpoints every boot should reach:

```
[✓] GDT initialized
[✓] IDT initialized
[✓] PIC initialized
[✓] Physical memory detected
[✓] Heap initialized
[✓] Timer initialized
[✓] Interrupts enabled
[✓] Threading initialized
[✓] Kernel ready
```

If boot stops before reaching a checkpoint, debug that subsystem.

## Best Practices

1. **Log initialization**: Every subsystem should log successful init
2. **Check prerequisites**: Verify dependencies before initializing
3. **Fail fast**: Panic early if critical init fails
4. **Add checkpoints**: Mark progress through boot sequence
5. **Time operations**: Identify bottlenecks
6. **Test changes**: Verify boot still works after changes
7. **Document order**: Comment why init order matters

## Quick Reference

### Key Boot Files
```
kernel/src/main.rs                  - Entry point, boot orchestration
kernel/src/gdt.rs                   - GDT initialization
kernel/src/interrupts/mod.rs        - IDT initialization
kernel/src/memory/frame_allocator.rs - Physical memory
kernel/src/time/timer.rs            - Timer initialization
kernel/src/time/rtc.rs              - RTC initialization
```

### Boot Signals to Watch
```
"GDT initialized"
"IDT initialized"
"Physical memory:"
"Heap:"
"Timer initialized"
"Enabling interrupts"
"Threading subsystem initialized"
"Kernel initialization complete"
```

## Summary

Boot analysis requires:
- Understanding the complete boot sequence
- Identifying checkpoints and dependencies
- Using logs to diagnose failures
- Comparing working vs broken boots
- Optimizing slow operations
- Ensuring proper initialization order

A well-understood boot sequence makes debugging initialization issues straightforward.
