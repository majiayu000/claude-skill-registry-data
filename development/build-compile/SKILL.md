---
name: build-compile
description: Build Rust code with proper error handling and optimization for development, testing, and production. Use when compiling the self-learning memory project or troubleshooting build errors.
---

# Build and Compile

Build Rust code with proper error handling and optimization.

## Purpose
Compile the self-learning memory project with appropriate settings for development, testing, and production.

## Build Commands

### Development Build
```bash
# Fast compile, debug symbols, no optimization
cargo build

# Build all workspace members
cargo build --all

# Build specific package
cargo build -p memory-core
```

**Characteristics**:
- Fast compilation (~10-30s)
- Debug symbols included
- No optimization (faster builds)
- Larger binaries
- Slower runtime

### Release Build
```bash
# Optimized build for production
cargo release build

# With all optimizations
cargo build --release --all

# Specific package
cargo build --release -p memory-storage-turso
```

**Characteristics**:
- Slower compilation (1-5 min)
- Full optimizations (LTO, codegen-units=1)
- Smaller, faster binaries
- No debug symbols (unless configured)

### Check (No Binary)
```bash
# Type check only, fastest feedback
cargo check

# Check all workspace members
cargo check --all

# With all features
cargo check --all-features
```

**Use for**:
- Quick feedback loop
- Editor integration
- CI pre-checks

## Build Profiles

### Cargo.toml Configuration
```toml
[profile.dev]
opt-level = 0           # No optimization
debug = true            # Include debug info
split-debuginfo = "unpacked"

[profile.release]
opt-level = 3           # Maximum optimization
lto = "fat"             # Full link-time optimization
codegen-units = 1       # Single codegen unit for best optimization
strip = true            # Remove debug symbols
panic = "abort"         # Smaller binary, faster panic

[profile.test]
opt-level = 2           # Some optimization for faster tests
debug = true            # Keep debug info for test debugging
```

## Handling Build Errors

### Common Error Types

#### 1. Type Errors
```
error[E0308]: mismatched types
  expected `Result<Episode, Error>`
  found `Episode`
```

**Fix**: Add proper error type wrapping
```rust
// BEFORE
fn get_episode() -> Result<Episode, Error> {
    episode
}

// AFTER
fn get_episode() -> Result<Episode, Error> {
    Ok(episode)
}
```

#### 2. Lifetime Errors
```
error[E0597]: `data` does not live long enough
```

**Fix**: Clone data or adjust lifetimes
```rust
// BEFORE
fn process(data: &str) -> &str {
    let processed = data.to_uppercase();
    &processed  // Error: processed dropped
}

// AFTER
fn process(data: &str) -> String {
    data.to_uppercase()  // Return owned String
}
```

#### 3. Trait Bound Errors
```
error[E0277]: the trait bound `X: Send` is not satisfied
```

**Fix**: Use Send-safe types
```rust
// BEFORE
Arc<RefCell<Data>>  // Not Send

// AFTER
Arc<Mutex<Data>>    // Send + Sync
```

#### 4. Async Errors
```
error: `await` is only allowed inside `async` functions
```

**Fix**: Make function async
```rust
// BEFORE
fn fetch_data() -> Result<Data> {
    let data = async_fetch().await?;  // Error
    Ok(data)
}

// AFTER
async fn fetch_data() -> Result<Data> {
    let data = async_fetch().await?;  // OK
    Ok(data)
}
```

### Build Error Workflow

1. **Read error message carefully**
   - Rust errors are detailed and helpful
   - Follow the suggestions

2. **Check error code**
   ```bash
   # Get detailed explanation
   rustc --explain E0308
   ```

3. **Fix incrementally**
   ```bash
   # Fix one error at a time
   cargo check
   # Fix
   cargo check
   # Repeat
   ```

4. **Verify fix**
   ```bash
   cargo build --all
   ```

## Incremental Compilation

### Speed Up Builds
```bash
# Enable in .cargo/config.toml
[build]
incremental = true

# Or via environment
export CARGO_INCREMENTAL=1
```

