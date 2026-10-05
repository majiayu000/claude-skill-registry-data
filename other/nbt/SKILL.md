---
name: nbt
description: Use the nbt! macro from mc_protocol for creating NBT (Named Binary Tag) data for Minecraft protocol encoding.
---

# NBT Encoding Skill

Use the `nbt!` macro from `mc_protocol` for creating NBT data.

## When to Use

Use this skill when you need to:
- Encode NBT data for Minecraft packets
- Create text components for chat, action bar, titles
- Build compound NBT structures

## Basic Usage

```rust
use mc_protocol::nbt;

// Simple compound
let compound = nbt! {
    "text" => "Hello",
    "count" => 42i32,
    "flag" => true,
};

// Convert to network bytes
let bytes = compound.to_network_bytes();
```

## Nested Compounds

```rust
use mc_protocol::nbt;

let nested = nbt! {
    "outer" => nbt! {
        "inner" => 123i32,
    },
};
```

## Supported Types

- `i8` - Byte
- `i16` - Short
- `i32` - Int
- `i64` - Long
- `f32` - Float
- `f64` - Double
- `&str` / `String` - String
- `bool` - Byte (0 or 1)
- `NbtCompound` - Nested compound
- `NbtList` - List of same-type elements

## Text Components (Chat/Action Bar)

For Minecraft text components (used in chat, action bar, titles):

```rust
use mc_protocol::nbt;

// Simple text
let text_component = nbt! {
    "text" => "Hello World",
};

// With color
let colored = nbt! {
    "text" => "Red text",
    "color" => "red",
};
```

## Best Practices

1. **Always use the `nbt!` macro** instead of manual byte manipulation
2. Use explicit type suffixes (`42i32`, `1.0f32`) for numeric literals
3. Use `to_network_bytes()` for protocol encoding (adds type tag, no root name)
