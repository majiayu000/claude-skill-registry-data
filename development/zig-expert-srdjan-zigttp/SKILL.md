---
name: zig-expert
description: Write idiomatic Zig code following the Zen of Zig philosophy. Use for systems programming with Zig (.zig files), covering manual memory management with allocators, error unions and explicit error handling, compile-time programming (comptime), data-oriented design, and the new async/Io model. Applies functional programming parallels (Result types, ADTs, explicit effects) for C-free systems development.
---

# Idiomatic Zig Programming

Expert guidance for writing idiomatic Zig code that embodies the Zen of Zig: explicit intent, no hidden control flow, and compile-time over runtime.

## Zen of Zig (Core Philosophy)

These principles govern all idiomatic Zig code:

| Principle | Implication |
|-----------|-------------|
| Communicate intent precisely | Explicit code; APIs make requirements obvious |
| Edge cases matter | No undefined behaviors glossed over |
| Favor reading over writing | Optimize for clarity and maintainability |
| One obvious way | Avoid multiple complex features for same task |
| Runtime crashes > bugs | Fail fast and loudly, never corrupt state silently |
| Compile errors > runtime crashes | Catch issues at compile-time when possible |
| Resource deallocation must succeed | Design APIs with allocation failure in mind |
| Memory is a resource | Manage memory as consciously as any other resource |
| No hidden control flow | No exceptions, no GC, no implicit allocations |

## FP Conceptual Parallels

Zig shares key concepts with functional programming:

| FP Concept | Zig Equivalent |
|------------|----------------|
| Result/Either type | Error union `!T` (either error or value) |
| Option/Maybe | Optional `?T` (nullable type) |
| ADTs / Sum types | Tagged unions with `union(enum)` |
| Pattern matching | `switch` with exhaustive handling |
| Explicit effects | Allocator/Io parameters (dependency injection) |
| Immutability preference | `const` by default, `var` only when needed |
| Pure functions | Functions without hidden state or allocations |

## Workflow Decision Tree

1. **Declaring a binding?** → Use `const` unless mutation required
2. **Function needs memory?** → Accept `Allocator` parameter, never global alloc
3. **Function can fail?** → Return error union `!T`, use `try` to propagate
4. **Handling an error?** → Use `catch` with explicit handler or `try` to propagate
5. **Need cleanup on exit?** → Use `defer` immediately after acquisition
6. **Cleanup only on error?** → Use `errdefer` for conditional cleanup
7. **Need generic code?** → Use `comptime` type parameters
8. **Compile-time known value?** → Use `comptime` to evaluate at build time
9. **Calling C code?** → Use `@cImport` for seamless FFI
10. **Need async I/O?** → Pass `Io` interface, use `io.async()` and `future.await()`
11. **Optimizing hot path?** → Consider data-oriented design (SoA vs AoS)

## Essential Patterns

### Error Unions (Result Type Equivalent)

```zig
const FileError = error{ NotFound, PermissionDenied, InvalidPath };

fn readConfig(path: []const u8) FileError!Config {
    const file = std.fs.cwd().openFile(path, .{}) catch |err| {
        return switch (err) {
            error.FileNotFound => error.NotFound,
            error.AccessDenied => error.PermissionDenied,
            else => error.InvalidPath,
        };
    };
    defer file.close();
    // ... parse config
    return config;
}

// Propagate with try (like Rust's ?)
pub fn main() !void {
    const config = try readConfig("app.conf");
    // ...
}

// Handle explicitly with catch
pub fn mainSafe() void {
    const config = readConfig("app.conf") catch |err| {
        std.debug.print("Failed: {}\n", .{err});
        return;
    };
    // ...
}
```

### Allocator Pattern (Explicit Effects)

```zig
const std = @import("std");

// Function signature communicates: "I need to allocate"
fn processData(allocator: std.mem.Allocator, input: []const u8) ![]u8 {
    var result = try allocator.alloc(u8, input.len * 2);
    errdefer allocator.free(result); // cleanup only on error path
    
    // ... process into result
    
    return result; // caller owns this memory
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    
    const data = try processData(allocator, "input");
    defer allocator.free(data); // caller responsible for cleanup
}
```

### Tagged Unions (ADTs / Sum Types)

