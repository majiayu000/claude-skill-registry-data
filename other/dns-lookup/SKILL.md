---
name: dns-lookup
description: Resolve domain name to IP addresses using DNS
---

# DNS Lookup

Resolve domain name to IP addresses using DNS

## When to Use

- User wants to dns lookup
- User wants to resolve domain
- Keywords: dns, lookup, network, resolve

## Required Parameters

- **domain** (string): Domain to resolve

## Output

- **ip_addresses** (array): Resolved IPs
- **domain** (string): Queried domain

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `resolve` -> 4 steps -> Exit: `ret_ok`, `ret_fail`
