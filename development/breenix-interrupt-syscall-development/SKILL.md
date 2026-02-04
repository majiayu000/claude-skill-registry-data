---
name: breenix-interrupt-syscall-development
description: Enforce pristine interrupt/syscall paths with no logging, diagnostics, or heavy operations. Use when developing interrupt handlers, syscall entry/exit, context switches, or timer code.
---

# Breenix Interrupt and Syscall Path Development

## CRITICAL PATH REQUIREMENTS - MANDATORY RULES

These requirements are **NON-NEGOTIABLE**. Violations will cause catastrophic performance degradation and subtle timing bugs that are extremely difficult to debug.

### ABSOLUTELY FORBIDDEN in interrupt/syscall paths:

1. **NO logging or serial output**
   - No `serial_println!` or `println!` of any kind
   - No debug prints, trace messages, or diagnostics
   - This includes "temporary" debug code that you plan to remove later
   - **EXCEPTION**: Only in initialization code that runs once at boot, before interrupts are enabled

2. **NO page table walks or memory diagnostics**
   - No calls to `translate_address()` or similar
   - No memory allocation diagnostics
   - No stack usage analysis
   - No heap introspection

3. **NO function calls that allocate or take locks**
   - No heap allocations (Box, Vec, String, etc.)
   - No lock acquisitions (except purpose-built lock-free critical sections)
   - No panic!() - handlers must be infallible or use explicit error codes

4. **Interrupt handlers must complete in < 1000 cycles**
   - On modern x86_64 at 2GHz, this is ~500 nanoseconds
   - Timer fires every 10ms = 20,000,000 cycles
   - You have 0.005% of that budget
   - Serial output takes 10,000+ cycles per character

5. **Context switch path must be deterministic and fast**
   - No conditional diagnostics based on process state
   - No complex validation beyond assertions
   - Register save/restore must be branchless where possible

### Why These Rules Exist

Violating these rules causes a specific failure pattern that is extremely difficult to diagnose:

**Case Study: The trace_iretq_to_ring3 Bug (December 2024)**

**Symptom**: Userspace process appeared to be created successfully but never executed a single instruction. Process remained stuck at RIP=0x40000000 (entry point) through 2,389 scheduler iterations.

**Root Cause**: Heavy diagnostics in `trace_iretq_to_ring3()`:
```rust
// THIS WAS THE BUG - DO NOT DO THIS
unsafe fn trace_iretq_to_ring3(frame: &TrapFrame) {
    serial_println!("=== IRETQ to Ring 3 ===");
    serial_println!("  RIP: {:#x}", frame.rip);
    serial_println!("  RSP: {:#x}", frame.rsp);
    // ... more logging ...
    let phys_addr = current_page_table.translate_address(VirtAddr::new(frame.rip));
    // ... even more diagnostics ...
}
```

**What Actually Happened**:

1. Kernel prepared perfect interrupt frame for userspace
2. `iretq` instruction successfully transitioned to Ring 3
3. **CPU immediately took timer interrupt within 100-500 cycles**
4. Userspace RIP never changed from 0x40000000 - not even one instruction executed
5. Timer preempted userspace before it could do anything
6. Scheduler selected same process again
7. Loop repeated 2,389 times with zero forward progress

**Why This Happened**:

Serial output in `trace_iretq_to_ring3()` consumed ~10,000-50,000 cycles. Timer fires every 20,000,000 cycles. The logging pushed the kernel dangerously close to the next timer interrupt. By the time `iretq` completed:

- Timer interrupt was already pending or fired within microseconds
- Userspace had 100-500 cycles of execution time (enough for ~50-250 instructions theoretically)
- But context switch overhead consumed most of that window
- Process never got to execute even its first `mov` instruction

**Evidence**:
- 2,389 scheduler loop iterations with ZERO userspace progress
- RIP frozen at 0x40000000 across all iterations
- All registers frozen in initial state
- Timer interrupt dominated CPU time

**The Fix**:

Remove ALL diagnostics from the interrupt return path:
```rust
// CORRECT - pristine path
unsafe fn return_to_ring3(frame: &TrapFrame) {
    // No logging. No diagnostics. Just return.
    core::arch::asm!(
        "iretq",
        in("rsp") frame as *const _ as u64,
        options(noreturn)
    );
}
```

After this fix: Userspace executed immediately and correctly.

### Key Insight

**You cannot debug interrupt paths by adding logging to interrupt paths.**

The act of observation changes the system behavior so dramatically that what you're debugging no longer exists. It's a kernel-level Heisenbug - the diagnostic itself destroys the evidence.

## APPROVED PATTERNS - What IS Allowed

These operations are acceptable in interrupt/syscall paths:

