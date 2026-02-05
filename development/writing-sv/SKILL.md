---
name: writing-sv
description:
  Provides SVC naming conventions, comment style, code structure order, and
  reset patterns. Triggers when writing or modifying any .sv file.
---

# Writing SystemVerilog

## Naming Conventions

- **Modules**: `svc_` prefix (e.g., `svc_arbiter`)
- **Clock**: Always `clk`
- **Reset**: Always `rst_n` (active-low)
- **Next-cycle signals**: `_next` suffix (e.g., `grant_valid_next`)
- **Pipeline stages**: `_p1`, `_p2` suffixes
- **Interfaces**: `s_` for subordinate, `m_` for manager
- **Valid/ready**: Use `valid`/`ready` for stream interfaces
- **Multi-cycle ops**: Use `start`/`done`

## Comment Style

- **NEVER use end-of-line comments** - ALL comments on line above
- Use blank comment separators for sections:

```systemverilog
//
// Write pointer logic
//
```

## Signal Declarations

- Use `logic` instead of `wire`/`reg`
- Declare each signal on separate line, never group
- Align signal widths for readability:

```systemverilog
logic [  ADDR_WIDTH:0] ptr;
logic [DATA_WIDTH-1:0] data;
```

## Code Structure Order

1. Localparams
2. Internal signals
3. Child module instantiations
4. Combinational logic (`always_comb`)
5. Sequential logic (`always_ff`)
6. Formal assertions (if applicable)

## State Machines

- Use `typedef enum` without explicit bit width
- Prefix states with `STATE_` (or `READ_STATE_`/`WRITE_STATE_` for multiple
  FSMs)
- Separate `always_ff` for transitions, `always_comb` for outputs

```systemverilog
typedef enum {
  STATE_IDLE,
  STATE_BUSY,
  STATE_DONE
} state_t;
```

## Reset Pattern

Always use synchronous active-low reset:

```systemverilog
always_ff @(posedge clk) begin
  if (!rst_n) begin
    counter <= '0;
    state   <= STATE_IDLE;
  end else begin
    counter <= counter_next;
    state   <= state_next;
  end
end
```

## Assignments

- Use `always_ff` with non-blocking (`<=`) for sequential logic
- Use `always_comb` with blocking (`=`) for combinational logic
- For complex conditionals, prefer if/else over ternary operators

## Unused Signals

Use the `SVC_UNUSED` macro:

```systemverilog
`SVC_UNUSED({signal1, signal2, signal3});
```

## After Writing Code

Always run:

- `make format` - format code
- `make lint` - check for errors

For full details see `docs/style.md`
