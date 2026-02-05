---
name: debug-tb
description:
  Debug SystemVerilog testbench failures in the SVC project. Use when a
  testbench fails (make <module>_tb), to analyze CHECK_* assertion failures,
  watchdog timeouts, or unexpected signal values. Provides systematic debugging
  workflow using VCD waveforms and failure output analysis.
---

# Debugging Testbenches

## Workflow

1. **Capture failure output** - Run `make <module>_tb` and note the error
2. **Parse failure message** - Extract file, line, assertion type, and values
3. **Read failing test** - Find the test task and understand expected behavior
4. **Read module under test** - Understand the RTL logic being tested
5. **Analyze root cause** - Compare expected vs actual behavior
6. **Fix and verify** - Apply fix, run test again

## Failure Message Format

Test failures display:

```
FAIL
<file>:<line> CHECK_<type>(<signal>=0x<actual>, <expected>=0x<expected>)
make <module>_tb RUN=<test_name>
gtkwave .build/<module>.vcd &
```

Key information:

- **File:line** - Location of failed assertion
- **CHECK type** - EQ, TRUE, FALSE, WAIT_FOR, etc.
- **Signal values** - Actual vs expected (hex format)
- **Re-run command** - Isolate the failing test
- **VCD path** - Waveform file for visual debugging

## Assertion Types

| Macro                           | Fails When                               |
| ------------------------------- | ---------------------------------------- |
| `CHECK_TRUE(a)`                 | `a !== 1`                                |
| `CHECK_FALSE(a)`                | `a !== 0`                                |
| `CHECK_EQ(a, b)`                | `a !== b`                                |
| `CHECK_NEQ(a, b)`               | `a === b`                                |
| `CHECK_LT(a, b)`                | `a >= b` or X/Z values                   |
| `CHECK_WAIT_FOR(clk, sig, max)` | Signal never becomes 1 within max cycles |

Note: `CHECK_EQ` uses `!==` (4-state), so X/Z mismatches fail.

## Common Failure Patterns

### Signal Never Asserts (CHECK_WAIT_FOR timeout)

Causes:

- Missing handshake (valid without ready, or vice versa)
- Reset not properly released
- Clock domain issue
- Logic stuck waiting for upstream event

Debug steps:

1. Check reset sequence in test
2. Verify all required inputs are driven
3. Look for combinatorial loops or missing clock edges

### Wrong Value (CHECK_EQ failure)

Causes:

- Off-by-one in counters or indices
- Incorrect bit slicing or width mismatch
- Endianness confusion
- Combinatorial vs registered output timing

Debug steps:

1. Check data width consistency
2. Verify timing (are you checking one cycle too early/late?)
3. Trace data path through module

### X or Z Values

Causes:

- Uninitialized signal
- Missing reset initialization
- Unconnected port
- Multiple drivers

Debug steps:

1. Check all signals initialized in reset block
2. Verify port connections in UUT instantiation
3. Look for undriven module outputs

### Watchdog Timeout

Causes:

- Deadlock in handshake protocol
- Infinite loop in test logic
- Test expects condition that never occurs

Debug steps:

1. Find where simulation is stuck (last passing assertion)
2. Check for circular dependencies in ready/valid
3. Verify test doesn't wait for impossible state

## Debugging Commands

```bash
# Run specific test
make <module>_tb RUN=<test_name>

# View waveforms
gtkwave .build/<module>.vcd &

# Debug RISC-V core (prints instruction trace)
make <module>_tb SVC_RV_DBG_CPU=1

# Run all tests
make tb
```

## Adding Debug Output

When existing debug capabilities aren't sufficient, add `$display` statements
directly in the testbench being debugged. Don't try to brute-force reason
through signal values - actually look at what's happening.

```systemverilog
// Add ungated - just do it, remove later
$display("state=%0d valid=%b ready=%b data=%h", uut.state, out_valid, out_ready, out_data);
```

Add an `always` block in the testbench to monitor UUT internals:

```systemverilog
always @(posedge clk) begin
  if (uut.some_valid && uut.some_ready)
    $display("handshake: data=%h", uut.some_data);
end
```

Good things to display:

- UUT internal state machines (`uut.state`)
- Handshake completions (valid && ready)
- Counter values
- Data at pipeline stage boundaries

Remove debug statements after fixing the issue.

## Reading Waveforms

Focus signals:

1. `clk` and `rst_n` - Verify timing and reset
2. `*_valid` / `*_ready` - Handshake signals
3. Signals mentioned in failure message
4. Internal state machines (if exposed)

Look for:

- Signals stuck at X/Z
- Handshakes that never complete
- Unexpected transitions
- Missing clock edges

## AXI Debugging

For AXI/AXI-Lite protocol issues, see
[references/axi_debug.md](references/axi_debug.md).

## Reference

- Test framework: `rtl/common/svc_unit.sv`
- Full testbench guide: `docs/tb.md`
- Example testbench: `tb/common/svc_arbiter_tb.sv`