### 1. Atomic Counter Increments (for statistics)
```rust
TIMER_TICKS.fetch_add(1, Ordering::Relaxed);
SYSCALL_COUNT.fetch_add(1, Ordering::SeqCst);
```

### 2. Simple Flag Checks
```rust
if should_reschedule.load(Ordering::Acquire) {
    schedule();
}
```

### 3. Direct Register Manipulation
```rust
unsafe {
    core::arch::asm!(
        "mov {}, cr3",
        out(reg) cr3_value
    );
}
```

### 4. Calling Other Minimal Inline Functions
```rust
#[inline(always)]
fn save_context(regs: &mut Registers) {
    // Direct memory writes, no allocations
    regs.rax = read_rax();
    regs.rbx = read_rbx();
    // ...
}
```

### 5. Assertions (but use sparingly)
```rust
debug_assert!(is_kernel_address(stack_ptr));
debug_assert_eq!(cs & 3, 0); // Must be ring 0
```

Assertions compile to nothing in release builds, so they're safe for sanity checks.

## DEBUGGING ALTERNATIVES - How to Debug Without Breaking the Path

Since you cannot add logging to interrupt paths, use these techniques instead:

### 1. QEMU Interrupt Tracing (BEST OPTION)
```bash
# External interrupt tracing - zero overhead
cargo run --bin qemu-uefi -- -d int,cpu_reset -D /tmp/qemu.log

# Then grep the log
grep "interrupt" /tmp/qemu.log
```

This shows every interrupt entry/exit with register state. No kernel instrumentation required.

### 2. GDB Breakpoints (SECOND BEST)
```bash
# Terminal 1: Start QEMU with GDB server
cargo run --bin qemu-uefi -- -s -S

# Terminal 2: Attach GDB
gdb target/x86_64-breenix/release/breenix
(gdb) target remote :1234
(gdb) break timer_interrupt_handler
(gdb) continue
```

GDB lets you inspect state without modifying the timing characteristics.

### 3. Conditional Compilation (USE SPARINGLY)
```rust
#[cfg(debug_assertions)]
{
    // This compiles out in release builds
    INTERRUPT_COUNT.fetch_add(1, Ordering::Relaxed);
}
```

Only for counters and flags - never for serial output.

### 4. Post-Interrupt Diagnostics
```rust
fn timer_interrupt_handler() {
    // PRISTINE PATH - no logging
    TIMER_TICKS.fetch_add(1, Ordering::Relaxed);
    acknowledge_interrupt();
    schedule_if_needed();
}

// Later, in a non-critical path:
pub fn print_timer_stats() {
    let ticks = TIMER_TICKS.load(Ordering::Relaxed);
    serial_println!("Timer ticks: {}", ticks);
}
```

Accumulate data in the hot path, log it in a cold path.

### 5. Hardware Performance Counters (ADVANCED)
```rust
// Use CPU performance monitoring to count cycles
// This has minimal overhead (~10 cycles per read)
let start = read_tsc();
critical_operation();
let end = read_tsc();
CYCLE_COUNTS[operation_id].fetch_add(end - start, Ordering::Relaxed);
```

## CODE REVIEW CHECKLIST

Before merging ANY code that touches interrupt or syscall paths, ask these questions:

### Mandatory Rejection Criteria

- [ ] **Does this add any serial output?** → **REJECT IMMEDIATELY**
- [ ] **Does this add any memory allocation?** → **REJECT IMMEDIATELY**
- [ ] **Does this add any heap diagnostics?** → **REJECT IMMEDIATELY**
- [ ] **Does this add page table walks in hot path?** → **REJECT IMMEDIATELY**

### Careful Review Required

- [ ] **Does this take any locks?** → If yes, document why it's necessary and prove it's lock-free
- [ ] **Does this call external functions?** → Audit those functions for the above violations
- [ ] **What's the worst-case cycle count?** → Must be < 1000 cycles for interrupt handlers
- [ ] **Is this code conditional on debug mode?** → Verify it compiles out in release

### Acceptable Operations

- [ ] **Atomic counter increments?** → OK if relaxed ordering
- [ ] **Simple flag checks?** → OK if no branching complexity
- [ ] **Direct register reads/writes?** → OK, encouraged
- [ ] **Inline function calls?** → OK if callee is also pristine

### Testing Requirements

- [ ] **Did you test in release mode?** → Debug builds have different timing
- [ ] **Did you verify userspace makes forward progress?** → RIP should change
- [ ] **Did you run for multiple seconds?** → Timing bugs may be intermittent
- [ ] **Did you check QEMU interrupt logs?** → Verify interrupt frequency is sane

## IMPLEMENTATION WORKFLOW

When implementing interrupt or syscall handlers:

