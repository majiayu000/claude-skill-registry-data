---
name: cron-delete
description: "Delete a scheduled cron task by name or ID"
version: 1.0.0
author: custodian
license: MIT
platforms: [linux, darwin, windows]
metadata:
  hermes:
    tags: [Scheduling, Cron]
  custodian:
    band: L2
    cost_usd: 0.0
    configured: false
---

# Cron Delete

Delete a scheduled cron task by name or ID

## Authority band

This tool runs under **L2** authority in the Custodian kernel. Autonomous up to the per-action and session caps; escalates above threshold.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (see execute.py for full schema) | | | |

## Configuration

Set the required environment variables before use. Until configured, `custodian tools run cron-delete` returns a stub response indicating which variables are needed.

## Usage

```bash
custodian tools run cron-delete --param value
```

## Custodian governance

Every call to this tool passes through the Custodian kernel authority check
before executing. The kernel verifies the current authority band, checks
spending caps where applicable, logs the action to the OCSF audit trail,
and escalates to a human operator if the action exceeds the declared band.

Adding this tool to any Hermes agent session requires no code changes —
declare `custodian-band: L2` in the SKILL.md frontmatter and the kernel
wraps it automatically.
