---
name: memory-ticketing
description: "Use when adding Memory Events, Memory Tickets, memory-map.json, vault-references.json, PM Soul memory ownership, or Memory Curator routing to an agent repo."
---

# Memory Ticketing

## Required Files

- `.agentlas/memory-map.json`
- `.agentlas/memory-tickets.jsonl`
- `.agentlas/vault-references.json`

## Flow

1. Workers emit `## Memory Events`.
2. Runtime or orchestrator wraps events into tickets.
3. Memory Curator validates, redacts, deduplicates, and routes.
4. PM Soul owns project memory and open loops.
5. Policy Gate approves shared team-memory promotion.

## Never Store

Secrets, credentials, private keys, tokens, service-account JSON, raw logs, or
full transcripts.
