---
name: writing-module
description:
  Provides module template with include guard, port ordering, and checklist.
  Triggers when creating a new svc_ module from scratch.
---

# Writing a New Module

## Module Template

```systemverilog
`ifndef SVC_MODULE_NAME_SV
`define SVC_MODULE_NAME_SV

`include "svc.sv"

module svc_module_name #(
    parameter WIDTH = 32
) (
    input  logic             clk,
    input  logic             rst_n,

    input  logic             in_valid,
    input  logic [WIDTH-1:0] in_data,
    output logic             in_ready,

    output logic             out_valid,
    output logic [WIDTH-1:0] out_data,
    input  logic             out_ready
);
  //
  // Localparams
  //

  //
  // Internal signals
  //
  logic [WIDTH-1:0] data_next;

  //
  // Child module instantiations
  //

  //
  // Combinational logic
  //
  always_comb begin
    data_next = in_data;
  end

  //
  // Sequential logic
  //
  always_ff @(posedge clk) begin
    if (!rst_n) begin
      out_valid <= 1'b0;
      out_data  <= '0;
    end else begin
      // Logic here
    end
  end

endmodule

`endif
```

## Checklist

- [ ] Include guard with `_SV` suffix (uppercase module name)
- [ ] `include "svc.sv"` after guard
- [ ] Module name has `svc_` prefix
- [ ] Ports: `clk`, `rst_n` first
- [ ] Parameters before ports
- [ ] Group related ports with blank lines
- [ ] Align port declarations
- [ ] Comments above code, never at end of line
- [ ] Use blank comment blocks for section separators
- [ ] Run `make format` when done
- [ ] Run `make lint` before committing

## File Location

Place in appropriate `rtl/` subdirectory:

- `rtl/axi/` - AXI/AXI-Lite
- `rtl/cdc/` - Clock domain crossing
- `rtl/common/` - Fundamental building blocks
- `rtl/fifo/` - FIFOs
- `rtl/gfx/` - Graphics/VGA
- `rtl/ice40/` - iCE40 FPGA-specific
- `rtl/rv/` - RISC-V processor
- `rtl/stats/` - Statistics collection
- `rtl/uart/` - Serial communication

## Reference Implementation

See `rtl/common/svc_arbiter.sv` for a well-structured example.
