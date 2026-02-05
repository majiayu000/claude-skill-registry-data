---
name: adding-formal
description:
  Provides ASSERT/ASSUME macro pattern, .sby file template, and f_past_valid
  usage. Triggers when adding formal verification or writing assertions.
---

# Adding Formal Verification

## Overview

Formal verification uses SymbiYosys (sby). Assertions are embedded in the RTL
module itself within `ifdef FORMAL` blocks. A separate `.sby` file configures
the formal run.

## Adding Formal to a Module

### Step 1: Add Formal Block to RTL

Add at the end of the module, before `endmodule`:

```systemverilog
`ifdef FORMAL
`ifdef FORMAL_SVC_MODULE_NAME
  `define ASSERT(label, a) label: assert(a)
  `define ASSUME(label, a) label: assume(a)
  `define COVER(label, a) label: cover(a)
`else
  `define ASSERT(label, a) label: assume(a)
  `define ASSUME(label, a) label: assert(a)
  `define COVER(label, a)
`endif

  logic f_past_valid = 1'b0;
  always @(posedge clk) begin
    f_past_valid <= 1'b1;
  end

  always @(*) begin
    assume (rst_n == f_past_valid);
  end

  //
  // Assumptions
  //
  always_ff @(posedge clk) begin
    if (f_past_valid && $past(rst_n) && rst_n) begin
      // Add assumptions about inputs here
    end
  end

  //
  // Assertions
  //
  always_ff @(posedge clk) begin
    if (f_past_valid && $past(rst_n) && rst_n) begin
      // Add assertions here
      `ASSERT(a_example, some_condition);
    end
  end

  //
  // Covers
  //
  always_ff @(posedge clk) begin
    if (f_past_valid && $past(rst_n) && rst_n) begin
      `COVER(c_example, interesting_scenario);
    end
  end

  `undef ASSERT
  `undef ASSUME
  `undef COVER
`endif
```

### Step 2: Create .sby File

Create `tb/formal/svc_module_name.sby`:

```
[tasks]
bmc
cover

[options]
bmc: mode bmc
cover: mode cover
cover: depth 40

[engines]
smtbmc boolector

[script]
read_verilog -formal -DFORMAL_SVC_MODULE_NAME -sv path/to/svc_module_name.sv
prep -top svc_module_name

[files]
rtl/
```

## Key Patterns

### The Dual-Use Macro Pattern

The `ASSERT`/`ASSUME` macros swap roles based on whether the module is being
verified directly:

- When verifying this module: `ASSERT` = assert, `ASSUME` = assume
- When used as submodule: `ASSERT` = assume (becomes constraint), `ASSUME` =
  assert (verified by parent)

### f_past_valid

Always use `f_past_valid` to guard `$past()` references - they're undefined on
the first cycle.

### Reset Assumption

```systemverilog
assume (rst_n == f_past_valid);
```

This assumes reset is active at start, then deasserted.

## Common Assertions

```systemverilog
// Signal stability
`ASSERT(a_stable, $stable(signal) || condition_allowing_change);

// Grant corresponds to request
`ASSERT(a_grant_req, grant_valid |-> $past(request != 0));

// Valid range
`ASSERT(a_range, signal < MAX_VALUE);
```

## Running Formal

```bash
make <module>_f     # Run formal verification for module
make formal         # Run all formal verification
```

**NEVER run `sby` directly** - always use make targets.

## Reference

See `rtl/common/svc_arbiter.sv` for a complete formal verification example
within a module.
