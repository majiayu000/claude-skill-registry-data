---
name: openai-complete
description: "Send a completion request to the OpenAI API"
version: 1.0.0
author: custodian
license: MIT
platforms: [linux, darwin, windows]
metadata:
  hermes:
    tags: [OpenAI, AI]
  custodian:
    band: L1
    cost_usd: 0.01
    configured: false
---

# Openai Complete

Send a completion request to the OpenAI API

## Authority band

This tool runs under **L1** authority in the Custodian kernel. Trivial autonomous spend or free side-effect — no human approval required.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (see execute.py for full schema) | | | |

## Configuration

Set the required environment variables before use. Until configured, `custodian tools run openai-complete` returns a stub response indicating which variables are needed.

## Usage

```bash
custodian tools run openai-complete --param value
```

## Custodian governance

Every call to this tool passes through the Custodian kernel authority check
before executing. The kernel verifies the current authority band, checks
spending caps where applicable, logs the action to the OCSF audit trail,
and escalates to a human operator if the action exceeds the declared band.

Adding this tool to any Hermes agent session requires no code changes —
declare `custodian-band: L1` in the SKILL.md frontmatter and the kernel
wraps it automatically.
