---
name: implementing-valid-ready
description:
  Provides SVC-specific valid/ready streaming interface patterns and common
  pitfalls. Triggers when implementing valid/ready handshakes or debugging
  backpressure issues.
---

# Valid/Ready Interfaces

## Protocol Rules

1. **Transfer occurs when both `valid` AND `ready` are high** on the same clock
   edge
2. **Producer controls `valid`**, consumer controls `ready`
3. **Data must be stable** while `valid` is high until transfer completes
4. **`valid` should not depend on `ready`** (to avoid combinational loops)
5. **`ready` can depend on `valid`** (consumer can wait to see valid data)

## Basic Pattern

### Port Declaration

```systemverilog
// Input side (this module is consumer)
input  logic             in_valid,
input  logic [WIDTH-1:0] in_data,
output logic             in_ready,

// Output side (this module is producer)
output logic             out_valid,
output logic [WIDTH-1:0] out_data,
input  logic             out_ready
```

### Combinational Valid/Ready Logic

```systemverilog
always_comb begin
  out_valid = data_available && !blocked;
  in_ready  = !full && !blocked;
end
```

### Transfer Detection

```systemverilog
always_ff @(posedge clk) begin
  if (!rst_n) begin
    // Reset state
  end else begin
    // Capture on handshake
    if (in_valid && in_ready) begin
      captured_data <= in_data;
    end

    // Produce on handshake
    if (out_valid && out_ready) begin
      // Data was consumed, can produce next
    end
  end
end
```

## Common Patterns

### Pass-Through (Zero Latency)

```systemverilog
assign out_valid = in_valid;
assign out_data  = in_data;
assign in_ready  = out_ready;
```

### Single Register Buffer

```systemverilog
logic             buf_valid;
logic [WIDTH-1:0] buf_data;

assign in_ready  = !buf_valid || out_ready;
assign out_valid = buf_valid;
assign out_data  = buf_data;

always_ff @(posedge clk) begin
  if (!rst_n) begin
    buf_valid <= 1'b0;
  end else begin
    if (in_valid && in_ready) begin
      buf_valid <= 1'b1;
      buf_data  <= in_data;
    end else if (out_ready) begin
      buf_valid <= 1'b0;
    end
  end
end
```

### Backpressure Handling

When downstream is not ready, hold data:

```systemverilog
always_ff @(posedge clk) begin
  if (!rst_n) begin
    out_valid <= 1'b0;
  end else begin
    if (out_valid && !out_ready) begin
      // Hold - downstream not ready
    end else if (have_new_data) begin
      out_valid <= 1'b1;
      out_data  <= new_data;
    end else begin
      out_valid <= 1'b0;
    end
  end
end
```

## Common Pitfalls

### Combinational Loop

**BAD** - `valid` depends on `ready`:

```systemverilog
assign out_valid = in_valid && out_ready;  // Creates loop!
```

**GOOD** - `valid` independent of `ready`:

```systemverilog
assign out_valid = in_valid && internal_condition;
```

### Missing Backpressure

**BAD** - Ignoring ready:

```systemverilog
if (in_valid) begin  // Missing && in_ready
  process_data(in_data);
end
```

**GOOD** - Proper handshake:

```systemverilog
if (in_valid && in_ready) begin
  process_data(in_data);
end
```

### Data Instability

**BAD** - Data changes while valid:

```systemverilog
assign out_data = some_changing_signal;  // Changes every cycle!
```

**GOOD** - Registered data:

```systemverilog
always_ff @(posedge clk) begin
  if (capture_condition) begin
    out_data <= stable_source;
  end
end
```

## Testing Valid/Ready

In testbenches, test:

1. Normal flow (both valid and ready)
2. Backpressure (valid high, ready low)
3. Not-ready consumer (ready toggling)
4. Burst transfers
5. Idle periods

```systemverilog
task automatic test_backpressure();
  out_ready = 1'b0;  // Apply backpressure
  in_valid  = 1'b1;
  in_data   = 8'h42;

  repeat (3) `TICK(clk);

  // Verify data held stable
  `CHECK_TRUE(out_valid);
  `CHECK_EQ(out_data, 8'h42);

  out_ready = 1'b1;  // Release
  `TICK(clk);
endtask
```

## Reference Implementations

- `rtl/fifo/svc_sync_fifo.sv` - FIFO with valid/ready
- `rtl/common/svc_arbiter.sv` - Arbiter using handshakes