```zig
const PaymentState = union(enum) {
    pending: void,
    processing: struct { transaction_id: []const u8 },
    completed: Receipt,
    failed: PaymentError,
    
    // Methods on the union
    pub fn describe(self: PaymentState) []const u8 {
        return switch (self) {
            .pending => "Waiting for payment",
            .processing => |p| p.transaction_id,
            .completed => |r| r.summary,
            .failed => |e| e.message,
        };
    }
};

// Exhaustive switch (compiler enforces all cases)
fn handlePayment(state: PaymentState) void {
    switch (state) {
        .pending => startProcessing(),
        .processing => |p| pollStatus(p.transaction_id),
        .completed => |receipt| sendConfirmation(receipt),
        .failed => |err| notifyFailure(err),
    }
}
```

### Compile-Time Programming

```zig
// comptime function for generics
fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

// Compile-time computed constants
const LOOKUP_TABLE = blk: {
    var table: [256]u8 = undefined;
    for (&table, 0..) |*entry, i| {
        entry.* = @intCast((i * 7) % 256);
    }
    break :blk table;
};

// Generic container (like TypeScript generics)
fn ArrayList(comptime T: type) type {
    return struct {
        items: []T,
        allocator: std.mem.Allocator,
        
        const Self = @This();
        
        pub fn init(allocator: std.mem.Allocator) Self {
            return .{ .items = &[_]T{}, .allocator = allocator };
        }
        
        pub fn append(self: *Self, item: T) !void {
            // ...
        }
    };
}
```

### Resource Management with defer

```zig
fn processFile(allocator: std.mem.Allocator, path: []const u8) !void {
    // Open file
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close(); // ALWAYS runs on scope exit
    
    // Allocate buffer
    const buffer = try allocator.alloc(u8, 4096);
    defer allocator.free(buffer); // cleanup guaranteed
    
    // errdefer for conditional cleanup
    var result = try allocator.alloc(u8, 1024);
    errdefer allocator.free(result); // only on error
    
    // If we reach here successfully, caller owns result
    // ...
}
```

## Quick Reference

```zig
// Imports
const std = @import("std");

// Variables
const immutable: u32 = 42;        // prefer const
var mutable: u32 = 0;             // only when needed

// Optionals (?T) - like Option/Maybe
var maybe_value: ?u32 = null;
const unwrapped = maybe_value orelse 0;        // default value
const ptr = maybe_value orelse return error.Missing;  // early return

// Error unions (!T) - like Result/Either
fn canFail() !u32 { return error.SomeError; }
const value = try canFail();                   // propagate error
const safe = canFail() catch |err| handleError(err);  // catch error

// Slices (pointer + length, not null-terminated)
const slice: []const u8 = "hello";             // string literal is []const u8
const arr: [5]u8 = .{ 1, 2, 3, 4, 5 };
const sub = arr[1..3];                         // slice of array

// Iteration
for (slice, 0..) |byte, index| { }             // value and index
for (slice) |byte| { }                         // value only

// Switch (exhaustive, can capture)
switch (tagged_union) {
    .variant => |captured| doSomething(captured),
    else => {},  // or handle all cases
}

// Comptime
const SIZE = comptime blk: { break :blk 64; };
fn generic(comptime T: type, val: T) T { return val; }
```

## Detailed References

- **[references/idioms.md](references/idioms.md)** - Data-oriented design, memory patterns, testing
- **[references/async-io.md](references/async-io.md)** - New async/Io model, futures, cancellation
- **[references/c-interop.md](references/c-interop.md)** - C FFI, @cImport, ABI compatibility

## Forbidden Patterns

| ❌ Never | ✅ Instead |
|----------|-----------|
| Global allocator / hidden malloc | Pass `Allocator` explicitly |
| Exceptions / panic for errors | Return error union `!T` |
| Null pointers without type | Use optional `?*T` |
| Preprocessor macros | Use `comptime` and inline functions |
| C-style strings in Zig code | Use slices `[]const u8` |
| Ignoring errors silently | Handle with `catch` or propagate with `try` |
| `var` when `const` works | Default to `const`, mutate only when necessary |
| Hidden control flow | Make all branches explicit |
| OOP inheritance hierarchies | Use composition and tagged unions |
