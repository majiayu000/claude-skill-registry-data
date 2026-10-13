---
name: automation
description: Scripts, cron jobs, background tasks, and automation setups.
---

# Automation

Scripts, cron jobs, background tasks, and automation setups.

## Core Guidelines

- **Idempotency**: Ensure automation scripts can run multiple times safely without corrupting data.
- **Dry-run Support**: Provide dry-run options to preview script actions.
- **Logging**: Emit timestamped logs to ease tracing.
