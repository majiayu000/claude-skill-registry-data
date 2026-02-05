---
name: qemu-debug-session
description: Use when setting up comprehensive QEMU debugging for Breenix - investigating interrupt handling bugs, debugging memory management issues, analyzing boot sequence problems, tracing hardware interactions, or inspecting CPU state during failures.
---

# Breenix QEMU Debug Session

This skill provides comprehensive QEMU debugging capabilities for Breenix kernel development, including live inspection, detailed logging, and monitor access.

## Usage

Invoke this skill when:
- Investigating interrupt handling bugs
- Debugging memory management issues
- Analyzing boot sequence problems
- Tracing hardware interactions
- Inspecting CPU state during failures

## Debugging Scenarios

### 1. Interrupt and Timer Debugging

For interrupt-related issues (context switches, timer behavior, IRQ handling):

```bash
BREENIX_QEMU_LOG_PATH=/tmp/breenix-debug.log \
BREENIX_QEMU_DEBUG_FLAGS="int,cpu_reset,guest_errors" \
BREENIX_QEMU_MONITOR=tcp \
cargo run --release --bin qemu-uefi -- -serial stdio -display none
```

This enables:
- `int`: Log all interrupts (IRQ delivery, exceptions, traps)
- `cpu_reset`: Track CPU resets and initialization
- `guest_errors`: Capture guest OS errors (page faults, invalid ops, etc.)

### 2. Memory and Page Table Debugging

For memory allocation, paging, or MMU issues:

```bash
BREENIX_QEMU_LOG_PATH=/tmp/breenix-memory.log \
BREENIX_QEMU_DEBUG_FLAGS="mmu,guest_errors,page" \
BREENIX_QEMU_MONITOR=tcp \
cargo run --release --bin qemu-uefi -- -serial stdio -display none
```

This enables:
- `mmu`: Memory Management Unit operations
- `page`: Page table walks and TLB operations
- `guest_errors`: Page faults and access violations

### 3. Boot Sequence Analysis

For boot hangs, firmware issues, or early initialization problems:

```bash
BREENIX_QEMU_DEBUGCON_FILE=/tmp/ovmf-debug.log \
BREENIX_QEMU_LOG_PATH=/tmp/breenix-boot.log \
BREENIX_QEMU_DEBUG_FLAGS="guest_errors,cpu_reset" \
BREENIX_QEMU_MONITOR=tcp \
cargo run --release --bin qemu-uefi -- -serial stdio -display none
```

This captures:
- OVMF firmware debug output to separate file
- CPU reset events
- Guest errors during boot

### 4. CPU State Inspection

For register corruption, flag issues, or instruction tracing:

```bash
BREENIX_QEMU_LOG_PATH=/tmp/breenix-cpu.log \
BREENIX_QEMU_DEBUG_FLAGS="cpu,in_asm,int,guest_errors" \
BREENIX_QEMU_MONITOR=tcp \
cargo run --release --bin qemu-uefi -- -serial stdio -display none
```

WARNING: This generates MASSIVE logs (100+ MB/second). Use only for targeted debugging:
- `cpu`: Dump CPU state after each instruction
- `in_asm`: Show instruction disassembly
- Only run for short durations!

## QEMU Monitor Access

The monitor allows live inspection of the running kernel without stopping execution.

### TCP Monitor (Recommended for Development)

```bash
BREENIX_QEMU_MONITOR=tcp cargo run --release --bin qemu-uefi
```

Then in another terminal:
```bash
telnet localhost 4444
```

### Stdio Monitor (Interactive)

```bash
BREENIX_QEMU_MONITOR=stdio cargo run --release --bin qemu-uefi
```

WARNING: Stdio monitor mixes with kernel output. Use TCP for cleaner separation.

## Monitor Commands

Once connected to the monitor, useful commands:

### CPU and Register Inspection
```
info registers          # Show all CPU registers
info registers -a       # Show all registers including hidden state
info cpus              # List all virtual CPUs
info fpu               # Show FPU registers
info idt               # Show Interrupt Descriptor Table
info gdt               # Show Global Descriptor Table
```

### Memory Inspection
```
info mem               # Show virtual memory mappings
info tlb               # Show TLB entries
x/10i $rip             # Disassemble 10 instructions at current RIP
x/32xb 0xdeadbeef      # Dump 32 bytes at address in hex
xp/10gx 0xdeadbeef     # Dump 10 8-byte values (physical address)
```

### Interrupt and Timer State
```
info pic               # Show PIC (legacy interrupt controller) state
info ioapic            # Show I/O APIC state
info lapic             # Show Local APIC state
info qtree             # Show device tree (find timer devices)
```

### Execution Control
```
stop                   # Pause execution
cont                   # Resume execution
system_reset          # Reset the system
quit                  # Exit QEMU
```

## Available Debug Flags

Set via `BREENIX_QEMU_DEBUG_FLAGS` (comma-separated):

### High-Level Flags
- `guest_errors`: Guest OS errors (page faults, invalid ops) - **Start here**
- `unimp`: Unimplemented device/feature access
- `int`: Interrupt delivery and exceptions
- `cpu_reset`: CPU initialization and resets