### 1. Design the Pristine Path First
```rust
// Write this FIRST - the minimal handler
pub extern "C" fn syscall_entry() {
    // Save registers
    // Dispatch to handler
    // Restore registers
    // Return
}
```

### 2. Add Atomic Counters for Observability
```rust
static SYSCALL_COUNTS: [AtomicU64; 256] = [/* ... */];

pub extern "C" fn syscall_entry(syscall_num: u64) {
    SYSCALL_COUNTS[syscall_num as usize].fetch_add(1, Ordering::Relaxed);
    // ... rest of handler
}
```

### 3. Test in Release Mode
```bash
cargo run --release --bin qemu-uefi
```

### 4. Verify with External Tracing
```bash
cargo run --release --bin qemu-uefi -- -d int -D /tmp/qemu.log
```

### 5. Only Then Add Debug-Only Diagnostics (if absolutely necessary)
```rust
#[cfg(all(debug_assertions, feature = "interrupt-trace"))]
{
    INTERRUPT_TRACE_BUFFER[index].store(rip, Ordering::Relaxed);
}
```

## ANTI-PATTERNS TO AVOID

### Anti-Pattern 1: "Temporary" Debug Logging
```rust
// NO! This is how bugs hide for months
fn timer_handler() {
    serial_println!("Timer fired"); // "I'll remove this later"
    // ...
}
```

**Why it's wrong**: You'll forget to remove it, or it will get copied to other handlers. When the bug appears in production, the logging will be the bug.

### Anti-Pattern 2: Conditional Diagnostics on Process State
```rust
// NO! This creates timing-dependent behavior
fn context_switch(next: &Process) {
    if next.is_userspace() {
        serial_println!("Switching to PID {}", next.pid); // WRONG
    }
    // ...
}
```

**Why it's wrong**: Userspace processes get slower context switches than kernel processes. Creates Heisenbugs where timing depends on process type.

### Anti-Pattern 3: "Just This Once" Memory Allocation
```rust
// NO! Interrupt handlers must be infallible
fn interrupt_handler() {
    let msg = format!("Interrupt at {:#x}", rip); // WRONG - allocates
    log_message(&msg);
}
```

**Why it's wrong**: What if the allocator is out of memory? What if the allocator lock is held? Handler must never fail.

### Anti-Pattern 4: Complex Validation
```rust
// NO! Validation should be in non-critical paths
fn syscall_handler(num: u64, args: &[u64]) {
    validate_user_memory(args[0]); // May page fault, walk tables, allocate
    validate_file_descriptor(args[1]); // May take locks
    // ...
}
```

**Why it's wrong**: Validation can be expensive. Do it before entering the critical path, or use hardware-based validation (page faults).

## SUCCESS METRICS

You've implemented a pristine interrupt/syscall path if:

1. **Userspace makes forward progress immediately**
   - RIP changes on every scheduler quantum
   - Processes complete in expected time
   - No infinite loops at entry point

2. **Interrupt frequency is stable**
   - Timer fires at configured rate (e.g., 100 Hz = every 10ms)
   - No interrupt storms
   - QEMU logs show regular intervals

3. **Zero overhead in release builds**
   - No serial output
   - No allocations
   - Cycle counts < 1000 per handler

4. **Debuggable with external tools**
   - QEMU tracing shows correct behavior
   - GDB breakpoints work
   - Performance counters provide visibility

## WHEN TO USE THIS SKILL

Invoke this skill when:

- Implementing new interrupt handlers (timer, keyboard, syscall, page fault)
- Modifying syscall entry/exit paths
- Implementing context switch logic
- Adding scheduler hooks
- Debugging performance issues where userspace seems "stuck"
- Reviewing PRs that touch interrupt.asm, syscall/entry.asm, or timer.rs
- Investigating "works in debug, fails in release" bugs (timing-related)

## RELATED SKILLS

- `breenix-kernel-debug-loop`: For iterative debugging with external tools
- `breenix-systematic-debugging`: For documenting root cause analysis
- `breenix-code-quality-check`: For enforcing zero-warning builds
- `breenix-interrupt-trace`: For QEMU-based interrupt tracing
- `breenix-gdb-attach`: For breakpoint-based debugging

## REFERENCES

- Intel Software Developer Manual Vol 3, Chapter 6: Interrupt and Exception Handling
- AMD64 Architecture Manual Vol 2, Chapter 8: Exceptions and Interrupts
- Linux kernel: arch/x86/entry/entry_64.S - pristine syscall entry path
- FreeBSD: sys/amd64/amd64/exception.S - interrupt handling

## VERSION HISTORY

- v1.0 (2024-12-02): Initial skill creation after fixing trace_iretq_to_ring3 bug
