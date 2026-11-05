---
name: diagnose
description: Run safe diagnostic commands on the remote memory server. Use for checking logs, container status, disk usage, memory, and running read-only database queries.
---

# Server Diagnostics

The diagnostics script is at `tools/diagnose.sh`. It provides safe, read-only commands for inspecting the remote server `memory` at `/home/ec2-user/memory`.

There are two deployments:

* memory - my personal stuff
* chris - Equistamp stuff

The default is to use the `memory` version - to use the `chris` one, call with `DEPLOY_DIR=/home/ec2-user/chris`

## Commands

### Status (overview)
Get overall system health:
```bash
./tools/diagnose.sh status
```
Shows: container status, memory, disk, and recent errors.

### Logs
View docker logs:
```bash
./tools/diagnose.sh logs              # all services, last 100 lines
./tools/diagnose.sh logs api          # specific service
./tools/diagnose.sh logs api 500      # last 500 lines
./tools/diagnose.sh logs worker 200   # worker logs
```

### Container Status
```bash
./tools/diagnose.sh ps
```

### System Resources
```bash
./tools/diagnose.sh disk    # disk usage breakdown
./tools/diagnose.sh mem     # memory usage
./tools/diagnose.sh top     # top processes by memory
```

### File Operations
```bash
./tools/diagnose.sh ls <path>              # list directory
./tools/diagnose.sh cat <file>             # view file
./tools/diagnose.sh tail <file> [lines]    # tail file (default: 50)
./tools/diagnose.sh grep <pattern> <path>  # search files
```

### Database Queries
Run read-only SQL queries (SELECT only):
```bash
./tools/diagnose.sh db "SELECT count(*) FROM source_item"
./tools/diagnose.sh db "SELECT * FROM source_item ORDER BY created_at DESC LIMIT 5"
./tools/diagnose.sh db "SELECT status, count(*) FROM source_item GROUP BY status"
```
Non-SELECT queries are blocked for safety.

## Common Diagnostics

**Check why API is failing:**
```bash
./tools/diagnose.sh logs api 200
```

**Check worker processing:**
```bash
./tools/diagnose.sh logs worker 100
```

**Database stats:**
```bash
./tools/diagnose.sh db "SELECT count(*) FROM source_item"
./tools/diagnose.sh db "SELECT modality, count(*) FROM source_item GROUP BY modality"
```

**Find recent errors:**
```bash
./tools/diagnose.sh status   # includes error grep
./tools/diagnose.sh grep "ERROR" src/
```

**Check disk space:**
```bash
./tools/diagnose.sh disk
```
