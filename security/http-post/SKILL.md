---
name: http-post
description: "Perform an HTTP POST with JSON body and return the response"
version: 1.0.0
author: custodian
license: MIT
platforms: [linux, darwin, windows]
metadata:
  hermes:
    tags: [HTTP, Web]
  custodian:
    band: L1
    cost_usd: 0.0
    configured: true
---

# Http Post

Perform an HTTP POST with JSON body and return the response

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
custodian tools run http-post --param value
```

## Custodian governance

Every call to this tool passes through the Custodian kernel authority check
before executing. The kernel verifies the current authority band, checks
spending caps where applicable, logs the action to the OCSF audit trail,
and escalates to a human operator if the action exceeds the declared band.

Adding this tool to any Hermes agent session requires no code changes —
declare `custodian-band: L1` in the SKILL.md frontmatter and the kernel
wraps it automatically.
