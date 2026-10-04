---
name: shell-exec
description: "Run a sandboxed shell command with timeout and allowlist"
version: 1.0.0
author: custodian
license: MIT
platforms: [linux, darwin, windows]
metadata:
  hermes:
    tags: [Shell, Local]
  custodian:
    band: L2
    cost_usd: 0.0
    configured: true
---

# Shell Exec

Run a sandboxed shell command with timeout and allowlist

## Authority band

This tool runs under **L2** authority in the Custodian kernel. Autonomous up to the per-action and session caps; escalates above threshold.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (see execute.py for full schema) | | | |

## Configuration

No additional configuration required — uses credentials already wired to Custodian.

## Usage

```bash
custodian tools run shell-exec --param value
```

## Custodian governance

Every call to this tool passes through the Custodian kernel authority check
before executing. The kernel verifies the current authority band, checks
spending caps where applicable, logs the action to the OCSF audit trail,
and escalates to a human operator if the action exceeds the declared band.

Adding this tool to any Hermes agent session requires no code changes —
declare `custodian-band: L2` in the SKILL.md frontmatter and the kernel
wraps it automatically.
