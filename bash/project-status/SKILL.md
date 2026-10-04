---
name: project-status
description: Checks the health of the project, including PM2 services, disk space, and configuration.
---

# Project Status Skill

Diagnose the current state of the application and server.

## Usage

Run the status check script:

```bash
node .agent/skills/project-status/scripts/status.js
```

## What it Checks

1.  **System Resources**: RAM and Disk usage.
2.  **PM2 Processes**: List of running bots/services, their status (online/stopped), CPU, and Memory usage.
3.  **Configuration**: Validity of the `.env` file and presence of critical variables.
