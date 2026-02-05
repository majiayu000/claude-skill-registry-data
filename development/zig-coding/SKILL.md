---
name: zig-coding
description: Enforces Zig coding conventions from the Zig Zero to Hero guide. Use when writing, reviewing, or refactoring Zig code. Applies naming conventions, error handling patterns, resource management, and module organization best practices.
---

# Zig Coding Conventions

This skill ensures all Zig code follows the conventions from [Zig: Zero to Hero](https://github.com/jkingston/zig_guide) guide.

## When to Use

- Writing new Zig code
- Reviewing Zig code changes
- Refactoring existing Zig code
- Designing new modules or types

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Types (struct, enum, union) | PascalCase | `const NodeConfig = struct { ... }` |
| Functions returning values | camelCase | `fn parseConfig(path: []const u8) !Config` |
| Functions returning types | PascalCase | `fn ArrayList(comptime T: type) type` |
| Variables, parameters, constants | snake_case | `const max_retry_count = 5` |
| File names | snake_case | `compose_parser.zig` |
| Units in identifiers | Suffix with unit | `timeout_ms`, `buffer_size_bytes` |
| Acronyms | Fully capitalized | `CRDTState`, `SWIMProtocol` |

## Error Handling Patterns

### Use Error Unions (`!T`) for Failures
```zig
fn loadConfig(path: []const u8) !Config {
    const file = try std.fs.openFileAbsolute(path, .{});
    defer file.close();
    // ...
}
```

### Use Optionals (`?T`) for Valid Absence
```zig
fn findService(name: []const u8) ?*Service {
    return services.get(name);  // null is valid - service doesn't exist
}
```

### Error Propagation
```zig
// Propagate with try
const config = try loadConfig(path);

// Provide fallback with catch
const port = parsePort(input) catch 7946;

// Handle optionals with orelse
const service = findService(name) orelse return error.ServiceNotFound;
```

## Resource Management

### Immediate Defer Pattern
```zig
fn processFile(path: []const u8) !void {
    const file = try std.fs.openFileAbsolute(path, .{});
    defer file.close();  // Immediately after acquisition

    const buffer = try allocator.alloc(u8, 4096);
    defer allocator.free(buffer);

    // Work with file and buffer...
}
```

### Partial Failure Rollback with errdefer
```zig
fn initializeNode(allocator: Allocator) !*Node {
    const node = try allocator.create(Node);
    errdefer allocator.destroy(node);  // Cleanup if subsequent operations fail

    node.config = try loadConfig();
    errdefer node.config.deinit();

    node.network = try initNetwork();
    return node;
}
```

### Nested Blocks in Loops
```zig
// WRONG: defers accumulate
for (items) |item| {
    const resource = try acquire(item);
    defer release(resource);  // All defers run at function end!
}

// CORRECT: nested block scopes the defer
for (items) |item| {
    {
        const resource = try acquire(item);
        defer release(resource);  // Runs at block end
        process(resource);
    }
}
```

## Module Organization

### Visibility Control
```zig
// Public API - exported
pub fn startNode(config: Config) !*Node { ... }

// Internal implementation - not exported
fn validateConfig(config: Config) !void { ... }
```

### Explicit Re-exports
```zig
// In orchestrator/orchestrator.zig
pub const Scheduler = @import("scheduler.zig").Scheduler;
pub const HealthMonitor = @import("health.zig").HealthMonitor;
pub const StateManager = @import("state.zig").StateManager;
```

### Interface Pattern (for Fizz simulation testing)
```zig
pub const Time = struct {
    nowFn: *const fn () i64,

    pub fn now(self: Time) i64 {
        return self.nowFn();
    }
};

// Production implementation
pub fn realTime() Time {
    return .{ .nowFn = struct {
        fn now() i64 {
            return std.time.timestamp();
        }
    }.now };
}
```

## Anti-Patterns to Avoid

1. **Optionals for errors** - Use `!T` when absence indicates failure
2. **Defer in loops** - Use nested blocks to scope cleanup
3. **Unmarked comptime** - Always mark type parameters with `comptime`
4. **Direct syscalls in core logic** - Use injected interfaces for testability

## Fizz-Specific Conventions

### Allocator Naming
- `gpa` - General Purpose Allocator (explicit deinit required)
- `arena` - Arena Allocator (bulk-free at end)
- `page_allocator` - Direct page allocation

### Interface Injection
All core logic must accept interfaces rather than using system calls directly:
```zig
pub const Orchestrator = struct {
    time: Time,
    network: Network,
    runtime: Runtime,

    pub fn init(time: Time, network: Network, runtime: Runtime) Orchestrator {
        return .{ .time = time, .network = network, .runtime = runtime };
    }
};
```

## Review Checklist

- [ ] Naming follows conventions (PascalCase types, camelCase functions, snake_case variables)
- [ ] Error unions used for failures, optionals for valid absence
- [ ] Resources have immediate defer cleanup
- [ ] errdefer used for partial failure rollback
- [ ] No defer inside loops without nested blocks
- [ ] Core logic uses injected interfaces (no direct syscalls)
- [ ] Public API marked with `pub`
- [ ] File names use snake_case
