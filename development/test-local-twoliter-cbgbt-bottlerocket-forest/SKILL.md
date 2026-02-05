---
name: test-local-twoliter
description: Build and test local changes to twoliter before releasing
---

# Skill: Test Local Twoliter Changes

## Purpose

Build twoliter from local source and configure kits to use the locally-built binary for testing changes before release.

## When to Use

- Making changes to twoliter source code
- Testing twoliter modifications before creating a PR
- Debugging twoliter behavior
- Validating fixes to twoliter

## Prerequisites

- Twoliter repository cloned in the forest
- Rust toolchain installed
- At least one kit repository to test with

## Procedure

### 1. Make changes to twoliter source

Edit files in `twoliter/twoliter/src/` or `twoliter/twoliter/embedded/`.

### 2. Build twoliter

```bash
cd twoliter
cargo build --release
```

The binary will be at `target/release/twoliter`.

### 3. Test the changes

Override `TWOLITER_DIR` to point to your local build directory:

```bash
cd kits/bottlerocket-core-kit
make build TWOLITER_DIR=$FOREST_ROOT/twoliter/target/release
```

### 4. Iterate

After making more changes:
```bash
# Rebuild twoliter
cd $FOREST_ROOT/twoliter
cargo build --release

# Test again
cd kits/bottlerocket-core-kit
make build TWOLITER_DIR=$FOREST_ROOT/twoliter/target/release
```

## Validation

Verify the local twoliter is being used by checking the path:

```bash
cd kits/bottlerocket-core-kit
make build TWOLITER_DIR=$FOREST_ROOT/twoliter/target/release 2>&1 | head -5
```

You should see your modified twoliter being invoked.

## Common Issues

**Changes not taking effect:**
- Ensure you ran `cargo build --release` after making changes
- Verify the path in `TWOLITER_DIR` is correct
- Check that the binary exists: `ls -lh $FOREST_ROOT/twoliter/target/release/twoliter`

**Build errors in twoliter:**
- Run `cargo check` to see detailed error messages
- Run `cargo clippy` to catch common issues
- Run `cargo test` to verify tests pass

**Kit build fails with local twoliter:**
- Check twoliter output for error messages
- Add `--log-level debug` by modifying the Makefile temporarily or using the twoliter binary directly

## Reverting to Released Version

To go back to using the released version, simply omit the `TWOLITER_DIR` override:

```bash
cd kits/bottlerocket-core-kit
make build
```

This uses the default `tools/twoliter/twoliter` from the released version.

## Related Skills

- **update-twoliter** - For updating to a new released version after testing

## Notes

- No file modifications needed - use `TWOLITER_DIR` override on command line
- This is for local testing only
- For variant builds, you may need to update `bottlerocket/Makefile.toml` similarly
- The `prep` target will still download the official version to `tools/twoliter/`, but your override takes precedence
