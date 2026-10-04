---
name: github-repo-list
description: "List repositories for a GitHub user or organization"
version: 1.0.0
author: custodian
license: MIT
platforms: [linux, darwin, windows]
metadata:
  hermes:
    tags: [GitHub, Repos]
  custodian:
    band: L0
    cost_usd: 0.0
    configured: false
---

# Github Repo List

List repositories for a GitHub user or organization

## Authority band

This tool runs under **L0** authority in the Custodian kernel. Read-only; no real-world effects — always autonomous.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (see execute.py for full schema) | | | |

## Configuration

Set the required environment variables before use. Until configured, `custodian tools run github-repo-list` returns a stub response indicating which variables are needed.

## Usage

```bash
custodian tools run github-repo-list --param value
```

## Custodian governance

Every call to this tool passes through the Custodian kernel authority check
before executing. The kernel verifies the current authority band, checks
spending caps where applicable, logs the action to the OCSF audit trail,
and escalates to a human operator if the action exceeds the declared band.

Adding this tool to any Hermes agent session requires no code changes —
declare `custodian-band: L0` in the SKILL.md frontmatter and the kernel
wraps it automatically.
