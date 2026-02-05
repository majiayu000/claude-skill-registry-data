---
name: kernel-debug-loop
description: This skill should be used when performing fast iterative kernel debugging, running time-bound kernel sessions to detect specific log signals or test kernel behavior. Use for rapid feedback cycles during kernel development, boot sequence analysis, or feature verification.
---

# Kernel Debug Loop

Fast iterative kernel debugging with signal detection and time-bounded execution.

## Purpose

This skill provides a rapid feedback loop for kernel development by running the Breenix kernel for short, time-bounded sessions (default 15 seconds) while monitoring logs in real-time for specific signals. The kernel terminates immediately when the expected signal is detected, or when the timeout expires, enabling fast iteration cycles during debugging.

## When to Use This Skill

Use this skill when:

- **Iterative debugging**: Testing kernel changes with quick feedback loops
- **Boot sequence analysis**: Verifying the kernel reaches specific initialization checkpoints
- **Signal detection**: Waiting for specific kernel log messages before proceeding
- **Behavior verification**: Confirming the kernel responds correctly to tests or inputs
- **Fast failure detection**: Identifying boot failures or hangs quickly without waiting for full timeout
- **Checkpoint validation**: Ensuring the kernel reaches expected states during execution

## How to Use

### Basic Usage

The skill provides the `quick_debug.py` script for time-bounded kernel runs with optional signal detection.

**Run kernel with signal detection:**

```bash
kernel-debug-loop/scripts/quick_debug.py --signal "KERNEL_INITIALIZED"
```

This runs the kernel for up to 15 seconds, terminating immediately when "KERNEL_INITIALIZED" appears in the logs.

**Run kernel with custom timeout:**

```bash
kernel-debug-loop/scripts/quick_debug.py --timeout 30
```

Runs the kernel for up to 30 seconds without specific signal detection.

**Run in BIOS mode:**

```bash
kernel-debug-loop/scripts/quick_debug.py --signal "Boot complete" --mode bios
```

**Quiet mode (kernel output only):**

```bash
kernel-debug-loop/scripts/quick_debug.py --signal "READY" --quiet
```

Suppresses progress messages, showing only kernel output.

### Common Signals to Watch For

Based on Breenix's test infrastructure, common signals include:

- `🎯 KERNEL_POST_TESTS_COMPLETE 🎯` - All runtime tests completed
- `KERNEL_INITIALIZED` - Basic kernel initialization complete
- `USER_PROCESS_STARTED` - User process execution began
- `MEMORY_MANAGER_READY` - Memory management subsystem initialized
- Custom checkpoint markers added for specific debugging needs

### Workflow Patterns

#### Pattern 1: Fast Iteration During Development

When making changes to kernel initialization:

1. Make code change
2. Run: `kernel-debug-loop/scripts/quick_debug.py --signal "TARGET_CHECKPOINT" --timeout 10`
3. Verify signal appears or analyze why it didn't
4. Iterate

This provides feedback in ~10-15 seconds instead of waiting for full kernel execution or manual termination.

#### Pattern 2: Boot Sequence Verification

When debugging boot issues:

1. Identify the checkpoint expected to be reached
2. Run with that checkpoint as the signal
3. If timeout occurs, the kernel failed to reach that point
4. Examine the output buffer to see how far boot progressed
5. Add intermediate checkpoints to narrow down the failure point

#### Pattern 3: Regression Testing

When verifying fixes:

1. Run with the signal that was previously failing to appear
2. Success (signal found) confirms the fix worked
3. Failure (timeout) indicates the issue persists
4. The output buffer contains diagnostic information

#### Pattern 4: Performance Checkpoint Analysis

When optimizing boot time:

1. Run with a specific checkpoint signal
2. Note the elapsed time when signal is found
3. Make optimization changes
4. Re-run to measure improvement
5. The script reports exact elapsed time for comparison

### Integration with Claude Workflows

When assisting with kernel debugging:

1. **Suggest checkpoints**: Recommend adding strategic log markers at key points
2. **Run quick tests**: Use this script to verify changes before full test suite
3. **Analyze output**: Parse the output buffer to diagnose issues
4. **Iterate rapidly**: Chain multiple quick debug runs to test hypotheses
5. **Report findings**: Summarize what signals were found and timing information

### Script Output

The script provides:

- **Real-time kernel output**: All kernel logs stream to stdout during execution
- **Status indicators**: Visual feedback on signal detection and timeout
- **Session summary**: Success/failure status, timing, and output statistics
- **Exit code**: 0 if signal found (or no signal specified), 1 if timeout without signal

### Output Buffer Analysis

After a debug session, the entire kernel output is available for analysis:

- Search for error messages or warnings
- Verify initialization sequence order
- Check memory allocation patterns
- Analyze interrupt handling
- Examine test results

### Advanced Usage

**Multiple checkpoint verification:**

Run sequential sessions to verify a series of checkpoints:

```bash
for signal in "PHASE1" "PHASE2" "PHASE3"; do
  kernel-debug-loop/scripts/quick_debug.py --signal "$signal" --quiet || break
done
```

**Capture output for analysis:**

```bash
kernel-debug-loop/scripts/quick_debug.py --signal "READY" > kernel_output.log 2>&1
```

**Integration with test scripts:**

```python
import subprocess

result = subprocess.run(
    ['kernel-debug-loop/scripts/quick_debug.py', '--signal', 'TEST_COMPLETE'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("Test passed!")
else:
    print("Test failed or timed out")
    analyze_output(result.stdout)
```

## Best Practices

1. **Add strategic checkpoints**: Insert log markers at key kernel execution points
2. **Use descriptive signals**: Make signal patterns unique and meaningful
3. **Set appropriate timeouts**: Balance between waiting long enough and fast iteration
4. **Check exit codes**: Use return codes in scripts for automation
5. **Save output for analysis**: Redirect output when debugging complex issues
6. **Start broad, narrow down**: If a checkpoint isn't reached, add earlier checkpoints
7. **Combine with full tests**: Use for quick iteration, then validate with full test suite

## Technical Details

- **Timeout**: Default 15 seconds, configurable via `--timeout`
- **Signal detection**: Performs substring matching on each output line
- **Termination**: Graceful SIGTERM followed by SIGKILL if needed
- **Output buffering**: Line-buffered for real-time display
- **Exit codes**: 0 for success (signal found or no signal specified), 1 for timeout/failure

## Examples

**Verify kernel reaches user mode:**

```bash
kernel-debug-loop/scripts/quick_debug.py --signal "USER_PROCESS_STARTED" --timeout 20
```

**Quick sanity check after changes:**

```bash
kernel-debug-loop/scripts/quick_debug.py --timeout 5
```

**Debug memory initialization:**

```bash
kernel-debug-loop/scripts/quick_debug.py --signal "MEMORY_MANAGER_READY" --quiet > mem_init.log
```

**Test both UEFI and BIOS modes:**

```bash
kernel-debug-loop/scripts/quick_debug.py --signal "BOOT_COMPLETE" --mode uefi
kernel-debug-loop/scripts/quick_debug.py --signal "BOOT_COMPLETE" --mode bios
```
