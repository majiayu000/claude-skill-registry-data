---
name: stripe-payout
description: "Initiate a Stripe payout to the connected bank account"
version: 1.0.0
author: custodian
license: MIT
platforms: [linux, darwin, windows]
metadata:
  hermes:
    tags: [Stripe, Finance, Payouts]
  custodian:
    band: L4
    cost_usd: 0.0
    configured: false
---

# Stripe Payout

Initiate a Stripe payout to the connected bank account

## Authority band

This tool runs under **L4** authority in the Custodian kernel. Unlimited potential impact — always escalates; never executes autonomously.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (see execute.py for full schema) | | | |

## Configuration

Set the required environment variables before use. Until configured, `custodian tools run stripe-payout` returns a stub response indicating which variables are needed.

## Usage

```bash
custodian tools run stripe-payout --param value
```

## Custodian governance

Every call to this tool passes through the Custodian kernel authority check
before executing. The kernel verifies the current authority band, checks
spending caps where applicable, logs the action to the OCSF audit trail,
and escalates to a human operator if the action exceeds the declared band.

Adding this tool to any Hermes agent session requires no code changes —
declare `custodian-band: L4` in the SKILL.md frontmatter and the kernel
wraps it automatically.
