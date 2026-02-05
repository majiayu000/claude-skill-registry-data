---
name: odin-dev
description: |
  Odin programming language development workflow. Use when:
  - Writing or modifying Odin code (.odin files)
  - Building Odin projects
  - Debugging Odin applications
  - Need Odin-specific idioms and patterns
---

# Odin Development

## Build Commands

```bash
# Build for debug
odin build src -out:build/app -debug

# Build optimized release
odin build src -out:build/app -o:speed

# Run tests
odin test src -out:build/test

# Check without building
odin check src

# Build and run
odin run src
```

## Project Structure

```
project/
├── src/
│   ├── main.odin       # Entry point (package main)
│   └── module/         # Sub-packages
│       └── mod.odin
├── vendor/             # Third-party dependencies
├── build/              # Build output (gitignored)
├── Makefile            # Build automation
└── ols.json            # Language server config
```

## Odin Idioms

### Error Handling

```odin
// Return tuple with success bool
load_file :: proc(path: string) -> ([]u8, bool) {
    data, ok := os.read_entire_file(path)
    return data, ok
}

// Use Maybe for explicit optionality
find_item :: proc(list: []Item, id: int) -> Maybe(Item) {
    for item in list {
        if item.id == id do return item
    }
    return nil
}
```

### Bit Fields (for hardware registers)

```odin
// Perfect for GBA hardware registers
Status_Register :: bit_field u16 {
    mode:      u8  | 3,   // bits 0-2
    enabled:   bool | 1,  // bit 3
    priority:  u8  | 2,   // bits 4-5
    _reserved: u8  | 10,  // bits 6-15
}
```

### Dispatch Tables

```odin
Handler :: #type proc(ctx: ^Context, data: u32)

@(private="file")
handlers: [256]Handler

@(init)
init_handlers :: proc() {
    for i in 0..<256 {
        handlers[i] = decode_handler(u8(i))
    }
}
```

### Force Inline for Hot Paths

```odin
get_flag :: #force_inline proc(cpu: ^CPU) -> bool {
    return (cpu.status & FLAG_MASK) != 0
}
```

### Defer for Cleanup

```odin
process_file :: proc(path: string) -> bool {
    handle, ok := os.open(path)
    if !ok do return false
    defer os.close(handle)

    // handle automatically closed on return
    return process_contents(handle)
}
```

## Common Patterns

### Slices vs Pointers

```odin
// Slices for collections
process_data :: proc(data: []u8) { ... }

// Pointers for single mutable values
modify_state :: proc(state: ^State) { ... }

// Raw pointers for memory-mapped I/O
read_mmio :: proc(addr: rawptr) -> u32 {
    return (cast(^u32)addr)^
}
```

### Switch Completeness

```odin
// #partial switch for subset handling
#partial switch mode {
case .Mode0, .Mode1:
    handle_tiled()
case .Mode3:
    handle_bitmap()
}

// Regular switch must be exhaustive
switch button {
case .A: ...
case .B: ...
// Must handle all cases
}
```

### Context System

```odin
// Custom allocator via context
my_allocator := create_arena_allocator()
context.allocator = my_allocator

// All allocations in this scope use arena
data := make([]u8, 1024)  // Uses arena
```

## SDL2 Integration

```odin
import "vendor:sdl2"

init_display :: proc() -> bool {
    if sdl2.Init({.VIDEO, .AUDIO}) != 0 {
        return false
    }

    window := sdl2.CreateWindow(
        "GBA Emulator",
        sdl2.WINDOWPOS_CENTERED,
        sdl2.WINDOWPOS_CENTERED,
        480, 320,  // 2x native GBA
        {.SHOWN, .RESIZABLE}
    )

    renderer := sdl2.CreateRenderer(window, -1, {.ACCELERATED})

    // BGR555 matches GBA native format
    texture := sdl2.CreateTexture(
        renderer,
        .BGR555,
        .STREAMING,
        240, 160
    )

    return true
}
```

## Debugging

```bash
# Build with debug info
odin build src -debug -out:build/app

# Use gdb/lldb
gdb build/app
lldb build/app

# Print debug info
import "core:fmt"
fmt.printf("value: %v\n", value)
```

## Language Server (OLS) and Formatting

### Check OLS Installation

```bash
# Verify OLS and odinfmt are installed
which ols odinfmt

# If not installed, use the odin-install skill
```

### Using odinfmt

```bash
# Format a single file (to stdout)
odinfmt src/main.odin

# Format and overwrite in place
odinfmt -w src/main.odin

# Format from stdin
echo 'package main; x:=1' | odinfmt -stdin
```

### Project Configuration (ols.json)

Every Odin project should have an `ols.json` at the root:

```json
{
    "$schema": "https://raw.githubusercontent.com/DanielGavin/ols/master/misc/ols.schema.json",
    "collections": [
        { "name": "core", "path": "/opt/odin-linux-amd64-nightly+2025-12-04/core" },
        { "name": "vendor", "path": "/opt/odin-linux-amd64-nightly+2025-12-04/vendor" }
    ],
    "enable_semantic_tokens": true,
    "enable_hover": true,
    "enable_format": true,
    "enable_references": true,
    "odin_command": "/usr/local/bin/odin"
}
```

### Claude Code LSP Integration

For Claude Code to use OLS, projects need:

1. **`.lsp.json`** at project root:
```json
{
  "odin": {
    "command": "ols",
    "extensionToLanguage": { ".odin": "odin" }
  }
}
```

2. **`.claude/settings.json`** to enable LSP tools:
```json
{
  "env": { "ENABLE_LSP_TOOLS": "1" }
}
```

This enables goToDefinition, findReferences, and documentSymbol operations.

## Testing

```odin
// In test file or same package
@(test)
test_add :: proc(t: ^testing.T) {
    result := add(2, 3)
    testing.expect_value(t, result, 5)
}

// Run with: odin test src
```

## Common Gotchas

1. **No comptime** - Use `@(init)` for table initialization
2. **No generics** - Use `$T` for polymorphic procs
3. **Slices are fat pointers** - Contains ptr + len, not just ptr
4. **Default allocator is context-based** - Can be changed per scope
5. **Bit fields are packed** - Good for hardware, watch alignment