### Memory Flags
- `mmu`: MMU operations (PT walks, TLB fills)
- `page`: Page table operations
- `pcall`: Protected mode call gates

### CPU Flags (VERY VERBOSE)
- `cpu`: Full CPU state after each instruction
- `in_asm`: Disassembly of executed instructions
- `exec`: Basic execution trace
- `nochain`: Disable TB chaining

### Device Flags
- `ioport`: I/O port access (useful for timer/PIC debugging)
- `pci`: PCI configuration space access

## Log Analysis Tips

### Finding Interrupt Issues

```bash
grep -A5 "exception\|interrupt\|IRQ" /tmp/breenix-debug.log
```

Look for:
- Unexpected exceptions (e.g., GPF, Page Fault during interrupt handling)
- Missing or duplicate interrupts
- Interrupt delivery to wrong CPU

### Detecting Timer Problems

```bash
grep -E "APIC|timer|IRQ 0|IRQ 32" /tmp/breenix-debug.log
```

Look for:
- Timer interrupts not firing at expected rate
- Spurious interrupts
- APIC timer configuration changes

### Memory Issues

```bash
grep -E "page fault|#PF|CR3|MMU" /tmp/breenix-memory.log
```

Look for:
- Page faults in kernel space (usually bugs)
- CR3 changes (context switches)
- Invalid page table entries

### Boot Hangs

```bash
tail -f /tmp/ovmf-debug.log  # Watch firmware output
grep "cpu_reset\|triple fault" /tmp/breenix-boot.log
```

Look for:
- Triple faults (usually bad IDT or bad interrupt handler)
- Hangs after specific firmware phase
- Repeated resets

## Example Debugging Workflow

### Scenario: Timer interrupt not firing

1. **Start with basic interrupt logging:**
```bash
BREENIX_QEMU_LOG_PATH=/tmp/debug.log \
BREENIX_QEMU_DEBUG_FLAGS="int,guest_errors" \
BREENIX_QEMU_MONITOR=tcp \
cargo run --release --bin qemu-uefi -- -serial stdio
```

2. **In another terminal, connect to monitor:**
```bash
telnet localhost 4444
```

3. **Check APIC state:**
```
info lapic
```

Look for:
- Timer mode (one-shot vs periodic)
- Initial count vs current count
- Whether timer interrupt is masked

4. **Check interrupt delivery:**
```
info pic
info ioapic
```

Verify IRQ 0 (PIT) or IRQ 32 (APIC timer) is not masked.

5. **Grep log for interrupt activity:**
```bash
grep "IRQ.*timer\|exception 32" /tmp/debug.log | less
```

6. **If no interrupts appear, check IDT:**
In monitor:
```
info idt
```

Verify entry 32 (or appropriate vector) has valid handler address.

## Environment Variables Reference

| Variable | Values | Purpose |
|----------|--------|---------|
| `BREENIX_QEMU_LOG_PATH` | File path | Destination for QEMU debug logs |
| `BREENIX_QEMU_DEBUG_FLAGS` | Comma-separated flags | Enable specific QEMU logging (see flags above) |
| `BREENIX_QEMU_MONITOR` | `none`/`stdio`/`tcp` | Monitor interface (default: none) |
| `BREENIX_QEMU_DEBUGCON_FILE` | File path | Capture firmware debug console (0x402) |
| `BREENIX_QEMU_DEBUGCON` | `1` | Route debug console to stdio |
| `BREENIX_VISUAL_TEST` | `1` | Show QEMU window (for visual debugging) |
| `BREENIX_QEMU_STORAGE` | `ide`/`virtio` | Storage controller type |
| `BREENIX_GDB` | `1` | Enable GDB server on localhost:1234 |

## Common Pitfalls

1. **Stdio monitor + serial output = chaos**: Always use `BREENIX_QEMU_MONITOR=tcp`
2. **Forgetting -serial stdio**: Monitor doesn't show kernel output; you need both
3. **Too much logging**: Start with `guest_errors,int`, not `cpu,in_asm`
4. **Log file grows huge**: Check log size; `cpu` flag can fill GB in seconds
5. **Monitor commands fail**: Ensure QEMU is still running (kernel panic exits QEMU)

## Quick Reference Card

```bash
# Start debugging session (interrupt focus)
BREENIX_QEMU_LOG_PATH=/tmp/debug.log \
BREENIX_QEMU_DEBUG_FLAGS="int,guest_errors" \
BREENIX_QEMU_MONITOR=tcp \
cargo run --release --bin qemu-uefi -- -serial stdio

# Connect to monitor
telnet localhost 4444

# Essential monitor commands
info registers         # CPU state
info lapic            # Timer and interrupts
x/10i $rip            # Disassemble at current position
info mem              # Virtual memory map

# Analyze logs
grep -A5 "exception\|IRQ" /tmp/debug.log
```

## Notes

- Debug logging adds overhead; execution will be slower
- TCP monitor allows inspection without pausing execution
- Most bugs are visible with just `guest_errors,int` logging
- Save logs before QEMU exits; they're not persistent across runs
- GDB stub (`BREENIX_GDB=1`) is complementary; use for source-level debugging
