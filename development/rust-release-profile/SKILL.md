---
name: rust-release-profile
description: Configure release builds for maximum performance with LTO, optimizations, and binary stripping. Use for production deployments.
---

# Release Profile

Optimize Rust builds for production performance and binary size.

## Production Cargo.toml Profile

```toml
[profile.release]
opt-level = 3           # Maximum optimization
lto = true              # Link-time optimization (slower build, faster binary)
codegen-units = 1       # Single codegen unit (better optimization)
strip = true            # Strip debug symbols
panic = 'abort'         # Smaller binary, no unwinding

[profile.release-with-debug]
inherits = "release"
debug = true            # Keep debug info for profiling
strip = false
```

## Optimization Levels

```toml
# opt-level options:
# 0 - No optimization (fastest compile)
# 1 - Basic optimization
# 2 - Default release optimization
# 3 - Maximum optimization (default for release)
# "s" - Optimize for size
# "z" - Optimize for size, disable loop vectorization

opt-level = 3   # Best performance
opt-level = "s" # Smallest binary with good performance
opt-level = "z" # Smallest binary
```

## Link-Time Optimization (LTO)

```toml
# LTO options:
# false - No LTO (fastest build)
# true/"fat" - Full LTO (slowest build, best performance)
# "thin" - Incremental LTO (good balance)

lto = true       # Best performance, slow build
lto = "thin"     # Good performance, faster build
lto = false      # Fastest build, no cross-crate optimization
```

## Codegen Units

```toml
# Fewer units = better optimization, slower parallel compilation
codegen-units = 1    # Best optimization
codegen-units = 16   # Default, faster parallel builds
```

## Debug Symbols

```toml
# For release builds
strip = true          # Remove all symbols
strip = "symbols"     # Remove symbols, keep sections
strip = "debuginfo"   # Remove debug info only
strip = "none"        # Keep everything

# Keep debug info for profiling
[profile.release-perf]
inherits = "release"
debug = true
strip = false
```

## Panic Behavior

```toml
# 'unwind' - Default, allows catch_unwind, larger binary
# 'abort' - Smaller binary, faster, no unwinding

panic = 'abort'  # Production: smaller, faster
panic = 'unwind' # Development: catch panics, better debugging
```

## Target-Specific Optimization

```toml
# Enable CPU-specific features
[build]
rustflags = ["-C", "target-cpu=native"]

# Or in .cargo/config.toml
[target.x86_64-unknown-linux-gnu]
rustflags = ["-C", "target-cpu=native"]
```

## Profile for Different Use Cases

```toml
# Fast iteration during development
[profile.dev]
opt-level = 0
debug = true

# Quick release for testing
[profile.release-quick]
inherits = "release"
lto = false
codegen-units = 16

# Maximum performance
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
panic = 'abort'

# Profiling build
[profile.release-perf]
inherits = "release"
debug = true
strip = false

# Smallest binary
[profile.release-small]
inherits = "release"
opt-level = "z"
lto = true
codegen-units = 1
strip = true
panic = 'abort'
```

## Workspace Settings

```toml
# In workspace Cargo.toml
[profile.release]
opt-level = 3
lto = true

# Override for specific packages
[profile.release.package.expensive-crate]
opt-level = 2  # Faster build for this crate
```

## Build Commands

```bash
# Standard release build
cargo build --release

# With specific profile
cargo build --profile release-perf

# Check binary size
ls -la target/release/my-binary

# Strip binary manually (if not using strip = true)
strip target/release/my-binary

# Check for debug info
file target/release/my-binary
```

## Measuring Impact

```bash
# Build time comparison
time cargo build --release
time cargo build --release --config 'profile.release.lto=false'

# Binary size comparison
cargo build --release
ls -la target/release/my-binary

cargo build --profile release-small
ls -la target/release-small/my-binary

# Performance comparison
hyperfine './target/release/my-binary' './target/release-quick/my-binary'
```

## Guidelines

- Use `lto = true` and `codegen-units = 1` for production
- Use `strip = true` and `panic = 'abort'` for smallest binaries
- Use `--profile release-perf` with debug symbols for profiling
- Use `lto = "thin"` for faster builds with good optimization
- Test different `opt-level` values for your workload
- Use `target-cpu=native` for deployment on known hardware

## Examples

See `hercules-local-algo/Cargo.toml` for production profile.
