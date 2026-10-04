---
name: nim-model-list
description: "List available NVIDIA NIM models and their status"
version: 1.0.0
author: custodian
license: MIT
platforms: [linux, darwin, windows]
metadata:
  hermes:
    tags: [NVIDIA, NIM, AI]
  custodian:
    band: L0
    cost_usd: 0.0
    configured: true
---

# Nim Model List

List available NVIDIA NIM models and their status

## Authority band

This tool runs under **L0** authority in the Custodian kernel. Read-only; no real-world effects — always autonomous.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (see execute.py for full schema) | | | |

## Configuration

No additional configuration required — uses credentials already wired to Custodian.

## Usage

```bash
custodian tools run nim-model-list --param value
```

## Custodian governance

Every call to this tool passes through the Custodian kernel authority check
before executing. The kernel verifies the current authority band, checks
spending caps where applicable, logs the action to the OCSF audit trail,
and escalates to a human operator if the action exceeds the declared band.

Adding this tool to any Hermes agent session requires no code changes —
declare `custodian-band: L0` in the SKILL.md frontmatter and the kernel
wraps it automatically.
