---
name: build-variant-from-local-kits
description: Build a variant using locally published kits for development validation
---

# Skill: Build Variant from Local Kits

## Purpose

Build a complete Bottlerocket variant image using kits published to the local development registry. This enables end-to-end testing of kit changes before publishing to production registries.

## When to Use

- Testing kit changes in a complete variant build
- Creating bootable images for local testing
- End-to-end validation of kit modifications

## Prerequisites

- Kits already built and published to local registry (use `build-kit-locally` skill)
- Local registry running
- Bottlerocket variant repository

## Procedure

### 1. Configure for local registry

```bash
cd ./bottlerocket
brdev twoliter use-local-deps
```

This creates `Twoliter.override` pointing to the local registry for fetching kits.

### 2. Select which kits to fetch locally

Edit `Twoliter.toml` and set `vendor = "local"` for kits you want from the local registry:

```toml
[kit.bottlerocket-core-kit]
vendor = "local"  # Fetch from local registry
version = "2.0.0"

[kit.bottlerocket-kernel-6.1-kit]
# No vendor override - uses upstream
version = "2.0.0"
```

Only kits with `vendor = "local"` will be fetched from the local registry; others use upstream.

### 3. Update lock file

```bash
./tools/twoliter/twoliter update
```

### 4. Build the variant

```bash
cargo make
```

For specific variant:
```bash
cargo make -e BUILDSYS_VARIANT=aws-k8s-1.31
```

For specific architecture:
```bash
cargo make -e BUILDSYS_ARCH=aarch64
```

### 5. Locate the built image

```bash
ls -lh build/images/*.img
```

## Validation

The build should complete successfully and produce an `.img` file in `build/images/`.

## Cleanup

When done testing, restore upstream configuration:

```bash
brdev twoliter use-upstream-deps
```

This removes `Twoliter.override`.
Remember to also revert any `vendor = "local"` changes in `Twoliter.toml`.

## Common Issues

**Kit not found in registry:**
```
Error: failed to pull kit
```
Solution: Verify kit is published with `brdev registry list`

**Version mismatch:**
Solution: Ensure `Twoliter.toml` version matches the published kit version

**Lock file out of sync:**
Solution: Run `./tools/twoliter/twoliter update` again
