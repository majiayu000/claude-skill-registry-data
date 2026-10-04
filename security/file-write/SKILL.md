---
name: file-write
description: "Write content to a file at an allowed path"
version: 1.0.0
author: custodian
license: MIT
platforms: [linux, darwin, windows]
metadata:
  hermes:
    tags: [Files, Local]
  custodian:
    band: L1
    cost_usd: 0.0
    configured: true
---

# File Write

Write content to a file at an allowed path

## Authority band

This tool runs under **L1** authority in the Custodian kernel. Trivial autonomous spend or free side-effect — no human approval required.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (see execute.py for full schema) | | | |

## Configuration

No additional configuration required — uses credentials already wired to Custodian.

## Usage

```bash
custodian tools run file-write --param value
```

## Custodian governance

Every call to this tool passes through the Custodian kernel authority check
before executing. The kernel verifies the current authority band, checks
spending caps where applicable, logs the action to the OCSF audit trail,
and escalates to a human operator if the action exceeds the declared band.

Adding this tool to any Hermes agent session requires no code changes —
declare `custodian-band: L1` in the SKILL.md frontmatter and the kernel
wraps it automatically.
