---
name: local-registry
description: Start and manage a local OCI registry for Bottlerocket kit development
---

# Skill: Local OCI Registry

## Purpose

Start and manage a local OCI registry for development. This allows building and publishing kits locally without requiring external registry access.

## When to Use

- Developing changes to kits that need to be consumed by variants
- Testing kit changes before publishing to production registries
- Working offline or in isolated environments

## Prerequisites

- Docker installed and running
- Working from within a grove directory

## Procedure

### Start the registry

```bash
brdev registry start
```

This will:
- Start a local Docker registry on `localhost:5000`
- Configure persistence (registry data survives restarts)
- Wait for the registry to be healthy before returning
- Output the registry URL for use in builds

### Verify registry is running

```bash
brdev registry status
```

Returns exit code 0 if running, non-zero otherwise.

### Get registry URL

```bash
brdev registry url
```

Outputs `localhost:{port}` for the current grove. Use this in scripts instead of hardcoding ports.

### View registry logs

```bash
brdev registry logs
```

To follow logs in real-time:
```bash
brdev registry logs --follow
```

### Stop the registry

```bash
brdev registry stop
```

Note: This preserves the registry data volume.

### Clean registry data

```bash
brdev registry clean
```

This removes both the container and the data volume.

## Configuration

brdev uses environment variables for configuration. Create a `.env` file in the forest root or set environment variables:

```bash
# Custom image (default: registry:2)
BRDEV_REGISTRY_IMAGE=registry:2.8
```

Note: Container and volume names are automatically derived from the grove name as `brdev-registry-{grove}` and `brdev-registry-data-{grove}`. The port is auto-derived from a hash of the grove name (range 5001-5999).

## Validation

After starting the registry:
```bash
brdev registry list
```

Should return: `{"repositories":[]}`

## Common Issues

**Docker not installed:**
```
Error: Docker is not installed or not in PATH. Install Docker and ensure it's in your PATH
```
Solution: Install Docker and ensure it's in your PATH.

**Docker daemon not running:**
```
Error: Docker daemon is not running. Start Docker with: sudo systemctl start docker
```
Solution: Start the Docker daemon.

**Port already in use:**
```
Error: Failed to start container. The port may already be in use
```
Solution: 
- Check for existing registry: `docker ps | grep registry`
- Stop conflicting container: `docker stop <container-id>`
- Or use a custom port via `FORESTER_REGISTRY_PORT`

**Permission denied:**
- Ensure user is in docker group: `groups | grep docker`
- Add user to docker group: `sudo usermod -aG docker $USER`
- May need to restart shell after adding to group

## Related Skills

- `build-kit-locally` - Uses local registry to publish built kits
- `build-variant-from-local-kits` - Configures variant builds to use local registry

## See Also

Configuration commands for local registry usage:

**For publishing kits:**
- `brdev twoliter use-local-publish` - Create `Infra.toml` for publishing to local registry
- `brdev twoliter use-upstream-publish` - Remove `Infra.toml`

**For fetching kits:**
- `brdev twoliter use-local-deps` - Create `Twoliter.override` for fetching from local registry
- `brdev twoliter use-upstream-deps` - Remove `Twoliter.override`

**Both (convenience):**
- `brdev twoliter use-local` - Create both files
- `brdev twoliter use-upstream` - Remove both files

When fetching, also set `vendor = "local"` in `Twoliter.toml` for specific kits you want from the local registry.

