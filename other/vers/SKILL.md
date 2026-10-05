---
name: vers
description: Manage VERS VMs - list, create, branch, pause, resume, delete VMs and clusters. Use when working with vers commands, VM management, or when disk space issues occur.
---

# VERS VM Management

## Overview

VERS is a VM platform that supports branching, snapshots, and clusters. VMs can be managed via the `vers` CLI or the REST API at `http://13.219.19.157/api/`.

## CLI Commands

```bash
# List/view VMs
vers tree <cluster-alias>       # Show VM tree for a cluster

# VM lifecycle
vers run <rootfs> -n <cluster> -N <vm-alias>  # Create new cluster with VM
vers branch <vm-id>             # Branch a VM (creates child)
vers pause <vm-id>              # Pause a running VM
vers resume <vm-id>             # Resume a paused VM
vers kill <vm-id>               # Delete a VM
vers kill <cluster-id>          # Delete entire cluster

# Interaction
vers connect <vm-id>            # SSH into VM
vers execute <vm-id> "command"  # Run command on VM
vers copy <vm-id> <local> <remote>  # Copy files to VM
vers copy -r <vm-id> <local-dir> <remote-dir>  # Copy directory recursively

# State management
vers commit <vm-id>             # Commit VM state
vers checkout <vm-id>           # Switch to a different VM
```

## REST API

Base URL: `http://13.219.19.157/api/`

Authorization header: `Authorization: Bearer <API_KEY>`

### Endpoints

```bash
# List all VMs
curl -s -H "Authorization: Bearer $API_KEY" "http://13.219.19.157/api/vm"

# Get specific VM
curl -s -H "Authorization: Bearer $API_KEY" "http://13.219.19.157/api/vm/<vm-id>"

# Update VM state (pause/resume)
curl -X PATCH -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "Running"}' \
  "http://13.219.19.157/api/vm/<vm-id>"

# Branch a VM
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  "http://13.219.19.157/api/vm/<vm-id>/branch"

# Delete a VM
curl -X DELETE -H "Authorization: Bearer $API_KEY" \
  "http://13.219.19.157/api/vm/<vm-id>"

# List clusters
curl -s -H "Authorization: Bearer $API_KEY" "http://13.219.19.157/api/cluster"
```

## Common Issues

### Thin Pool Out of Space

Error: `Thin pool ... is out of data space`

This means the VERS storage is full. To free space:

1. List all VMs and identify unnecessary ones:
```bash
curl -s -H "Authorization: Bearer $API_KEY" "http://13.219.19.157/api/vm" | jq '.data[] | {id, alias, state, children}'
```

2. Delete unused VMs (children first, then parents):
```bash
vers kill <vm-id>
# Or via API:
curl -X DELETE -H "Authorization: Bearer $API_KEY" "http://13.219.19.157/api/vm/<vm-id>"
```

3. Delete entire clusters if not needed:
```bash
vers kill <cluster-id>
```

### VM States

- `Running` - VM is active
- `Paused` - VM is suspended (can be resumed)
- VMs get paused during branch operations

### SSH Keys

SSH keys are stored in `.vers/keys/<vm-id>.key` after first connection.

## Environment Variables

- `VERS_API_KEY` - API key for authentication (required for API calls from within VMs)

## Project-Specific Notes

This project (rhizome) develops the vers-client and vers-dsl Haskell libraries:
- `vers-client/` - Servant API types and client
- `vers-dsl/` - Polysemy effect for VERS operations
- Test VM: `15ad103d-7ed6-4dfd-80ff-87c5588a5001`
