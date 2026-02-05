---
name: rust-wasm-optimization
description: Optimize Rust code for WebAssembly compilation and runtime performance. Use when building WASM applications, optimizing binary size, or improving WASM runtime performance.
---

# Rust WASM Optimization

## Overview

This skill covers optimization techniques for Rust code compiled to WebAssembly, including binary size reduction, runtime performance improvements, and build configuration.

## Build Configuration

### Cargo.toml Profiles

```toml
[profile.release]
opt-level = "z"        # Optimize for size
lto = "thin"           # Thin LTO for faster builds
codegen-units = 1      # Single codegen unit for better optimization
panic = "abort"        # Smaller binary (no unwinding)

[profile.wasm-release]
inherits = "release"
strip = false          # WASM doesn't support strip the same way

[profile.wasm-dev]
inherits = "dev"
opt-level = 1          # Light optimization for dev
incremental = true
codegen-units = 16     # Faster compilation
```

### Linker Optimization

```toml
# .cargo/config.toml
[target.wasm32-unknown-unknown]
# wasm-ld is already optimized for WASM
```

## Binary Size Optimization

### Minimize Dependencies

```toml
# Only include needed features
[dependencies]
dioxus = { version = "0.6", features = ["web"] }  # Not ["web", "router", "ssr"]
serde = { version = "1.0", features = ["derive"] }  # Minimal features
```

### Avoid Large Types

```rust
// ❌ Don't store large binary data
struct Reminder {
    image_data: Vec<u8>,  // Large allocation
}

// ✅ Store URL instead
struct Reminder {
    image_url: String,  // Small string
}
```

### Use Compact Types

```rust
// Use small types when possible
struct Reminder {
    id: String,        // Required
    title: String,     // Required
    completed: bool,   // 1 byte
    // Avoid large types unless needed
}
```

## Runtime Performance

### Avoid Unnecessary Allocations

```rust
// ❌ Unnecessary clone
for reminder in reminders.clone() {
    process(reminder);
}

// ✅ Use reference
for reminder in reminders.iter() {
    process(reminder);
}
```

### Minimize Serialization Overhead

```rust
// Use compact JSON field names
#[derive(Serialize, Deserialize)]
struct Reminder {
    #[serde(rename = "id")]
    id: String,
    #[serde(rename = "t")]
    title: String,  // Shorter name = smaller JSON
}
```

### Efficient String Handling

```rust
// ✅ Use &str when possible
fn format_title(title: &str) -> String {
    format!("Title: {}", title)
}

// ✅ Pre-allocate capacity
let mut buffer = String::with_capacity(100);
buffer.push_str("prefix");
```

## Memory Management

### Let Rust Manage Memory

```rust
// Rust automatically manages memory
let reminders = load_reminders();  // Dropped when out of scope
```

### Avoid Smart Pointers Unless Needed

```rust
// ❌ Usually not needed in Dioxus
use std::rc::Rc;
let shared = Rc::new(data);

// ✅ Dioxus handles sharing via signals
let mut data = use_signal(|| value);
```

## Build Optimization

### Parallel Compilation

```bash
# Use all CPU cores
export CARGO_BUILD_JOBS=$(nproc)
dx build --release
```

### Incremental Compilation

```toml
[profile.dev]
incremental = true  # Faster rebuilds
```

### Codegen Units

```toml
[profile.wasm-dev]
codegen-units = 16  # More units = faster compilation, slightly larger binary

[profile.release]
codegen-units = 1   # Single unit = better optimization, smaller binary
```

## WASM-Specific Considerations

### Panic Strategy

```toml
[profile.release]
panic = "abort"  # Smaller binary, no unwinding code
```

### LTO Configuration

```toml
[profile.release]
lto = "thin"  # Faster builds than "fat", still good optimization
```

### Strip Configuration

```toml
[profile.wasm-release]
strip = false  # WASM doesn't support strip the same way as native binaries
```

## Performance Profiling

### Measure Binary Size

```bash
# Check WASM file size
ls -lh target/wasm32-unknown-unknown/release/*.wasm

# Use wasm-opt for further optimization
wasm-opt -Oz target/.../app.wasm -o app.optimized.wasm
```

### Runtime Profiling

```rust
// Use web_sys::console for timing
use web_sys::console;

let start = js_sys::Date::now();
// ... operation ...
let duration = js_sys::Date::now() - start;
console::log_1(&format!("Operation took: {}ms", duration).into());
```

## Best Practices

### DO:
- ✅ Use `opt-level = "z"` for size optimization
- ✅ Use `lto = "thin"` for balance of size and build time
- ✅ Minimize dependencies and features
- ✅ Use references instead of clones
- ✅ Pre-allocate collections when size is known
- ✅ Use compact JSON field names

### DON'T:
- ❌ Don't include unused features in dependencies
- ❌ Don't store large binary data in structs
- ❌ Don't clone unnecessarily
- ❌ Don't use `strip = true` for WASM (not supported)
- ❌ Don't use `lto = true` (use "thin" instead)

## Resources

- [Rust WASM Book](https://rustwasm.github.io/docs/book/)
- [wasm-pack Documentation](https://rustwasm.github.io/wasm-pack/)
- [Dioxus Performance Guide](https://dioxuslabs.com/learn/0.6/performance/)