**Benefits**:
- Faster rebuilds (only changed code)
- Useful during active development

**Tradeoffs**:
- Larger target/ directory
- Occasional need to clean for fresh build

### Clean Builds
```bash
# Remove build artifacts
cargo clean

# Clean specific package
cargo clean -p memory-core

# Full clean rebuild
cargo clean && cargo build --all
```

**When to clean**:
- Weird build errors
- After major refactoring
- Before benchmarking
- Disk space issues

## Dependency Management

### Update Dependencies
```bash
# Check for updates
cargo update --dry-run

# Update dependencies
cargo update

# Update specific crate
cargo update tokio
```

### Add Dependencies
```bash
# Add to Cargo.toml
cargo add anyhow
cargo add tokio --features full

# Development dependency
cargo add --dev tempfile
```

### Feature Flags

```toml
[features]
default = ["turso", "redb"]
embedding = ["openai", "tiktoken"]
experimental = []
```

```bash
# Build with specific features
cargo build --features embedding

# Build with all features
cargo build --all-features

# Build with no default features
cargo build --no-default-features
```

## Build Caching

### Sccache (Distributed Cache)
```bash
# Install
cargo install sccache

# Configure
export RUSTC_WRAPPER=sccache

# Build (will cache)
cargo build
```

**Benefits**:
- Share cache across projects
- Faster CI builds
- Reduce redundant compilation

## Cross-Compilation

### For Different Targets
```bash
# List available targets
rustup target list

# Add target
rustup target add x86_64-unknown-linux-musl

# Build for target
cargo build --target x86_64-unknown-linux-musl
```

## Build Scripts

### build.rs
Create custom build logic:

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=migrations/");

    // Set environment variables
    println!("cargo:rustc-env=BUILD_TIME={}", now());

    // Link libraries
    println!("cargo:rustc-link-lib=sqlite3");
}
```

## Workspace Builds

### Build All Members
```bash
# Build entire workspace
cargo build --workspace

# Or
cargo build --all
```

### Build Specific Member
```bash
cargo build -p memory-core
cargo build -p memory-storage-turso
```

### Build Order
Cargo automatically determines dependency order.

## Optimization Tips

### 1. Parallel Compilation
```bash
# Use more CPU cores
cargo build -j 8
```

### 2. Link-Time Optimization (LTO)
```toml
[profile.release]
lto = "fat"  # Best optimization, slowest build
lto = "thin" # Good balance
```

### 3. Code Generation Units
```toml
[profile.release]
codegen-units = 1  # Best runtime, slowest build
codegen-units = 16 # Faster build, good runtime
```

## Build Monitoring

### Build Time
```bash
# Measure build time
time cargo build --all

# With timing info
cargo build --timings
# Open cargo-timing.html for visualization
```

### Build Size
```bash
# Check binary size
ls -lh target/release/binary_name

# Analyze binary
cargo bloat --release
```

## CI Integration

### GitHub Actions Example
```yaml
- name: Check
  run: cargo check --all

- name: Build
  run: cargo build --all --verbose

- name: Build Release
  run: cargo build --release --all
```

### Cache Dependencies
```yaml
- uses: actions/cache@v3
  with:
    path: |
      ~/.cargo/registry
      ~/.cargo/git
      target
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
```

## Troubleshooting

### Build Hangs
- Check for cyclic dependencies
- Kill zombie processes
- Clean and rebuild

### Out of Memory
- Reduce parallel jobs: `-j 2`
- Use incremental compilation
- Add swap space

### Linking Errors
- Check system libraries installed
- Verify `ld` version
- Use `lld` linker for speed:
  ```toml
  [target.x86_64-unknown-linux-gnu]
  linker = "clang"
  rustflags = ["-C", "link-arg=-fuse-ld=lld"]
  ```

## Best Practices

1. **Run `cargo check` often** (fastest feedback)
2. **Full `cargo build --all` before commits**
3. **Test release builds periodically**
4. **Keep dependencies updated**
5. **Use feature flags for optional code**
6. **Clean build when in doubt**
7. **Monitor build times** (should stay reasonable)
