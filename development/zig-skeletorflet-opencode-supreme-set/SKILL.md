---
name: zig
description: Zig systems programming skill covering comptime, allocators, cross-compilation, build system, and error unions. Use when building Zig applications.
trigger: zig, ziglang, zig build, zig cross-compilation, comptime, zig allocators, zig vs c
---

## zig

### Core Concepts
- Comptime: compile-time code execution, comptime parameters/values, inline for loops, compile-time reflection
- Allocators: explicit memory management — ArenaAllocator (batch free), page_allocator (OS pages), heap page allocator (general purpose), FixedBufferAllocator (fixed buffer)
- Error Union Types: !T syntax combining error set with value type, try/catch, error return traces
- Testing: test blocks inline with code, test runner, expect/expectEqual, memory leak detection

### Build System
- build.zig: declarative build configuration, Build object with addExecutable/addLibrary, step dependencies
- Cross-compilation: target triple (arch-os-abi), built-in libc detection, no need for cross toolchains
- Zig vs C: no hidden control flow, no implicit allocations, first-class cross-compilation, @cImport for C interop

### Common Patterns
- var vs const: explicit mutability, const pointer vs mutable pointer distinct
- Optionals: T? with orelse for defaults, unwrap by capture (?)
- Slices: []const T for read-only views, len + ptr primitive, slice syntax
- Standard library: std.fs (file system), std.net (networking), std.json (JSON parsing), std.ArrayList (growable arrays)
