---
name: build-kit-locally
description: Build a kit and publish it to a locally hosted registry for development testing
---

# Skill: Build and Publish Kit

## Purpose

Build a Bottlerocket kit (core-kit or kernel-kit) and publish it to a local OCI registry for development testing and validation. This allows you to test kit changes in variant builds without publishing to production registries.

## When to Use

- Making changes to kit packages and testing them in variants
- Iterative development on kits
- Before building a variant image that depends on kit changes

## Prerequisites

- Docker installed and running
- Working from within a grove directory
- Kit repository cloned in `kits/` directory

## Procedure

### 1. Ensure local registry is running

```bash
brdev registry start
```

### 2. Configure for local registry

```bash
cd kits/<kit-name>
brdev twoliter use-local-publish
```

This creates `Infra.toml` pointing to the local registry for publishing.

### 3. Build the kit

```bash
make build
```

For specific architecture:
```bash
make build ARCH=x86_64
# or
make build ARCH=aarch64
```

### 4. Publish to local registry

```bash
make publish VENDOR=local
```

This publishes the kit to `localhost:5000` with the vendor prefix "local".

### 5. Verify publication

```bash
brdev registry list
```

Should show your kit in the repositories list.

## Validation

Check the kit is available:
```bash
brdev registry list
```

Should return the published version tags.

## Common Issues

**Registry not running:**
```
Error: connection refused
```
Solution: Run `brdev registry start`

**Infra.toml not configured:**
```
Error: vendor 'local' not found
```
Solution: Run `brdev twoliter use-local-publish` to create the configuration

**Docker permission denied:**
Solution: Ensure user is in docker group and Docker daemon is running

## Next Steps

After publishing a kit:
1. Update variant's `Twoliter.toml` to reference the new kit version
2. Run `make update` in the variant repo
3. Build the variant with `cargo make`
